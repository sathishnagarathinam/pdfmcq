from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from PyPDF2 import PdfReader
import re

# Load environment variables
load_dotenv()

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

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
    if model_provider == 'custom':
        # Use custom configuration
        if not custom_api_key:
            raise ValueError("Custom API key is required for custom model provider")

        client_config = {"api_key": custom_api_key}
        if custom_base_url:
            client_config["base_url"] = custom_base_url

        return OpenAI(**client_config)

    elif model_provider == 'openrouter':
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    elif model_provider == 'openai':
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    elif model_provider == 'anthropic':
        # Note: Anthropic uses a different API format, but we'll use OpenAI-compatible wrapper
        return OpenAI(
            base_url="https://api.anthropic.com/v1",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )
    elif model_provider == 'deepseek':
        return OpenAI(
            base_url="https://api.deepseek.com",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

def get_model_name(model_provider, model_type):
    """Returns the appropriate model name based on provider and type."""
    models = {
        'openrouter': {
            'basic': 'deepseek/deepseek-chat:free',
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

def generate_mcq_questions(text, num_questions=5, model_provider='openrouter', model_type='basic', book_name='', chapter_name=''):
    """Generates MCQ questions using the selected AI model."""
    try:
        client = get_ai_client(model_provider)
        model = get_model_name(model_provider, model_type)

        # Build source reference using only manual inputs
        source_reference = build_reference_string({}, book_name, chapter_name)

        explanation_instruction = ""
        if source_reference:
            explanation_instruction = f" Include the source reference at the end: {source_reference}"

        prompt = f"""Generate exactly {num_questions} multiple-choice questions (MCQs) with 4 options, the correct answer, difficulty level, and a brief explanation for the correct answer from the following text.{explanation_instruction} Format the output as a JSON array with each question having the following structure:
        {{
            "question": "[Question Text]",
            "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
            "correct": "[Correct Option Letter]",
            "difficulty": "[easy/medium/hard]",
            "explanation": "[Explanation for the correct answer]{source_reference}"
        }}

    Text: {text}
    """

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates multiple-choice questions. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.7,
        )
        response = completion.choices[0].message.content.strip()
        return json.loads(response)
    except Exception as e:
        return f"Error generating questions: {e}"

def generate_mcq_questions_advanced(text, num_questions=5, difficulty='medium', model_config=None):
    """Advanced MCQ generation with custom model support."""
    try:
        if not model_config:
            # Fallback to default configuration
            return generate_mcq_questions(text, num_questions, 'openrouter', 'basic')

        provider = model_config.get('provider', 'openrouter')
        model_name = model_config.get('model_name', 'deepseek/deepseek-chat:free')
        custom_api_key = model_config.get('custom_api_key')
        custom_base_url = model_config.get('custom_base_url')
        book_name = model_config.get('book_name', '').strip()
        chapter_name = model_config.get('chapter_name', '').strip()

        # Get AI client with custom configuration
        client = get_ai_client(provider, custom_api_key, custom_base_url)

        # Build source reference using only manual inputs
        source_reference = build_reference_string({}, book_name, chapter_name)

        # Enhanced prompt with difficulty specification and source reference
        explanation_instruction = ""
        if source_reference:
            explanation_instruction = f"- In the explanation, include the source reference at the end: {source_reference}"

        prompt = f"""Generate exactly {num_questions} multiple-choice questions (MCQs) with {difficulty} difficulty level from the following text.

Requirements:
- Each question should have 4 options (A, B, C, D)
- Include the correct answer letter
- Provide a brief explanation for the correct answer
- Ensure questions match the specified difficulty: {difficulty}
- Format as valid JSON array
{explanation_instruction}

JSON Structure:
{{
    "question": "[Question Text]",
    "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
    "correct": "[Correct Option Letter]",
    "difficulty": "{difficulty}",
    "explanation": "[Explanation for the correct answer]{source_reference}"
}}

Text: {text}
"""

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert educator that creates high-quality multiple-choice questions. Always respond with valid JSON array format."},
                {"role": "user", "content": prompt}
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

        return json.loads(response)

    except Exception as e:
        return f"Error generating questions: {e}"