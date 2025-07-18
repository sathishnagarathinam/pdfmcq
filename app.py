import streamlit as st
import os
from mcq_generator import extract_text_from_pdf, generate_mcq_questions
import pandas as pd
from fpdf import FPDF
from io import BytesIO

st.title('PDF MCQ Generator-sathish')

# File uploader
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

# Input fields
col1, col2, col3 = st.columns(3)
with col1:
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=100, value=5)
with col2:
    difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], index=1)
with col3:
    model_provider = st.selectbox("AI Model Provider", ["openrouter", "openai", "deepseek"])
    model_type = st.selectbox("Model Type", ["basic", "advanced"])

# Book and Chapter Information
col1, col2 = st.columns(2)
with col1:
    book_name = st.text_input("Book Name (optional)", placeholder="e.g., Introduction to Computer Science")
with col2:
    chapter_name = st.text_input("Chapter Name (optional)", placeholder="e.g., Chapter 5: Data Structures")

if uploaded_file is not None:
    if st.button('Generate MCQs'):
        with st.spinner('Processing PDF...'):
            # Save temporarily
            temp_path = os.path.join('uploads', uploaded_file.name)
            os.makedirs('uploads', exist_ok=True)
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getvalue())
            
            # Extract text and generate questions
            extracted_text = extract_text_from_pdf(temp_path)
            questions = generate_mcq_questions(
                extracted_text,
                num_questions=num_questions,
                model_provider=model_provider,
                model_type=model_type,
                book_name=book_name.strip(),
                chapter_name=chapter_name.strip()
            )
            
            # Clean up
            os.remove(temp_path)
            
            if isinstance(questions, str) and 'Error' in questions:
                st.error(questions)
            else:
                # Display questions
                st.subheader('Generated Questions')
                for i, q in enumerate(questions, 1):
                    st.write(f"**Question {i}:** {q['question']}")
                    st.write(f"A) {q['options']['A']}")
                    st.write(f"B) {q['options']['B']}")
                    st.write(f"C) {q['options']['C']}")
                    st.write(f"D) {q['options']['D']}")
                    with st.expander("Show Answer and Explanation"):
                        st.write(f"**Correct Answer:** {q['correct']}")
                        st.write(f"**Difficulty:** {q['difficulty']}")
                        st.write(f"**Explanation:** {q['explanation']}")
                    st.write("---")
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                # CSV Download
                with col1:
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
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        "Download CSV",
                        csv,
                        "mcq_questions.csv",
                        "text/csv",
                        key='download-csv'
                    )
                
                # PDF Download
                with col2:
                    pdf = FPDF()
                    class PDF(FPDF):
                        def __init__(self):
                            super().__init__()
                            # Update this path if you place the font in a custom location
                            self.add_font('DejaVuSansCondensed', '', '/Volumes/sathish/pdfmcq/fonts/DejaVuSansCondensed.ttf', uni=True)
                            self.set_font('DejaVuSansCondensed', '', 12)
                    pdf.add_font('DejaVu', 'B', '/usr/share/fonts/TTF/DejaVuSansCondensed-Bold.ttf', uni=True)
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.add_page()
                    pdf.set_font("DejaVu", size=12)
                    
                    # Add title
                    pdf.set_font("DejaVu", 'B', 16)
                    pdf.cell(190, 10, "PDF MCQ Generator-sathish", ln=True, align='C')
                    pdf.ln(5)
                    pdf.set_font("DejaVu", 'B', 14)
                    pdf.cell(190, 10, "Multiple Choice Questions", ln=True, align='C')
                    pdf.ln(10)
                    
                    # Add questions
                    for i, q in enumerate(questions, 1):
                        pdf.set_font("DejaVu", 'B', 12)
                        pdf.multi_cell(190, 10, f"{i}. {q['question']}", ln=True)
                        pdf.set_font("DejaVu", size=12)
                        pdf.multi_cell(190, 10, f"A) {q['options']['A']}", ln=True)
                        pdf.multi_cell(190, 10, f"B) {q['options']['B']}", ln=True)
                        pdf.multi_cell(190, 10, f"C) {q['options']['C']}", ln=True)
                        pdf.multi_cell(190, 10, f"D) {q['options']['D']}", ln=True)
                        pdf.set_font("DejaVu", 'B', 12)
                        pdf.multi_cell(190, 10, f"Correct Answer: {q['correct']}", ln=True)
                        pdf.multi_cell(190, 10, f"Difficulty: {q['difficulty'].capitalize()}", ln=True)
                        pdf.set_font("DejaVu", size=12)
                        pdf.multi_cell(190, 10, f"Explanation: {q['explanation']}", ln=True)
                        pdf.ln(10)
                    
                    pdf_output = BytesIO()
                    pdf.output(pdf_output)
                    st.download_button(
                        "Download PDF",
                        pdf_output.getvalue(),
                        "mcq_questions.pdf",
                        "application/pdf",
                        key='download-pdf'
                    )