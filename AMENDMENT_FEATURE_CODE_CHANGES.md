# Amendment Feature - Code Changes Reference

## Summary of Changes

### 1. Flask Backend (flask_app.py)

#### Location: Lines 59-78
**Added Amendment PDF Handling**
```python
# Amendment PDF support
use_amendment = request.form.get('useAmendment') == 'on'
amendment_file = None
amendment_text = ""

if use_amendment and 'amendmentPdfFile' in request.files:
    amendment_file = request.files['amendmentPdfFile']
    if amendment_file and amendment_file.filename != '':
        amendment_temp_path = os.path.join('uploads', f"amendment_{amendment_file.filename}")
        os.makedirs('uploads', exist_ok=True)
        amendment_file.save(amendment_temp_path)
        amendment_text = extract_text_from_pdf(amendment_temp_path)
        
        # Check if amendment extraction was successful
        is_amendment_error = (isinstance(amendment_text, str) and
                             amendment_text.startswith('Error extracting text from PDF:'))
        if is_amendment_error:
            if os.path.exists(amendment_temp_path):
                os.remove(amendment_temp_path)
            return jsonify({'error': 'Failed to extract amendment PDF', 'details': amendment_text}), 400
```

#### Location: Lines 155-186
**Pass Amendment Data to Model Config**
```python
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
```

### 2. Streamlit Frontend (app.py)

#### Location: Lines 62-73
**Added Amendment UI Components**
```python
# Amendment PDF support
st.markdown("---")
use_amendment = st.checkbox("📝 Generate questions from PDF with amendments", 
                             help="Enable this to upload an amendment PDF and generate questions covering changes, differences, and new provisions")

amendment_file = None
if use_amendment:
    amendment_file = st.file_uploader("📋 Upload Amendment PDF (optional)", type="pdf", key="amendment_pdf")
    if amendment_file:
        st.success(f"✅ Amendment PDF loaded: {amendment_file.name}")
```

#### Location: Lines 180-211
**Extract Amendment Text**
```python
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
```

#### Location: Lines 279-333
**Pass Amendment Data to Generation**
```python
# Prepare model config for amendment support
model_config = None
if use_amendment and amendment_text:
    model_config = {
        'use_amendment': True,
        'amendment_text': amendment_text
    }
    st.info("📝 Amendment analysis enabled - generating questions covering changes and differences")

# ... in generation call:
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
```

#### Location: Lines 335-340
**Cleanup Amendment Files**
```python
# Clean up
if os.path.exists(temp_path):
    os.remove(temp_path)
if amendment_temp_path and os.path.exists(amendment_temp_path):
    os.remove(amendment_temp_path)
```

### 3. Flask Frontend (templates/index.html)

#### Location: Lines 191-210
**Amendment Upload UI**
```html
<!-- Amendment PDF Upload -->
<div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0;">
    <label style="font-weight: bold;">
        <input type="checkbox" id="useAmendment" name="useAmendment" onchange="toggleAmendmentUpload()">
        📝 Generate questions from PDF with amendments
    </label>
    <p style="font-size: 0.9em; color: #666; margin: 10px 0;">
        Enable this to upload an amendment PDF and generate questions covering changes, differences, and new provisions.
    </p>

    <div id="amendmentUploadSection" style="display: none; margin-top: 10px;">
        <label for="amendmentPdfFile" style="font-weight: bold;">📋 Upload Amendment PDF:</label>
        <input type="file" id="amendmentPdfFile" name="amendmentPdfFile" accept=".pdf">
        <p style="font-size: 0.85em; color: #666; margin-top: 5px;">
            ℹ️ Questions will analyze both documents and focus on amendments, changes, and differences.
        </p>
        <div id="amendmentFileInfo" style="margin-top: 10px; padding: 10px; background-color: #e7f3ff; border-radius: 3px; display: none;">
            <strong>✅ Amendment PDF loaded:</strong> <span id="amendmentFileName"></span>
        </div>
    </div>
</div>
```

#### Location: Lines 398-431
**JavaScript Functions**
```javascript
// Toggle amendment PDF upload section
function toggleAmendmentUpload() {
    const useAmendment = document.getElementById('useAmendment').checked;
    const amendmentSection = document.getElementById('amendmentUploadSection');
    const amendmentFile = document.getElementById('amendmentPdfFile');

    if (useAmendment) {
        amendmentSection.style.display = 'block';
    } else {
        amendmentSection.style.display = 'none';
        amendmentFile.value = '';
        document.getElementById('amendmentFileInfo').style.display = 'none';
    }
}

// Handle amendment file selection
document.addEventListener('DOMContentLoaded', function() {
    updateModelOptions();

    const amendmentFile = document.getElementById('amendmentPdfFile');
    if (amendmentFile) {
        amendmentFile.addEventListener('change', function() {
            const fileInfo = document.getElementById('amendmentFileInfo');
            const fileName = document.getElementById('amendmentFileName');

            if (this.files && this.files[0]) {
                fileName.textContent = this.files[0].name;
                fileInfo.style.display = 'block';
            } else {
                fileInfo.style.display = 'none';
            }
        });
    }
});
```

### 4. MCQ Generator (mcq_generator.py)

#### Location: Lines 746-814
**New Helper Functions**
```python
def create_amendment_prompt_section(use_amendment=False):
    """Creates amendment-specific prompt section"""
    if not use_amendment:
        return ""
    return """
    AMENDMENT ANALYSIS REQUIREMENTS:
    ================================
    [Amendment-specific instructions...]
    """

def merge_texts_for_amendment_analysis(original_text, amendment_text):
    """Intelligently merges original and amendment texts"""
    merged = f"""=== ORIGINAL DOCUMENT ===
{original_text}

=== AMENDMENT DOCUMENT ===
{amendment_text}

=== ANALYSIS INSTRUCTIONS ===
[Analysis instructions...]
"""
    return merged
```

#### Location: Lines 1106-1133
**Updated generate_mcq_questions_advanced()**
```python
use_amendment = model_config.get('use_amendment', False)
amendment_section = create_amendment_prompt_section(use_amendment)
```

#### Location: Lines 1199-1206
**Include Amendment Section in Prompt**
```python
{explanation_instruction}{amendment_section}
```

#### Location: Lines 1224-1239
**Amendment-Aware System Message**
```python
if use_amendment:
    system_message = "You are an expert educator analyzing an original document and its amendment..."
else:
    system_message = "You are an expert educator specializing in government rules..."
```

## Testing the Changes

### Flask Test
1. Start Flask: `python flask_app.py`
2. Upload base PDF
3. Check "Generate questions from PDF with amendments"
4. Upload amendment PDF
5. Generate MCQs
6. Verify questions focus on amendments

### Streamlit Test
1. Start Streamlit: `streamlit run app.py`
2. Upload base PDF
3. Check "Generate questions from PDF with amendments"
4. Upload amendment PDF
5. Generate MCQs
6. Verify questions focus on amendments

## Verification Checklist

- ✅ Amendment checkbox appears in UI
- ✅ Amendment file upload field shows when checked
- ✅ Amendment filename displays after upload
- ✅ Amendment text is extracted correctly
- ✅ Questions focus on amendments and changes
- ✅ References specify Original/Amendment
- ✅ Temporary files are cleaned up
- ✅ Backward compatibility maintained
- ✅ Error handling works correctly
- ✅ All 7 quality rules applied

