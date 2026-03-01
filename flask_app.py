from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, Response
import os
import json
import sys
import queue
import threading

from mcq_generator import (
    extract_text_from_pdf, generate_mcq_questions, generate_mcq_questions_advanced,
    estimate_max_questions, estimate_max_questions_detailed,
    generate_mcq_questions_with_offline_fallback, get_generation_capabilities,
    generate_mcq_questions_with_metadata, generate_pdf_summary, generate_comprehensive_notes
)

# Global progress queue for SSE (used for real-time progress updates)
progress_queues = {}

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
from PyPDF2 import PdfReader, PdfWriter
import uuid

# Load environment variables from .env file
load_dotenv()

# Version: 2.1.1 - PDF Notes Export & Model Selection (Summarize Feature Fix)
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

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 524288000  # 500MB max file size (increased from 50MB)

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


# Global variables to store current questions and PDF summary
current_questions = None
current_pdf_summary = None

def cleanup_temp_files(file_path):
    """Safely cleanup temporary files"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not cleanup temp file {file_path}: {e}")


# ============================================
# PDF Splitting Functions
# ============================================

def split_pdf_by_pages_per_file(pdf_path, pages_per_file):
    """
    Split PDF into multiple files with specified number of pages per file

    Args:
        pdf_path: Path to the PDF file
        pages_per_file: Number of pages in each split file

    Returns:
        List of tuples (filename, file_path) for split PDFs
    """
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        if pages_per_file <= 0:
            raise ValueError("Pages per file must be greater than 0")

        if pages_per_file >= total_pages:
            raise ValueError(f"Pages per file ({pages_per_file}) must be less than total pages ({total_pages})")

        split_files = []
        temp_dir = tempfile.mkdtemp()

        # Calculate number of output files
        num_files = (total_pages + pages_per_file - 1) // pages_per_file

        for file_num in range(num_files):
            writer = PdfWriter()
            start_page = file_num * pages_per_file
            end_page = min(start_page + pages_per_file, total_pages)

            # Add pages to this file
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            # Generate filename
            original_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename = f"{original_name}_part_{file_num + 1}_pages_{start_page + 1}-{end_page}.pdf"
            output_path = os.path.join(temp_dir, output_filename)

            # Write the split PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            split_files.append((output_filename, output_path))

        return split_files, temp_dir

    except Exception as e:
        raise Exception(f"Error splitting PDF by pages: {str(e)}")


def split_pdf_by_page_ranges(pdf_path, page_ranges):
    """
    Split PDF into multiple files based on specified page ranges

    Args:
        pdf_path: Path to the PDF file
        page_ranges: List of tuples [(start, end), ...] (1-indexed, inclusive)

    Returns:
        List of tuples (filename, file_path) for split PDFs
    """
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        split_files = []
        temp_dir = tempfile.mkdtemp()

        for range_num, (start, end) in enumerate(page_ranges):
            # Convert to 0-indexed
            start_idx = start - 1
            end_idx = end

            # Validate range
            if start_idx < 0 or end_idx > total_pages or start_idx >= end_idx:
                raise ValueError(f"Invalid page range: {start}-{end}. Total pages: {total_pages}")

            writer = PdfWriter()

            # Add pages to this file
            for page_num in range(start_idx, end_idx):
                writer.add_page(reader.pages[page_num])

            # Generate filename
            original_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename = f"{original_name}_range_{range_num + 1}_pages_{start}-{end}.pdf"
            output_path = os.path.join(temp_dir, output_filename)

            # Write the split PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            split_files.append((output_filename, output_path))

        return split_files, temp_dir

    except Exception as e:
        raise Exception(f"Error splitting PDF by ranges: {str(e)}")


def split_pdf_into_individual_pages(pdf_path):
    """
    Split PDF into individual page files

    Args:
        pdf_path: Path to the PDF file

    Returns:
        List of tuples (filename, file_path) for split PDFs
    """
    try:
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)

        split_files = []
        temp_dir = tempfile.mkdtemp()

        for page_num in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_num])

            # Generate filename
            original_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_filename = f"{original_name}_page_{page_num + 1}.pdf"
            output_path = os.path.join(temp_dir, output_filename)

            # Write the split PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            split_files.append((output_filename, output_path))

        return split_files, temp_dir

    except Exception as e:
        raise Exception(f"Error splitting PDF into individual pages: {str(e)}")

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
        pdf_summary = result.get('pdf_summary', 'Summary not available')

        # Store questions globally for download
        current_questions = questions
        # Store PDF summary globally for CSV download
        current_pdf_summary = pdf_summary

        return jsonify({
            'questions': questions,
            'summary': summary,
            'pdf_summary': pdf_summary,
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
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Handle both old format (direct questions array) and new format (with pdf_summary)
        if isinstance(data, list):
            questions = data
            pdf_summary = None
        else:
            questions = data.get('questions', [])
            pdf_summary = data.get('pdf_summary', None)

        if not questions:
            return jsonify({'error': 'No questions data provided'}), 400

        # Create DataFrame with l2 column (topic/summary)
        # Topic is limited to 200 characters and only filled in the FIRST row
        rows = []
        for idx, q in enumerate(questions):
            row = {
                'question': q.get('text') if q.get('text') else (q.get('question') if q.get('question') else ''),  # Support both 'text' and 'question' keys
                'option1': q['options'].get('A', ''),
                'option2': q['options'].get('B', ''),
                'option3': q['options'].get('C', ''),
                'option4': q['options'].get('D', ''),
                'correct': {'A':'1', 'B':'2', 'C':'3', 'D':'4'}.get(q.get('correct', ''), ''),
                'difficulty': q.get('difficulty', 'medium').capitalize(),
                'explanation': q.get('explanation', ''),
                'l2': ''  # Initialize l2 column as empty for all rows
            }
            # Add topic (PDF summary) to l2 column ONLY for the first row, limited to 200 characters
            if pdf_summary and idx == 0:
                row['l2'] = pdf_summary[:200] if len(pdf_summary) > 200 else pdf_summary
            rows.append(row)

        df = pd.DataFrame(rows)

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

@app.route('/upload-stream', methods=['POST'])
@csrf.exempt
@login_required
def upload_stream():
    """
    Streaming upload endpoint that returns real-time progress updates via Server-Sent Events.
    This endpoint provides detailed progress messages during question generation.
    """
    # Generate unique session ID for this upload
    session_id = str(uuid.uuid4())

    # Create a progress queue for this session
    progress_queue = queue.Queue()
    progress_queues[session_id] = progress_queue

    # IMPORTANT: Extract ALL request data BEFORE the generator function
    # This is because the request context is not available inside the generator
    file = request.files.get('pdfFile')
    if not file or file.filename == '':
        return Response(
            f"data: {json.dumps({'status': 'error', 'message': 'No PDF file provided'})}\n\n",
            mimetype='text/event-stream'
        )

    # Parse form parameters (must be done before generator)
    question_count = int(request.form.get('questionCount', 5))
    difficulty = request.form.get('difficulty', 'medium')
    model_provider = request.form.get('modelProvider', 'openrouter')
    model_name = request.form.get('modelName', 'deepseek/deepseek-chat')
    custom_api_key = request.form.get('customApiKey', '')
    custom_base_url = request.form.get('customBaseUrl', '')
    use_max_questions = request.form.get('useMaxQuestions', 'false').lower() == 'true'
    book_name = request.form.get('bookName', '')
    chapter_name = request.form.get('chapterName', '')
    prefer_offline = request.form.get('preferOffline', 'false').lower() == 'true'
    use_offline_estimation = request.form.get('useOfflineEstimation', 'false').lower() == 'true'
    use_amendment = request.form.get('useAmendment', 'false').lower() == 'true'

    # Handle amendment PDF if provided (must be done before generator)
    amendment_text = None
    amendment_temp_path = None
    if use_amendment and 'amendmentPdfFile' in request.files:
        amendment_file = request.files['amendmentPdfFile']
        if amendment_file and amendment_file.filename != '':
            amendment_temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"amendment_{amendment_file.filename}")
            amendment_file.save(amendment_temp_path)
            amendment_text = extract_text_from_pdf(amendment_temp_path)

    # Save main PDF (must be done before generator)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(temp_path)

    def send_progress(message, status='progress', data=None):
        """Send progress update to the queue."""
        event_data = {'message': message, 'status': status}
        if data:
            event_data.update(data)
        progress_queue.put(json.dumps(event_data))

    def generate():
        """Generator function for SSE stream."""
        try:
            yield f"data: {json.dumps({'status': 'progress', 'message': '� File received, starting processing...'})}\n\n"

            if amendment_text:
                yield f"data: {json.dumps({'status': 'progress', 'message': '📝 Amendment PDF processed'})}\n\n"

            # Extract text
            yield f"data: {json.dumps({'status': 'progress', 'message': '📄 Extracting text from PDF with page tracking...'})}\n\n"
            extracted_text = extract_text_from_pdf(temp_path)

            # Check for extraction errors
            is_error = (isinstance(extracted_text, str) and
                       (extracted_text.startswith('Error') or extracted_text.startswith('PDF') or
                        extracted_text.startswith('Failed') or extracted_text.startswith('No text')))

            if is_error:
                cleanup_temp_files(temp_path)
                cleanup_temp_files(amendment_temp_path)
                yield f"data: {json.dumps({'status': 'error', 'message': extracted_text})}\n\n"
                return

            yield f"data: {json.dumps({'status': 'progress', 'message': f'📊 Extracted {len(extracted_text)} characters from PDF'})}\n\n"

            # Estimate questions
            if use_offline_estimation:
                yield f"data: {json.dumps({'status': 'progress', 'message': '🔢 Estimating optimal question count...'})}\n\n"
                estimation_result = estimate_max_questions_detailed(extracted_text)
                max_questions = estimation_result["max_questions"]
            else:
                max_questions = estimate_max_questions(extracted_text, use_offline=False)

            questions_to_generate = max_questions if use_max_questions else question_count

            yield f"data: {json.dumps({'status': 'progress', 'message': f'🎯 Will generate {questions_to_generate} questions ({difficulty} difficulty)'})}\n\n"

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

            yield f"data: {json.dumps({'status': 'progress', 'message': f'🤖 Using model: {model_name}'})}\n\n"
            yield f"data: {json.dumps({'status': 'progress', 'message': '⚙️ Generating MCQ questions with AI...'})}\n\n"

            # Generate questions
            result = generate_mcq_questions_with_metadata(
                pdf_path=temp_path,
                num_questions=questions_to_generate,
                difficulty=difficulty,
                book_name=book_name,
                chapter_name=chapter_name,
                prefer_offline=prefer_offline,
                model_config=model_config
            )

            # Cleanup temp files
            cleanup_temp_files(temp_path)
            cleanup_temp_files(amendment_temp_path)

            # Check for errors
            if 'error' in result:
                yield f"data: {json.dumps({'status': 'error', 'message': result['error']})}\n\n"
                return

            questions = result['questions']
            summary = result['summary']
            pdf_summary = result.get('pdf_summary', 'Summary not available')

            yield f"data: {json.dumps({'status': 'progress', 'message': f'✅ Generated {len(questions)} questions successfully!'})}\n\n"
            yield f"data: {json.dumps({'status': 'progress', 'message': '📋 Adding page and section metadata...'})}\n\n"

            # Send final result
            final_result = {
                'status': 'complete',
                'message': f'Successfully generated {len(questions)} MCQ questions',
                'questions': questions,
                'summary': summary,
                'pdf_summary': pdf_summary,
                'text_length': len(extracted_text),
                'max_questions_estimate': max_questions,
                'questions_generated': len(questions),
                'total_pages': result.get('total_pages', 0),
                'sections_detected': len(result.get('sections', []))
            }
            yield f"data: {json.dumps(final_result)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
        finally:
            # Cleanup progress queue
            if session_id in progress_queues:
                del progress_queues[session_id]

    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no'
    })

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
                # Question - use multi_cell for proper text wrapping
                pdf.set_font("Arial", 'B', 12)
                # Support both 'text' and 'question' keys - check if text exists and is not empty
                question_content = q.get('text', '')
                if not question_content:
                    question_content = q.get('question', '')
                if not question_content:
                    question_content = 'No question text'
                # Encode to latin-1 to handle special characters
                question_text = f"{i}. {question_content}".encode('latin-1', errors='replace').decode('latin-1')

                # Use multi_cell for automatic text wrapping (supports long questions)
                pdf.multi_cell(0, 8, question_text)
                pdf.ln(2)

                # Options - use multi_cell for complete sentences without truncation
                pdf.set_font("Arial", '', 11)
                options = q.get('options', {})

                for opt_key in ['A', 'B', 'C', 'D']:
                    opt_text = options.get(opt_key, f'No option {opt_key}')
                    # Encode to latin-1 to handle special characters
                    opt_text = opt_text.encode('latin-1', errors='replace').decode('latin-1')
                    # Use multi_cell to properly wrap long option text
                    pdf.multi_cell(0, 6, f"{opt_key}) {opt_text}")

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

                # Explanation - use multi_cell for proper text wrapping
                pdf.set_font("Arial", '', 10)
                explanation = q.get('explanation', 'No explanation provided')
                # Encode to latin-1 to handle special characters
                explanation = f"Explanation: {explanation}".encode('latin-1', errors='replace').decode('latin-1')
                # Use multi_cell for automatic text wrapping
                pdf.multi_cell(0, 6, explanation)

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


class ProfessionalNotesPDF(FPDF):
    """Custom PDF class for professional notes with headers and footers"""

    def __init__(self, title="Study Material", website="www.example.com"):
        super().__init__()
        self.doc_title = title
        self.website = website
        self.header_title = "Study Material"

    def header(self):
        """Add header to each page (except cover page)"""
        if self.page_no() > 1:
            # Blue line at top
            self.set_draw_color(0, 102, 204)
            self.set_line_width(0.5)
            self.line(10, 15, 200, 15)

            # Left header - Study Material
            self.set_font('Arial', 'BI', 10)
            self.set_text_color(0, 102, 204)
            self.set_xy(10, 8)
            self.cell(95, 6, self.header_title, 0, 0, 'L')

            # Right header - Document title
            self.set_font('Arial', 'BI', 10)
            self.set_text_color(0, 102, 204)
            self.set_xy(105, 8)
            self.cell(95, 6, self.doc_title, 0, 0, 'R')

            self.ln(15)

    def footer(self):
        """Add footer to each page (except cover page)"""
        if self.page_no() > 1:
            self.set_y(-20)

            # Red line
            self.set_draw_color(204, 51, 51)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())

            # Page number (center)
            self.set_font('Arial', 'B', 10)
            self.set_text_color(0, 0, 0)
            self.set_y(-15)
            self.cell(0, 10, str(self.page_no()), 0, 0, 'C')

            # Website (right)
            self.set_font('Arial', 'B', 9)
            self.set_text_color(0, 102, 204)
            self.set_xy(150, -15)
            self.cell(50, 10, self.website, 0, 0, 'R')


def create_professional_notes_pdf(notes, filename, title=None, website="www.example.com"):
    """
    Create a professional PDF with cover page and formatted content.
    Style inspired by professional government exam study materials.

    Features:
    - Professional cover page with disclaimer
    - Rule-wise formatting with proper indentation
    - Table rendering with borders
    - Flowchart display
    - Exam-oriented section highlighting
    - Proper text alignment and spacing
    """
    import re

    clean_filename = filename.replace('.pdf', '') if filename else 'Study Notes'
    doc_title = title if title else clean_filename

    # Create PDF
    pdf = ProfessionalNotesPDF(title=doc_title, website=website)
    pdf.set_auto_page_break(auto=True, margin=25)

    # ============================================
    # COVER PAGE
    # ============================================
    pdf.add_page()

    # Title area - centered
    pdf.ln(35)

    # Main title
    pdf.set_font('Arial', 'B', 26)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, "STUDY NOTES", 0, 1, 'C')

    # Subtitle
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Self Learning Material", 0, 1, 'C')

    # Decorative line
    pdf.ln(5)
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(1.5)
    pdf.line(40, pdf.get_y(), 170, pdf.get_y())

    # Document Title Box
    pdf.ln(20)
    pdf.set_fill_color(240, 248, 255)  # Light blue background
    pdf.set_draw_color(0, 102, 204)
    pdf.rect(20, pdf.get_y(), 170, 35, 'DF')

    pdf.set_xy(25, pdf.get_y() + 8)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 51, 102)
    # Clean title of special characters
    clean_title = doc_title.encode('latin-1', errors='replace').decode('latin-1')
    pdf.multi_cell(160, 10, clean_title, 0, 'C')

    # Website
    pdf.ln(25)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 8, website, 0, 1, 'C')

    # Target Audience Section
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, "Prepared For:", 0, 1, 'C')

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 6, "DDO | Accounts Officers | Audit Officers | Exam Aspirants", 0, 1, 'C')

    # Disclaimer box at bottom
    pdf.set_y(-75)
    pdf.set_draw_color(180, 0, 0)
    pdf.set_fill_color(255, 250, 250)
    pdf.rect(15, pdf.get_y(), 180, 45, 'DF')

    pdf.set_xy(18, pdf.get_y() + 5)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(180, 0, 0)
    pdf.cell(0, 6, "DISCLAIMER", 0, 1)

    pdf.set_x(18)
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(60, 60, 60)
    disclaimer_text = (
        "These notes have been prepared for educational purposes only. While every effort "
        "has been made to ensure accuracy, this document is intended as a study aid. "
        "Readers are advised to refer to official government gazettes and circulars for "
        "authoritative information. The creator is not responsible for any errors or "
        "omissions. Always verify with original sources before official use."
    )
    pdf.multi_cell(172, 5, disclaimer_text, 0, 'J')

    # ============================================
    # CONTENT PAGES
    # ============================================
    pdf.add_page()

    # Set proper margins for content area
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.set_x(15)

    # Process the notes text
    lines = notes.split('\n')

    # State tracking for tables
    in_table = False
    table_rows = []
    table_col_widths = []

    i = 0
    while i < len(lines):
        line = lines[i]
        # Clean the line of problematic characters
        clean_line = line.encode('latin-1', errors='replace').decode('latin-1')
        # Replace common problematic characters
        clean_line = clean_line.replace('?', '-').replace('', '-').replace('', "'")
        stripped = clean_line.strip()

        # Always reset X position to left margin before each line
        pdf.set_x(pdf.l_margin)

        # ============================================
        # TABLE DETECTION AND RENDERING
        # ============================================
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []

            # Parse table row
            cells = [c.strip() for c in stripped.split('|')[1:-1]]

            # Skip separator rows (|---|---|---|)
            if cells and all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue

            table_rows.append(cells)
            i += 1
            continue

        elif in_table:
            # End of table - render it
            in_table = False
            if table_rows:
                pdf.ln(3)
                render_table(pdf, table_rows)
                pdf.ln(5)
            table_rows = []

        # ============================================
        # RULE HEADINGS (RULE 1, Rule 2, etc.)
        # ============================================
        rule_match = re.match(r'^(RULE\s*\d+|Rule\s*\d+)\s*[-:.]?\s*(.*)$', stripped, re.IGNORECASE)
        if rule_match:
            pdf.ln(8)
            # Draw a subtle top border for the rule
            pdf.set_draw_color(0, 102, 204)
            pdf.set_line_width(0.5)
            pdf.line(15, pdf.get_y(), 195, pdf.get_y())
            pdf.ln(3)

            pdf.set_font('Arial', 'B', 13)
            pdf.set_text_color(0, 51, 102)
            rule_title = f"{rule_match.group(1).upper()} - {rule_match.group(2)}" if rule_match.group(2) else rule_match.group(1).upper()
            pdf.multi_cell(0, 8, rule_title)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            i += 1
            continue

        # ============================================
        # CHAPTER/PART HEADINGS
        # ============================================
        if stripped.upper().startswith('CHAPTER') or stripped.upper().startswith('PART'):
            pdf.add_page()  # Start new page for chapters
            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(0, 51, 102)
            pdf.set_fill_color(230, 240, 250)
            pdf.cell(0, 12, stripped.upper(), 0, 1, 'C', True)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
            i += 1
            continue

        # ============================================
        # EXAM HIGHLIGHTS / IMPORTANT SECTIONS
        # ============================================
        if any(keyword in stripped.upper() for keyword in ['EXAM HIGHLIGHT', 'IMPORTANT', 'KEY POINT', 'EXAM FOCUS', 'MCQ FOCUS', 'QUICK REVISION']):
            pdf.ln(5)
            pdf.set_fill_color(255, 255, 220)  # Light yellow
            pdf.set_draw_color(200, 150, 0)
            pdf.rect(15, pdf.get_y(), 180, 10, 'DF')
            pdf.set_xy(18, pdf.get_y() + 2)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(150, 100, 0)
            header_text = stripped.strip('*#:').strip()
            pdf.cell(174, 6, header_text.upper(), 0, 1, 'L')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            i += 1
            continue

        # ============================================
        # FLOWCHART DETECTION (arrows)
        # ============================================
        if '->' in stripped or '-->' in stripped:
            pdf.ln(3)
            pdf.set_fill_color(245, 250, 255)
            pdf.set_draw_color(100, 150, 200)

            # Clean flowchart text
            flow_text = stripped.replace('-->', ' --> ').replace('->', ' -> ')
            flow_text = re.sub(r'\s+', ' ', flow_text).strip()

            # Calculate height needed
            text_width = pdf.get_string_width(flow_text)
            lines_needed = max(1, int(text_width / 160) + 1)
            box_height = lines_needed * 7 + 6

            pdf.rect(15, pdf.get_y(), 180, box_height, 'DF')
            pdf.set_xy(18, pdf.get_y() + 3)
            pdf.set_font('Arial', 'I', 10)
            pdf.set_text_color(50, 80, 120)
            pdf.multi_cell(174, 7, flow_text, 0, 'C')
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            i += 1
            continue

        # ============================================
        # SECTION HEADINGS
        # ============================================
        if stripped.lower().startswith('section') or (stripped.startswith('**') and 'section' in stripped.lower()):
            pdf.ln(5)
            section_text = stripped.strip('*').strip()
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(0, 102, 204)
            pdf.multi_cell(0, 7, section_text)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            i += 1
            continue

        # ============================================
        # MARKDOWN HEADERS (# and ##)
        # ============================================
        if stripped.startswith('###'):
            pdf.ln(4)
            header_text = stripped.lstrip('#').strip()
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(0, 80, 150)
            pdf.multi_cell(0, 7, header_text)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith('##'):
            pdf.ln(5)
            header_text = stripped.lstrip('#').strip()
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(0, 102, 204)
            pdf.multi_cell(0, 8, header_text)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith('#'):
            pdf.ln(6)
            header_text = stripped.lstrip('#').strip()
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(0, 51, 102)
            pdf.multi_cell(0, 8, header_text)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(3)
            i += 1
            continue

        # ============================================
        # BOLD TEXT MARKERS (**text**)
        # ============================================
        if stripped.startswith('**') and stripped.endswith('**'):
            bold_text = stripped.strip('*').strip()
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, bold_text)
            i += 1
            continue

        # ============================================
        # BULLET POINTS
        # ============================================
        if stripped.startswith('- ') or stripped.startswith('* '):
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(0, 0, 0)
            bullet_text = stripped[2:]
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(0, 6, chr(149) + " " + bullet_text)  # Use bullet character
            i += 1
            continue

        # Unicode bullet points - convert to ASCII
        if len(stripped) > 2 and stripped[0] in ['\u2022', '\u2023', '\u25cf', '\u25cb', '\u2713', '\u2714']:
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(0, 0, 0)
            bullet_text = stripped[2:] if stripped[1] == ' ' else stripped[1:]
            pdf.set_x(pdf.l_margin + 5)
            pdf.multi_cell(0, 6, chr(149) + " " + bullet_text)
            i += 1
            continue

        # ============================================
        # NUMBERED LISTS
        # ============================================
        if len(stripped) > 2 and stripped[0].isdigit():
            if stripped[1] == '.' or (len(stripped) > 2 and stripped[1].isdigit() and stripped[2] == '.'):
                pdf.set_font('Arial', '', 11)
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(pdf.l_margin + 3)
                pdf.multi_cell(0, 6, stripped)
                i += 1
                continue

        # ============================================
        # EMPTY LINE
        # ============================================
        if stripped == '':
            pdf.ln(3)
            i += 1
            continue

        # ============================================
        # SEPARATOR LINES (===, ---, etc.)
        # ============================================
        if re.match(r'^[=\-_]{3,}$', stripped):
            pdf.ln(2)
            pdf.set_draw_color(150, 150, 150)
            pdf.set_line_width(0.3)
            pdf.line(30, pdf.get_y(), 180, pdf.get_y())
            pdf.ln(3)
            i += 1
            continue

        # ============================================
        # REGULAR TEXT
        # ============================================
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, clean_line)
        i += 1

    # Handle any remaining table
    if in_table and table_rows:
        render_table(pdf, table_rows)

    return pdf


def render_table(pdf, rows):
    """
    Render a table with proper borders and alignment.
    """
    if not rows:
        return

    # Calculate column widths based on content
    num_cols = max(len(row) for row in rows)
    if num_cols == 0:
        return

    # Available width (page width minus margins)
    available_width = 180
    col_width = available_width / num_cols

    # Limit column width to reasonable size
    col_width = min(col_width, 60)

    # Start position
    start_x = pdf.l_margin

    for row_idx, row in enumerate(rows):
        # Determine if this is a header row (first row)
        is_header = (row_idx == 0)

        # Calculate row height based on content
        max_lines = 1
        for cell in row:
            cell_text = str(cell).encode('latin-1', errors='replace').decode('latin-1')
            text_width = pdf.get_string_width(cell_text)
            lines_needed = max(1, int(text_width / (col_width - 4)) + 1)
            max_lines = max(max_lines, lines_needed)

        row_height = max_lines * 6 + 2

        # Check if we need a new page
        if pdf.get_y() + row_height > 270:
            pdf.add_page()

        # Set style for header vs data rows
        if is_header:
            pdf.set_fill_color(230, 240, 250)  # Light blue for header
            pdf.set_font('Arial', 'B', 10)
        else:
            pdf.set_fill_color(255, 255, 255)  # White for data
            pdf.set_font('Arial', '', 10)

        pdf.set_draw_color(100, 100, 100)
        pdf.set_text_color(0, 0, 0)

        y_before = pdf.get_y()

        # Draw cells
        for col_idx, cell in enumerate(row):
            x_pos = start_x + (col_idx * col_width)
            cell_text = str(cell).encode('latin-1', errors='replace').decode('latin-1')

            # Draw cell border and fill
            pdf.rect(x_pos, y_before, col_width, row_height, 'DF' if is_header else 'D')

            # Add cell text
            pdf.set_xy(x_pos + 2, y_before + 1)
            pdf.multi_cell(col_width - 4, 5, cell_text, 0, 'L')

        # Handle cells that are fewer than num_cols
        for col_idx in range(len(row), num_cols):
            x_pos = start_x + (col_idx * col_width)
            pdf.rect(x_pos, y_before, col_width, row_height, 'D')

        pdf.set_y(y_before + row_height)


@app.route('/download-notes-pdf', methods=['POST'])
@csrf.exempt
@login_required
def download_notes_pdf():
    """Generate a professional PDF from the comprehensive notes"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        notes = data.get('notes', '')
        filename = data.get('filename', 'notes')
        title = data.get('title', None)  # Optional custom title
        website = data.get('website', 'PDF MCQ Generator')

        if not notes or notes.strip() == '':
            return jsonify({'error': 'No notes content provided'}), 400

        print(f"Generating professional PDF for notes: {len(notes)} characters")

        clean_filename = filename.replace('.pdf', '') if filename else 'notes'

        try:
            # Create professional PDF
            pdf = create_professional_notes_pdf(
                notes=notes,
                filename=filename,
                title=title,
                website=website
            )

            # Output PDF to buffer
            pdf_buffer = BytesIO()
            pdf_output = pdf.output(dest='S')

            if not pdf_output:
                print("Error: PDF generation returned empty content")
                return jsonify({'error': 'PDF generation failed - empty content'}), 500

            if isinstance(pdf_output, str):
                pdf_buffer.write(pdf_output.encode('latin-1'))
            else:
                pdf_buffer.write(pdf_output)

            pdf_buffer.seek(0)

            # Verify PDF content
            pdf_content = pdf_buffer.getvalue()
            if len(pdf_content) == 0:
                print("Error: PDF buffer is empty")
                return jsonify({'error': 'PDF generation failed - 0 bytes generated'}), 500

            print(f"Professional Notes PDF generated successfully: {len(pdf_content)} bytes")

            download_filename = clean_filename + '_notes.pdf'

            response = send_file(
                pdf_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=download_filename
            )

            # Add headers to prevent caching issues
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'

            return response

        except Exception as pdf_error:
            print(f"Error generating professional PDF: {pdf_error}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'PDF generation failed: {str(pdf_error)}'}), 500

    except Exception as e:
        print(f"Error in download_notes_pdf: {e}")
        import traceback
        traceback.print_exc()
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


@app.route('/split-pdf', methods=['POST'])
@csrf.exempt
@login_required
def split_pdf():
    """Split PDF file based on user-specified parameters"""
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get split parameters
    split_mode = request.form.get('splitMode', 'pages_per_file')
    pages_per_file = request.form.get('pagesPerFile', '')
    page_ranges = request.form.get('pageRanges', '')

    # Save file temporarily
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(temp_path)

    try:
        # Get total pages first
        reader = PdfReader(temp_path)
        total_pages = len(reader.pages)

        split_files = []
        temp_dir = None

        if split_mode == 'pages_per_file':
            # Split by pages per file
            if not pages_per_file or not pages_per_file.isdigit():
                return jsonify({'error': 'Please specify a valid number of pages per file'}), 400

            pages_per_file = int(pages_per_file)
            split_files, temp_dir = split_pdf_by_pages_per_file(temp_path, pages_per_file)

        elif split_mode == 'page_ranges':
            # Split by page ranges
            if not page_ranges:
                return jsonify({'error': 'Please specify page ranges'}), 400

            # Parse page ranges (format: "1-5, 6-10, 11-15")
            ranges = []
            try:
                for range_str in page_ranges.split(','):
                    range_str = range_str.strip()
                    if '-' in range_str:
                        start, end = range_str.split('-')
                        ranges.append((int(start.strip()), int(end.strip())))
                    else:
                        return jsonify({'error': f'Invalid range format: {range_str}. Use format: 1-5, 6-10'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid page range format. Use numbers only.'}), 400

            split_files, temp_dir = split_pdf_by_page_ranges(temp_path, ranges)

        elif split_mode == 'individual_pages':
            # Split into individual pages
            split_files, temp_dir = split_pdf_into_individual_pages(temp_path)

        else:
            return jsonify({'error': 'Invalid split mode'}), 400

        # Create a session ID for this split operation
        session_id = str(uuid.uuid4())

        # Store split files info in session
        if 'split_sessions' not in app.config:
            app.config['split_sessions'] = {}

        app.config['split_sessions'][session_id] = {
            'files': split_files,
            'temp_dir': temp_dir,
            'created_at': pd.Timestamp.now()
        }

        # Prepare response with file information
        files_info = []
        for filename, filepath in split_files:
            file_size = os.path.getsize(filepath)
            files_info.append({
                'filename': filename,
                'size': f"{file_size / 1024:.2f} KB",
                'download_id': f"{session_id}_{filename}"
            })

        return jsonify({
            'success': True,
            'message': f'✅ Successfully split PDF into {len(split_files)} file(s)',
            'session_id': session_id,
            'total_pages': total_pages,
            'split_count': len(split_files),
            'files': files_info
        }), 200

    except Exception as e:
        print(f"Error splitting PDF: {e}")
        import traceback
        return jsonify({
            'error': f'Error splitting PDF: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

    finally:
        # Clean up original uploaded file
        if os.path.exists(temp_path):
            cleanup_temp_files(temp_path)


@app.route('/download-split-pdf/<session_id>/<path:filename>', methods=['GET'])
@login_required
def download_split_pdf(session_id, filename):
    """Download a split PDF file"""
    try:
        from urllib.parse import unquote

        # Decode the filename from URL encoding
        filename = unquote(filename)

        if 'split_sessions' not in app.config or session_id not in app.config['split_sessions']:
            return jsonify({'error': 'Session not found or expired'}), 404

        session_data = app.config['split_sessions'][session_id]
        split_files = session_data['files']

        # Find the requested file
        file_path = None
        for fname, fpath in split_files:
            if fname == filename:
                file_path = fpath
                break

        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404

        # Send the file
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        print(f"Error downloading split PDF: {e}")
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500


@app.route('/summarize-pdf', methods=['POST'])
@csrf.exempt
@login_required
def summarize_pdf():
    """Generate comprehensive academic notes from the uploaded PDF content"""
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['pdfFile']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get model settings
    model_provider = request.form.get('modelProvider', 'openrouter')
    model_type = request.form.get('modelType', 'deepseek/deepseek-chat')

    # Save file temporarily
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(temp_path)

    try:
        # Extract text from PDF
        print(f"📄 Processing PDF for comprehensive notes: {file.filename}")
        extracted_text = extract_text_from_pdf(temp_path)

        if not extracted_text or len(extracted_text.strip()) < 100:
            return jsonify({'error': 'Could not extract sufficient text from PDF'}), 400

        # Get total pages
        from PyPDF2 import PdfReader
        reader = PdfReader(temp_path)
        total_pages = len(reader.pages)

        print(f"📊 Extracted {len(extracted_text)} characters from {total_pages} pages")
        print(f"🤖 Generating comprehensive notes with model: {model_type}")

        # Generate comprehensive academic notes using the AI model
        notes = generate_comprehensive_notes(
            text=extracted_text,
            model_provider=model_provider,
            model_type=model_type
        )

        if not notes or "failed" in notes.lower():
            return jsonify({'error': 'Failed to generate notes'}), 500

        print(f"✅ Notes generated: {len(notes)} characters")

        return jsonify({
            'success': True,
            'summary': notes,  # Keep 'summary' key for frontend compatibility
            'filename': file.filename,
            'total_pages': total_pages,
            'text_length': len(extracted_text),
            'model_used': model_type
        }), 200

    except Exception as e:
        print(f"Error generating notes: {e}")
        import traceback
        return jsonify({
            'error': f'Error generating notes: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            cleanup_temp_files(temp_path)


# For Vercel deployment - this must be at module level
application = app

if __name__ == '__main__':
    app.run(debug=True, port=5002)
