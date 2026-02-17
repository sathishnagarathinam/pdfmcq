# PDF Splitting Feature - Implementation Guide

## Overview

A new **PDF Splitting** feature has been added to the Flask web application (`flask_app.py`) and HTML template (`templates/index.html`). This feature allows users to split PDF files in multiple ways.

## Features Implemented

### 1. **Three Split Modes**

#### Mode 1: Split by Pages Per File
- Splits PDF into multiple files with a specified number of pages per file
- Example: 20-page PDF split by 5 pages per file = 4 output files
- Input: Number of pages per file (e.g., 5, 10, 15)

#### Mode 2: Split by Page Ranges
- Splits PDF based on user-specified page ranges
- Example: "1-5, 6-10, 11-15" creates 3 files
- Input: Comma-separated page ranges (1-indexed, inclusive)
- Format: "start-end, start-end, ..."

#### Mode 3: Split into Individual Pages
- Splits PDF into separate files, one page per file
- Useful for organizing large documents
- No additional input required

### 2. **Web Interface Updates**

#### New Radio Button Option
- Added "✂️ Split PDF File" option alongside existing modes
- Located in the Mode Selector section

#### Dynamic Form Sections
- Form fields change based on selected split mode
- "Pages Per File" input for Mode 1
- "Page Ranges" input for Mode 2
- Info message for Mode 3

#### Results Display
- Shows split summary (total pages, number of files)
- Displays each split file with:
  - Filename
  - File size
  - Download button

### 3. **Backend Implementation**

#### New Functions in `flask_app.py`

```python
split_pdf_by_pages_per_file(pdf_path, pages_per_file)
split_pdf_by_page_ranges(pdf_path, page_ranges)
split_pdf_into_individual_pages(pdf_path)
```

#### New Flask Routes

- **POST `/split-pdf`** - Handles PDF splitting requests
  - Parameters: splitMode, pagesPerFile, pageRanges
  - Returns: JSON with split file information and session ID

- **GET `/download-split-pdf/<session_id>/<filename>`** - Downloads split PDF
  - Secure file download with session validation
  - Automatic cleanup after download

### 4. **Technical Details**

#### Libraries Used
- **PyPDF2**: PDF reading and writing
- **uuid**: Session ID generation
- **tempfile**: Temporary file management

#### Session Management
- Each split operation gets a unique session ID
- Split files stored in temporary directory
- Session data stored in app.config['split_sessions']

#### Error Handling
- Validates page ranges
- Checks total page count
- Provides detailed error messages
- Automatic cleanup of temporary files

## Usage Instructions

### For Users

1. **Select Split Mode**
   - Click "✂️ Split PDF File" radio button

2. **Choose Split Method**
   - Select from dropdown: "Pages Per File", "Page Ranges", or "Individual Pages"

3. **Configure Parameters** (if needed)
   - For "Pages Per File": Enter number (e.g., 5)
   - For "Page Ranges": Enter ranges (e.g., "1-5, 6-10")
   - For "Individual Pages": No configuration needed

4. **Upload PDF**
   - Click file input and select PDF

5. **Click "Split PDF"**
   - Wait for processing

6. **Download Results**
   - Click download button for each split file

### Example Scenarios

**Scenario 1: Split 50-page document into 10-page chunks**
- Mode: "Split by Pages Per File"
- Pages Per File: 10
- Result: 5 files (pages 1-10, 11-20, 21-30, 31-40, 41-50)

**Scenario 2: Extract specific sections**
- Mode: "Split by Page Ranges"
- Page Ranges: "1-5, 15-20, 35-40"
- Result: 3 files with specified page ranges

**Scenario 3: Organize document by pages**
- Mode: "Split into Individual Pages"
- Result: One file per page (useful for large documents)

## Code Changes Summary

### `flask_app.py`
- Added PyPDF2 and uuid imports
- Added 3 PDF splitting functions
- Added `/split-pdf` POST route
- Added `/download-split-pdf/<session_id>/<filename>` GET route
- Session management for split operations

### `templates/index.html`
- Added "✂️ Split PDF File" radio button
- Added split mode section with dynamic form fields
- Added split results display container
- Updated `switchMode()` function
- Added `updateSplitOptions()` function
- Added `displaySplitResults()` function
- Updated form submission handler for split mode

## Security Considerations

✅ **CSRF Protection**: Routes use @csrf.exempt for file operations
✅ **Session Validation**: Download route validates session ID
✅ **File Cleanup**: Temporary files cleaned up after operations
✅ **Login Required**: All routes require authentication
✅ **File Size Limits**: Respects MAX_CONTENT_LENGTH (50MB)

## Testing Recommendations

1. Test each split mode with various PDF sizes
2. Test edge cases (single page, very large PDFs)
3. Test invalid page ranges
4. Test concurrent split operations
5. Verify file downloads work correctly
6. Check temporary file cleanup

## Future Enhancements

- Batch splitting of multiple PDFs
- Custom naming patterns for split files
- Merge split PDFs back together
- Preview pages before splitting
- Advanced filtering options

