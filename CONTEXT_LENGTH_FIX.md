# Context Length Fix for PDF MCQ Generator

## Problem Description

The PDF MCQ Generator was encountering a context length error when processing large PDF documents:

```
Error generating questions: Error code: 400 - {'error': {'message': 'This endpoint\'s maximum context length is 163840 tokens. However, you requested about 257823 tokens (253823 of text input, 4000 in the output). Please reduce the length of either one, or use the "middle-out" transform to compress your prompt automatically.', 'code': 400, 'metadata': {'provider_name': None}}}
```

This error occurred because the entire PDF text was being sent to the AI model in a single request, exceeding the model's context window limit of 163,840 tokens.

## Solution Overview

The fix implements intelligent text chunking to split large documents into manageable pieces that fit within the AI model's context limits while maintaining content coherence.

### Key Components

1. **Token Counting Utility** (`estimate_token_count`)
   - Estimates token count using a conservative 1 token per 3.5 characters ratio
   - Helps determine when chunking is needed

2. **Text Chunking Algorithm** (`chunk_text`)
   - Splits large text into chunks of ~108,000 tokens (90% of 120,000 limit for safety)
   - Preserves sentence boundaries for better context
   - Includes overlap between chunks to maintain continuity
   - Validates chunk sizes to ensure they stay within limits

3. **Updated MCQ Generation Functions**
   - `generate_mcq_questions`: Enhanced to handle chunked text processing
   - `generate_mcq_questions_advanced`: Enhanced with the same chunking capability
   - Distributes question generation across chunks
   - Combines results from all chunks

## Technical Details

### Token Estimation
```python
def estimate_token_count(text):
    """Conservative estimate: 1 token per 3.5 characters"""
    return math.ceil(len(text) / 3.5)
```

### Chunking Strategy
- **Target size**: 108,000 tokens per chunk (90% of 120,000 limit)
- **Overlap**: 2,000 tokens between chunks for context preservation
- **Boundary detection**: Breaks at sentence endings when possible
- **Safety validation**: Double-checks token count and trims if necessary

### Question Distribution
- Questions are distributed evenly across chunks
- Last chunk gets any remaining questions to reach the exact requested count
- Each chunk is processed independently with the AI model
- Results are combined into a single response

## Benefits

1. **Handles Large Documents**: Can process PDFs of any size without context length errors
2. **Maintains Quality**: Preserves content coherence through intelligent chunking
3. **Backward Compatible**: Small documents continue to work as before
4. **Error Resilient**: Graceful handling of chunking and API errors
5. **Efficient**: Only chunks when necessary, preserves original behavior for small texts

## Usage

The fix is transparent to users. The existing API remains unchanged:

```python
# This now works with large documents automatically
questions = generate_mcq_questions(
    large_text,
    num_questions=10,
    model_provider='openrouter',
    model_type='basic',
    book_name='Large Document',
    chapter_name='Chapter 1'
)
```

## Testing

The solution has been thoroughly tested with:
- ✅ Large documents exceeding 250,000 tokens
- ✅ Small documents under the token limit
- ✅ Empty text handling
- ✅ Chunk size validation
- ✅ Question distribution logic
- ✅ Error scenarios

## Files Modified

- `mcq_generator.py`: Added chunking utilities and updated MCQ generation functions
- Added test files for validation:
  - `test_chunking_simulation.py`
  - `test_complete_solution.py`
  - `debug_pdf.py`

## Performance Impact

- **Small documents**: No performance impact (original code path)
- **Large documents**: Slight increase in processing time due to multiple API calls
- **Memory usage**: Minimal increase for chunk storage
- **API costs**: Proportional to document size (multiple smaller requests vs. one failed large request)

## Future Enhancements

Potential improvements for future versions:
1. Implement OCR for image-based PDFs (like the PO_Guide_Part-II.pdf)
2. Add progress indicators for large document processing
3. Implement parallel chunk processing for faster results
4. Add configurable chunk sizes based on model capabilities
5. Implement smart content-aware chunking (e.g., by chapters or sections)
