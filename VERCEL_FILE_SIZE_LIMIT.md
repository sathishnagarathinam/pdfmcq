# Vercel File Size Limitation - Important Information

## Problem
When uploading large PDF files (>6MB) to the production server on Vercel, you may encounter a **413 Payload Too Large** error.

## Root Cause
Vercel's serverless functions have a hard limit of **6MB** for request body size. This is a platform limitation that cannot be overridden through Flask configuration alone.

## Solution

### For Production (Vercel)
- **Maximum file size: 6MB**
- If your PDF is larger than 6MB, you have two options:
  1. **Compress the PDF** - Use a PDF compression tool to reduce file size
  2. **Use Local Version** - Run the application locally for larger files (supports up to 500MB)

### For Local Development
- **Maximum file size: 500MB**
- No limitations on file size when running locally

## How to Check Your Environment
The application automatically detects whether you're on production or local:
- **Production**: Vercel domain (e.g., `pdfmcq.vercel.app`)
- **Local**: `localhost` or `127.0.0.1`

## Error Messages
If you try to upload a file that's too large:
- **Production**: "File too large! Maximum 6MB on Vercel"
- **Local**: "File too large! Maximum 500MB"

## Workarounds

### Option 1: Compress PDF
Use online tools or command-line tools to compress your PDF:
```bash
# Using ghostscript (command line)
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed.pdf input.pdf
```

### Option 2: Split Large PDF
Split your large PDF into smaller chunks (each <6MB) and process them separately.

### Option 3: Use Local Version
For development and testing with large files:
```bash
python flask_app.py
# Access at http://localhost:5000
```

## Technical Details
- Vercel function timeout: 900 seconds (15 minutes)
- Vercel function memory: 3008 MB
- Request body limit: 6MB (hardcoded by Vercel)
- Local Flask limit: 500MB (configurable)

## Future Improvements
To support larger files in production, consider:
1. Using AWS S3 or similar cloud storage for file uploads
2. Implementing chunked/streaming uploads
3. Using Vercel's file system for temporary storage
4. Migrating to a different hosting platform with higher limits

## Support
If you need to process files larger than 6MB in production, please:
1. Contact the development team
2. Use the local version for now
3. Consider the workarounds mentioned above

