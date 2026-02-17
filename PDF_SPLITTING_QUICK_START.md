# PDF Splitting Feature - Quick Start Guide

## Installation & Setup

### 1. Verify Dependencies
The feature uses PyPDF2 which should already be installed. Verify:

```bash
pip3 list | grep PyPDF2
```

If not installed:
```bash
pip3 install PyPDF2
```

### 2. Restart Flask App
The Flask app is already running. If you need to restart:

```bash
# Kill existing process
pkill -f "python3 flask_app.py"

# Start new instance
python3 flask_app.py
```

## Testing the Feature

### Test 1: Split by Pages Per File

**Steps:**
1. Open http://localhost:5002
2. Login with credentials
3. Select "✂️ Split PDF File" radio button
4. Keep "Split by Pages Per File" selected
5. Enter "2" in "Number of Pages Per File"
6. Upload `test_standard.pdf` (2 pages)
7. Click "Split PDF"

**Expected Result:**
- 1 file created (all pages fit in one file)
- Download button appears
- File size shown

### Test 2: Split by Page Ranges

**Steps:**
1. Select "✂️ Split PDF File"
2. Change to "Split by Page Ranges"
3. Enter "1-1, 2-2" in page ranges
4. Upload `test_standard.pdf`
5. Click "Split PDF"

**Expected Result:**
- 2 files created (one per page)
- Both files downloadable
- Correct page ranges in filenames

### Test 3: Split into Individual Pages

**Steps:**
1. Select "✂️ Split PDF File"
2. Change to "Split into Individual Pages"
3. Upload `test_standard.pdf`
4. Click "Split PDF"

**Expected Result:**
- 2 files created (one per page)
- Files named: `test_standard_page_1.pdf`, `test_standard_page_2.pdf`
- Both downloadable

## File Naming Convention

### Split by Pages Per File
```
original_name_part_1_pages_1-5.pdf
original_name_part_2_pages_6-10.pdf
original_name_part_3_pages_11-15.pdf
```

### Split by Page Ranges
```
original_name_range_1_pages_1-5.pdf
original_name_range_2_pages_6-10.pdf
original_name_range_3_pages_11-15.pdf
```

### Split into Individual Pages
```
original_name_page_1.pdf
original_name_page_2.pdf
original_name_page_3.pdf
```

## Error Handling

### Common Errors & Solutions

**Error: "Invalid page range"**
- Check page numbers are within PDF total pages
- Use 1-indexed numbering (start from 1, not 0)
- Format: "1-5, 6-10" (with hyphen and comma)

**Error: "Pages per file must be less than total pages"**
- Reduce pages per file value
- Example: For 5-page PDF, use 2 or 3, not 5

**Error: "No file uploaded"**
- Ensure PDF file is selected
- Check file is valid PDF format

## Performance Notes

- Small PDFs (< 10MB): < 1 second
- Medium PDFs (10-50MB): 1-5 seconds
- Large PDFs (> 50MB): May take longer
- Individual page splitting slower for large PDFs

## Troubleshooting

### Files not downloading?
- Check browser download settings
- Try different browser
- Check file permissions

### Temporary files not cleaning up?
- Check `/tmp` directory
- Manual cleanup: `rm -rf /tmp/tmp*`

### Session expired?
- Refresh page and try again
- Sessions expire after browser close

## Integration with Other Features

✅ Works alongside MCQ generation
✅ Works alongside MCQ parsing
✅ Independent mode - no conflicts
✅ Same authentication system
✅ Same upload folder structure

## Next Steps

1. Test all three split modes
2. Try with different PDF sizes
3. Test error cases
4. Verify downloads work
5. Check temporary file cleanup
6. Deploy to production when ready

## Support

For issues or questions:
1. Check error messages in browser console
2. Review Flask app logs
3. Verify PDF file is valid
4. Check page ranges are correct
5. Ensure sufficient disk space for temp files

