# Amendment Feature - Quick Start Guide

## What is the Amendment Feature?

The Amendment Feature allows you to upload **TWO PDF files**:
1. **Base PDF** - The original document
2. **Amendment PDF** - The updated/amended version

The system then generates MCQ questions that focus on **changes, differences, and new provisions** introduced by the amendment.

## How to Use

### Step 1: Start the Application
```bash
# For Flask
python flask_app.py

# For Streamlit
streamlit run app.py
```

### Step 2: Upload Base PDF
- Click "Choose PDF file" and select your original document
- Wait for text extraction to complete

### Step 3: Enable Amendment Mode
- Check the checkbox: **"📝 Generate questions from PDF with amendments"**
- The amendment upload section will appear

### Step 4: Upload Amendment PDF
- Click "📋 Upload Amendment PDF"
- Select the amended version of your document
- Confirm the filename is displayed

### Step 5: Generate Questions
- Select generation mode (Fast, Professional, or Hybrid)
- Set number of questions
- Click "Generate MCQs"
- Wait for generation to complete

## Expected Question Types

### Amendment-Focused Questions
```
Q: What was changed in the amendment regarding employee work hours?
A: Work hours reduced from 8 to 7 hours per day
Reference: Original Section 2 / Amendment Section 2

Q: Which provision was added in the amendment?
A: New provision for remote work eligibility
Reference: Amendment Section 5

Q: How does the amended version differ from the original?
A: Added flexibility for work-from-home arrangements
Reference: Original Section 3 / Amendment Section 3
```

## Reference Format

### In Explanations
- **Original Only**: "Reference: Original Section X"
- **Amendment Only**: "Reference: Amendment Section Y"
- **Both**: "Reference: Original Section X / Amendment Section Y"

## Quality Assurance

All questions follow the **7 Mandatory Quality Rules**:
1. ✅ Single correct answer
2. ✅ No conditional language
3. ✅ Verified options
4. ✅ Paragraph references
5. ✅ Independent verifiability
6. ✅ Exclusivity guarantee
7. ✅ Even coverage

## Tips for Best Results

### Document Preparation
- Ensure both PDFs have readable text (not scanned images)
- Use clear section numbering for easy reference
- Keep documents reasonably sized (< 50 pages each)

### Amendment Selection
- Choose amendments that introduce significant changes
- Ensure amendment clearly references original sections
- Include both additions and modifications

### Question Generation
- Start with 5-10 questions for testing
- Use "Professional" mode for higher quality
- Review questions for accuracy before use

## Troubleshooting

### Amendment PDF Not Uploading
- Check file size (should be < 50MB)
- Ensure file is a valid PDF
- Try a different PDF file

### Questions Don't Focus on Amendments
- Verify amendment text was extracted correctly
- Check that amendment contains significant changes
- Try with a different amendment document

### Missing References
- Ensure PDFs have clear section numbers
- Check that sections are referenced in text
- Verify amendment references original sections

## Backward Compatibility

✅ **Single PDF Upload Still Works**
- Uncheck the amendment checkbox
- Upload only the base PDF
- Generate questions normally

## File Cleanup

✅ **Automatic Cleanup**
- Temporary files are automatically deleted
- No manual cleanup required
- Safe to upload multiple times

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review AMENDMENT_FEATURE_IMPLEMENTATION.md
3. Check application logs for error messages
4. Contact support with error details

## Example Workflow

```
1. Upload "Aadhaar_Act_2016.pdf" (original)
2. Check "Generate questions from PDF with amendments"
3. Upload "Aadhaar_Amendment_2023.pdf"
4. Select "Professional" mode
5. Request 10 questions
6. Generate MCQs
7. Review questions focusing on 2023 amendments
8. Export to desired format (Web, CSV, PDF)
```

## Next Features (Planned)

- Amendment comparison visualization
- Amendment-specific export formats
- Amendment timeline tracking
- Multi-amendment support
- Amendment impact analysis

