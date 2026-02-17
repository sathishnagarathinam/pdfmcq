# 🚀 MCQ Parser - Quick Start Guide

## ⚡ 5-Minute Setup

### **Step 1: Verify Installation** (30 seconds)
The MCQ Parser is already installed! No additional setup needed.

### **Step 2: Start the Application** (30 seconds)
```bash
python flask_app.py
```
Open: http://127.0.0.1:5002

### **Step 3: Select Parse Mode** (10 seconds)
On the main page, select:
```
📋 Parse Existing MCQ PDF
```

### **Step 4: Upload Your PDF** (30 seconds)
- Click "Choose File"
- Select your MCQ PDF
- The form will show parse options

### **Step 5: Configure Answer Key** (30 seconds)
- **Default:** Leave as `-1` (uses last page)
- **Custom:** Enter page number if answer key is elsewhere
  - Example: If answer key is on page 6, enter `6`

### **Step 6: Parse** (10 seconds)
- Click "Parse MCQ PDF"
- Wait for processing

### **Step 7: Review & Export** (2 minutes)
- See extracted questions
- See parsing summary
- Download as CSV or PDF

---

## 📋 PDF Format Checklist

Before uploading, ensure your PDF has:

- ✅ **Clear question numbering**
  - `1. Question text` OR
  - `Q1: Question text` OR
  - `Question 1: Question text`

- ✅ **Exactly 4 options per question**
  - `A) Option A`
  - `B) Option B`
  - `C) Option C`
  - `D) Option D`

- ✅ **Answer key on separate page**
  - Last page (default) OR
  - Specific page number

- ✅ **Answer key format**
  - `1. A` OR
  - `Q1: B` OR
  - `Answer 1: C` OR
  - `1) D` OR
  - `1 A`

---

## 🎯 Example Workflow

### **Your PDF Structure:**
```
Pages 1-3: Questions
├─ 1. What is Python?
│  A) A snake
│  B) A programming language
│  C) A framework
│  D) A database
├─ 2. What is a variable?
│  A) A constant value
│  B) A storage location
│  C) A function
│  D) A class
└─ ... more questions

Page 4: Answer Key
├─ 1. B
├─ 2. B
└─ ... more answers
```

### **What You'll Get:**
```
✅ 2 questions extracted
✅ Both matched with answers
✅ Ready to export as CSV
```

### **CSV Output:**
```
question,option1,option2,option3,option4,correct,difficulty,explanation
"What is Python?","A snake","A programming language","A framework","A database",2,"Medium",""
"What is a variable?","A constant value","A storage location","A function","A class",2,"Medium",""
```

---

## 🔧 Common Scenarios

### **Scenario 1: Answer Key on Last Page (Default)**
```
1. Upload PDF
2. Leave "Answer Key Page" as -1
3. Click "Parse MCQ PDF"
4. Done! ✅
```

### **Scenario 2: Answer Key on Specific Page**
```
1. Upload PDF
2. Enter page number (e.g., 6)
3. Click "Parse MCQ PDF"
4. Done! ✅
```

### **Scenario 3: Multiple PDFs**
```
1. Parse first PDF → Export CSV
2. Parse second PDF → Export CSV
3. Combine CSVs in Excel/Google Sheets
4. Done! ✅
```

---

## ⚠️ Troubleshooting

### **Problem: "No questions found"**
**Solution:**
- ✅ Check question numbering format
- ✅ Ensure questions are on separate pages from answer key
- ✅ Verify options are marked A), B), C), D)

### **Problem: "No answer key found"**
**Solution:**
- ✅ Check answer key page number
- ✅ Verify answer key format (1. A, Q1: B, etc.)
- ✅ Ensure answer key is on a separate page

### **Problem: "Questions without answers"**
**Solution:**
- ✅ Check question numbers match answer key numbers
- ✅ Verify answer key has all questions
- ✅ Check for formatting inconsistencies

### **Problem: "Incorrect options extracted"**
**Solution:**
- ✅ Ensure options are clearly marked
- ✅ Avoid multi-column layouts
- ✅ Use standard formatting (A), B), C), D))

---

## 📊 What Gets Extracted

### **From Questions:**
- ✅ Question number
- ✅ Question text
- ✅ Option A text
- ✅ Option B text
- ✅ Option C text
- ✅ Option D text

### **From Answer Key:**
- ✅ Correct answer (A/B/C/D)

### **Automatically Set:**
- ✅ Difficulty: "Medium" (default)
- ✅ Explanation: "" (empty)

---

## 💾 Export Options

### **CSV Export**
- ✅ Import into Excel/Google Sheets
- ✅ Import into learning management systems
- ✅ Combine multiple PDFs
- ✅ Edit and modify questions

### **PDF Export**
- ✅ Print-friendly format
- ✅ Share with others
- ✅ Archive original format
- ✅ Preserve formatting

---

## 🎓 Use Cases

### **1. Exam Digitization**
```
Printed Exam Paper
    ↓
Upload PDF
    ↓
Parse MCQ PDF
    ↓
Export CSV
    ↓
Digital Question Bank ✅
```

### **2. Question Bank Building**
```
Multiple Sample Papers
    ↓
Parse each PDF
    ↓
Export CSVs
    ↓
Combine in spreadsheet
    ↓
Master Question Bank ✅
```

### **3. Format Conversion**
```
PDF MCQs
    ↓
Parse MCQ PDF
    ↓
Export CSV
    ↓
Import to LMS ✅
```

---

## 🚀 Pro Tips

1. **Test First**
   - Start with a small PDF (5-10 questions)
   - Verify extraction accuracy
   - Then process larger PDFs

2. **Consistent Formatting**
   - Use same numbering format throughout
   - Keep options clearly marked
   - Separate questions from answer key

3. **Batch Processing**
   - Parse multiple PDFs
   - Export each as CSV
   - Combine in spreadsheet

4. **Quality Check**
   - Review extracted questions
   - Verify answer mappings
   - Check for missing questions

5. **Backup Original**
   - Keep original PDF
   - Export CSV as backup
   - Maintain version history

---

## 📞 Need Help?

### **Check Documentation:**
- 📖 MCQ_PARSER_FEATURE.md - Full feature guide
- 🔧 MCQ_PARSER_IMPLEMENTATION.md - Technical details
- 🧪 test_mcq_parser.py - Test examples

### **Common Issues:**
- See "Troubleshooting" section above
- Check PDF format requirements
- Verify answer key page number

---

## ✅ Checklist Before Uploading

- [ ] PDF has clear question numbering
- [ ] Each question has exactly 4 options
- [ ] Options are marked A), B), C), D)
- [ ] Answer key is on a separate page
- [ ] Answer key format is supported
- [ ] Question numbers match answer key numbers
- [ ] PDF is not password-protected
- [ ] PDF has readable text (not scanned image)

---

## 🎉 You're Ready!

1. **Open:** http://127.0.0.1:5002
2. **Select:** 📋 Parse Existing MCQ PDF
3. **Upload:** Your MCQ PDF
4. **Parse:** Click "Parse MCQ PDF"
5. **Export:** Download CSV or PDF

**That's it! Happy parsing!** 🚀
