# PDF MCQ Generator - Deployment Notes

## Latest Changes (v2.1.0)

### Features Added
1. **PDF Export for Notes** - Users can now download comprehensive notes as PDF
2. **User Model Selection** - Notes generation now uses the user's selected model from OpenRouter instead of hardcoded DeepSeek
3. **Improved PDF Formatting** - Notes PDF includes proper formatting with headers and spacing

### Files Modified
- `flask_app.py` - Added `/download-notes-pdf` endpoint
- `templates/index.html` - Updated UI with PDF download button and model selection
- `mcq_generator.py` - Fixed model name handling for full model names

### Deployment Status
- **GitHub**: Changes pushed to main branch (commit: 3f29767)
- **Vercel**: Automatic redeploy triggered
- **Expected Availability**: Within 2-5 minutes

### What Changed in Production

#### 1. Notes Generation Mode
- **Before**: Always used `deepseek/deepseek-chat` model
- **After**: Uses the model selected in the "AI Model Provider" dropdown

#### 2. Download Options for Notes
- **Before**: Only "Download as Text" button
- **After**: Added "Download as PDF" button (red button next to text download)

#### 3. Backend Endpoints
- **New**: `/download-notes-pdf` - Generates PDF from notes content

### Testing the Changes

1. **Generate Notes**:
   - Select "📝 Generate Notes" mode
   - Choose a model from the "Model" dropdown (e.g., DeepSeek, Llama, etc.)
   - Upload a PDF
   - Click "Generate Notes"

2. **Download as PDF**:
   - After notes are generated, click "📄 Download as PDF" button
   - PDF will be downloaded with proper formatting

3. **Model Selection**:
   - Try different models from the dropdown
   - Notes should be generated using the selected model

### Troubleshooting

If changes are not visible:
1. **Clear browser cache** (Ctrl+Shift+Delete or Cmd+Shift+Delete)
2. **Hard refresh** (Ctrl+F5 or Cmd+Shift+R)
3. **Wait 5 minutes** for Vercel deployment to complete
4. **Check browser console** (F12) for any JavaScript errors

### API Endpoints

```
POST /summarize-pdf
- Parameters: pdfFile, modelProvider, modelType
- Returns: {success, summary, filename, total_pages, text_length, model_used}

POST /download-notes-pdf
- Parameters: {notes, filename}
- Returns: PDF file (application/pdf)
```

### Notes
- Vercel has a 6MB file size limit for serverless functions
- PDF generation uses FPDF library with latin-1 encoding
- Notes are formatted with proper headers and spacing

