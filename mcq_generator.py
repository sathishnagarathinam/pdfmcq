from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from PyPDF2 import PdfReader
import re
import math
import time

# Load environment variables
load_dotenv()

# Import offline MCQ generator
try:
    from offline_mcq_generator import (
        generate_mcq_questions_offline,
        estimate_max_questions_offline,
        is_offline_available
    )
    OFFLINE_AVAILABLE = is_offline_available()
except ImportError:
    OFFLINE_AVAILABLE = False
    print("Offline MCQ generation not available. Install offline dependencies for enhanced functionality.")

# Import professional MCQ generator
try:
    from professional_mcq_generator import (
        generate_professional_mcq_questions,
        is_professional_mode_available
    )
    PROFESSIONAL_AVAILABLE = is_professional_mode_available()
except ImportError:
    PROFESSIONAL_AVAILABLE = False
    print("Professional MCQ generation not available. Run 'python setup_professional_models.py' for best quality.")

# Import fast MCQ generator
try:
    from fast_mcq_generator import (
        generate_fast_mcq_questions,
        is_fast_mode_available
    )
    FAST_AVAILABLE = is_fast_mode_available()
except ImportError:
    FAST_AVAILABLE = False
    print("Fast MCQ generation not available. Run 'python setup_fast_models.py' for speed optimization.")

# Import enhanced professional MCQ generator
try:
    from enhanced_professional_mcq import (
        generate_enhanced_professional_mcq_questions,
        is_enhanced_professional_mode_available
    )
    ENHANCED_PROFESSIONAL_AVAILABLE = is_enhanced_professional_mode_available()
except ImportError:
    ENHANCED_PROFESSIONAL_AVAILABLE = False
    print("Enhanced professional MCQ generation not available.")

def estimate_token_count(text):
    """
    Estimates the number of tokens in a text string.
    Uses a rough approximation: 1 token ≈ 4 characters for English text.
    This is a conservative estimate to ensure we stay within limits.
    """
    if not text:
        return 0
    # Conservative estimate: 1 token per 3.5 characters (accounting for spaces and punctuation)
    return math.ceil(len(text) / 3.5)

def get_model_token_limits(provider, model_name):
    """
    Get the appropriate token limits for different models and providers.
    Returns a tuple of (max_context_tokens, is_free_tier, rate_limit_info)
    """
    # Free tier models have much lower limits and rate limits
    # Note: Free models on OpenRouter change frequently - some may become unavailable
    # Updated: Feb 2026 based on OpenRouter free models collection
    free_tier_models = {
        # DeepSeek Models (Most Reliable)
        'deepseek/deepseek-chat': {'tokens': 8000, 'rate_limit': '50/day'},  # DeepSeek V3 - Most reliable
        'deepseek/deepseek-r1-0528:free': {'tokens': 8000, 'rate_limit': '20/min'},  # DeepSeek R1 reasoning

        # Arcee AI Models (Frontier)
        'arcee-ai/trinity-large-preview:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Trinity Large Preview
        'arcee-ai/trinity-mini:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Trinity Mini

        # Meta Llama Models
        'meta-llama/llama-3.3-70b-instruct:free': {'tokens': 8000, 'rate_limit': '20/min'},

        # Qwen Models
        'qwen/qwen3-235b-a22b-instruct:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Qwen3 235B
        'qwen/qwen3-coder:free': {'tokens': 8000, 'rate_limit': '8/min'},  # Qwen3 Coder 480B

        # NVIDIA Models
        'nvidia/nemotron-nano-9b-v2:free': {'tokens': 8000, 'rate_limit': '50/min'},  # Nemotron Nano 9B
        'nvidia/nemotron-3-nano-30b-a3b:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Nemotron 3 Nano

        # OpenAI Open Source
        'openai/gpt-oss-20b:free': {'tokens': 8000, 'rate_limit': '20/min'},  # GPT OSS 20B
        'openai/gpt-oss-120b:free': {'tokens': 8000, 'rate_limit': '20/min'},  # GPT OSS 120B

        # StepFun
        'stepfun/step-3.5-flash:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Step 3.5 Flash

        # Z.ai
        'z-ai/glm-4.5-air:free': {'tokens': 8000, 'rate_limit': '20/min'},  # GLM 4.5 Air

        # Upstage
        'upstage/solar-pro-3:free': {'tokens': 8000, 'rate_limit': '20/min'},  # Solar Pro 3

        # Microsoft Phi
        'microsoft/phi-3-medium-128k-instruct:free': {'tokens': 16000, 'rate_limit': '20/min'},

        # Mistral
        'mistralai/mistral-7b-instruct:free': {'tokens': 8000, 'rate_limit': '20/min'},

        # Google (Limited Rate)
        'google/gemini-2.0-flash-exp:free': {'tokens': 6000, 'rate_limit': '4/min'},
    }

    # Check if it's a free tier model
    if model_name in free_tier_models:
        model_info = free_tier_models[model_name]
        # Leave room for prompt and response (use 60% of limit for input text)
        return int(model_info['tokens'] * 0.6), True, model_info['rate_limit']

    # Paid tier models have higher limits
    if provider == 'openrouter':
        return 120000, False, 'High'  # Most paid OpenRouter models
    elif provider == 'openai':
        if 'gpt-4' in model_name:
            return 120000, False, 'High'
        else:
            return 15000, False, 'Medium'  # GPT-3.5
    elif provider == 'deepseek':
        return 120000, False, 'High'  # Direct DeepSeek API
    elif provider == 'anthropic':
        return 180000, False, 'High'  # Claude models

    # Default conservative limit
    return 8000, True, 'Unknown'

def get_rate_limit_delay(model_name, chunk_number):
    """
    Get appropriate delay between requests based on model rate limits.
    Returns delay in seconds.
    """
    rate_limit_delays = {
        # Very limited models
        'google/gemini-2.0-flash-exp:free': 15,  # 4 req/min = 15 sec between requests
        'qwen/qwen3-coder:free': 8,  # 8 req/min = 8 sec between requests

        # Standard free tier models (20 req/min = 3 sec between requests)
        'meta-llama/llama-3.3-70b-instruct:free': 3,
        'qwen/qwen3-235b-a22b-instruct:free': 3,
        'deepseek/deepseek-r1-0528:free': 3,
        'arcee-ai/trinity-large-preview:free': 3,
        'arcee-ai/trinity-mini:free': 3,
        'nvidia/nemotron-nano-9b-v2:free': 2,  # 50 req/min
        'nvidia/nemotron-3-nano-30b-a3b:free': 3,
        'openai/gpt-oss-20b:free': 3,
        'openai/gpt-oss-120b:free': 3,
        'stepfun/step-3.5-flash:free': 3,
        'z-ai/glm-4.5-air:free': 3,
        'upstage/solar-pro-3:free': 3,
        'microsoft/phi-3-medium-128k-instruct:free': 3,
        'mistralai/mistral-7b-instruct:free': 3,

        # DeepSeek V3 (daily limit, conservative delay)
        'deepseek/deepseek-chat': 1,
    }

    # Only add delay after the first chunk
    if chunk_number > 1 and model_name in rate_limit_delays:
        return rate_limit_delays[model_name]

    return 0  # No delay for first chunk or unknown models

def generate_pdf_summary(text, model_provider='openrouter', model_type='basic'):
    """
    Generate a 2-line summary of the PDF content to help users understand the subject.

    Args:
        text (str): Extracted text from PDF
        model_provider (str): AI provider to use
        model_type (str): Type of model to use

    Returns:
        str: 2-line summary of the PDF content
    """
    try:
        if not text or len(text.strip()) < 50:
            return "Unable to generate summary - insufficient content"

        # Limit text to first 3000 characters for summary generation
        summary_text = text[:3000]

        client = get_ai_client(model_provider)
        model = get_model_name(model_provider, model_type)

        prompt = f"""Generate a concise 2-line summary of the following document content.
The summary should help users understand the main subject and topic of the document.
Keep it brief, informative, and in plain language.

Document Content:
{summary_text}

Provide ONLY the 2-line summary, nothing else."""

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise document summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5,
        )

        summary = completion.choices[0].message.content.strip()
        return summary

    except Exception as e:
        print(f"⚠️  Error generating PDF summary: {e}")
        return "Summary generation failed"


def generate_comprehensive_notes(text, model_provider='openrouter', model_type='deepseek/deepseek-chat'):
    """
    Generate EXHAUSTIVE, ERROR-FREE, AND COMPLETE NOTES from PDF content.
    Designed for academic/exam preparation with detailed rule-wise analysis.

    Args:
        text (str): Extracted text from PDF
        model_provider (str): AI provider to use
        model_type (str): Model identifier (can be 'basic', 'advanced', or a full model name like 'deepseek/deepseek-chat')

    Returns:
        str: Comprehensive notes with tables, flowcharts, and exam-oriented content
    """
    try:
        if not text or len(text.strip()) < 100:
            return "Unable to generate notes - insufficient content"

        client = get_ai_client(model_provider)

        # If model_type is a full model name (contains '/'), use it directly
        # Otherwise, use get_model_name to resolve 'basic'/'advanced' to actual model names
        if '/' in model_type:
            model = model_type
        else:
            model = get_model_name(model_provider, model_type)

        system_prompt = """You are an expert academic note-maker, government-exam trainer, and documentation analyst.
Your task is to prepare EXHAUSTIVE, ERROR-FREE, AND COMPLETE NOTES in paragraphs from the given PDF.

⚠️ IMPORTANT:
- Do NOT summarize loosely
- Do NOT omit even a single rule, note, explanation, proviso, example, government decision, footnote, appendix, or exception
- Every rule number, sub-rule, NOTE, and reference must be preserved

These notes will be used for:
- Daily reference
- Competitive & departmental examinations
- Revision before tests"""

        user_prompt = f"""📘 DOCUMENT HANDLING INSTRUCTIONS
- Process the PDF chapter-by-chapter and rule-by-rule
- Maintain original numbering (Chapter, Rule, Sub-rule, Notes)
- Preserve exact legal/technical meaning
- Use simple language ONLY for explanation, not for altering rules

🧠 NOTE-MAKING STRUCTURE (MANDATORY)

For EVERY chapter, follow this exact format:

🔹 CHAPTER OVERVIEW
- Purpose of the chapter
- Who should study it (DDO / Accounts / Audit / Exam point of view)
- Key financial concepts involved

🔹 DETAILED NOTES (RULE-WISE)
For each Rule, present information as:
📌 Rule Number & Title
- Exact rule text (simplified but complete)
- Break into bullet points wherever required
- Highlight keywords in bold
- Mention: Authority, Time limits, Financial powers, Conditions, Exceptions, Cross-references to other rules

🔹 STUDY TOOLS (VERY IMPORTANT)
After every 2–3 rules, add:
📊 TABLES - Example formats:
| Rule No | Subject | Authority | Time Limit | Key Condition |
| Situation | What is Allowed | What is Prohibited |

🔁 FLOWCHARTS (TEXT-BASED) - Example:
Claim Raised → Verification → Sanction → Audit → Payment → Record Entry

🔹 EXAM-ORIENTED SECTION (VERY IMPORTANT)
After each chapter, add:
📝 EXAM HIGHLIGHTS
- Most important rules
- Frequently confused provisions
- Common mistakes by students
- Areas from which MCQs are framed

🔹 QUICK REVISION SHEET (END OF CHAPTER)
- One-page ultra-summary
- Rule numbers only
- Tables only
- "Must-remember points"

📚 APPENDICES & ANNEXURES HANDLING
- Treat Appendices as equally important
- Convert: Lists → Tables, Procedures → Flowcharts, Conditions → Comparison charts

⚠️ QUALITY CONTROL CHECK
Before finalizing notes:
✔ No rule skipped
✔ No appendix skipped
✔ No note or proviso skipped
✔ All numerical limits preserved
✔ Language is exam-friendly but legally accurate

📤 OUTPUT FORMAT
- Use clear headings
- Use numbering
- Use tables frequently
- Make it suitable for: PDF printing, Daily revision, One-night exam revision

🔥 PRO TIP: If content is too long, continue automatically from where you stopped without repeating.

---
DOCUMENT CONTENT TO PROCESS:
{text}"""

        # For comprehensive notes, we need much higher token limit
        max_tokens = 16000 if 'deepseek' in model.lower() else 8000

        print(f"📝 Generating comprehensive notes with model: {model}")
        print(f"📊 Processing {len(text)} characters of text...")

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3,  # Lower temperature for more accurate/consistent output
        )

        notes = completion.choices[0].message.content.strip()
        print(f"✅ Generated {len(notes)} characters of comprehensive notes")
        return notes

    except Exception as e:
        print(f"⚠️  Error generating comprehensive notes: {e}")
        import traceback
        traceback.print_exc()
        return f"Notes generation failed: {str(e)}"

def equalize_answer_lengths(question):
    """
    Equalize the length of answer options to prevent correct answer identification by length.

    This function ensures that all answer options have similar lengths, making it harder
    for users to identify the correct answer based on option length alone.

    Args:
        question (dict): Question with options A, B, C, D

    Returns:
        dict: Question with equalized option lengths
    """
    try:
        if 'options' not in question:
            return question

        options = question['options']

        # Get lengths of all options
        lengths = {key: len(options.get(key, '')) for key in ['A', 'B', 'C', 'D']}

        # Calculate target length (average of all options)
        valid_lengths = [l for l in lengths.values() if l > 0]
        if not valid_lengths:
            return question

        avg_length = sum(valid_lengths) / len(valid_lengths)
        target_length = int(avg_length)

        # Equalize each option
        equalized_options = {}
        for key in ['A', 'B', 'C', 'D']:
            option_text = options.get(key, '')
            current_length = len(option_text)

            if current_length == 0:
                equalized_options[key] = option_text
            elif current_length > target_length:
                # Truncate to target length, trying to cut at word boundary
                truncated = option_text[:target_length]
                # Try to find last space to avoid cutting mid-word
                last_space = truncated.rfind(' ')
                if last_space > target_length * 0.7:  # Only use space if it's not too early
                    truncated = truncated[:last_space].rstrip()
                equalized_options[key] = truncated
            else:
                # Pad with ellipsis or keep as is if close to target
                if target_length - current_length <= 3:
                    equalized_options[key] = option_text
                else:
                    # Add ellipsis to indicate truncation if needed
                    equalized_options[key] = option_text

        question['options'] = equalized_options
        return question

    except Exception as e:
        print(f"⚠️  Error equalizing answer lengths: {e}")
        return question

def find_page_and_section_for_text(text_snippet, page_map, sections):
    """
    Finds which page(s) and section(s) a text snippet belongs to.

    Args:
        text_snippet (str): The text snippet to locate
        page_map (list): List of page metadata
        sections (list): List of detected sections

    Returns:
        dict: {'pages': list of page numbers, 'sections': list of section titles}
    """
    result = {'pages': [], 'sections': []}

    if not page_map:
        return result

    # Find first 100 chars of snippet for matching
    search_text = text_snippet[:100].strip()

    for page_info in page_map:
        if search_text in page_info['text']:
            result['pages'].append(page_info['page_number'])
            # Add sections from this page
            for section in page_info.get('sections', []):
                section_label = f"{section['title']}"
                if section['number']:
                    section_label = f"{section['number']} {section['title']}"
                if section_label not in result['sections']:
                    result['sections'].append(section_label)

    return result

def chunk_text_with_metadata(text, page_map, sections, max_tokens=120000, overlap_tokens=2000):
    """
    Splits text into chunks with metadata about pages and sections.

    Args:
        text (str): The text to chunk
        page_map (list): List of page metadata
        sections (list): List of detected sections
        max_tokens (int): Maximum tokens per chunk
        overlap_tokens (int): Number of tokens to overlap between chunks

    Returns:
        list: List of dicts with 'text', 'pages', and 'sections' for each chunk
    """
    # Get basic text chunks
    text_chunks = chunk_text(text, max_tokens, overlap_tokens)

    # Add metadata to each chunk
    chunks_with_metadata = []
    for chunk_text in text_chunks:
        metadata = find_page_and_section_for_text(chunk_text, page_map, sections)
        chunks_with_metadata.append({
            'text': chunk_text,
            'pages': metadata['pages'],
            'sections': metadata['sections']
        })

    return chunks_with_metadata

def chunk_text(text, max_tokens=120000, overlap_tokens=2000):
    """
    Splits text into chunks that fit within the token limit.

    Args:
        text (str): The text to chunk
        max_tokens (int): Maximum tokens per chunk (default: 120,000 to leave room for prompt)
        overlap_tokens (int): Number of tokens to overlap between chunks for context

    Returns:
        list: List of text chunks
    """
    if not text:
        return []

    total_tokens = estimate_token_count(text)

    # If text is small enough, return as single chunk
    if total_tokens <= max_tokens:
        return [text]

    # Use a more conservative approach - aim for 90% of max tokens to ensure we stay under
    target_tokens = int(max_tokens * 0.9)
    chars_per_token = len(text) / total_tokens
    target_chars_per_chunk = int(target_tokens * chars_per_token)
    overlap_chars = int(overlap_tokens * chars_per_token)

    chunks = []
    start = 0

    while start < len(text):
        # Calculate end position for this chunk
        end = start + target_chars_per_chunk

        # If this is not the last chunk, try to break at a sentence or paragraph
        if end < len(text):
            # Look for sentence endings within the last 1000 characters
            search_start = max(end - 1000, start)
            sentence_breaks = []

            # Find sentence endings (., !, ?)
            for i in range(search_start, min(end + 500, len(text))):
                if text[i] in '.!?' and i + 1 < len(text) and text[i + 1] in ' \n\t':
                    sentence_breaks.append(i + 1)

            # Use the last sentence break before our target end
            if sentence_breaks:
                good_breaks = [b for b in sentence_breaks if b <= end + 200]  # Allow some flexibility
                if good_breaks:
                    end = good_breaks[-1]

        # Extract chunk and verify it's within token limits
        chunk = text[start:end].strip()
        if chunk:
            # Double-check token count and trim if necessary
            chunk_tokens = estimate_token_count(chunk)
            if chunk_tokens > max_tokens:
                # If still too large, trim more aggressively
                reduction_factor = max_tokens / chunk_tokens
                new_end = start + int((end - start) * reduction_factor * 0.9)  # Extra safety margin
                chunk = text[start:new_end].strip()

            chunks.append(chunk)

        # Move start position for next chunk (with overlap)
        start = max(start + 1, end - overlap_chars)

        # Prevent infinite loop
        if start >= len(text):
            break

    return chunks

def estimate_max_questions(text, use_offline=True):
    """
    Estimates the maximum number of questions that can be generated from the text.
    Now supports both offline and online estimation methods.

    Args:
        text (str): The extracted text
        use_offline (bool): Whether to use offline analysis for better estimation

    Returns:
        int or dict: Estimated maximum number of questions (int for backward compatibility)
                    or detailed analysis dict when using offline mode
    """
    if not text or not text.strip():
        return 0

    # Try offline estimation first if available and requested
    if use_offline and OFFLINE_AVAILABLE:
        try:
            offline_result = estimate_max_questions_offline(text)
            # Return just the number for backward compatibility, but store detailed info
            return offline_result["max_questions"]
        except Exception as e:
            print(f"Offline estimation failed, falling back to basic method: {e}")

    # Fallback to original estimation method
    # Count meaningful content indicators
    sentences = len([s for s in text.split('.') if len(s.strip()) > 15])
    paragraphs = len([p for p in text.split('\n') if len(p.strip()) > 30])
    words = len(text.split())
    lines = len([line for line in text.split('\n') if len(line.strip()) > 10])

    # Multiple estimation approaches
    # 1. Word-based estimate (1 question per 80-120 words)
    word_based_estimate = max(1, words // 100)

    # 2. Sentence-based estimate (1 question per 2-3 sentences)
    sentence_based_estimate = max(1, sentences // 3)

    # 3. Paragraph-based estimate (1 question per paragraph with substantial content)
    paragraph_based_estimate = max(1, paragraphs // 2)

    # 4. Line-based estimate (for structured content)
    line_based_estimate = max(1, lines // 5)

    # Take the maximum of the estimates (optimistic approach)
    estimated_max = max(word_based_estimate, sentence_based_estimate,
                       paragraph_based_estimate, line_based_estimate)

    # Apply scaling based on text length
    if words < 50:
        estimated_max = max(1, estimated_max // 2)  # Very short text
    elif words < 200:
        estimated_max = max(2, estimated_max)       # Short text
    elif words > 1000:
        estimated_max = min(estimated_max * 2, 50)  # Long text, but cap at 50

    # Final bounds
    estimated_max = min(estimated_max, 100)  # Maximum 100 questions
    estimated_max = max(estimated_max, 1)    # Minimum 1 question

    return estimated_max


def estimate_max_questions_detailed(text):
    """
    Get detailed estimation analysis including breakdown and confidence.

    Args:
        text (str): The extracted text

    Returns:
        dict: Detailed analysis with max_questions, confidence, and breakdown
    """
    if not text or not text.strip():
        return {"max_questions": 0, "confidence": "low", "breakdown": {}}

    if OFFLINE_AVAILABLE:
        try:
            return estimate_max_questions_offline(text)
        except Exception as e:
            print(f"Offline detailed estimation failed: {e}")

    # Fallback to basic estimation with simple breakdown
    basic_estimate = estimate_max_questions(text, use_offline=False)
    return {
        "max_questions": basic_estimate,
        "confidence": "medium",
        "breakdown": {
            "basic_estimate": basic_estimate,
            "method": "fallback"
        }
    }

def detect_sections_in_text(text, page_number):
    """
    Detects sections and headings in text using pattern matching.

    Args:
        text (str): Text to analyze
        page_number (int): Page number this text is from

    Returns:
        list: List of detected sections with metadata
    """
    sections = []
    lines = text.split('\n')

    # Patterns for detecting headings
    heading_patterns = [
        # Chapter patterns
        (r'^(?:Chapter|CHAPTER|Ch\.?)\s+(\d+(?:\.\d+)*)\s*[:\-]?\s*(.+)$', 'chapter'),
        (r'^(?:Chapter|CHAPTER|Ch\.?)\s+([IVXLCDM]+)\s*[:\-]?\s*(.+)$', 'chapter'),

        # Section patterns
        (r'^(?:Section|SECTION|Sec\.?)\s+(\d+(?:\.\d+)*)\s*[:\-]?\s*(.+)$', 'section'),
        (r'^(\d+(?:\.\d+)+)\s+(.+)$', 'numbered_section'),  # e.g., "1.2.3 Introduction"

        # All caps headings (likely section titles)
        (r'^([A-Z][A-Z\s]{3,50})$', 'heading'),

        # Title case headings
        (r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,8})$', 'title'),
    ]

    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 3:
            continue

        for pattern, section_type in heading_patterns:
            match = re.match(pattern, line)
            if match:
                if section_type in ['chapter', 'section', 'numbered_section']:
                    section_number = match.group(1) if len(match.groups()) >= 1 else ''
                    section_title = match.group(2) if len(match.groups()) >= 2 else line
                else:
                    section_number = ''
                    section_title = match.group(1) if match.groups() else line

                sections.append({
                    'type': section_type,
                    'number': section_number,
                    'title': section_title.strip(),
                    'page': page_number,
                    'line': line_num
                })
                break  # Only match first pattern

    return sections

def validate_pdf_file(pdf_path):
    """Validates if the file is a valid PDF."""
    try:
        # Check file extension
        if not pdf_path.lower().endswith('.pdf'):
            return False, "File is not a PDF (wrong extension)"

        # Check if file exists and is readable
        if not os.path.exists(pdf_path):
            return False, "PDF file not found"

        if os.path.getsize(pdf_path) == 0:
            return False, "PDF file is empty"

        # Try to read the PDF header
        with open(pdf_path, 'rb') as f:
            header = f.read(8)
            if not header.startswith(b'%PDF-'):
                return False, "File is not a valid PDF (invalid header)"

        return True, "Valid PDF file"
    except Exception as e:
        return False, f"Error validating PDF: {e}"

def extract_text_from_pdf_with_metadata(pdf_path):
    """
    Extracts text from a PDF file with page and section metadata tracking.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        dict: {
            'text': str (full text),
            'page_map': list of dicts with page info,
            'sections': list of detected sections,
            'total_pages': int
        } or error message string
    """
    try:
        # First validate the PDF file
        is_valid, validation_message = validate_pdf_file(pdf_path)
        if not is_valid:
            return f"PDF Validation Error: {validation_message}"

        # Try to read the PDF
        try:
            reader = PdfReader(pdf_path)
        except Exception as read_error:
            return f"Failed to load PDF document: {read_error}. The PDF might be corrupted, password-protected, or in an unsupported format."

        # Check if PDF has pages
        if len(reader.pages) == 0:
            return "Error: PDF document has no pages"

        # Extract text from all pages with metadata
        full_text = ""
        page_map = []
        sections = []
        pages_with_text = 0
        total_pages = len(reader.pages)
        current_char_position = 0

        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    # Detect sections/headings in this page
                    page_sections = detect_sections_in_text(page_text, page_num + 1)
                    sections.extend(page_sections)

                    # Track page metadata
                    page_info = {
                        'page_number': page_num + 1,
                        'start_char': current_char_position,
                        'end_char': current_char_position + len(page_text),
                        'text': page_text,
                        'sections': page_sections
                    }
                    page_map.append(page_info)

                    full_text += page_text + "\n"
                    current_char_position += len(page_text) + 1
                    pages_with_text += 1
            except Exception as page_error:
                print(f"Warning: Could not extract text from page {page_num + 1}: {page_error}")
                continue

        # Check if any text was extracted
        if not full_text.strip():
            error_msg = f"No text could be extracted from the PDF. This might be a scanned document (image-based PDF) with {total_pages} pages."
            error_msg += "\n\n💡 Solutions:"
            error_msg += "\n• Install OCR support: pip install pytesseract pillow pymupdf"
            error_msg += "\n• Use a PDF with selectable text instead"
            error_msg += "\n• Convert the scanned PDF to text using online OCR tools"
            return error_msg

        # Check if text extraction was partial
        if pages_with_text < total_pages:
            full_text += f"\n\nNote: Text was successfully extracted from {pages_with_text} out of {total_pages} pages."

        return {
            'text': full_text.strip(),
            'page_map': page_map,
            'sections': sections,
            'total_pages': total_pages,
            'pages_with_text': pages_with_text
        }

    except Exception as e:
        return f"Unexpected error extracting text from PDF: {e}. Please ensure the PDF is not corrupted and try again."

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file with enhanced error handling, validation, and OCR support.
    This is the legacy function that returns just text for backward compatibility.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        str: Extracted text or error message
    """
    try:
        # Try enhanced extraction with OCR support
        try:
            from ocr_pdf_extractor import extract_text_from_pdf_enhanced
            return extract_text_from_pdf_enhanced(pdf_path, use_ocr=True)
        except ImportError:
            # Fallback to standard extraction if OCR module not available
            pass

        # Use the new metadata extraction but return only text
        result = extract_text_from_pdf_with_metadata(pdf_path)

        # If it's an error string, return it
        if isinstance(result, str):
            return result

        # Otherwise return just the text
        return result['text']

    except Exception as e:
        return f"Unexpected error extracting text from PDF: {e}. Please ensure the PDF is not corrupted and try again."

def extract_reference_info(text):
    """Extracts reference information like book name, chapter, section, rule numbers from PDF text."""
    reference_info = {}

    # Convert text to lines for better analysis
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    first_few_lines = '\n'.join(lines[:15])  # Analyze first 15 lines for title/book info

    # Improved patterns to match various reference formats more precisely
    patterns = {
        'book_title': [
            r'^([A-Z][A-Z\s&,.-]*(?:LAW|CODE|ACT|MANUAL|HANDBOOK|GUIDE|RULES|REGULATIONS|CONSTITUTION|STATUTE)[A-Z\s&,.-]*)$',
            r'^(THE\s+[A-Z][A-Z\s&,.-]*(?:LAW|CODE|ACT|MANUAL|HANDBOOK|GUIDE|RULES|REGULATIONS|CONSTITUTION|STATUTE)[A-Z\s&,.-]*)$',
            r'^([A-Z][A-Za-z\s&,.-]*(?:in|and|of)\s+[A-Z][A-Za-z\s&,.-]*)$',  # Academic titles
            r'^([A-Z][A-Z\s&,.-]*GUIDE[A-Z\s&,.-]*PART[A-Z\s&,.-]*[IVXLCDM]+)$',  # Guide with parts
            r'^([A-Z][A-Z\s&,.-]*GUIDE[A-Z\s&,.-]*PART[A-Z\s&,.-]*\d+)$',  # Guide with numbered parts
        ],
        'chapter': [
            r'^(?:Chapter|CHAPTER|Ch\.?)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,50})$',
            r'^(?:Chapter|CHAPTER|Ch\.?)\s*([IVXLCDM]+)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,50})$',
        ],
        'section': [
            r'^(?:Section|SECTION|Sec\.?|§)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
            r'^(?:Section|SECTION|Sec\.?|§)\s*([IVXLCDM]+)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
        ],
        'rule': [
            r'^(?:Rule|RULE|R\.?)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
        ],
        'article': [
            r'^(?:Article|ARTICLE|Art\.?)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
            r'^(?:Article|ARTICLE)\s*([IVXLCDM]+)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
        ],
        'part': [
            r'^(?:Part|PART|Pt\.?)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,50})$',
            r'^(?:Part|PART)\s*([IVXLCDM]+)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,50})$',
        ],
        'clause': [
            r'^(?:Clause|CLAUSE|Cl\.?)\s*(\d+(?:\.\d+)*)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
            r'^(?:Clause|CLAUSE)\s*([IVXLCDM]+)\s*[:\-]?\s*([A-Za-z][A-Za-z\s,.-]{0,80})$',
        ]
    }

    # Extract book title from first few lines
    for line in lines[:10]:  # Check first 10 lines
        for pattern in patterns['book_title']:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 5 and len(title) < 100:  # Reasonable title length
                    reference_info['book_title'] = title
                    break
        if 'book_title' in reference_info:
            break

    # Extract structural elements from the entire text, line by line
    for line in lines:
        for ref_type, pattern_list in patterns.items():
            if ref_type == 'book_title':
                continue  # Already processed

            for pattern in pattern_list:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    if ref_type not in reference_info:
                        reference_info[ref_type] = []

                    if len(match.groups()) >= 2:
                        # Pattern with number and title
                        number = match.group(1).strip()
                        title = match.group(2).strip()
                        if title and len(title) > 3:  # Ensure meaningful title
                            reference_info[ref_type].append(f"{ref_type.title()} {number}: {title}")
                    else:
                        # Pattern with just number
                        number = match.group(1).strip()
                        reference_info[ref_type].append(f"{ref_type.title()} {number}")

                    # Limit to first few matches to avoid clutter
                    if len(reference_info[ref_type]) >= 2:
                        break
                    break  # Found match, move to next line

            if ref_type in reference_info and len(reference_info[ref_type]) >= 2:
                break  # Found enough matches for this type

    return reference_info

def build_reference_string(reference_info, manual_book_name='', manual_chapter_name=''):
    """Builds a formatted reference string using only manual override inputs."""
    ref_parts = []

    # Only use manual inputs - no AI extraction fallback
    if manual_book_name.strip():
        ref_parts.append(manual_book_name.strip())

    if manual_chapter_name.strip():
        ref_parts.append(manual_chapter_name.strip())

    if ref_parts:
        return f" (Source: {', '.join(ref_parts)})"
    else:
        return ""

def get_ai_client(model_provider, custom_api_key=None, custom_base_url=None):
    """Returns the appropriate AI client based on the selected model."""
    print(f"🔑 Setting up AI client for provider: {model_provider}")

    if model_provider == 'custom':
        # Use custom configuration
        if not custom_api_key:
            raise ValueError("Custom API key is required for custom model provider")

        client_config = {"api_key": custom_api_key}
        if custom_base_url:
            client_config["base_url"] = custom_base_url

        return OpenAI(**client_config)

    elif model_provider == 'openrouter':
        api_key = os.getenv("OPENROUTER_API_KEY")
        print(f"🔑 OpenRouter API key: {'✅ Found' if api_key else '❌ Missing'}")
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    elif model_provider == 'openai':
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"🔑 OpenAI API key: {'✅ Found' if api_key else '❌ Missing'}")
        return OpenAI(api_key=api_key)
    elif model_provider == 'anthropic':
        # Note: Anthropic uses a different API format, but we'll use OpenAI-compatible wrapper
        return OpenAI(
            base_url="https://api.anthropic.com/v1",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif model_provider == 'deepseek':
        api_key = os.getenv("DEEPSEEK_API_KEY")
        print(f"🔑 DeepSeek API key: {'✅ Found' if api_key else '❌ Missing'}")
        return OpenAI(
            base_url="https://api.deepseek.com",
            api_key=api_key,
        )
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

def get_model_name(model_provider, model_type):
    """Returns the appropriate model name based on provider and type."""
    models = {
        'openrouter': {
            'basic': 'deepseek/deepseek-chat',
            'advanced': 'meta-llama/llama-3.3-70b-instruct:free'
        },
        'openai': {
            'basic': 'gpt-3.5-turbo',
            'advanced': 'gpt-4'
        },
        'deepseek': {
            'basic': 'deepseek-chat',
            'advanced': 'deepseek-coder'
        }
    }
    return models[model_provider][model_type]

def create_amendment_prompt_section(use_amendment=False):
    """
    Creates the amendment-specific prompt section for MCQ generation.

    Args:
        use_amendment (bool): Whether amendment analysis is enabled

    Returns:
        str: Amendment-specific prompt instructions
    """
    if not use_amendment:
        return ""

    return """
    AMENDMENT ANALYSIS REQUIREMENTS:
    ================================
    You are analyzing BOTH an original document AND its amendment.

    1. AMENDMENT-FOCUSED QUESTIONS:
       - Generate questions that cover changes introduced in the amendment
       - Include questions about differences between original and amended versions
       - Ask about new provisions added in the amendment
       - Ask about provisions removed or modified by the amendment
       - Example: "What was changed in the amendment regarding...?"
       - Example: "Which provision was added/removed in the amendment?"

    2. REFERENCE SPECIFICATION:
       - In explanations, specify whether the answer comes from:
         * Original document only
         * Amendment only
         * Both documents (for comparative questions)
       - Use format: "Reference: Original Section X / Amendment Section Y"
       - Or: "Reference: Original Section X (amended by Amendment Section Y)"

    3. COMPARATIVE ANALYSIS:
       - Create questions that test understanding of changes
       - Include "before and after" type questions
       - Ask about the impact of amendments
       - Ensure questions highlight the differences clearly

    4. COVERAGE:
       - Ensure at least 50% of questions focus on amendment-related content
       - Balance between original document and amendment questions
       - Cover all major changes and new provisions
    """

def merge_texts_for_amendment_analysis(original_text, amendment_text):
    """
    Intelligently merges original and amendment texts for analysis.

    Args:
        original_text (str): Text from the original document
        amendment_text (str): Text from the amendment document

    Returns:
        str: Merged text with clear separation markers
    """
    merged = f"""=== ORIGINAL DOCUMENT ===
{original_text}

=== AMENDMENT DOCUMENT ===
{amendment_text}

=== ANALYSIS INSTRUCTIONS ===
The above contains two documents: the original and its amendment.
Analyze both to understand what has changed, what was added, and what was removed.
Generate questions that test understanding of these changes and differences.
"""
    return merged

def generate_mcq_questions(text, num_questions=5, model_provider='openrouter', model_type='basic', book_name='', chapter_name=''):
    """Generates MCQ questions using the selected AI model."""
    try:
        print(f"🌐 Starting online generation with {model_provider} ({model_type})")
        print(f"📝 Text length: {len(text)} characters")
        print(f"🎯 Requested questions: {num_questions}")
        print(f"🔑 Getting AI client for {model_provider}")
        client = get_ai_client(model_provider)
        model = get_model_name(model_provider, model_type)
        print(f"🤖 Using model: {model}")

        # Build source reference using only manual inputs
        source_reference = build_reference_string({}, book_name, chapter_name)

        explanation_instruction = ""
        if source_reference:
            explanation_instruction = f" Include the source reference at the end: {source_reference}"

        # Check if text needs to be chunked
        token_count = estimate_token_count(text)
        max_context_tokens, is_free_tier, rate_limit = get_model_token_limits(model_provider, model)

        print(f"📊 Text analysis: {token_count} tokens, limit: {max_context_tokens} ({'free tier' if is_free_tier else 'paid tier'}, rate limit: {rate_limit})")

        # If text is too large, chunk it
        if token_count > max_context_tokens:
            chunks = chunk_text(text, max_context_tokens)
            all_questions = []
            questions_per_chunk = max(1, math.ceil(num_questions / len(chunks)))

            # Process each chunk
            for i, chunk in enumerate(chunks):
                # For the last chunk, adjust questions to match total requested
                if i == len(chunks) - 1:
                    remaining = num_questions - len(all_questions)
                    if remaining <= 0:
                        break
                    questions_per_chunk = remaining

                chunk_prompt = f"""Generate exactly {questions_per_chunk} multiple-choice questions (MCQs) from the following text.

                ⚠️ MANDATORY QUALITY RULES - MUST FOLLOW STRICTLY:

                1. SINGLE CORRECT ANSWER RULE (CRITICAL):
                   - Ensure ONLY ONE option is correct under ALL circumstances
                   - The correct answer must be unambiguous and absolute
                   - No option should be "partially correct" or "correct in some cases"

                2. NO CONDITIONAL/SITUATIONAL LANGUAGE:
                   - Do NOT frame questions involving conditional, optional, or situational clauses unless explicitly stated in the question
                   - Avoid words like "may", "can", "if required", "in case of", "unless", "sometimes", "usually", "generally"
                   - Only use absolute statements that are always true or always false

                3. VERIFICATION FOR 'NOT CORRECT' QUESTIONS:
                   - For questions asking "Which is NOT correct?", verify that the remaining three options are EXPLICITLY stated in the PDF as correct
                   - Do NOT infer or assume - only use facts directly stated in the text
                   - If exclusivity cannot be guaranteed, DO NOT generate the question

                4. PARAGRAPH REFERENCE (MANDATORY):
                   - Include the exact paragraph/section reference in the explanation for validation
                   - Format: "Reference: [Section/Rule/Paragraph number or identifier]"

                5. INDEPENDENT VERIFIABILITY:
                   - Each option must be independently verifiable from the PDF
                   - Generate assertion-reason or statement-based MCQs where possible
                   - Each statement in options should be traceable to specific text

                6. EXCLUSIVITY GUARANTEE:
                   - If exclusivity of the correct answer cannot be guaranteed, DO NOT generate the question
                   - Skip ambiguous topics rather than creating potentially incorrect questions

                7. COVERAGE AND DISTRIBUTION:
                   - Cover ALL major rules and notes evenly
                   - DO NOT over-emphasize a single rule
                   - Distribute questions across different topics
                   - Include: Applicability, exclusions, definitions, numerical provisions, amendments

                DIFFICULTY DISTRIBUTION:
                   - 40% easy (direct rule-based facts)
                   - 40% medium (rule + condition combination)
                   - 20% tricky (exceptions, notes, negative framing)

                FORMAT REQUIREMENTS:
                   - Each question must have 4 options (A, B, C, D)
                   - Include correct answer letter
                   - Provide brief explanation WITH paragraph reference
                   - Format as valid JSON array
                {explanation_instruction}

                JSON Structure:
                {{
                    "question": "[Question Text]",
                    "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
                    "correct": "[Correct Option Letter]",
                    "difficulty": "[easy/medium/hard]",
                    "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]{source_reference}"
                }}

                Text: {chunk}
                """

                print(f"📤 Sending prompt for chunk {i+1}: {chunk_prompt[:300]}...")

                # Add rate limiting delay for free tier models
                delay = get_rate_limit_delay(model, i+1)
                if delay > 0:
                    print(f"⏳ Rate limit delay: waiting {delay} seconds before chunk {i+1}...")
                    time.sleep(delay)

                try:
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are an expert educator specializing in government rules, regulations, and policy documents. You create high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON."},
                            {"role": "user", "content": chunk_prompt}
                        ],
                        max_tokens=4000,
                        temperature=0.7,
                    )
                    response = completion.choices[0].message.content.strip()
                    print(f"📥 Raw API response for chunk {i+1}: {response[:200]}...")

                    # Clean up response if it contains markdown formatting
                    if response.startswith('```json'):
                        response = response[7:]
                    if response.endswith('```'):
                        response = response[:-3]
                    response = response.strip()

                    print(f"🧹 Cleaned response: {response[:200]}...")

                    chunk_questions = json.loads(response)
                    print(f"✅ Parsed {len(chunk_questions) if isinstance(chunk_questions, list) else 1} questions from chunk {i+1}")

                    # Add questions from this chunk with validation
                    if isinstance(chunk_questions, list):
                        valid_questions = []
                        for q in chunk_questions:
                            if (isinstance(q, dict) and
                                q.get('question') and
                                q.get('options') and
                                q.get('correct')):
                                valid_questions.append(q)
                                print(f"✅ Valid question: {q.get('question', '')[:50]}...")
                            else:
                                print(f"⚠️ Skipping invalid question: {q}")
                        all_questions.extend(valid_questions)
                    else:
                        # Handle case where API returns a single question object instead of a list
                        if (isinstance(chunk_questions, dict) and
                            chunk_questions.get('question') and
                            chunk_questions.get('options') and
                            chunk_questions.get('correct')):
                            all_questions.append(chunk_questions)
                            print(f"✅ Valid single question: {chunk_questions.get('question', '')[:50]}...")
                        else:
                            print(f"⚠️ Skipping invalid single question: {chunk_questions}")

                    # If we have enough questions, stop processing chunks
                    if len(all_questions) >= num_questions:
                        all_questions = all_questions[:num_questions]  # Trim to exact number
                        break

                except Exception as chunk_error:
                    print(f"Error processing chunk {i+1}: {chunk_error}")
                    continue

            return all_questions
        else:
            # Original behavior for text that fits in context window
            prompt = f"""Generate exactly {num_questions} multiple-choice questions (MCQs) from the following text.

            ⚠️ MANDATORY QUALITY RULES - MUST FOLLOW STRICTLY:

            1. SINGLE CORRECT ANSWER RULE (CRITICAL):
               - Ensure ONLY ONE option is correct under ALL circumstances
               - The correct answer must be unambiguous and absolute
               - No option should be "partially correct" or "correct in some cases"

            2. NO CONDITIONAL/SITUATIONAL LANGUAGE:
               - Do NOT frame questions involving conditional, optional, or situational clauses unless explicitly stated in the question
               - Avoid words like "may", "can", "if required", "in case of", "unless", "sometimes", "usually", "generally"
               - Only use absolute statements that are always true or always false

            3. VERIFICATION FOR 'NOT CORRECT' QUESTIONS:
               - For questions asking "Which is NOT correct?", verify that the remaining three options are EXPLICITLY stated in the PDF as correct
               - Do NOT infer or assume - only use facts directly stated in the text
               - If exclusivity cannot be guaranteed, DO NOT generate the question

            4. PARAGRAPH REFERENCE (MANDATORY):
               - Include the exact paragraph/section reference in the explanation for validation
               - Format: "Reference: [Section/Rule/Paragraph number or identifier]"

            5. INDEPENDENT VERIFIABILITY:
               - Each option must be independently verifiable from the PDF
               - Generate assertion-reason or statement-based MCQs where possible
               - Each statement in options should be traceable to specific text

            6. EXCLUSIVITY GUARANTEE:
               - If exclusivity of the correct answer cannot be guaranteed, DO NOT generate the question
               - Skip ambiguous topics rather than creating potentially incorrect questions

            7. COVERAGE AND DISTRIBUTION:
               - Cover ALL major rules and notes evenly
               - DO NOT over-emphasize a single rule
               - Distribute questions across different topics
               - Include: Applicability, exclusions, definitions, numerical provisions, amendments

            DIFFICULTY DISTRIBUTION:
               - 40% easy (direct rule-based facts)
               - 40% medium (rule + condition combination)
               - 20% tricky (exceptions, notes, negative framing)

            FORMAT REQUIREMENTS:
               - Each question must have 4 options (A, B, C, D)
               - Include correct answer letter
               - Provide brief explanation WITH paragraph reference
               - Format as valid JSON array
            {explanation_instruction}

            JSON Structure:
            {{
                "question": "[Question Text]",
                "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
                "correct": "[Correct Option Letter]",
                "difficulty": "[easy/medium/hard]",
                "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]{source_reference}"
            }}

            Text: {text}
            """

            print(f"📤 Sending main prompt: {prompt[:300]}...")
            print(f"📤 Sending API request to {model}")
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an expert educator specializing in government rules, regulations, and policy documents. You create high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7,
            )
            response = completion.choices[0].message.content.strip()
            print(f"📥 Raw API response: {response[:300]}...")

            # Clean up response if it contains markdown formatting
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()

            print(f"🧹 Cleaned response: {response[:300]}...")

            parsed_response = json.loads(response)
            print(f"✅ Successfully parsed {len(parsed_response) if isinstance(parsed_response, list) else 1} questions")

            # Validate the response
            if isinstance(parsed_response, list):
                valid_questions = []
                for q in parsed_response:
                    if (isinstance(q, dict) and
                        q.get('question') and
                        q.get('options') and
                        q.get('correct')):
                        valid_questions.append(q)
                        print(f"✅ Valid question: {q.get('question', '')[:50]}...")
                    else:
                        print(f"⚠️ Skipping invalid question: {q}")

                if valid_questions:
                    print(f"🎯 Returning {len(valid_questions)} valid questions")
                    return valid_questions
                else:
                    print("❌ No valid questions found in response")
                    return "Error: No valid questions generated"
            else:
                print("❌ Response is not a list of questions")
                return "Error: Invalid response format"
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"📄 Raw response that failed to parse: {response if 'response' in locals() else 'No response captured'}")
        return f"Error parsing AI response: {str(e)}"
    except Exception as e:
        print(f"❌ Unexpected error in online generation: {e}")
        import traceback
        traceback.print_exc()
        return f"Error generating questions: {e}"

def generate_mcq_questions_advanced(text, num_questions=5, difficulty='medium', model_config=None):
    """Advanced MCQ generation with custom model support."""
    try:
        if not model_config:
            # Fallback to default configuration
            return generate_mcq_questions(text, num_questions, 'openrouter', 'basic')

        provider = model_config.get('provider', 'openrouter')
        model_name = model_config.get('model_name', 'deepseek/deepseek-chat')
        custom_api_key = model_config.get('custom_api_key')
        custom_base_url = model_config.get('custom_base_url')
        book_name = model_config.get('book_name', '').strip()
        chapter_name = model_config.get('chapter_name', '').strip()
        use_amendment = model_config.get('use_amendment', False)

        print(f"🚀 Starting advanced generation with provider: {provider}")
        print(f"🤖 Model selected: {model_name}")
        print(f"📝 Text length: {len(text)} characters")
        print(f"🎯 Questions requested: {num_questions}")

        # Get AI client with custom configuration
        client = get_ai_client(provider, custom_api_key, custom_base_url)

        # Build source reference using only manual inputs
        source_reference = build_reference_string({}, book_name, chapter_name)

        # Enhanced prompt with difficulty specification and source reference
        explanation_instruction = ""
        if source_reference:
            explanation_instruction = f"- In the explanation, include the source reference at the end: {source_reference}"

        # Add amendment-specific instructions if enabled
        amendment_section = create_amendment_prompt_section(use_amendment)

        # Check if text needs to be chunked
        token_count = estimate_token_count(text)
        max_context_tokens, is_free_tier, rate_limit = get_model_token_limits(provider, model_name)

        print(f"📊 Text analysis: {token_count} tokens, limit: {max_context_tokens} ({'free tier' if is_free_tier else 'paid tier'}, rate limit: {rate_limit})")

        # If text is too large, chunk it
        if token_count > max_context_tokens:
            chunks = chunk_text(text, max_context_tokens)
            all_questions = []
            questions_per_chunk = max(1, math.ceil(num_questions / len(chunks)))

            # Process each chunk
            for i, chunk in enumerate(chunks):
                # For the last chunk, adjust questions to match total requested
                if i == len(chunks) - 1:
                    remaining = num_questions - len(all_questions)
                    if remaining <= 0:
                        break
                    questions_per_chunk = remaining

                chunk_prompt = f"""Generate exactly {questions_per_chunk} multiple-choice questions (MCQs) from the following text.

                ⚠️ MANDATORY QUALITY RULES - MUST FOLLOW STRICTLY:

                1. SINGLE CORRECT ANSWER RULE (CRITICAL):
                   - Ensure ONLY ONE option is correct under ALL circumstances
                   - The correct answer must be unambiguous and absolute
                   - No option should be "partially correct" or "correct in some cases"

                2. NO CONDITIONAL/SITUATIONAL LANGUAGE:
                   - Do NOT frame questions involving conditional, optional, or situational clauses unless explicitly stated in the question
                   - Avoid words like "may", "can", "if required", "in case of", "unless", "sometimes", "usually", "generally"
                   - Only use absolute statements that are always true or always false

                3. VERIFICATION FOR 'NOT CORRECT' QUESTIONS:
                   - For questions asking "Which is NOT correct?", verify that the remaining three options are EXPLICITLY stated in the PDF as correct
                   - Do NOT infer or assume - only use facts directly stated in the text
                   - If exclusivity cannot be guaranteed, DO NOT generate the question

                4. PARAGRAPH REFERENCE (MANDATORY):
                   - Include the exact paragraph/section reference in the explanation for validation
                   - Format: "Reference: [Section/Rule/Paragraph number or identifier]"

                5. INDEPENDENT VERIFIABILITY:
                   - Each option must be independently verifiable from the PDF
                   - Generate assertion-reason or statement-based MCQs where possible
                   - Each statement in options should be traceable to specific text

                6. EXCLUSIVITY GUARANTEE:
                   - If exclusivity of the correct answer cannot be guaranteed, DO NOT generate the question
                   - Skip ambiguous topics rather than creating potentially incorrect questions

                7. COVERAGE AND DISTRIBUTION:
                   - Cover ALL major rules and notes evenly
                   - DO NOT over-emphasize a single rule
                   - Distribute questions across different topics
                   - Include: Applicability, exclusions, definitions, numerical provisions, amendments

                DIFFICULTY DISTRIBUTION:
                   - 40% easy (direct rule-based facts)
                   - 40% medium (rule + condition combination)
                   - 20% tricky (exceptions, notes, negative framing)

                FORMAT REQUIREMENTS:
                   - Each question must have 4 options (A, B, C, D)
                   - Include correct answer letter
                   - Provide brief explanation WITH paragraph reference
                   - Format as valid JSON array
                {explanation_instruction}{amendment_section}

                JSON Structure:
                {{
                    "question": "[Question Text]",
                    "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
                    "correct": "[Correct Option Letter]",
                    "difficulty": "[easy/medium/hard]",
                    "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]{source_reference}"
                }}

                Text: {chunk}
                """

                # Add rate limiting delay for free tier models
                delay = get_rate_limit_delay(model_name, i+1)
                if delay > 0:
                    print(f"⏳ Rate limit delay: waiting {delay} seconds before chunk {i+1}...")
                    time.sleep(delay)

                try:
                    # Build system message based on amendment mode
                    if use_amendment:
                        system_message = "You are an expert educator analyzing an original document and its amendment. You create high-quality MCQs with ONLY ONE correct answer per question, focusing on changes, differences, and new provisions introduced by amendments. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation (specify Original/Amendment), 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed, 6) Focus on amendment changes and differences. Always respond with valid JSON array format."
                    else:
                        system_message = "You are an expert educator specializing in government rules, regulations, and policy documents. You create high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON array format."

                    completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": chunk_prompt}
                        ],
                        max_tokens=4000,
                        temperature=0.7,
                    )

                    response = completion.choices[0].message.content.strip()

                    # Clean up response if it contains markdown formatting
                    if response.startswith('```json'):
                        response = response[7:]
                    if response.endswith('```'):
                        response = response[:-3]
                    response = response.strip()

                    chunk_questions = json.loads(response)

                    # Add questions from this chunk
                    if isinstance(chunk_questions, list):
                        all_questions.extend(chunk_questions)
                    else:
                        # Handle case where API returns a single question object instead of a list
                        all_questions.append(chunk_questions)

                    # If we have enough questions, stop processing chunks
                    if len(all_questions) >= num_questions:
                        all_questions = all_questions[:num_questions]  # Trim to exact number
                        break

                except Exception as chunk_error:
                    print(f"Error processing chunk {i+1}: {chunk_error}")
                    continue

            return all_questions
        else:
            # Original behavior for text that fits in context window
            prompt = f"""Generate exactly {num_questions} multiple-choice questions (MCQs) from the following text.

            ⚠️ MANDATORY QUALITY RULES - MUST FOLLOW STRICTLY:

            1. SINGLE CORRECT ANSWER RULE (CRITICAL):
               - Ensure ONLY ONE option is correct under ALL circumstances
               - The correct answer must be unambiguous and absolute
               - No option should be "partially correct" or "correct in some cases"

            2. NO CONDITIONAL/SITUATIONAL LANGUAGE:
               - Do NOT frame questions involving conditional, optional, or situational clauses unless explicitly stated in the question
               - Avoid words like "may", "can", "if required", "in case of", "unless", "sometimes", "usually", "generally"
               - Only use absolute statements that are always true or always false

            3. VERIFICATION FOR 'NOT CORRECT' QUESTIONS:
               - For questions asking "Which is NOT correct?", verify that the remaining three options are EXPLICITLY stated in the PDF as correct
               - Do NOT infer or assume - only use facts directly stated in the text
               - If exclusivity cannot be guaranteed, DO NOT generate the question

            4. PARAGRAPH REFERENCE (MANDATORY):
               - Include the exact paragraph/section reference in the explanation for validation
               - Format: "Reference: [Section/Rule/Paragraph number or identifier]"

            5. INDEPENDENT VERIFIABILITY:
               - Each option must be independently verifiable from the PDF
               - Generate assertion-reason or statement-based MCQs where possible
               - Each statement in options should be traceable to specific text

            6. EXCLUSIVITY GUARANTEE:
               - If exclusivity of the correct answer cannot be guaranteed, DO NOT generate the question
               - Skip ambiguous topics rather than creating potentially incorrect questions

            7. COVERAGE AND DISTRIBUTION:
               - Cover ALL major rules and notes evenly
               - DO NOT over-emphasize a single rule
               - Distribute questions across different topics
               - Include: Applicability, exclusions, definitions, numerical provisions, amendments

            DIFFICULTY DISTRIBUTION:
               - 40% easy (direct rule-based facts)
               - 40% medium (rule + condition combination)
               - 20% tricky (exceptions, notes, negative framing)

            FORMAT REQUIREMENTS:
               - Each question must have 4 options (A, B, C, D)
               - Include correct answer letter
               - Provide brief explanation WITH paragraph reference
               - Format as valid JSON array
            {explanation_instruction}

            JSON Structure:
            {{
                "question": "[Question Text]",
                "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
                "correct": "[Correct Option Letter]",
                "difficulty": "[easy/medium/hard]",
                "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]{source_reference}"
            }}

            Text: {text}
            """

            print(f"📤 Sending API request to model: {model_name}")

            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an expert educator specializing in government rules, regulations, and policy documents. You create high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON array format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7,
            )

            print(f"✅ API response received from {model_name}")
            response = completion.choices[0].message.content.strip()

            # Clean up response if it contains markdown formatting
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            response = response.strip()

            # Also handle markdown with just "json" (some models)
            if response.startswith('```'):
                # Find the end of the first line
                first_newline = response.find('\n')
                if first_newline != -1:
                    response = response[first_newline+1:]
                if response.endswith('```'):
                    response = response[:-3]
                response = response.strip()

            parsed_response = json.loads(response)
            print(f"✅ Successfully parsed {len(parsed_response) if isinstance(parsed_response, list) else 1} questions from {model_name}")
            return parsed_response

    except json.JSONDecodeError as json_error:
        print(f"❌ JSON parsing error with model {model_name}: {json_error}")
        print(f"📄 Raw response: {response[:500] if 'response' in locals() else 'No response'}")
        return f"Error parsing AI response from {model_name}: {json_error}"
    except Exception as e:
        print(f"❌ Error with model {model_name}: {type(e).__name__}: {e}")
        return f"Error generating questions with {model_name}: {e}"


def generate_mcq_questions_with_offline_fallback(text, num_questions=5, difficulty='medium',
                                                book_name='', chapter_name='',
                                                prefer_offline=False, prefer_professional=False,
                                                prefer_fast=False, model_config=None, use_amendment=False):
    """
    Generate MCQ questions with multiple fallback options including professional and fast modes.

    Args:
        text (str): Text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)
        book_name (str): Book name for reference
        chapter_name (str): Chapter name for reference
        prefer_offline (bool): Whether to prefer offline generation
        prefer_professional (bool): Whether to prefer professional models
        prefer_fast (bool): Whether to prefer fast generation
        model_config (dict): Configuration for online models
        use_amendment (bool): Whether amendment analysis is enabled

    Returns:
        list: Generated MCQ questions or error message
    """
    # Try fast generation first if preferred and available
    if prefer_fast and FAST_AVAILABLE:
        try:
            print("⚡ Attempting fast MCQ generation...")
            questions = generate_fast_mcq_questions(text, num_questions, difficulty)
            if questions and len(questions) > 0:
                # Add source reference if provided
                if book_name or chapter_name:
                    source_ref = f" (Source: {book_name} {chapter_name})".strip()
                    for question in questions:
                        question["explanation"] += source_ref

                print(f"✅ Successfully generated {len(questions)} questions quickly")
                return questions
            else:
                print("Fast generation returned no questions, falling back...")
        except Exception as e:
            print(f"Fast generation failed: {e}, falling back...")

    # Try enhanced professional generation first if professional is preferred
    if prefer_professional and ENHANCED_PROFESSIONAL_AVAILABLE:
        try:
            print("🎯 Attempting enhanced professional MCQ generation...")
            questions = generate_enhanced_professional_mcq_questions(text, num_questions, difficulty)
            if questions and len(questions) > 0:
                # Add source reference if provided
                if book_name or chapter_name:
                    source_ref = f" (Source: {book_name} {chapter_name})".strip()
                    for question in questions:
                        question["explanation"] += source_ref

                print(f"✅ Successfully generated {len(questions)} enhanced professional questions")
                return questions
            else:
                print("Enhanced professional generation returned no questions, falling back...")
        except Exception as e:
            print(f"Enhanced professional generation failed: {e}, falling back...")

    # Try regular professional generation if enhanced not available
    if prefer_professional and PROFESSIONAL_AVAILABLE:
        try:
            print("🎯 Attempting professional MCQ generation...")
            questions = generate_professional_mcq_questions(text, num_questions, difficulty)
            if questions and len(questions) > 0:
                # Add source reference if provided
                if book_name or chapter_name:
                    source_ref = f" (Source: {book_name} {chapter_name})".strip()
                    for question in questions:
                        question["explanation"] += source_ref

                print(f"✅ Successfully generated {len(questions)} professional questions")
                return questions
            else:
                print("Professional generation returned no questions, falling back...")
        except Exception as e:
            print(f"Professional generation failed: {e}, falling back...")

    # Try offline generation if preferred and available
    if prefer_offline and OFFLINE_AVAILABLE:
        try:
            print("Attempting offline MCQ generation...")
            questions = generate_mcq_questions_offline(
                text, num_questions, difficulty, book_name, chapter_name
            )
            if questions and len(questions) > 0:
                print(f"Successfully generated {len(questions)} questions offline")
                return questions
            else:
                print("Offline generation returned no questions, falling back to online...")
        except Exception as e:
            print(f"Offline generation failed: {e}, falling back to online...")

    # Fallback to online generation
    try:
        if model_config:
            return generate_mcq_questions_advanced(
                text, num_questions, difficulty, model_config
            )
        else:
            return generate_mcq_questions(
                text, num_questions, 'openrouter', 'basic', book_name, chapter_name
            )
    except Exception as e:
        # Final fallbacks in order of preference
        if not prefer_fast and FAST_AVAILABLE:
            try:
                print("⚡ Online failed, trying fast as fallback...")
                questions = generate_fast_mcq_questions(text, num_questions, difficulty)
                if questions and len(questions) > 0:
                    print(f"✅ Fast fallback successful: {len(questions)} questions")
                    return questions
            except Exception as fast_error:
                print(f"Fast fallback failed: {fast_error}")

        if not prefer_professional and ENHANCED_PROFESSIONAL_AVAILABLE:
            try:
                print("🎯 Trying enhanced professional as fallback...")
                questions = generate_enhanced_professional_mcq_questions(text, num_questions, difficulty)
                if questions and len(questions) > 0:
                    print(f"✅ Enhanced professional fallback successful: {len(questions)} questions")
                    return questions
            except Exception as enhanced_prof_error:
                print(f"Enhanced professional fallback failed: {enhanced_prof_error}")

        if not prefer_professional and PROFESSIONAL_AVAILABLE:
            try:
                print("🎯 Trying professional as fallback...")
                questions = generate_professional_mcq_questions(text, num_questions, difficulty)
                if questions and len(questions) > 0:
                    print(f"✅ Professional fallback successful: {len(questions)} questions")
                    return questions
            except Exception as prof_error:
                print(f"Professional fallback failed: {prof_error}")

        if not prefer_offline and OFFLINE_AVAILABLE:
            try:
                print("Trying offline as final fallback...")
                questions = generate_mcq_questions_offline(
                    text, num_questions, difficulty, book_name, chapter_name
                )
                if questions and len(questions) > 0:
                    print(f"Offline fallback successful: {len(questions)} questions")
                    return questions
            except Exception as offline_error:
                print(f"Offline fallback also failed: {offline_error}")

        return f"Error generating questions: {e}"


def generate_professional_mcq_questions_enhanced(text, num_questions=10, difficulty='medium',
                                               book_name='', chapter_name=''):
    """
    Generate professional-quality MCQ questions using the best available models.

    Args:
        text (str): Text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)
        book_name (str): Book name for reference
        chapter_name (str): Chapter name for reference

    Returns:
        list: Professional-quality MCQ questions or error message
    """
    # Try enhanced professional first
    if ENHANCED_PROFESSIONAL_AVAILABLE:
        try:
            print("🎯 Generating enhanced professional-quality MCQ questions...")
            questions = generate_enhanced_professional_mcq_questions(text, num_questions, difficulty)

            # Add source reference if provided
            if book_name or chapter_name:
                source_ref = f" (Source: {book_name} {chapter_name})".strip()
                for question in questions:
                    question["explanation"] += source_ref

            return questions

        except Exception as e:
            print(f"Enhanced professional generation failed: {e}, trying regular professional...")

    # Fallback to regular professional
    if PROFESSIONAL_AVAILABLE:
        try:
            print("🎯 Generating professional-quality MCQ questions...")
            questions = generate_professional_mcq_questions(text, num_questions, difficulty)

            # Add source reference if provided
            if book_name or chapter_name:
                source_ref = f" (Source: {book_name} {chapter_name})".strip()
                for question in questions:
                    question["explanation"] += source_ref

            return questions

        except Exception as e:
            return f"Error generating professional questions: {e}"

    return "Professional MCQ generation not available. Install professional models to enable."


def generate_fast_mcq_questions_enhanced(text, num_questions=10, difficulty='medium',
                                        book_name='', chapter_name=''):
    """
    Generate MCQ questions quickly using optimized fast models.

    Args:
        text (str): Text to generate questions from
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level (easy/medium/hard)
        book_name (str): Book name for reference
        chapter_name (str): Chapter name for reference

    Returns:
        list: Fast-generated MCQ questions or error message
    """
    if not FAST_AVAILABLE:
        return "Fast MCQ generation not available. Run 'python setup_fast_models.py' to enable."

    try:
        print("⚡ Generating fast MCQ questions...")
        questions = generate_fast_mcq_questions(text, num_questions, difficulty)

        # Add source reference if provided
        if book_name or chapter_name:
            source_ref = f" (Source: {book_name} {chapter_name})".strip()
            for question in questions:
                question["explanation"] += source_ref

        return questions

    except Exception as e:
        return f"Error generating fast questions: {e}"


def get_generation_capabilities():
    """
    Get information about available generation methods.

    Returns:
        dict: Available capabilities and their status
    """
    capabilities = {
        "online_available": True,  # Assuming online is always available if API keys are set
        "offline_available": OFFLINE_AVAILABLE,
        "professional_available": PROFESSIONAL_AVAILABLE or ENHANCED_PROFESSIONAL_AVAILABLE,
        "enhanced_professional_available": ENHANCED_PROFESSIONAL_AVAILABLE,
        "fast_available": FAST_AVAILABLE,
        "recommended_method": "professional" if ENHANCED_PROFESSIONAL_AVAILABLE else ("fast" if FAST_AVAILABLE else ("professional" if PROFESSIONAL_AVAILABLE else "hybrid")),
        "max_questions_offline": 50 if OFFLINE_AVAILABLE else 0,
        "max_questions_online": 100,
        "max_questions_professional": 150 if (PROFESSIONAL_AVAILABLE or ENHANCED_PROFESSIONAL_AVAILABLE) else 0,
        "max_questions_fast": 100 if FAST_AVAILABLE else 0,
        "quality_ranking": [],
        "speed_ranking": []
    }

    # Check if API keys are available for online generation
    online_keys_available = any([
        os.getenv("OPENAI_API_KEY"),
        os.getenv("OPENROUTER_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("DEEPSEEK_API_KEY")
    ])

    capabilities["online_available"] = online_keys_available

    # Determine recommended method, quality ranking, and speed ranking
    if ENHANCED_PROFESSIONAL_AVAILABLE:
        capabilities["recommended_method"] = "professional"
        capabilities["quality_ranking"] = ["enhanced_professional", "professional", "fast", "online", "offline"]
        capabilities["speed_ranking"] = ["fast", "offline", "online", "professional", "enhanced_professional"]
    elif FAST_AVAILABLE:
        capabilities["recommended_method"] = "fast"
        capabilities["quality_ranking"] = ["professional", "fast", "online", "offline"] if PROFESSIONAL_AVAILABLE else ["fast", "online", "offline"]
        capabilities["speed_ranking"] = ["fast", "offline", "online", "professional"]
    elif PROFESSIONAL_AVAILABLE:
        capabilities["recommended_method"] = "professional"
        capabilities["quality_ranking"] = ["professional", "online", "offline"]
        capabilities["speed_ranking"] = ["offline", "online", "professional"]
    elif online_keys_available and OFFLINE_AVAILABLE:
        capabilities["recommended_method"] = "hybrid"
        capabilities["quality_ranking"] = ["online", "offline"]
        capabilities["speed_ranking"] = ["offline", "online"]
    elif online_keys_available:
        capabilities["recommended_method"] = "online_only"
        capabilities["quality_ranking"] = ["online"]
        capabilities["speed_ranking"] = ["online"]
    elif OFFLINE_AVAILABLE:
        capabilities["recommended_method"] = "offline_only"
        capabilities["quality_ranking"] = ["offline"]
        capabilities["speed_ranking"] = ["offline"]
    else:
        capabilities["recommended_method"] = "none"
        capabilities["quality_ranking"] = []
        capabilities["speed_ranking"] = []

    # Add setup instructions
    capabilities["setup_instructions"] = {
        "fast": "Run 'python setup_fast_models.py' for speed optimization",
        "professional": "Run 'python setup_professional_models.py' for best quality",
        "offline": "Run 'python setup_offline.py' for offline capability",
        "online": "Configure API keys in .env file"
    }

    return capabilities

def generate_mcq_questions_with_metadata(pdf_path, num_questions=5, difficulty='medium',
                                        book_name='', chapter_name='',
                                        prefer_offline=False, model_config=None):
    """
    Generate MCQ questions with detailed page and section metadata tracking.

    Args:
        pdf_path (str): Path to the PDF file
        num_questions (int): Number of questions to generate
        difficulty (str): Difficulty level
        book_name (str): Book name for reference
        chapter_name (str): Chapter name for reference
        prefer_offline (bool): Whether to prefer offline generation
        model_config (dict): Model configuration

    Returns:
        dict: {
            'questions': list of MCQ questions with metadata,
            'summary': dict with distribution statistics,
            'page_map': list of page information,
            'sections': list of detected sections
        }
    """
    try:
        # Extract text with metadata
        print("📄 Extracting text with page and section tracking...")
        extraction_result = extract_text_from_pdf_with_metadata(pdf_path)

        # Check if extraction failed
        if isinstance(extraction_result, str):
            return {'error': extraction_result}

        text = extraction_result['text']
        page_map = extraction_result['page_map']
        sections = extraction_result['sections']
        total_pages = extraction_result['total_pages']

        print(f"📊 Extracted {len(text)} characters from {total_pages} pages")
        print(f"🔍 Detected {len(sections)} sections/headings")

        # Handle amendment text if provided
        use_amendment = False
        amendment_text = None
        if model_config and model_config.get('use_amendment'):
            amendment_text = model_config.get('amendment_text')
            if amendment_text and amendment_text.strip():
                use_amendment = True
                print("📝 Amendment text detected - merging for analysis...")
                text = merge_texts_for_amendment_analysis(text, amendment_text)
                print(f"📊 Merged text length: {len(text)} characters")

        # Generate questions using existing function
        questions = generate_mcq_questions_with_offline_fallback(
            text=text,
            num_questions=num_questions,
            difficulty=difficulty,
            book_name=book_name,
            chapter_name=chapter_name,
            prefer_offline=prefer_offline,
            model_config=model_config,
            use_amendment=use_amendment
        )

        # Check if generation failed
        if isinstance(questions, str):
            return {'error': questions}

        # Generate PDF summary
        print("📋 Generating PDF summary...")
        pdf_summary = generate_pdf_summary(text)
        print(f"✅ PDF Summary: {pdf_summary}")

        # Add metadata to each question by analyzing the question text
        print("🏷️  Adding page and section metadata to questions...")
        for i, question in enumerate(questions):
            # Try to find which part of the PDF this question relates to
            question_text = question.get('question', '')

            # Search for question keywords in page text
            metadata = {'pages': [], 'sections': []}

            # Extract key terms from question (simple approach)
            question_words = set(re.findall(r'\b\w{4,}\b', question_text.lower()))

            best_match_score = 0
            best_match_pages = []
            best_match_sections = []

            for page_info in page_map:
                page_text_lower = page_info['text'].lower()
                # Count how many question keywords appear in this page
                matches = sum(1 for word in question_words if word in page_text_lower)

                if matches > best_match_score:
                    best_match_score = matches
                    best_match_pages = [page_info['page_number']]
                    best_match_sections = [s['title'] for s in page_info.get('sections', [])]
                elif matches == best_match_score and matches > 0:
                    best_match_pages.append(page_info['page_number'])
                    best_match_sections.extend([s['title'] for s in page_info.get('sections', [])])

            # Remove duplicates and sort
            metadata['pages'] = sorted(list(set(best_match_pages)))
            metadata['sections'] = list(set(best_match_sections))

            # Add metadata to question
            question['metadata'] = metadata
            question['question_number'] = i + 1

            # Equalize answer lengths to prevent correct answer identification by length
            question = equalize_answer_lengths(question)

        # Generate summary statistics
        summary = generate_question_distribution_summary(questions, page_map, sections, total_pages)

        return {
            'questions': questions,
            'summary': summary,
            'page_map': page_map,
            'sections': sections,
            'total_pages': total_pages,
            'pdf_summary': pdf_summary
        }

    except Exception as e:
        print(f"❌ Error in metadata generation: {e}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}

def generate_question_distribution_summary(questions, page_map, sections, total_pages):
    """
    Generates a detailed summary of question distribution across pages and sections.

    Args:
        questions (list): List of questions with metadata
        page_map (list): List of page information
        sections (list): List of detected sections
        total_pages (int): Total number of pages

    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_questions': len(questions),
        'total_pages': total_pages,
        'total_sections': len(sections),
        'page_distribution': {},
        'section_distribution': {},
        'pages_with_questions': [],
        'pages_without_questions': [],
        'coverage_percentage': 0
    }

    # Count questions per page
    for question in questions:
        for page_num in question.get('metadata', {}).get('pages', []):
            if page_num not in summary['page_distribution']:
                summary['page_distribution'][page_num] = 0
            summary['page_distribution'][page_num] += 1

    # Count questions per section
    for question in questions:
        for section in question.get('metadata', {}).get('sections', []):
            if section not in summary['section_distribution']:
                summary['section_distribution'][section] = 0
            summary['section_distribution'][section] += 1

    # Identify pages with and without questions
    summary['pages_with_questions'] = sorted(summary['page_distribution'].keys())
    all_pages = set(range(1, total_pages + 1))
    summary['pages_without_questions'] = sorted(all_pages - set(summary['pages_with_questions']))

    # Calculate coverage
    if total_pages > 0:
        summary['coverage_percentage'] = (len(summary['pages_with_questions']) / total_pages) * 100

    return summary