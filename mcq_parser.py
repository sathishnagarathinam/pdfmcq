"""
MCQ PDF Parser - Extract questions and answers from existing MCQ PDFs
Handles various question numbering formats and answer key layouts
"""

import re
from PyPDF2 import PdfReader
from typing import List, Dict, Tuple, Optional
import traceback


def extract_pages_from_pdf(pdf_path: str) -> List[str]:
    """
    Extract text from each page of a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of page texts
    """
    try:
        reader = PdfReader(pdf_path)
        pages = []
        
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    pages.append(page_text)
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                pages.append("")
        
        return pages
    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")


def detect_question_pattern(text: str) -> Optional[str]:
    """
    Detect the question numbering pattern in the text.

    Returns:
        Pattern type: 'descriptive', 'parenthesis_inline', 'numbered', 'q_format', 'question_word', or None
    """
    patterns = {
        'descriptive': r'Question\s+No\.\s+\d+:',  # "Question No. 1: Question text"
        'parenthesis_inline': r'^\s*\(\d+\.\)',  # "(1.) Question with (A.) option (B.) option"
        'numbered': r'^\s*\d+\.\s+',  # "1. Question text"
        'q_format': r'^\s*Q\d+\s*[:.]?\s+',  # "Q1: Question text" or "Q1. Question text"
        'question_word': r'^\s*Question\s+\d+\s*[:.]?\s+',  # "Question 1: Question text"
    }

    for pattern_name, pattern in patterns.items():
        if re.search(pattern, text, re.MULTILINE | re.IGNORECASE):
            return pattern_name

    return None


def extract_question_number(line: str) -> Optional[int]:
    """Extract question number from a line."""
    # Try different patterns
    patterns = [
        r'^\s*\((\d+)\.\)',  # "(1.) " - parenthesis format
        r'^\s*(\d+)\.',  # "1. "
        r'^\s*Q(\d+)',  # "Q1"
        r'^\s*Question\s+(\d+)',  # "Question 1"
    ]

    for pattern in patterns:
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def parse_inline_format_questions(text: str, debug: bool = False) -> List[Dict]:
    """
    Parse questions in inline format where options are on the same line.
    Format: (1.) Question text (A.) Option A (B.) Option B (C.) Option C (D.) Option D

    Args:
        text: Combined text from all question pages
        debug: Enable debug output

    Returns:
        List of question dictionaries
    """
    questions = []

    # Split by question pattern: (1.), (2.), etc.
    question_pattern = r'\((\d+)\.\)\s+(.+?)(?=\(\d+\.\)|$)'
    matches = re.finditer(question_pattern, text, re.DOTALL)

    for match in matches:
        question_num = int(match.group(1))
        question_content = match.group(2).strip()

        # Extract question text and options from the content
        # Pattern: Question text (A.) option (B.) option (C.) option (D.) option
        option_pattern = r'\(([A-D])\.\)\s+([^(]+?)(?=\([A-D]\.\)|$)'
        option_matches = list(re.finditer(option_pattern, question_content))

        if option_matches:
            # First part before first option is the question text
            first_option_start = option_matches[0].start()
            question_text = question_content[:first_option_start].strip()

            # Extract options
            options = {}
            for opt_match in option_matches:
                option_letter = opt_match.group(1).upper()
                option_text = opt_match.group(2).strip()
                options[option_letter] = option_text

            # Only add if we have at least 2 options
            if len(options) >= 2:
                question_dict = {
                    'number': question_num,
                    'text': question_text,
                    'options': options
                }
                questions.append(question_dict)

                if debug:
                    print(f"[DEBUG] Found question {question_num}")
                    print(f"[DEBUG]   Question text: '{question_text}'")
                    print(f"[DEBUG]   Question text length: {len(question_text)}")
                    print(f"[DEBUG]   Question text is empty: {not question_text}")
                    for letter, opt_text in options.items():
                        print(f"[DEBUG]   Option {letter}: {opt_text[:40]}...")

    return questions


def parse_standard_format_questions(text: str, debug: bool = False) -> List[Dict]:
    """
    Parse questions in standard format where each question and option is on separate lines.

    Args:
        text: Combined text from all question pages
        debug: Enable debug output

    Returns:
        List of question dictionaries
    """
    questions = []
    current_question = None
    current_options = {}

    lines = text.split('\n')

    if debug:
        print(f"[DEBUG] Total lines to process: {len(lines)}")

    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Check if this is a new question
        question_num = extract_question_number(line)

        if question_num is not None:
            # Save previous question if exists
            if current_question:
                if len(current_options) >= 2:  # Accept questions with 2+ options (more lenient)
                    current_question['options'] = current_options
                    questions.append(current_question)
                    if debug:
                        print(f"[DEBUG] Saved question {current_question['number']} with {len(current_options)} options")

            # Start new question
            question_text_match = re.sub(r'^\s*(?:\()?(?:Q)?\d+(?:\.)?\)?\s*[:.]?\s*', '', line, flags=re.IGNORECASE)
            current_question = {
                'number': question_num,
                'text': question_text_match,
                'options': {}
            }
            current_options = {}

            if debug:
                print(f"[DEBUG] Found question {question_num}: {question_text_match[:50]}...")

        # Check if this is an option line (A), B), C), D))
        elif current_question and re.match(r'^[A-D]\s*[\)\.:\-]\s*', line):
            option_letter = line[0].upper()
            option_text = re.sub(r'^[A-D]\s*[\)\.:\-]\s*', '', line)
            current_options[option_letter] = option_text

            if debug:
                print(f"[DEBUG]   Option {option_letter}: {option_text[:40]}...")

        # If we have a question but no options yet, append to question text
        elif current_question and not current_options:
            current_question['text'] += " " + line

    # Don't forget the last question
    if current_question:
        if len(current_options) >= 2:  # Accept questions with 2+ options
            current_question['options'] = current_options
            questions.append(current_question)
            if debug:
                print(f"[DEBUG] Saved last question {current_question['number']} with {len(current_options)} options")

    return questions


def parse_descriptive_format_questions(text: str, debug: bool = False) -> List[Dict]:
    """
    Parse questions in descriptive format with numbered options.
    Format:
        Question No. 1: Question text?
        Options: 1) Option 1
                 2) Option 2
                 3) Option 3
                 4) Option 4
        Answer: 2

    Args:
        text: Combined text from all question pages
        debug: Enable debug output

    Returns:
        List of question dictionaries
    """
    questions = []

    # Split by "Question No." to find all questions
    # This is more reliable than regex lookahead
    question_blocks = re.split(r'(?=Question\s+No\.\s+\d+\s*:)', text, flags=re.IGNORECASE)

    if debug:
        print(f"[DEBUG] Found {len(question_blocks)} question blocks")

    for block in question_blocks:
        if not block.strip():
            continue

        # Extract question number and text
        question_match = re.match(r'Question\s+No\.\s+(\d+)\s*:\s*(.+?)(?=\n|$)', block, re.IGNORECASE)
        if not question_match:
            continue

        question_num = int(question_match.group(1))
        question_text = question_match.group(2).strip()

        # Extract options from the block
        # Look for patterns like "1) Option text", "2) Option text", etc.
        option_pattern = r'^\s*(\d+)\s*[\)\.:\-]\s*(.+?)$'

        # Find all options in this block
        options = {}
        lines = block.split('\n')

        # Skip the first line (question line)
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            # Check if this line is an option (starts with 1), 2), 3), 4), etc.)
            opt_match = re.match(option_pattern, line)
            if opt_match:
                opt_num = int(opt_match.group(1))
                opt_text = opt_match.group(2).strip()

                # Convert number to letter (1->A, 2->B, 3->C, 4->D)
                if 1 <= opt_num <= 4:
                    opt_letter = chr(ord('A') + opt_num - 1)
                    options[opt_letter] = opt_text
            elif not options and not line.lower().startswith('options'):
                # If we haven't found options yet and this isn't "Options:" label,
                # this might be part of the question
                question_text += " " + line

        # Only add if we have at least 2 options
        if len(options) >= 2:
            question_dict = {
                'number': question_num,
                'text': question_text.strip(),
                'options': options
            }
            questions.append(question_dict)

            if debug:
                print(f"[DEBUG] Found question {question_num}: {question_text[:50]}...")
                for letter, opt_text in options.items():
                    print(f"[DEBUG]   Option {letter}: {opt_text[:40]}...")

    return questions


def parse_questions_from_pages(pages: List[str], answer_page_index: int = -1, debug: bool = False) -> Tuple[List[Dict], List[str]]:
    """
    Parse questions and options from pages (excluding answer key page).
    Supports both inline format (options on same line) and separate line format.

    Args:
        pages: List of page texts
        answer_page_index: Index of the answer key page (default: last page)
        debug: Enable debug output

    Returns:
        Tuple of (questions_list, answer_key_lines)
    """
    if answer_page_index == -1:
        answer_page_index = len(pages) - 1

    # Validate answer page index
    if answer_page_index >= len(pages):
        answer_page_index = len(pages) - 1

    # Combine all pages except the answer key page
    question_text = "\n".join([pages[i] for i in range(len(pages)) if i != answer_page_index])
    answer_key_text = pages[answer_page_index] if answer_page_index < len(pages) else ""

    if debug:
        print(f"[DEBUG] Total pages: {len(pages)}")
        print(f"[DEBUG] Answer page index: {answer_page_index}")
        print(f"[DEBUG] Question text length: {len(question_text)}")
        print(f"[DEBUG] Answer key text length: {len(answer_key_text)}")

    # Detect question pattern
    detected_pattern = detect_question_pattern(question_text)
    if debug:
        print(f"[DEBUG] Detected question pattern: {detected_pattern}")

    # Route to appropriate parser based on detected format
    if detected_pattern == 'descriptive':
        if debug:
            print(f"[DEBUG] Using descriptive format parser (Question No. X: ...)")
        questions = parse_descriptive_format_questions(question_text, debug=debug)
    elif detected_pattern == 'parenthesis_inline':
        if debug:
            print(f"[DEBUG] Using inline format parser for parenthesis format")
        questions = parse_inline_format_questions(question_text, debug=debug)
    else:
        # Use standard line-by-line parser
        if debug:
            print(f"[DEBUG] Using standard line-by-line parser")
        questions = parse_standard_format_questions(question_text, debug=debug)

    if debug:
        print(f"[DEBUG] Total questions found: {len(questions)}")

    # Extract answer key lines
    answer_lines = [line.strip() for line in answer_key_text.split('\n') if line.strip()]

    return questions, answer_lines


def parse_answer_key(answer_lines: List[str], debug: bool = False) -> Dict[int, str]:
    """
    Parse answer key and return mapping of question number to correct answer.

    Handles formats like:
    - "1. A"
    - "Q1: B"
    - "Answer 1: C"
    - "1) D"
    - "1 A"
    - Table format: "(1.) B (2.) C (3.) A (4.) A (5.) A"
    - Parenthesis format: "(1.) B" on separate lines
    """
    answers = {}

    # Combine all lines into one text for table format parsing
    combined_text = " ".join(answer_lines)

    if debug:
        print(f"[DEBUG] Parsing answer key from {len(answer_lines)} lines")
        print(f"[DEBUG] Combined text length: {len(combined_text)}")

    # Try table format first: (1.) B (2.) C (3.) A etc.
    # This pattern matches: (number.) letter with optional whitespace
    table_pattern = r'\(\s*(\d+)\s*\.\s*\)\s*([A-D])'
    table_matches = re.findall(table_pattern, combined_text)

    if table_matches:
        if debug:
            print(f"[DEBUG] Detected table format with {len(table_matches)} answers")
        for question_num_str, answer in table_matches:
            question_num = int(question_num_str)
            answers[question_num] = answer.upper()
        return answers

    if debug:
        print(f"[DEBUG] Table format not detected, trying line-by-line format")

    # Try line-by-line formats
    current_question_num = 0  # Track which question we're on for "Answer: X" format

    for line in answer_lines:
        # Try different answer key formats
        patterns = [
            (r'^\s*\(\s*(\d+)\s*\.\s*\)\s*([A-D])', 'parenthesis'),  # "(1.) A"
            (r'^\s*(\d+)\s*[\)\.:]?\s*([A-D])', 'numbered'),  # "1. A" or "1) A" or "1: A"
            (r'^\s*Q(\d+)\s*[\)\.:]?\s*([A-D])', 'q_format'),  # "Q1: A"
            (r'^\s*Answer\s+(\d+)\s*[\)\.:]?\s*([A-D])', 'answer_word'),  # "Answer 1: A"
            (r'^\s*(\d+)\s+([A-D])', 'space_separated'),  # "1 A"
            (r'^\s*(\d+)\s*[\)\.:]?\s*(\d+)', 'numeric_option'),  # "1. 2" or "1) 2" (numeric option)
        ]

        # Check for "Answer: X" format first (where X is 1-4, not question number)
        answer_numeric_match = re.match(r'^\s*Answer\s*:\s*(\d+)', line, re.IGNORECASE)
        if answer_numeric_match:
            answer_num = int(answer_numeric_match.group(1))
            if 1 <= answer_num <= 4:
                # Increment question number for this answer
                current_question_num += 1
                answer = chr(ord('A') + answer_num - 1)
                answers[current_question_num] = answer
                if debug:
                    print(f"[DEBUG] Found answer: Q{current_question_num} = {answer} (format: answer_numeric)")
                continue

        for pattern, pattern_type in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                question_num = int(match.group(1))
                answer_raw = match.group(2) if len(match.groups()) > 1 else match.group(1)

                # Convert numeric answer (1, 2, 3, 4) to letter (A, B, C, D)
                if answer_raw.isdigit():
                    answer_num = int(answer_raw)
                    if 1 <= answer_num <= 4:
                        answer = chr(ord('A') + answer_num - 1)
                    else:
                        continue  # Skip invalid numeric answers
                else:
                    answer = answer_raw.upper()

                answers[question_num] = answer
                current_question_num = question_num  # Update current question number
                if debug:
                    print(f"[DEBUG] Found answer: Q{question_num} = {answer} (format: {pattern_type})")
                break

    if debug:
        print(f"[DEBUG] Total answers parsed: {len(answers)}")

    return answers


def match_questions_with_answers(questions: List[Dict], answers: Dict[int, str]) -> List[Dict]:
    """
    Match questions with their correct answers.
    
    Args:
        questions: List of question dictionaries
        answers: Dictionary mapping question number to correct answer
        
    Returns:
        List of questions with 'correct' field added
    """
    matched_questions = []
    
    for question in questions:
        q_num = question.get('number')
        
        if q_num in answers:
            question['correct'] = answers[q_num]
            question['difficulty'] = 'medium'  # Default difficulty
            question['explanation'] = ''  # No explanation available
            matched_questions.append(question)
        else:
            print(f"Warning: No answer found for question {q_num}")
    
    return matched_questions


def parse_mcq_pdf(pdf_path: str, answer_page_index: int = -1, debug: bool = True) -> Dict:
    """
    Main function to parse an MCQ PDF.

    Args:
        pdf_path: Path to the PDF file
        answer_page_index: Index of the answer key page (default: last page)
        debug: Enable debug output

    Returns:
        Dictionary with 'questions' list and 'summary' dict
    """
    try:
        if debug:
            print(f"\n[DEBUG] Starting MCQ PDF parsing: {pdf_path}")

        # Extract pages
        pages = extract_pages_from_pdf(pdf_path)

        if not pages:
            return {'error': 'No pages extracted from PDF'}

        if debug:
            print(f"[DEBUG] Successfully extracted {len(pages)} pages")

        # Parse questions and answer key
        questions, answer_lines = parse_questions_from_pages(pages, answer_page_index, debug=debug)

        if not questions:
            # Provide more detailed error message
            if debug:
                print(f"[DEBUG] No questions found. Checking PDF content...")
                for i, page in enumerate(pages):
                    print(f"[DEBUG] Page {i+1} content preview: {page[:200]}...")

            return {
                'error': 'No questions found in PDF. Please verify:\n1. Questions are numbered (1., Q1:, Question 1:, etc.)\n2. Each question has options (A), B), C), D))\n3. Answer key is on the last page or specified page',
                'debug_info': {
                    'pages_extracted': len(pages),
                    'questions_found': 0,
                    'answer_lines_found': len(answer_lines)
                }
            }

        if debug:
            print(f"[DEBUG] Found {len(questions)} questions")

        # Parse answer key
        answers = parse_answer_key(answer_lines, debug=debug)

        if debug:
            print(f"[DEBUG] Found {len(answers)} answers in answer key")

        if not answers:
            if debug:
                print(f"[DEBUG] No answer key found. Answer lines: {answer_lines[:5]}")

            return {
                'error': 'No answer key found in PDF. Please verify:\n1. Answer key is on the last page or specified page\n2. Answers are in format: "1. A", "Q1: B", "Answer 1: C", "1) D", or "1 A"',
                'debug_info': {
                    'pages_extracted': len(pages),
                    'questions_found': len(questions),
                    'answer_lines_found': len(answer_lines),
                    'answer_lines_preview': answer_lines[:10]
                }
            }

        # Match questions with answers
        matched_questions = match_questions_with_answers(questions, answers)

        if debug:
            print(f"[DEBUG] Matched {len(matched_questions)} questions with answers")

        # Generate summary
        summary = {
            'total_questions': len(matched_questions),
            'total_pages': len(pages),
            'answer_page': answer_page_index if answer_page_index >= 0 else len(pages) - 1,
            'questions_with_answers': len(matched_questions),
            'questions_without_answers': len(questions) - len(matched_questions)
        }

        return {
            'questions': matched_questions,
            'summary': summary,
            'error': None,
            'debug_info': {
                'pages_extracted': len(pages),
                'questions_found': len(questions),
                'answers_found': len(answers),
                'matched_questions': len(matched_questions)
            }
        }

    except Exception as e:
        error_msg = f'Error parsing MCQ PDF: {str(e)}'
        if debug:
            print(f"[DEBUG] Exception occurred: {error_msg}")
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")

        return {
            'error': error_msg,
            'debug_info': {
                'exception': str(e),
                'traceback': traceback.format_exc()
            }
        }


def debug_pdf_content(pdf_path: str, max_lines_per_page: int = 20) -> Dict:
    """
    Debug function to inspect PDF content and identify issues.

    Args:
        pdf_path: Path to the PDF file
        max_lines_per_page: Maximum lines to display per page

    Returns:
        Dictionary with detailed PDF content analysis
    """
    try:
        print(f"\n{'='*80}")
        print(f"PDF CONTENT ANALYSIS: {pdf_path}")
        print(f"{'='*80}\n")

        pages = extract_pages_from_pdf(pdf_path)
        print(f"Total pages: {len(pages)}\n")

        analysis = {
            'total_pages': len(pages),
            'pages': []
        }

        for page_num, page_text in enumerate(pages):
            print(f"\n{'─'*80}")
            print(f"PAGE {page_num + 1}")
            print(f"{'─'*80}")

            lines = page_text.split('\n')
            print(f"Total lines: {len(lines)}\n")

            # Show first N lines
            print("CONTENT PREVIEW:")
            for i, line in enumerate(lines[:max_lines_per_page]):
                if line.strip():
                    print(f"  {i+1:3d}: {line[:100]}")

            if len(lines) > max_lines_per_page:
                print(f"  ... ({len(lines) - max_lines_per_page} more lines)")

            # Analyze patterns
            print(f"\nPATTERN ANALYSIS:")

            # Check for question patterns
            question_patterns = {
                'numbered': r'^\s*\d+\.\s+',
                'q_format': r'^\s*Q\d+\s*[:.]?\s+',
                'question_word': r'^\s*Question\s+\d+\s*[:.]?\s+',
            }

            pattern_counts = {}
            for pattern_name, pattern in question_patterns.items():
                count = len([l for l in lines if re.match(pattern, l.strip(), re.IGNORECASE)])
                pattern_counts[pattern_name] = count
                if count > 0:
                    print(f"  - {pattern_name}: {count} matches")

            # Check for option patterns
            option_count = len([l for l in lines if re.match(r'^[A-D]\s*[\)\.:\-]\s*', l.strip())])
            print(f"  - Options (A/B/C/D): {option_count} matches")

            # Check for answer key patterns
            answer_patterns = {
                'numbered': r'^\s*(\d+)\s*[\)\.:]?\s*([A-D])',
                'q_format': r'^\s*Q(\d+)\s*[\)\.:]?\s*([A-D])',
                'answer_word': r'^\s*Answer\s+(\d+)\s*[\)\.:]?\s*([A-D])',
                'space_separated': r'^\s*(\d+)\s+([A-D])',
            }

            answer_counts = {}
            for pattern_name, pattern in answer_patterns.items():
                count = len([l for l in lines if re.match(pattern, l.strip(), re.IGNORECASE)])
                answer_counts[pattern_name] = count
                if count > 0:
                    print(f"  - Answer format ({pattern_name}): {count} matches")

            analysis['pages'].append({
                'page_num': page_num + 1,
                'total_lines': len(lines),
                'question_patterns': pattern_counts,
                'option_count': option_count,
                'answer_patterns': answer_counts
            })

        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Total pages: {len(pages)}")

        # Overall statistics
        total_questions = sum(sum(p['question_patterns'].values()) for p in analysis['pages'])
        total_options = sum(p['option_count'] for p in analysis['pages'])
        total_answers = sum(sum(p['answer_patterns'].values()) for p in analysis['pages'])

        print(f"Total question markers found: {total_questions}")
        print(f"Total option markers found: {total_options}")
        print(f"Total answer markers found: {total_answers}")

        print(f"\n{'='*80}\n")

        return analysis

    except Exception as e:
        print(f"Error analyzing PDF: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {'error': str(e)}

