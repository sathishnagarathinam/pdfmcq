# 📊 Question Metadata Tracking Guide

## 🎯 **Overview**

The MCQ Generator now includes **detailed page and section tracking** for every generated question! This feature helps you understand:

- **Which pages** each question was generated from
- **Which sections/headings** each question relates to
- **Question distribution** across your PDF
- **Coverage analysis** showing which parts of the document were used

---

## ✨ **New Features**

### **1. Page-by-Page Tracking**
Every question now includes metadata showing which page(s) it was generated from:
```
Question 1: Generated from Page 3
Question 2: Generated from Pages 5, 6
Question 3: Generated from Page 7
```

### **2. Section/Heading Attribution**
Questions are linked to detected sections and headings:
```
Question 1: Section "Introduction to Python"
Question 2: Section "2.1 Data Types and Variables"
Question 3: Chapter 3 "Control Flow Statements"
```

### **3. Distribution Summary**
After generation, you'll see a comprehensive summary:
- **Overview**: Total questions, pages, sections, coverage percentage
- **Questions per Page**: Visual breakdown of how many questions from each page
- **Questions per Section**: Distribution across detected sections
- **Pages Without Questions**: Identifies gaps in coverage

### **4. Visual Metadata Display**
Each question shows its source with color-coded badges:
- 🟠 **Orange badges** for page numbers
- 🟠 **Orange badges** for section names

---

## 🔍 **How It Works**

### **Step 1: PDF Analysis**
When you upload a PDF, the system:
1. Extracts text from each page separately
2. Detects headings and sections using pattern matching
3. Tracks character positions for each page

### **Step 2: Section Detection**
The system automatically detects:
- **Chapters**: "Chapter 1", "Ch. 2", "CHAPTER III"
- **Sections**: "Section 1.2", "Sec. 3.4"
- **Numbered headings**: "1.2.3 Introduction"
- **All-caps headings**: "INTRODUCTION", "METHODOLOGY"
- **Title case headings**: "Getting Started", "Advanced Topics"

### **Step 3: Question Matching**
For each generated question:
1. Extracts key terms from the question text
2. Searches for these terms across all pages
3. Identifies the best matching page(s)
4. Links to sections found on those pages

### **Step 4: Summary Generation**
Creates detailed statistics:
- Questions per page distribution
- Questions per section distribution
- Coverage percentage
- Gaps in coverage

---

## 📱 **Using the Feature**

### **In the Web Interface:**

1. **Upload your PDF** as usual
2. **Configure settings** (model, difficulty, etc.)
3. **Click "Generate Questions"**
4. **View the Summary** (appears before questions):
   - 📈 Overview statistics
   - 📄 Questions per page breakdown
   - 📚 Questions per section breakdown
   - ⚠️ Pages without questions

5. **View Individual Questions** with metadata:
   - Each question shows source pages and sections
   - Color-coded badges for easy identification

### **In Downloaded Files:**

**CSV Export** includes two new columns:
- `pages`: Comma-separated list of page numbers
- `sections`: Comma-separated list of section names

**PDF Export** includes metadata line for each question:
- "Source: Page(s) 3, 5 | Introduction to Python"

---

## 📊 **Example Output**

### **Summary Display:**
```
📈 Overview
Total Questions: 10
Total Pages: 25
Sections Detected: 8
Coverage: 40.0% of pages (10/25 pages)

📄 Questions per Page
Page 1: 2 questions
Page 3: 1 question
Page 5: 3 questions
Page 7: 2 questions
Page 10: 2 questions

📚 Questions per Section
Introduction to Python: 3 questions
Data Types and Variables: 2 questions
Control Flow Statements: 2 questions
Functions and Modules: 3 questions

⚠️ Pages Without Questions
2, 4, 6, 8, 9, 11-25
```

### **Question Display:**
```
Question 1: What is a variable in Python?
📍 Source: Page: 3 | 2.1 Data Types and Variables

A) A container for storing data
B) A function
C) A loop
D) A class

Correct Answer: A
Difficulty: Easy
Explanation: Variables are containers for storing data values...
```

---

## 🎯 **Benefits**

### **1. Quality Assurance**
- Verify questions cover all important sections
- Identify over-represented or under-represented topics
- Ensure balanced distribution across the document

### **2. Content Analysis**
- Understand which parts of the PDF the AI focused on
- Identify sections that may need more questions
- Track coverage gaps

### **3. Educational Value**
- Students can see which pages to review for each question
- Teachers can verify alignment with curriculum sections
- Easy reference back to source material

### **4. Debugging**
- Identify if certain pages are being ignored
- Verify section detection is working correctly
- Understand AI's content selection process

---

## 🔧 **Technical Details**

### **Section Detection Patterns:**
- Chapter patterns: `Chapter 1`, `Ch. 2`, `CHAPTER III`
- Section patterns: `Section 1.2`, `Sec. 3.4`
- Numbered sections: `1.2.3 Introduction`
- All-caps headings: `INTRODUCTION` (3-50 characters)
- Title case: `Getting Started with Python`

### **Matching Algorithm:**
1. Extract 4+ letter words from question
2. Count occurrences in each page
3. Select page(s) with highest match count
4. Include sections from matched pages

### **Coverage Calculation:**
```
Coverage % = (Pages with Questions / Total Pages) × 100
```

---

## 💡 **Tips for Best Results**

1. **Well-Structured PDFs**: PDFs with clear headings produce better section detection
2. **Text-Based PDFs**: Scanned PDFs may need OCR for accurate tracking
3. **Consistent Formatting**: Documents with consistent heading styles work best
4. **Review Summary**: Check the summary to ensure good coverage
5. **Adjust Question Count**: Generate more questions for better coverage

---

## 🚀 **Future Enhancements**

Potential improvements:
- Manual section editing
- Custom section detection patterns
- Export summary as separate report
- Visual coverage heatmap
- Question rebalancing suggestions

---

## ✅ **Compatibility**

- Works with all AI models (OpenRouter, OpenAI, DeepSeek, etc.)
- Compatible with OCR-processed PDFs
- Supports all difficulty levels
- Works with chunked large documents

The metadata tracking is automatic and requires no additional configuration! 🎉
