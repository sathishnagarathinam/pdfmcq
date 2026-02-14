from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from PyPDF2 import PdfReader

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
            'basic': 'openrouter/cypher-alpha:free',
            'advanced': 'openrouter/anthropic/claude-2:free'
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

def generate_mcq_questions(text, num_questions=5, model_provider='openrouter', model_type='basic'):
    """Generates MCQ questions using the selected AI model."""
    try:
        client = get_ai_client(model_provider)
        model = get_model_name(model_provider, model_type)

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
           - Distribute questions across different topics

        Format the output as a JSON array with each question having the following structure:
        {{
            "question": "[Question Text]",
            "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
            "correct": "[Correct Option Letter]",
            "difficulty": "[easy/medium/hard]",
            "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]"
        }}

    Text: {text}
    """

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert educator that generates high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON."},
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
        model_name = model_config.get('model_name', 'openrouter/cypher-alpha:free')
        custom_api_key = model_config.get('custom_api_key')
        custom_base_url = model_config.get('custom_base_url')

        # Get AI client with custom configuration
        client = get_ai_client(provider, custom_api_key, custom_base_url)

        # Enhanced prompt with difficulty specification and quality rules
        prompt = f"""Generate exactly {num_questions} multiple-choice questions (MCQs) with {difficulty} difficulty level from the following text.

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

6. EXCLUSIVITY GUARANTEE:
   - If exclusivity of the correct answer cannot be guaranteed, DO NOT generate the question

7. COVERAGE AND DISTRIBUTION:
   - Cover ALL major rules and notes evenly
   - Distribute questions across different topics

JSON Structure:
{{
    "question": "[Question Text]",
    "options": {{"A": "[Option A]", "B": "[Option B]", "C": "[Option C]", "D": "[Option D]"}},
    "correct": "[Correct Option Letter]",
    "difficulty": "{difficulty}",
    "explanation": "[Explanation for the correct answer. Reference: Section/Rule X]"
}}

Text: {text}
"""

        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert educator that creates high-quality MCQs with ONLY ONE correct answer per question. You MUST: 1) Ensure single correct answer under all circumstances, 2) Avoid conditional words like 'may', 'can', 'if required', 3) Include paragraph references for validation, 4) Make each option independently verifiable, 5) Skip questions if exclusivity cannot be guaranteed. Always respond with valid JSON array format."},
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