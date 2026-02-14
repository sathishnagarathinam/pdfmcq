import streamlit as st
import os
from mcq_generator import (
    extract_text_from_pdf, generate_mcq_questions, estimate_max_questions,
    estimate_max_questions_detailed, generate_mcq_questions_with_offline_fallback,
    generate_professional_mcq_questions_enhanced, generate_fast_mcq_questions_enhanced,
    get_generation_capabilities
)
import pandas as pd
from fpdf import FPDF
from io import BytesIO

st.title('PDF MCQ Generator-sathish')

# Show generation capabilities
capabilities = get_generation_capabilities()

# Check API key availability
api_keys_available = any([
    os.getenv("OPENAI_API_KEY"),
    os.getenv("OPENROUTER_API_KEY"),
    os.getenv("ANTHROPIC_API_KEY"),
    os.getenv("DEEPSEEK_API_KEY")
])

if capabilities["enhanced_professional_available"]:
    st.success("🎯 Enhanced Professional generation available (Academic Grade)")
    if capabilities["fast_available"]:
        st.info("⚡ Fast mode also available for speed")
    if api_keys_available:
        st.info("🌐 Online generation also available with API keys")
elif capabilities["fast_available"]:
    st.success("⚡ Fast generation available (Optimized Speed)")
    if capabilities["professional_available"]:
        st.info("🎯 Professional mode also available for best quality")
    if api_keys_available:
        st.info("🌐 Online generation also available with API keys")
elif capabilities["professional_available"]:
    st.success("🎯 Professional generation available (Best Quality)")
    st.info("💡 For faster generation, run: `python setup_fast_models.py`")
    if api_keys_available:
        st.info("🌐 Online generation also available with API keys")
elif capabilities["offline_available"]:
    st.success("✅ Offline generation available")
    st.info("💡 For speed: `python setup_fast_models.py`")
    st.info("🎯 For best quality: `python setup_enhanced_professional.py`")
    if api_keys_available:
        st.info("🌐 Online generation also available with API keys")
elif api_keys_available:
    st.success("🌐 Online generation available (Original Method)")
    st.info("⚡ For speed: `python setup_fast_models.py`")
    st.info("💡 For offline: `python setup_offline.py`")
    st.info("🎯 For best quality: `python setup_enhanced_professional.py`")
else:
    st.warning("⚠️ No generation methods configured")
    st.error("Please set up at least one generation method:")
    st.info("🌐 For online: Configure API keys in .env file")
    st.info("⚡ For speed: `python setup_fast_models.py`")
    st.info("💡 For offline: `python setup_offline.py`")
    st.info("🎯 For best quality: `python setup_enhanced_professional.py`")

# File uploader
uploaded_file = st.file_uploader("📄 Upload a PDF document", type="pdf")

# Amendment PDF support
st.markdown("---")
use_amendment = st.checkbox("📝 Generate questions from PDF with amendments", help="Enable this to upload an amendment PDF and generate questions covering changes, differences, and new provisions")

amendment_file = None
if use_amendment:
    amendment_file = st.file_uploader("📋 Upload Amendment PDF (optional)", type="pdf", key="amendment_pdf")
    if amendment_file:
        st.success(f"✅ Amendment PDF loaded: {amendment_file.name}")

st.markdown("---")

# Input fields
col1, col2, col3 = st.columns(3)
with col1:
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=100, value=5)
    use_max_questions = st.checkbox("🚀 Generate Maximum Questions", help="Generate the maximum number of questions possible from the PDF content")
with col2:
    difficulty = st.selectbox("Difficulty Level", ["easy", "medium", "hard"], index=1)

    # Generation mode selection
    generation_modes = []
    if capabilities["fast_available"]:
        generation_modes.append("⚡ Fast (Optimized Speed)")
    if capabilities["professional_available"]:
        generation_modes.append("🎯 Professional (Best Quality)")
    if capabilities["offline_available"]:
        generation_modes.append("🔒 Offline")
    if capabilities["online_available"]:
        generation_modes.append("🌐 Online")

    if generation_modes:
        generation_mode = st.selectbox("Generation Mode", generation_modes, index=0)
    else:
        st.error("No generation methods available!")
        generation_mode = None

with col3:
    model_provider = st.selectbox("AI Model Provider", ["openrouter", "openai", "deepseek", "anthropic"])
    model_type = st.selectbox("Model Type", ["basic", "advanced"])

    # Show API key status for online generation
    if generation_mode and generation_mode.startswith("🌐 Online"):
        st.write("**API Key Status:**")
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API key configured")
        if os.getenv("OPENROUTER_API_KEY"):
            st.success("✅ OpenRouter API key configured")
        if os.getenv("DEEPSEEK_API_KEY"):
            st.success("✅ DeepSeek API key configured")
        if os.getenv("ANTHROPIC_API_KEY"):
            st.success("✅ Anthropic API key configured")

        if not api_keys_available:
            st.error("❌ No API keys configured")
            st.info("Add API keys to .env file to use online generation")

# Advanced options
with st.expander("🔧 Advanced Options"):
    use_offline_estimation = st.checkbox("Use Enhanced Estimation", help="Use offline analysis for better question count estimation")
    debug_mode = st.checkbox("🐛 Debug Mode", help="Show detailed debug information")
    st.info(f"Recommended method: {capabilities['recommended_method']}")

    if capabilities["quality_ranking"]:
        st.info(f"Quality ranking: {' > '.join(capabilities['quality_ranking'])}")

    if capabilities["speed_ranking"]:
        st.info(f"Speed ranking: {' > '.join(capabilities['speed_ranking'])}")

    # Show setup instructions
    for method, instruction in capabilities.get("setup_instructions", {}).items():
        if method not in [m.lower().split()[0] for m in generation_modes] if generation_modes else []:
            st.info(f"💡 {instruction}")

    # Debug information
    if debug_mode:
        st.write("**Debug Information:**")
        st.write(f"Generation mode: {generation_mode}")
        st.write(f"Model provider: {model_provider}")
        st.write(f"Model type: {model_type}")
        st.write(f"API keys configured:")
        st.write(f"  - OpenAI: {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
        st.write(f"  - OpenRouter: {'✅' if os.getenv('OPENROUTER_API_KEY') else '❌'}")
        st.write(f"  - DeepSeek: {'✅' if os.getenv('DEEPSEEK_API_KEY') else '❌'}")
        st.write(f"  - Anthropic: {'✅' if os.getenv('ANTHROPIC_API_KEY') else '❌'}")

# Show all available methods
with st.expander("📋 All Available Generation Methods"):
    st.markdown("""
    **🎯 Enhanced Professional** - Academic-grade questions (T5-Large + advanced analysis)
    - Best for: Universities, certification, professional training
    - Quality: ⭐⭐⭐⭐⭐ | Speed: ⚡⚡⚡ | Setup: `python setup_enhanced_professional.py`

    **⚡ Fast** - Speed-optimized generation (T5-Base + optimizations)
    - Best for: Real-time applications, high-volume processing
    - Quality: ⭐⭐⭐⭐ | Speed: ⚡⚡⚡⚡⚡ | Setup: `python setup_fast_models.py`

    **🌐 Online** - Original method with latest AI models (OpenAI, Claude, etc.)
    - Best for: Flexible model access, latest capabilities
    - Quality: ⭐⭐⭐⭐ | Speed: ⚡⚡⚡⚡ | Setup: Configure API keys in .env file

    **🔒 Offline** - Privacy-focused, no internet required
    - Best for: Privacy-sensitive environments, no internet access
    - Quality: ⭐⭐⭐ | Speed: ⚡⚡⚡ | Setup: `python setup_offline.py`
    """)

    st.info("💡 See GENERATION_METHODS_GUIDE.md for complete setup and usage instructions")

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

            # Extract text from main PDF
            extracted_text = extract_text_from_pdf(temp_path)

            # Extract text from amendment PDF if provided
            amendment_text = ""
            amendment_temp_path = None
            if use_amendment and amendment_file:
                amendment_temp_path = os.path.join('uploads', f"amendment_{amendment_file.name}")
                with open(amendment_temp_path, 'wb') as f:
                    f.write(amendment_file.getvalue())
                amendment_text = extract_text_from_pdf(amendment_temp_path)

                # Check if amendment extraction was successful
                is_amendment_error = (isinstance(amendment_text, str) and
                                     amendment_text.startswith('Error extracting text from PDF:'))
                if is_amendment_error:
                    st.error("Failed to extract amendment PDF")
                    st.error(amendment_text)
                    if os.path.exists(amendment_temp_path):
                        os.remove(amendment_temp_path)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.stop()

            # Check if text extraction was successful (check for specific error patterns at the start)
            is_error = (isinstance(extracted_text, str) and
                       (extracted_text.startswith('Error extracting text from PDF:') or
                        extracted_text.startswith('PDF Validation Error:') or
                        extracted_text.startswith('Failed to load PDF document:') or
                        extracted_text.startswith('No text could be extracted from the PDF') or
                        extracted_text.startswith('Unexpected error extracting text from PDF:')))

            if is_error:
                # Clean up before showing error
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                # Show detailed error message
                st.error("📄 PDF Processing Error")
                st.error(extracted_text)

                # Provide helpful suggestions
                if "scanned document" in extracted_text or "image-based PDF" in extracted_text:
                    st.info("💡 **Suggestions for scanned PDFs:**")
                    st.info("• Try using a PDF with selectable text instead")
                    st.info("• Convert the scanned PDF to text using OCR tools")
                    st.info("• Use a different PDF document")
                elif "corrupted" in extracted_text or "password-protected" in extracted_text:
                    st.info("💡 **Suggestions:**")
                    st.info("• Check if the PDF file is corrupted")
                    st.info("• If password-protected, remove the password first")
                    st.info("• Try uploading a different PDF file")
                else:
                    st.info("💡 **Suggestions:**")
                    st.info("• Ensure the file is a valid PDF document")
                    st.info("• Try uploading a different PDF file")
                    st.info("• Check if the PDF contains readable text")
            else:
                # Text extraction successful, proceed with MCQ generation
                if not extracted_text.strip():
                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    st.error("📄 The PDF appears to be empty or contains no readable text.")
                    st.info("💡 Please upload a PDF with text content.")
                else:
                    # Show text extraction success
                    st.success(f"✅ Successfully extracted text from PDF ({len(extracted_text)} characters)")

                    # Estimate maximum questions
                    if use_offline_estimation:
                        estimation_result = estimate_max_questions_detailed(extracted_text)
                        max_questions = estimation_result["max_questions"]
                        st.info(f"🔍 Enhanced estimation: {max_questions} questions (confidence: {estimation_result['confidence']})")
                        if estimation_result.get("breakdown"):
                            with st.expander("📊 Estimation Details"):
                                st.json(estimation_result["breakdown"])
                    else:
                        max_questions = estimate_max_questions(extracted_text, use_offline=False)

                    # Determine number of questions to generate
                    if use_max_questions:
                        questions_to_generate = max_questions
                        st.info(f"🚀 Generating maximum possible questions: {max_questions}")
                    else:
                        questions_to_generate = num_questions
                        st.info(f"📊 Estimated maximum questions from this PDF: {max_questions}")
                        if num_questions > max_questions:
                            st.warning(f"⚠️ You requested {num_questions} questions, but the PDF content may only support ~{max_questions} quality questions. Consider using fewer questions for better quality.")

                    # Prepare model config for amendment support
                    model_config = None
                    if use_amendment and amendment_text:
                        model_config = {
                            'use_amendment': True,
                            'amendment_text': amendment_text
                        }
                        st.info("📝 Amendment analysis enabled - generating questions covering changes and differences")

                    # Generate MCQ questions based on selected mode
                    if generation_mode and generation_mode.startswith("⚡ Fast"):
                        with st.spinner(f'⚡ Generating {questions_to_generate} MCQ questions quickly...'):
                            questions = generate_fast_mcq_questions_enhanced(
                                extracted_text,
                                num_questions=questions_to_generate,
                                difficulty=difficulty,
                                book_name=book_name.strip(),
                                chapter_name=chapter_name.strip()
                            )
                    elif generation_mode and generation_mode.startswith("🎯 Professional"):
                        with st.spinner(f'🎯 Generating {questions_to_generate} professional-quality MCQ questions...'):
                            questions = generate_professional_mcq_questions_enhanced(
                                extracted_text,
                                num_questions=questions_to_generate,
                                difficulty=difficulty,
                                book_name=book_name.strip(),
                                chapter_name=chapter_name.strip()
                            )
                    else:
                        # Determine preferences based on mode
                        prefer_fast = generation_mode and generation_mode.startswith("⚡ Fast")
                        prefer_professional = generation_mode and generation_mode.startswith("🎯 Professional")
                        prefer_offline = generation_mode and generation_mode.startswith("🔒 Offline")

                        generation_method = generation_mode.split()[1] if generation_mode else "hybrid"

                        if debug_mode:
                            st.write(f"🐛 Debug: Using generation method: {generation_method}")
                            st.write(f"🐛 Debug: Preferences - Fast: {prefer_fast}, Professional: {prefer_professional}, Offline: {prefer_offline}")
                            if use_amendment:
                                st.write(f"🐛 Debug: Amendment mode enabled")

                        with st.spinner(f'Generating {questions_to_generate} MCQ questions using {generation_method}...'):
                            questions = generate_mcq_questions_with_offline_fallback(
                                extracted_text,
                                num_questions=questions_to_generate,
                                difficulty=difficulty,
                                book_name=book_name.strip(),
                                chapter_name=chapter_name.strip(),
                                prefer_offline=prefer_offline,
                                prefer_professional=prefer_professional,
                                prefer_fast=prefer_fast,
                                model_config=model_config,
                                use_amendment=use_amendment
                            )

                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    if amendment_temp_path and os.path.exists(amendment_temp_path):
                        os.remove(amendment_temp_path)

                    # Debug output
                    if debug_mode:
                        st.write(f"🐛 Debug: Generation result type: {type(questions)}")
                        st.write(f"🐛 Debug: Generation result length: {len(questions) if isinstance(questions, list) else 'N/A'}")
                        if isinstance(questions, str):
                            st.write(f"🐛 Debug: Error message: {questions[:200]}...")

                    # Check MCQ generation results
                    if isinstance(questions, str) and 'Error' in questions:
                        st.error("🤖 MCQ Generation Error")
                        st.error(questions)

                        # Provide suggestions for MCQ generation errors
                        if "context length" in questions.lower():
                            st.info("💡 The document might be too large. Try with a smaller document or fewer questions.")
                        elif "api" in questions.lower():
                            st.info("💡 Check your API key configuration and internet connection.")
                        else:
                            st.info("💡 Please try again or contact support if the issue persists.")
                    elif not questions or len(questions) == 0:
                        st.error("🤖 No Questions Generated")
                        st.error("The AI model did not generate any valid questions from the provided text.")
                        st.info("💡 Try:")
                        st.info("• Using a different generation method")
                        st.info("• Providing more detailed text content")
                        st.info("• Reducing the number of requested questions")
                        st.info("• Checking your API key configuration")
                    else:
                        # Validate questions before displaying
                        valid_questions = []
                        for q in questions:
                            if (isinstance(q, dict) and
                                q.get('question') and
                                q.get('options') and
                                q.get('correct')):
                                valid_questions.append(q)

                        if not valid_questions:
                            st.error("🤖 Invalid Questions Generated")
                            st.error("The AI model generated questions but they are missing required fields.")
                            st.info("💡 Try using a different generation method or check your API configuration.")
                        else:
                            # Display valid questions
                            st.subheader(f'Generated Questions ({len(valid_questions)} valid)')

                            if len(valid_questions) < len(questions):
                                st.warning(f"⚠️ {len(questions) - len(valid_questions)} questions were invalid and filtered out.")

                            for i, q in enumerate(valid_questions, 1):
                                try:
                                    st.write(f"**Question {i}:** {q.get('question', 'Missing question')}")
                                    options = q.get('options', {})
                                    st.write(f"A) {options.get('A', 'Missing option A')}")
                                    st.write(f"B) {options.get('B', 'Missing option B')}")
                                    st.write(f"C) {options.get('C', 'Missing option C')}")
                                    st.write(f"D) {options.get('D', 'Missing option D')}")
                                    with st.expander("Show Answer and Explanation"):
                                        st.write(f"**Correct Answer:** {q.get('correct', 'Missing')}")
                                        st.write(f"**Difficulty:** {q.get('difficulty', 'Not specified')}")
                                        st.write(f"**Explanation:** {q.get('explanation', 'No explanation provided')}")
                                    st.write("---")
                                except Exception as e:
                                    st.error(f"Error displaying question {i}: {e}")
                                    st.json(q)  # Show raw question data for debugging

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
                            try:
                                # Create PDF with proper error handling
                                pdf = FPDF()
                                pdf.set_auto_page_break(auto=True, margin=15)
                                pdf.add_page()

                                # Use Arial font (built-in, no external font files needed)
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
                                        question_text = f"{i}. {q['question']}"

                                        # Handle long questions by splitting into multiple lines
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
                                        pdf.cell(0, 6, f"A) {q['options']['A']}", 0, 1)
                                        pdf.cell(0, 6, f"B) {q['options']['B']}", 0, 1)
                                        pdf.cell(0, 6, f"C) {q['options']['C']}", 0, 1)
                                        pdf.cell(0, 6, f"D) {q['options']['D']}", 0, 1)
                                        pdf.ln(2)

                                        # Answer and explanation
                                        pdf.set_font("Arial", 'B', 11)
                                        pdf.cell(0, 6, f"Correct Answer: {q['correct']}", 0, 1)
                                        pdf.cell(0, 6, f"Difficulty: {q['difficulty'].capitalize()}", 0, 1)

                                        # Explanation
                                        pdf.set_font("Arial", '', 10)
                                        explanation = f"Explanation: {q['explanation']}"

                                        # Handle long explanations
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
                                        st.error(f"Error processing question {i}: {question_error}")
                                        # Add a simple error message and continue
                                        pdf.set_font("Arial", '', 10)
                                        pdf.cell(0, 6, f"Error processing question {i}", 0, 1)
                                        pdf.ln(4)
                                        continue

                                # Generate PDF output
                                pdf_output = BytesIO()
                                try:
                                    pdf_string = pdf.output(dest='S')

                                    if not pdf_string:
                                        st.error("PDF generation failed: Empty PDF content")
                                        st.info("PDF generation failed. You can still download the CSV file.")
                                    else:
                                        if isinstance(pdf_string, str):
                                            pdf_output.write(pdf_string.encode('latin-1'))
                                        else:
                                            pdf_output.write(pdf_string)
                                        pdf_output.seek(0)

                                        pdf_content = pdf_output.getvalue()
                                        if len(pdf_content) == 0:
                                            st.error("PDF generation failed: 0 bytes generated")
                                            st.info("PDF generation failed. You can still download the CSV file.")
                                        else:
                                            st.success(f"✅ PDF generated successfully ({len(pdf_content)} bytes)")
                                            st.download_button(
                                                "Download PDF",
                                                pdf_content,
                                                "mcq_questions.pdf",
                                                "application/pdf",
                                                key='download-pdf'
                                            )
                                except Exception as pdf_output_error:
                                    st.error(f"PDF output error: {pdf_output_error}")
                                    st.info("PDF generation failed. You can still download the CSV file.")

                            except Exception as pdf_error:
                                st.error(f"Error generating PDF: {pdf_error}")
                                st.info("PDF generation failed. You can still download the CSV file.")