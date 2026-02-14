# 📋 MCQ Generation Guidelines

## 🎯 **Strict Guidelines Implemented**

The MCQ Generator now follows **strict guidelines** optimized for government rules, regulations, and policy documents (like LTC rules, service rules, etc.).

---

## ✅ **1. Coverage Rules**

### **Even Distribution:**
- ✅ Cover **ALL major rules and notes evenly**
- ❌ **DO NOT** over-emphasize a single rule
- ✅ Distribute questions across different topics
- ✅ Ensure balanced coverage of the entire document

### **Example:**
If a PDF has 10 major rules, questions should be distributed across all 10 rules, not concentrated on just 2-3 rules.

---

## 🎯 **2. High Priority Topics (Maximum Weightage)**

The AI will give **maximum weightage** to these topics:

### **Priority 1: Applicability and Exclusions**
- Who is eligible/not eligible
- Which cases are covered/not covered
- Conditions for applicability
- Exception cases

**Example Questions:**
- "Which of the following is NOT eligible for LTC?"
- "Under which condition is LTC NOT admissible?"

### **Priority 2: Definitions and Key Terms**
- Official definitions from the document
- Technical terms and their meanings
- Abbreviations and full forms

**Example Questions:**
- "What is the definition of 'family' under LTC rules?"
- "What does 'home town' mean in the context of LTC?"

### **Priority 3: Public Interest vs Own Request**
- Differences between public interest and own request cases
- Entitlements in each case
- Conditions and restrictions

**Example Questions:**
- "What is the difference between transfer on own request vs public interest?"
- "Which allowance is NOT admissible for transfer on own request?"

### **Priority 4: Numerical/Table-Based Provisions**
- Distance slabs (e.g., 0-500 km, 500-1000 km)
- Limits and ceilings (e.g., maximum amount, maximum days)
- Rates and percentages
- Time periods and deadlines

**Example Questions:**
- "What is the distance slab for LTC entitlement to hill stations?"
- "What is the maximum number of days allowed for LTC?"

### **Priority 5: Pay, Allowances, and Entitlements**
- Salary components
- Allowance rates
- Entitlement conditions
- Calculation methods

**Example Questions:**
- "What percentage of basic pay is admissible as DA?"
- "Which allowance is NOT included in retirement benefits?"

### **Priority 6: Amendments and Latest Notifications**
- Amendment years
- Notification numbers
- Changes from previous rules
- Effective dates

**Example Questions:**
- "In which year was the LTC rule amended to include domestic help?"
- "What is the notification number for the latest LTC amendment?"

---

## 📝 **3. Question Types (MUST Include)**

### **Exception-Based Questions:**
Questions that test knowledge of exceptions and exclusions.

**Examples:**
- "Which of the following is **NOT** admissible under LTC?"
- "Which case is **NOT** covered by the transfer policy?"
- "Which employee is **NOT** eligible for this benefit?"

### **Negative Framing Questions:**
Questions with negative keywords to test careful reading.

**Examples:**
- "Which statement is **NOT** correct?"
- "Which provision does **NOT** apply to temporary employees?"
- "Which allowance is **NOT** included in gross salary?"

### **Rule Number-Based Questions:**
Questions that reference specific rule numbers.

**Examples:**
- "According to Rule 5.3, what is the entitlement for...?"
- "Under which rule is the definition of 'family' provided?"
- "Rule 7.2 deals with which aspect of LTC?"

### **Distance Slabs/Limits/Ceilings Questions:**
Questions about numerical provisions.

**Examples:**
- "What is the distance limit for LTC to hometown?"
- "What is the maximum ceiling for hotel accommodation?"
- "For distances between 500-1000 km, what is the entitlement?"

### **Special Provisions and Notes:**
Questions about special cases and footnotes.

**Examples:**
- "According to Note 1 under Rule 5, what is the special provision for...?"
- "What is the special case mentioned for employees in remote areas?"

### **Amendment Years and Notification Numbers:**
Questions about document history.

**Examples:**
- "In which year was this rule last amended?"
- "What is the notification number of the 2023 amendment?"

---

## 📊 **4. Difficulty Distribution (STRICT)**

The AI **MUST** follow this exact distribution:

### **40% Easy (Direct Rule-Based Facts)**
Simple, straightforward questions testing basic knowledge.

**Characteristics:**
- Direct facts from the text
- No complex conditions
- Single-step reasoning

**Example:**
```
Q: What is the full form of LTC?
A) Leave Travel Concession
B) Long Term Contract
C) Local Travel Claim
D) Leave Transfer Certificate
Correct: A
Difficulty: easy
```

### **40% Moderate (Rule + Condition Combination)**
Questions combining multiple concepts or conditions.

**Characteristics:**
- Requires understanding of 2-3 related concepts
- Involves conditions or qualifications
- Multi-step reasoning

**Example:**
```
Q: An employee in Grade A wants to travel to a hill station 800 km away. 
   What is the applicable entitlement?
A) Economy class air fare
B) AC First Class rail fare
C) AC Two Tier rail fare
D) Not admissible
Correct: C
Difficulty: medium
```

### **20% Tricky (Exceptions, Notes, Negative Framing)**
Challenging questions testing deep understanding.

**Characteristics:**
- Exception cases
- Negative framing
- Subtle distinctions
- Notes and special provisions

**Example:**
```
Q: Which of the following is NOT a valid reason for denying LTC?
A) Employee has not completed 1 year of service
B) Employee is on probation
C) Employee's spouse is a government employee
D) Employee has already availed LTC in the same block year
Correct: C
Difficulty: hard
```

---

## 🎨 **5. Format Requirements**

Every question must have:
- ✅ Clear question text
- ✅ Exactly 4 options (A, B, C, D)
- ✅ Correct answer letter (A/B/C/D)
- ✅ Difficulty level (easy/medium/hard)
- ✅ Brief explanation for the correct answer

---

## 📥 **6. CSV Download Changes**

As per user request:
- ❌ **Removed:** `pages` column
- ❌ **Removed:** `sections` column
- ✅ **Kept:** question, option1-4, correct, difficulty, explanation

**Note:** Page and section metadata is still visible in the web interface and PDF download, just not in CSV.

---

## 🧪 **Example Question Set (10 Questions)**

For a 10-question set, the distribution would be:

```
Questions 1-4: Easy (40%)
├─ Q1: Definition question
├─ Q2: Direct rule fact
├─ Q3: Simple numerical limit
└─ Q4: Basic eligibility

Questions 5-8: Moderate (40%)
├─ Q5: Rule + condition combination
├─ Q6: Distance slab with grade
├─ Q7: Allowance calculation
└─ Q8: Public interest vs own request

Questions 9-10: Tricky (20%)
├─ Q9: Exception-based (NOT admissible)
└─ Q10: Negative framing with note reference
```

---

## ✅ **Benefits of These Guidelines**

1. **Comprehensive Coverage:** All important topics are covered evenly
2. **Practical Focus:** Emphasis on real-world applicability
3. **Exception Awareness:** Tests understanding of edge cases
4. **Balanced Difficulty:** Suitable for learners at all levels
5. **Rule-Specific:** Optimized for government documents
6. **Amendment Tracking:** Ensures up-to-date knowledge

---

## 🚀 **How to Use**

1. **Upload your PDF** (government rules, regulations, policy documents)
2. **Select number of questions** (e.g., 10, 20, 50)
3. **Choose a model** (e.g., Qwen 2.5 Coder 32B Free)
4. **Click "Generate Questions"**
5. **Review the questions** - they will automatically follow these guidelines!

The AI will automatically:
- ✅ Distribute questions evenly across topics
- ✅ Focus on high-priority areas
- ✅ Include exception-based questions
- ✅ Follow the 40-40-20 difficulty split
- ✅ Cover numerical provisions and amendments

---

## 📊 **Quality Indicators**

A good question set should have:
- ✅ Questions from different sections of the document
- ✅ Mix of positive and negative framing
- ✅ At least 2-3 numerical/table-based questions
- ✅ At least 2-3 exception-based questions
- ✅ Even distribution across easy/medium/hard
- ✅ References to specific rules and notes

---

## 🎯 **Perfect for:**

- ✅ LTC (Leave Travel Concession) Rules
- ✅ Service Rules and Regulations
- ✅ Transfer Policies
- ✅ Allowance Guidelines
- ✅ Government Orders and Notifications
- ✅ Policy Documents
- ✅ Administrative Manuals
- ✅ Financial Rules

---

**These guidelines are now active and will be applied to all MCQ generation!** 🎉
