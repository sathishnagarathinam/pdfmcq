from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from mcq_generator import extract_text_from_pdf, generate_mcq_questions, generate_mcq_questions_advanced
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import tempfile

app = Flask(__name__)

# Global variable to store current questions
current_questions = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
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
        difficulty = request.form.get('difficulty', 'medium')
        model_provider = request.form.get('modelProvider', 'openrouter')
        model_name = request.form.get('modelName', 'openrouter/cypher-alpha:free')
        custom_api_key = request.form.get('customApiKey', '')
        custom_base_url = request.form.get('customBaseUrl', '')
        
        # Save file temporarily
        temp_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(temp_path)
        
        # Extract text and generate questions
        extracted_text = extract_text_from_pdf(temp_path)

        # Prepare model configuration
        model_config = {
            'provider': model_provider,
            'model_name': model_name,
            'custom_api_key': custom_api_key,
            'custom_base_url': custom_base_url
        }

        # Debug: Print model configuration
        print(f"Model Config: {model_config}")

        questions = generate_mcq_questions_advanced(
            extracted_text,
            num_questions=question_count,
            difficulty=difficulty,
            model_config=model_config
        )
        
        # Clean up
        os.remove(temp_path)
        
        if isinstance(questions, str) and 'Error' in questions:
            return jsonify({'error': questions}), 500
        
        # Store questions globally for download
        current_questions = questions
        
        return jsonify({'questions': questions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-csv', methods=['POST'])
def download_csv():
    try:
        questions = request.json
        if not questions:
            return jsonify({'error': 'No questions data provided'}), 400
        
        # Create DataFrame
        df = pd.DataFrame([
            {
                'question': q['question'],
                'option1': q['options']['A'],
                'option2': q['options']['B'],
                'option3': q['options']['C'],
                'option4': q['options']['D'],
                'correct': {'A':'1', 'B':'2', 'C':'3', 'D':'4'}[q['correct']],
                'difficulty': q['difficulty'].capitalize(),
                'explanation': q['explanation']
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
def download_pdf():
    try:
        questions = request.json
        if not questions:
            return jsonify({'error': 'No questions data provided'}), 400

        print(f"Generating PDF for {len(questions)} questions")
        
        # Create PDF using older FPDF version compatible methods
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Multiple Choice Questions", 0, 1, 'C')
        pdf.ln(10)

        # Add questions
        for i, q in enumerate(questions, 1):
            try:
                # Question
                pdf.set_font("Arial", 'B', 12)
                question_text = f"{i}. {q.get('question', 'No question text')}"

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
        
        # Create PDF in memory (compatible with older FPDF)
        pdf_buffer = BytesIO()
        pdf_string = pdf.output(dest='S')
        pdf_buffer.write(pdf_string.encode('latin-1'))
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='mcq_questions.pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
