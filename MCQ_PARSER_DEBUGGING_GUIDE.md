# 🔍 MCQ Parser - Debugging Guide

## Problem: "No Questions Found in PDF"

If you're getting this error even though your PDF contains questions, follow this guide to diagnose and fix the issue.

---

## 🎯 Root Causes

The parser requires:
1. **Clear question numbering** - Questions must start with a number
2. **Proper option formatting** - Options must be marked A), B), C), D)
3. **Valid answer key** - Answer key must be on a separate page
4. **Readable text** - PDF must have extractable text (not scanned image)

---

## 🔧 Step-by-Step Debugging

### **Step 1: Check PDF Format**

Your PDF should look like this:

```
Page 1-5: Questions
─────────────────
1. What is Python?
A) A snake
B) A programming language
C) A framework
D) A database

2. What is a variable?
A) A constant value
B) A storage location
C) A function
D) A class

Page 6: Answer Key
──────────────────
1. B
2. B
```

### **Step 2: Verify Question Numbering**

The parser supports these formats:

✅ **Numbered Format:**
```
1. Question text
2. Question text
```

✅ **Q Format:**
```
Q1: Question text
Q2: Question text
```

✅ **Question Word Format:**
```
Question 1: Question text
Question 2: Question text
```

❌ **NOT Supported:**
```
Question 1 Question text (missing colon/period)
1 Question text (missing period)
(1) Question text (parenthesis instead of period)
```

### **Step 3: Verify Option Formatting**

Options must be marked clearly:

✅ **Supported Formats:**
```
A) Option text
B) Option text
C) Option text
D) Option text
```

OR

```
A. Option text
B. Option text
C. Option text
D. Option text
```

❌ **NOT Supported:**
```
A Option text (missing ) or .)
(A) Option text (parenthesis)
A: Option text (colon)
Option A: text (reversed format)
```

### **Step 4: Verify Answer Key Format**

Answer key must be on the last page (or specified page):

✅ **Supported Formats:**
```
1. A
2. B
3. C
```

OR

```
Q1: A
Q2: B
Q3: C
```

OR

```
Answer 1: A
Answer 2: B
Answer 3: C
```

OR

```
1) A
2) B
3) C
```

OR

```
1 A
2 B
3 C
```

❌ **NOT Supported:**
```
1 A (with extra spaces)
Answer: A (without question number)
A (without question number)
```

---

## 🐛 Common Issues & Solutions

### **Issue 1: Questions Not Detected**

**Symptom:** "No questions found in PDF"

**Causes:**
- Questions don't start with a number
- Questions use unsupported format
- PDF is a scanned image (not text-based)

**Solution:**
1. Check question numbering format
2. Ensure questions start with "1.", "Q1:", or "Question 1:"
3. If PDF is scanned, use OCR tool first

### **Issue 2: Options Not Extracted**

**Symptom:** Questions found but options missing

**Causes:**
- Options not marked as A), B), C), D)
- Options on separate lines from question
- Extra spaces or formatting issues

**Solution:**
1. Ensure options are marked A), B), C), D)
2. Options should be on separate lines
3. Remove extra spaces before options

### **Issue 3: Answer Key Not Found**

**Symptom:** "No answer key found in PDF"

**Causes:**
- Answer key on wrong page
- Answer key format not recognized
- Answer key mixed with questions

**Solution:**
1. Ensure answer key is on last page
2. Use supported answer format (1. A, Q1: B, etc.)
3. Separate answer key from questions

### **Issue 4: Partial Extraction**

**Symptom:** Some questions extracted, some missing

**Causes:**
- Inconsistent numbering format
- Some questions missing options
- Multi-line questions not handled

**Solution:**
1. Use consistent numbering throughout
2. Ensure all questions have 4 options
3. Keep questions on single line if possible

---

## 🔍 Advanced Debugging

### **Method 1: Check Console Output**

When parsing, the console shows debug information:

```
[DEBUG] Starting MCQ PDF parsing: sample.pdf
[DEBUG] Successfully extracted 6 pages
[DEBUG] Found question 1: What is Python?...
[DEBUG]   Option A: A snake...
[DEBUG]   Option B: A programming language...
[DEBUG]   Option C: A framework...
[DEBUG]   Option D: A database...
[DEBUG] Found 50 questions
[DEBUG] Found 50 answers in answer key
[DEBUG] Matched 50 questions with answers
```

### **Method 2: Use Debug Endpoint**

Create a test script to analyze your PDF:

```python
from mcq_parser import debug_pdf_content

# Analyze your PDF
analysis = debug_pdf_content('your_pdf.pdf')

# Check results
print(f"Total pages: {analysis['total_pages']}")
for page in analysis['pages']:
    print(f"Page {page['page_num']}:")
    print(f"  Question patterns: {page['question_patterns']}")
    print(f"  Options found: {page['option_count']}")
    print(f"  Answer patterns: {page['answer_patterns']}")
```

### **Method 3: Manual PDF Inspection**

1. Open PDF in text editor
2. Copy first page content
3. Check for:
   - Question numbering format
   - Option formatting
   - Special characters or encoding issues

---

## ✅ Verification Checklist

Before uploading, verify:

- [ ] Questions are numbered (1., Q1:, Question 1:, etc.)
- [ ] Each question has exactly 4 options
- [ ] Options are marked A), B), C), D)
- [ ] Answer key is on last page or specified page
- [ ] Answer key uses supported format
- [ ] PDF is not password-protected
- [ ] PDF has readable text (not scanned image)
- [ ] No extra spaces or special characters
- [ ] Consistent formatting throughout

---

## 📋 PDF Preparation Checklist

### **Before Uploading:**

1. **Extract from Word/Google Docs:**
   - Export as PDF
   - Ensure text is selectable
   - Check formatting is preserved

2. **If from Scanned Document:**
   - Use OCR tool (Adobe, Google Docs, etc.)
   - Verify text extraction quality
   - Fix any OCR errors

3. **Format Verification:**
   - Open PDF in text editor
   - Check question numbering
   - Check option formatting
   - Check answer key format

4. **Test with Sample:**
   - Create small test PDF (5 questions)
   - Upload and test parser
   - Fix any issues
   - Then upload full PDF

---

## 🚀 Quick Fix Steps

### **If Parser Fails:**

1. **Check question format:**
   ```
   ✓ Change "Question 1 What is..." to "1. What is..."
   ✓ Change "A Option text" to "A) Option text"
   ```

2. **Check answer key:**
   ```
   ✓ Change "Answer: A" to "1. A"
   ✓ Change "1-A" to "1. A"
   ```

3. **Verify PDF:**
   ```
   ✓ Open in text editor
   ✓ Copy-paste content
   ✓ Check for special characters
   ```

4. **Test with sample:**
   ```
   ✓ Create 5-question test PDF
   ✓ Upload and test
   ✓ Fix issues
   ✓ Upload full PDF
   ```

---

## 📞 Getting Help

### **If Still Having Issues:**

1. **Check console output** for debug messages
2. **Review this guide** for common issues
3. **Verify PDF format** matches examples
4. **Test with sample PDF** from documentation
5. **Check PDF is readable** (not scanned image)

---

## 💡 Pro Tips

1. **Start small** - Test with 5-question PDF first
2. **Use consistent format** - Same numbering throughout
3. **Keep it simple** - Avoid complex formatting
4. **Verify answer key** - Ensure all questions have answers
5. **Check PDF quality** - Ensure text is extractable

---

## 🎯 Expected Results

### **Successful Parse:**
```
✅ Successfully extracted 50 questions from the PDF
📊 Parsing Summary
   Total Questions: 50
   Total Pages: 6
   Answer Key Page: 6
   Questions with Answers: 50
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

**Need more help? Check the full documentation in MCQ_PARSER_FEATURE.md**
