from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import os
import json
import sys

from mcq_generator import (
    extract_text_from_pdf, generate_mcq_questions, generate_mcq_questions_advanced,
    estimate_max_questions, estimate_max_questions_detailed,
    generate_mcq_questions_with_offline_fallback, get_generation_capabilities,
    generate_mcq_questions_with_metadata
)

from mcq_parser import parse_mcq_pdf, debug_pdf_content

import pandas as pd
from fpdf import FPDF
from io import BytesIO
import tempfile
import shutil
from pathlib import Path
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# Serverless Configuration
# ============================================
# Detect if running on Vercel (VERCEL env var is set automatically by Vercel)
IS_VERCEL = bool(os.environ.get('VERCEL'))

# Use system temp directory for serverless environments
if IS_VERCEL:
    UPLOAD_FOLDER = tempfile.gettempdir()
else:
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 52428800  # 50MB max file size

# Secret key for session management (loaded from .env)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-in-production')

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access - return JSON for AJAX, redirect for pages"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return jsonify({'error': 'Authentication required. Please log in.'}), 401
    return redirect(url_for('login', next=request.url))

# ============================================
# Authentication Configuration
# ============================================
# Hardcoded user with bcrypt-hashed password (cost factor 12)
# Username: sathishsat04
# Password hash generated with bcrypt.gensalt(rounds=12)
USERS = {
    'sathishsat04': {
        'id': '1',
        'username': 'sathishsat04',
        'password_hash': '$2b$12$Z/AfIKQmaWHxw0z4Qtzu0uHal0p7GQmJDOzhKBRp433lOkdsFIxVG'
    }
}


class User(UserMixin):
    """User model for Flask-Login"""
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login session management"""
    for username, user_data in USERS.items():
        if user_data['id'] == user_id:
            return User(user_data['id'], username)
    return None


class LoginForm(FlaskForm):
    """Login form with CSRF protection"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Global variable to store current questions
current_questions = None

def cleanup_temp_files(file_path):
    """Safely cleanup temporary files"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not cleanup temp file {file_path}: {e}")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication handler"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if user exists
        user_data = USERS.get(username)
        if user_data:
            # Verify password against bcrypt hash
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
                user = User(user_data['id'], username)
                login_user(user)
                # Redirect to the page they were trying to access, or home
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))

        flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Logout and redirect to login page"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/capabilities', methods=['GET'])
@login_required
def get_capabilities():
    """Get information about available generation methods"""
    try:
        capabilities = get_generation_capabilities()
        return jsonify(capabilities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
@csrf.exempt
@login_required
def upload_file():
    global current_questions

    try:
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['pdfFile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Get form parameters
        question_count = int(request.form.get('questionCount', 5))
        use_max_questions = request.form.get('useMaxQuestions') == 'on'
        difficulty = request.form.get('difficulty', 'medium')
        model_provider = request.form.get('modelProvider', 'openrouter')
        model_name = request.form.get('modelName', 'deepseek/deepseek-chat')
        custom_api_key = request.form.get('customApiKey', '')
        custom_base_url = request.form.get('customBaseUrl', '')
        book_name = request.form.get('bookName', '').strip()
        chapter_name = request.form.get('chapterName', '').strip()
        prefer_offline = request.form.get('preferOffline') == 'on'
        use_offline_estimation = request.form.get('useOfflineEstimation') == 'on'

        # Amendment PDF support
        use_amendment = request.form.get('useAmendment') == 'on'
        amendment_file = None
        amendment_text = ""

        amendment_temp_path = None
        if use_amendment and 'amendmentPdfFile' in request.files:
            amendment_file = request.files['amendmentPdfFile']
            if amendment_file and amendment_file.filename != '':
                amendment_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"amendment_{amendment_file.filename}")
                amendment_file.save(amendment_temp_path)
                amendment_text = extract_text_from_pdf(amendment_temp_path)

                # Check if amendment extraction was successful
                is_amendment_error = (isinstance(amendment_text, str) and
                                     amendment_text.startswith('Error extracting text from PDF:'))
                if is_amendment_error:
                    cleanup_temp_files(amendment_temp_path)
                    return jsonify({'error': 'Failed to extract amendment PDF', 'details': amendment_text}), 400

        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(temp_path)

        # Extract text and generate questions
        extracted_text = extract_text_from_pdf(temp_path)

        # Check if text extraction was successful (check for specific error patterns at the start)
        is_error = (isinstance(extracted_text, str) and
                   (extracted_text.startswith('Error extracting text from PDF:') or
                    extracted_text.startswith('PDF Validation Error:') or
                    extracted_text.startswith('Failed to load PDF document:') or
                    extracted_text.startswith('No text could be extracted from the PDF') or
                    extracted_text.startswith('Unexpected error extracting text from PDF:')))

        if is_error:
            # Clean up before returning error
            cleanup_temp_files(temp_path)
            cleanup_temp_files(amendment_temp_path)

            # Return detailed error message
            error_response = {
                'error': 'PDF Processing Failed',
                'details': extracted_text,
                'suggestions': []
            }

            # Add specific suggestions based on error type
            if "scanned document" in extracted_text or "image-based PDF" in extracted_text:
                error_response['suggestions'] = [
                    "🚀 Enable OCR support: Run 'python setup_ocr.py' to handle image PDFs",
                    "📄 Use a PDF with selectable text instead",
                    "🌐 Convert using online OCR: https://www.onlineocr.net/",
                    "📝 Use a different PDF document"
                ]
            elif "corrupted" in extracted_text or "password-protected" in extracted_text:
                error_response['suggestions'] = [
                    "Check if the PDF file is corrupted",
                    "If password-protected, remove the password first",
                    "Try uploading a different PDF file"
                ]
            else:
                error_response['suggestions'] = [
                    "Ensure the file is a valid PDF document",
                    "Try uploading a different PDF file",
                    "Check if the PDF contains readable text"
                ]

            return jsonify(error_response), 400

        # Check if extracted text is empty
        if not extracted_text.strip():
            cleanup_temp_files(temp_path)
            cleanup_temp_files(amendment_temp_path)
            return jsonify({
                'error': 'Empty PDF Content',
                'details': 'The PDF appears to be empty or contains no readable text.',
                'suggestions': ['Please upload a PDF with text content.']
            }), 400

        # Estimate maximum questions and determine how many to generate
        if use_offline_estimation:
            estimation_result = estimate_max_questions_detailed(extracted_text)
            max_questions = estimation_result["max_questions"]
            estimation_info = estimation_result
        else:
            max_questions = estimate_max_questions(extracted_text, use_offline=False)
            estimation_info = {"max_questions": max_questions, "confidence": "basic"}

        if use_max_questions:
            questions_to_generate = max_questions
        else:
            questions_to_generate = question_count

        # Prepare model configuration
        model_config = {
            'provider': model_provider,
            'model_name': model_name,
            'custom_api_key': custom_api_key,
            'custom_base_url': custom_base_url,
            'book_name': book_name,
            'chapter_name': chapter_name,
            'use_amendment': use_amendment,
            'amendment_text': amendment_text if use_amendment else None
        }

        # Generate MCQ questions with metadata tracking
        print("🏷️  Generating questions with page and section metadata...")
        if use_amendment and amendment_text:
            print("📝 Amendment analysis enabled - generating questions covering amendments and changes...")

        result = generate_mcq_questions_with_metadata(
            pdf_path=temp_path,
            num_questions=questions_to_generate,
            difficulty=difficulty,
            book_name=book_name,
            chapter_name=chapter_name,
            prefer_offline=prefer_offline,
            model_config=model_config
        )

        # Clean up temporary files
        cleanup_temp_files(temp_path)
        cleanup_temp_files(amendment_temp_path)

        # Check if generation failed
        if 'error' in result:
            error_response = {
                'error': 'MCQ Generation Failed',
                'details': result['error'],
                'suggestions': []
            }

            # Add specific suggestions based on error type
            if "context length" in result['error'].lower():
                error_response['suggestions'] = [
                    "The document might be too large",
                    "Try with a smaller document or fewer questions"
                ]
            elif "api" in result['error'].lower():
                error_response['suggestions'] = [
                    "Check your API key configuration",
                    "Verify your internet connection",
                    "Try again in a few moments"
                ]
            else:
                error_response['suggestions'] = [
                    "Please try again",
                    "Contact support if the issue persists"
                ]

            return jsonify(error_response), 500

        questions = result['questions']
        summary = result['summary']

        # Store questions globally for download
        current_questions = questions

        return jsonify({
            'questions': questions,
            'summary': summary,
            'message': f'Successfully generated {len(questions)} MCQ questions',
            'text_length': len(extracted_text),
            'max_questions_estimate': max_questions,
            'used_max_questions': use_max_questions,
            'questions_generated': len(questions),
            'estimation_info': estimation_info,
            'generation_method': 'offline' if prefer_offline else 'online_with_fallback',
            'total_pages': result.get('total_pages', 0),
            'sections_detected': len(result.get('sections', []))
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-csv', methods=['POST'])
@csrf.exempt
@login_required
def download_csv():
    try:
        questions = request.json
        if not questions:
            return jsonify({'error': 'No questions data provided'}), 400
        
        # Create DataFrame without metadata columns (as per user request)
        df = pd.DataFrame([
            {
                'question': q.get('text') if q.get('text') else (q.get('question') if q.get('question') else ''),  # Support both 'text' and 'question' keys
                'option1': q['options'].get('A', ''),
                'option2': q['options'].get('B', ''),
                'option3': q['options'].get('C', ''),
                'option4': q['options'].get('D', ''),
                'correct': {'A':'1', 'B':'2', 'C':'3', 'D':'4'}.get(q.get('correct', ''), ''),
                'difficulty': q.get('difficulty', 'medium').capitalize(),
                'explanation': q.get('explanation', '')
            } for q in questions
        ])
        
        # Create CSV in memory
        csv_buffer = BytesIO()
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        csv_buffer.write(csv_data)
        csv_buffer.seek(0)
        
        return send_file(
            csv_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name='mcq_questions.csv'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-pdf', methods=['POST'])
@csrf.exempt
@login_required
def download_pdf():
    try:
        questions = request.json
        if not questions:
            return jsonify({'error': 'No questions data provided'}), 400

        print(f"Generating PDF for {len(questions)} questions")

        # Create PDF with proper error handling
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "PDF MCQ Generator-sathish", 0, 1, 'C')
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Multiple Choice Questions", 0, 1, 'C')
        pdf.ln(10)

        # Add questions
        for i, q in enumerate(questions, 1):
            try:
                # Question
                pdf.set_font("Arial", 'B', 12)
                # Support both 'text' and 'question' keys - check if text exists and is not empty
                question_content = q.get('text', '')
                if not question_content:
                    question_content = q.get('question', '')
                if not question_content:
                    question_content = 'No question text'
                question_text = f"{i}. {question_content}"

                # Split long questions into multiple lines
                if len(question_text) > 80:
                    words = question_text.split(' ')
                    lines = []
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 80:
                            current_line += word + " "
                        else:
                            lines.append(current_line.strip())
                            current_line = word + " "
                    if current_line:
                        lines.append(current_line.strip())

                    for line in lines:
                        pdf.cell(0, 8, line, 0, 1)
                else:
                    pdf.cell(0, 8, question_text, 0, 1)

                pdf.ln(2)

                # Options
                pdf.set_font("Arial", '', 11)
                options = q.get('options', {})
                pdf.cell(0, 6, f"A) {options.get('A', 'No option A')}", 0, 1)
                pdf.cell(0, 6, f"B) {options.get('B', 'No option B')}", 0, 1)
                pdf.cell(0, 6, f"C) {options.get('C', 'No option C')}", 0, 1)
                pdf.cell(0, 6, f"D) {options.get('D', 'No option D')}", 0, 1)
                pdf.ln(2)

                # Answer and explanation
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 6, f"Correct Answer: {q.get('correct', 'N/A')}", 0, 1)
                pdf.cell(0, 6, f"Difficulty: {q.get('difficulty', 'medium').capitalize()}", 0, 1)

                # Add metadata if available
                metadata = q.get('metadata', {})
                if metadata:
                    pages = metadata.get('pages', [])
                    sections = metadata.get('sections', [])
                    if pages or sections:
                        pdf.set_font("Arial", 'I', 10)
                        metadata_text = "Source: "
                        if pages:
                            metadata_text += f"Page(s) {', '.join(map(str, pages))}"
                        if sections:
                            if pages:
                                metadata_text += " | "
                            metadata_text += f"{', '.join(sections)}"
                        pdf.cell(0, 6, metadata_text, 0, 1)

                # Explanation
                pdf.set_font("Arial", '', 10)
                explanation = f"Explanation: {q.get('explanation', 'No explanation provided')}"
                if len(explanation) > 80:
                    words = explanation.split(' ')
                    lines = []
                    current_line = ""
                    for word in words:
                        if len(current_line + word) < 80:
                            current_line += word + " "
                        else:
                            lines.append(current_line.strip())
                            current_line = word + " "
                    if current_line:
                        lines.append(current_line.strip())

                    for line in lines:
                        pdf.cell(0, 6, line, 0, 1)
                else:
                    pdf.cell(0, 6, explanation, 0, 1)

                pdf.ln(8)

            except Exception as question_error:
                print(f"Error processing question {i}: {question_error}")
                # Add a simple error message and continue
                pdf.set_font("Arial", '', 10)
                pdf.cell(0, 6, f"Error processing question {i}", 0, 1)
                pdf.ln(4)
                continue
        
        # Create PDF in memory (use the working method)
        pdf_buffer = BytesIO()
        try:
            # Use output(dest='S') which works reliably
            pdf_string = pdf.output(dest='S')

            if not pdf_string:
                print("Error: PDF generation returned empty content")
                return jsonify({'error': 'PDF generation failed - empty content'}), 500

            if isinstance(pdf_string, str):
                pdf_buffer.write(pdf_string.encode('latin-1'))
            else:
                pdf_buffer.write(pdf_string)
            pdf_buffer.seek(0)

            # Verify PDF content
            pdf_content = pdf_buffer.getvalue()
            if len(pdf_content) == 0:
                print("Error: PDF buffer is empty")
                return jsonify({'error': 'PDF generation failed - 0 bytes generated'}), 500

            print(f"PDF generated successfully: {len(pdf_content)} bytes")

            return send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='mcq_questions.pdf'
            )

        except Exception as output_error:
            print(f"Error generating PDF output: {output_error}")
            return jsonify({'error': f'PDF generation failed: {output_error}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/parse-mcq', methods=['POST'])
@csrf.exempt
@login_required
def parse_mcq():
    """Parse an existing MCQ PDF and extract questions with answers"""
    global current_questions

    try:
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['pdfFile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Get form parameters
        answer_page = request.form.get('answerPage', '-1')
        try:
            answer_page_index = int(answer_page)
        except ValueError:
            answer_page_index = -1

        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(temp_path)

        try:
            # Parse the MCQ PDF with debug enabled
            print(f"📄 Parsing MCQ PDF: {file.filename}")
            result = parse_mcq_pdf(temp_path, answer_page_index, debug=True)

            if result.get('error'):
                error_msg = result['error']
                debug_info = result.get('debug_info', {})

                # Provide detailed error response
                error_response = {
                    'error': error_msg,
                    'debug_info': debug_info,
                    'suggestions': [
                        '✓ Ensure questions are numbered (1., Q1:, Question 1:, etc.)',
                        '✓ Each question must have options marked as A), B), C), D)',
                        '✓ Answer key should be on the last page or specified page',
                        '✓ Answer key format: "1. A", "Q1: B", "Answer 1: C", "1) D", or "1 A"',
                        '✓ Try uploading a different PDF to test the parser'
                    ]
                }

                return jsonify(error_response), 400

            questions = result.get('questions', [])
            summary = result.get('summary', {})

            if not questions:
                return jsonify({
                    'error': 'No questions could be extracted from the PDF',
                    'suggestions': [
                        '✓ Check if questions are properly numbered',
                        '✓ Verify options are marked as A), B), C), D)',
                        '✓ Ensure answer key is on the last page'
                    ]
                }), 400

            # Store questions globally for download
            current_questions = questions

            # Format response
            response = {
                'questions': questions,
                'summary': {
                    'total_questions': summary.get('total_questions', 0),
                    'total_pages': summary.get('total_pages', 0),
                    'answer_page': summary.get('answer_page', 0),
                    'questions_with_answers': summary.get('questions_with_answers', 0),
                    'questions_without_answers': summary.get('questions_without_answers', 0)
                },
                'message': f'✅ Successfully extracted {len(questions)} questions from the PDF',
                'debug_info': result.get('debug_info', {})
            }

            return jsonify(response), 200

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        print(f"Error parsing MCQ PDF: {e}")
        import traceback
        return jsonify({
            'error': f'Error parsing MCQ PDF: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


@app.route('/debug-pdf', methods=['POST'])
@csrf.exempt
@login_required
def debug_pdf():
    """Debug endpoint to analyze PDF content and identify issues"""
    try:
        if 'pdfFile' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['pdfFile']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(temp_path)

        try:
            # Debug the PDF
            print(f"🔍 Debugging PDF: {file.filename}")
            analysis = debug_pdf_content(temp_path)

            return jsonify({
                'success': True,
                'analysis': analysis,
                'message': 'PDF analysis complete. Check console output for detailed information.'
            }), 200

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        print(f"Error debugging PDF: {e}")
        import traceback
        return jsonify({
            'error': f'Error debugging PDF: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500


# For Vercel deployment - this must be at module level
application = app

if __name__ == '__main__':
    app.run(debug=True, port=5002)
