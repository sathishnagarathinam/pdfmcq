# 🆘 MCQ Parser - Troubleshooting Guide

## Error: "No Questions Found in PDF"

This is the most common error. Follow this guide to fix it.

---

## 🔍 Diagnosis Steps

### **Step 1: Verify PDF is Text-Based**

**Problem:** PDF is a scanned image (not text)

**How to Check:**
1. Open PDF in Adobe Reader
2. Try to select and copy text
3. If you can't select text → PDF is scanned

**Solution:**
- Use OCR tool to convert scanned PDF to text:
  - Adobe Acrobat (paid)
  - Google Docs (free) - Upload PDF, download as PDF
  - Online OCR tools (free)

---

### **Step 2: Check Question Numbering**

**Problem:** Questions don't use supported format

**Supported Formats:**
```
✅ 1. Question text
✅ Q1: Question text
✅ Question 1: Question text
```

**Unsupported Formats:**
```
❌ 1 Question text (missing period)
❌ (1) Question text (parenthesis)
❌ Question 1 Question text (missing colon)
❌ 1) Question text (parenthesis instead of period)
```

**How to Fix:**
1. Open PDF in text editor
2. Find question lines
3. Ensure they match supported format
4. Edit PDF or recreate it

---

### **Step 3: Check Option Formatting**

**Problem:** Options not marked correctly

**Supported Formats:**
```
✅ A) Option text
✅ B) Option text
✅ C) Option text
✅ D) Option text
```

**Unsupported Formats:**
```
❌ A Option text (missing parenthesis)
❌ (A) Option text (parenthesis)
❌ A: Option text (colon)
❌ Option A: text (reversed)
```

**How to Fix:**
1. Check each option line
2. Ensure format is "A) text", "B) text", etc.
3. Edit PDF or recreate it

---

### **Step 4: Check Answer Key**

**Problem:** Answer key not found or wrong format

**Supported Formats:**
```
✅ 1. A
✅ Q1: B
✅ Answer 1: C
✅ 1) D
✅ 1 A
```

**Unsupported Formats:**
```
❌ A (no question number)
❌ Answer: A (no question number)
❌ 1-A (dash instead of period)
❌ 1:A (no space)
```

**How to Fix:**
1. Ensure answer key is on last page
2. Use supported format
3. One answer per line
4. Include question number

---

## 🛠️ Common Issues & Solutions

### **Issue 1: "No questions found" but PDF has questions**

**Cause:** Question numbering format not recognized

**Solution:**
```
1. Check question format in PDF
2. Ensure questions start with: 1., Q1:, or Question 1:
3. If different format, edit PDF to match
4. Re-upload and test
```

**Example Fix:**
```
BEFORE:
Question 1 What is Python?
A) Option A
B) Option B
C) Option C
D) Option D

AFTER:
1. What is Python?
A) Option A
B) Option B
C) Option C
D) Option D
```

---

### **Issue 2: Questions found but options missing**

**Cause:** Options not marked as A), B), C), D)

**Solution:**
```
1. Check option format in PDF
2. Ensure options are: A) text, B) text, C) text, D) text
3. Each option on separate line
4. No extra spaces before option letter
5. Re-upload and test
```

**Example Fix:**
```
BEFORE:
1. What is Python?
A - A snake
B - A programming language
C - A framework
D - A database

AFTER:
1. What is Python?
A) A snake
B) A programming language
C) A framework
D) A database
```

---

### **Issue 3: "No answer key found"**

**Cause:** Answer key format not recognized

**Solution:**
```
1. Ensure answer key is on last page
2. Use supported format: 1. A, Q1: B, etc.
3. One answer per line
4. Include question number
5. Re-upload and test
```

**Example Fix:**
```
BEFORE:
Answer Key
A, B, C, D, A, B, C, D

AFTER:
Answer Key
1. A
2. B
3. C
4. D
5. A
6. B
7. C
8. D
```

---

### **Issue 4: Partial extraction (some questions missing)**

**Cause:** Inconsistent formatting

**Solution:**
```
1. Use consistent numbering throughout
2. All questions should use same format
3. All options should use same format
4. Check for special characters
5. Re-upload and test
```

---

## 🧪 Testing Steps

### **Step 1: Create Test PDF**

Run the test PDF generator:
```bash
python create_test_pdf.py
```

This creates 3 test PDFs:
- test_standard.pdf (1., 2., etc.)
- test_q_format.pdf (Q1:, Q2:, etc.)
- test_question_format.pdf (Question 1:, etc.)

### **Step 2: Upload Test PDF**

1. Open http://127.0.0.1:5002
2. Select "📋 Parse Existing MCQ PDF"
3. Upload test_standard.pdf
4. Click "Parse MCQ PDF"

### **Step 3: Verify Results**

Expected output:
```
✅ Successfully extracted 5 questions from the PDF
📊 Parsing Summary
   Total Questions: 5
   Total Pages: 2
   Answer Key Page: 2
   Questions with Answers: 5
```

### **Step 4: Test Your PDF**

If test PDF works:
1. Compare your PDF with test PDF
2. Identify differences
3. Fix your PDF to match format
4. Re-upload and test

---

## 📋 PDF Preparation Checklist

Before uploading, verify:

- [ ] PDF is text-based (not scanned image)
- [ ] Questions are numbered (1., Q1:, Question 1:)
- [ ] Each question has exactly 4 options
- [ ] Options are marked A), B), C), D)
- [ ] Each option on separate line
- [ ] Answer key on last page
- [ ] Answer key uses supported format
- [ ] One answer per line
- [ ] No extra spaces or special characters
- [ ] Consistent formatting throughout

---

## 🔧 Advanced Debugging

### **Check Console Output**

When parsing, console shows debug info:

```
[DEBUG] Starting MCQ PDF parsing: sample.pdf
[DEBUG] Successfully extracted 6 pages
[DEBUG] Total lines to process: 250
[DEBUG] Found question 1: What is Python?...
[DEBUG]   Option A: A snake...
[DEBUG]   Option B: A programming language...
[DEBUG]   Option C: A framework...
[DEBUG]   Option D: A database...
[DEBUG] Saved question 1 with 4 options
[DEBUG] Found 50 questions
[DEBUG] Found 50 answers in answer key
[DEBUG] Matched 50 questions with answers
```

### **Analyze PDF Content**

Use Python to analyze your PDF:

```python
from mcq_parser import debug_pdf_content

# Analyze your PDF
analysis = debug_pdf_content('your_pdf.pdf')

# Check results
print(f"Total pages: {analysis['total_pages']}")
for page in analysis['pages']:
    print(f"Page {page['page_num']}:")
    print(f"  Questions: {page['question_patterns']}")
    print(f"  Options: {page['option_count']}")
    print(f"  Answers: {page['answer_patterns']}")
```

---

## 💡 Pro Tips

1. **Start with test PDF** - Verify parser works first
2. **Use consistent format** - Same numbering throughout
3. **Keep it simple** - Avoid complex formatting
4. **One question per section** - Clear separation
5. **Verify answer key** - All questions have answers
6. **Check PDF quality** - Ensure text is readable

---

## 🚀 Quick Fixes

### **If PDF has questions but parser doesn't find them:**

1. **Check question format:**
   ```
   Change: "Question 1 What is..."
   To:     "1. What is..."
   ```

2. **Check option format:**
   ```
   Change: "A Option text"
   To:     "A) Option text"
   ```

3. **Check answer key:**
   ```
   Change: "Answer: A"
   To:     "1. A"
   ```

4. **Test with sample:**
   - Run: `python create_test_pdf.py`
   - Upload test_standard.pdf
   - If it works, compare with your PDF
   - Fix differences

---

## 📞 Still Having Issues?

1. **Check MCQ_PARSER_DEBUGGING_GUIDE.md** for detailed guide
2. **Review console output** for debug messages
3. **Test with sample PDF** from create_test_pdf.py
4. **Verify PDF format** matches examples
5. **Check PDF is readable** (not scanned image)

---

## ✅ Success Indicators

### **Successful Parse:**
```
✅ Successfully extracted 50 questions from the PDF
📊 Parsing Summary
   Total Questions: 50
   Total Pages: 6
   Answer Key Page: 6
   Questions with Answers: 50
   Questions without Answers: 0
```

### **Failed Parse:**
```
❌ No questions found in PDF
💡 Suggestions:
   ✓ Ensure questions are numbered (1., Q1:, Question 1:, etc.)
   ✓ Each question must have options marked as A), B), C), D)
   ✓ Answer key should be on the last page or specified page
```

---

**For more help, see MCQ_PARSER_DEBUGGING_GUIDE.md**
