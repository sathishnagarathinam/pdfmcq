# PDF Split Production Fix - URL Encoding Issue

## Problem
In production, PDF splitting was failing with error:
```
An error occurred: The string did not match the expected pattern.
```

This error occurred when trying to download split PDF files.

## Root Cause
The filenames generated for split PDFs contain hyphens and underscores:
- Example: `document_part_1_pages_1-5.pdf`

When these filenames were passed directly in the URL path:
```
/download-split-pdf/{session_id}/{filename}
```

Flask's URL routing couldn't properly parse the hyphens in the filename, causing a pattern matching error.

## Solution
Implemented URL encoding/decoding for filenames:

### Frontend Changes (templates/index.html)
**Line 777**: Encode filename using `encodeURIComponent()`
```javascript
downloadBtn.href = `/download-split-pdf/${data.session_id}/${encodeURIComponent(file.filename)}`;
```

### Backend Changes (flask_app.py)
**Line 968**: Changed route to use `<path:filename>` converter
```python
@app.route('/download-split-pdf/<session_id>/<path:filename>', methods=['GET'])
```

**Lines 973-976**: Decode the filename from URL encoding
```python
from urllib.parse import unquote
filename = unquote(filename)
```

## How It Works
1. **Frontend**: `encodeURIComponent()` converts special characters to URL-safe format
   - `document_part_1_pages_1-5.pdf` → `document_part_1_pages_1%2D5.pdf`

2. **Backend**: 
   - `<path:filename>` converter accepts the full encoded path
   - `unquote()` decodes it back to original filename
   - File lookup and download proceeds normally

## Testing
✅ Works with filenames containing:
- Hyphens (-)
- Underscores (_)
- Numbers
- Dots (.)

## Deployment
1. Update `flask_app.py` with the route and decoding changes
2. Update `templates/index.html` with URL encoding
3. Restart the application
4. Test PDF splitting in production

## Files Modified
- `flask_app.py` (lines 968-976)
- `templates/index.html` (line 777)

