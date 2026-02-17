# 📋 MCQ Parser Feature - Parse Existing MCQ PDFs

## 🎯 Overview

The MCQ Parser is a new feature that allows you to **extract questions and answers from existing MCQ PDFs** instead of generating new questions from content.

**Perfect for:**
- Converting exam papers to digital format
- Extracting questions from sample papers
- Building question banks from existing MCQ documents
- Digitizing printed exam materials

---

## ✨ Features

### **1. Automatic Question Extraction**
- ✅ Detects various question numbering formats
- ✅ Extracts question text and options (A, B, C, D)
- ✅ Handles different formatting styles

### **2. Answer Key Parsing**
- ✅ Extracts answers from the answer key page
- ✅ Supports multiple answer key formats
- ✅ Maps answers to corresponding questions

### **3. Format Support**
Handles these question numbering patterns:
- `1. Question text` (numbered)
- `Q1: Question text` (Q format)
- `Question 1: Question text` (word format)

Handles these answer key formats:
- `1. A` (numbered with period)
- `Q1: B` (Q format)
- `Answer 1: C` (answer word)
- `1) D` (numbered with parenthesis)
- `1 A` (space separated)

### **4. CSV Export**
- ✅ Export extracted questions to CSV
- ✅ Same format as generated questions
- ✅ Ready for import into other systems

---

## 🚀 How to Use

### **Step 1: Select Parse Mode**
On the main page, select the radio button:
```
📋 Parse Existing MCQ PDF
```

### **Step 2: Upload Your PDF**
Click "Choose File" and select your MCQ PDF

### **Step 3: Configure Answer Key Page**
- **Default (-1):** Uses the last page as answer key
- **Custom number:** Enter the page number (1-indexed)
  - Example: If answer key is on page 6, enter `6`

### **Step 4: Parse**
Click "Parse MCQ PDF" button

### **Step 5: Review & Export**
- Review extracted questions
- Download as CSV for further use

---

## 📄 PDF Structure Requirements

### **Recommended Structure:**

```
Pages 1-5: Questions
├─ Question 1
│  A) Option A
│  B) Option B
│  C) Option C
│  D) Option D
├─ Question 2
│  A) Option A
│  B) Option B
│  C) Option C
│  D) Option D
└─ ... more questions

Page 6: Answer Key
├─ 1. B
├─ 2. C
├─ 3. A
└─ ... more answers
```

### **Key Requirements:**
1. ✅ Questions must have clear numbering (1, 2, 3, etc.)
2. ✅ Each question must have exactly 4 options (A, B, C, D)
3. ✅ Options must be clearly marked (A), B), C), D))
4. ✅ Answer key must be on a separate page
5. ✅ Answer key must have clear question-answer mapping

---

## 📊 Output Format

### **CSV Columns:**
```
question,option1,option2,option3,option4,correct,difficulty,explanation
"What is Python?","A snake","A programming language","A framework","A database",2,"Medium",""
"What is a variable?","A constant value","A storage location","A function","A class",2,"Medium",""
```

### **Correct Answer Format:**
- `1` = Option A
- `2` = Option B
- `3` = Option C
- `4` = Option D

---

## 🔧 Technical Details

### **Files Involved:**

1. **mcq_parser.py** (New)
   - `extract_pages_from_pdf()` - Extract text from each page
   - `detect_question_pattern()` - Detect numbering format
   - `parse_questions_from_pages()` - Extract questions and options
   - `parse_answer_key()` - Extract answer key
   - `match_questions_with_answers()` - Match Q&A
   - `parse_mcq_pdf()` - Main function

2. **flask_app.py** (Updated)
   - `/parse-mcq` - New route for parsing MCQ PDFs
   - Imports `parse_mcq_pdf` from mcq_parser

3. **templates/index.html** (Updated)
   - Mode selector (Generate vs Parse)
   - Parse mode form fields
   - `switchMode()` function
   - `displayParseSummary()` function
   - Updated form submission handler

---

## 📈 Parsing Summary

After parsing, you'll see:

```
📊 Parsing Summary

Total Questions Extracted: 50
Total Pages: 6
Answer Key Page: 6
Questions with Answers: 50
```

---

## ⚠️ Limitations & Tips

### **Limitations:**
- ❌ Difficulty level is set to "Medium" (not extracted)
- ❌ Explanations are empty (not in original PDF)
- ❌ Requires clear, structured PDF format
- ❌ May struggle with complex layouts

### **Tips for Best Results:**
1. ✅ Use PDFs with clear text (not scanned images)
2. ✅ Ensure consistent question numbering
3. ✅ Keep answer key on a separate page
4. ✅ Use standard option formatting (A), B), C), D))
5. ✅ Avoid multi-column layouts
6. ✅ Test with a small PDF first

---

## 🧪 Example Workflow

### **Input PDF:**
```
Page 1-2: Questions
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

Page 3: Answer Key
1. B
2. B
```

### **Output CSV:**
```
question,option1,option2,option3,option4,correct,difficulty,explanation
"What is Python?","A snake","A programming language","A framework","A database",2,"Medium",""
"What is a variable?","A constant value","A storage location","A function","A class",2,"Medium",""
```

---

## 🎯 Use Cases

1. **Exam Digitization**
   - Convert printed exam papers to digital format
   - Build digital question banks

2. **Question Bank Building**
   - Extract questions from multiple PDFs
   - Combine into single database

3. **Format Conversion**
   - Convert PDF MCQs to CSV
   - Import into learning management systems

4. **Quality Assurance**
   - Verify question extraction accuracy
   - Check answer key mapping

---

## 🔄 Workflow Comparison

### **Generate Mode:**
```
PDF Content → AI Analysis → Generate New Questions → CSV/PDF Export
```

### **Parse Mode:**
```
PDF Questions → Extract Questions & Answers → CSV/PDF Export
```

---

## 📞 Troubleshooting

### **Issue: No questions extracted**
- ✅ Check PDF has clear question numbering
- ✅ Verify questions are on separate pages from answer key
- ✅ Ensure options are marked A), B), C), D)

### **Issue: Answers not matched**
- ✅ Check answer key format matches supported formats
- ✅ Verify answer key page number is correct
- ✅ Ensure question numbers in answer key match question numbers

### **Issue: Incorrect option extraction**
- ✅ Check options are clearly marked
- ✅ Avoid multi-column layouts
- ✅ Use standard formatting

---

## 🚀 Future Enhancements

Potential improvements:
- 🔄 Support for image-based PDFs (OCR)
- 🔄 Automatic difficulty detection
- 🔄 Multi-column layout support
- 🔄 Batch processing multiple PDFs
- 🔄 Answer explanation extraction
- 🔄 Question category detection

---

**The MCQ Parser is now ready to use!** 🎉
