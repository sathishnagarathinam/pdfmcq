# Amendment Feature - Architecture & Data Flow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Flask (templates/index.html)      Streamlit (app.py)           │
│  ├─ Base PDF Upload                ├─ Base PDF Upload           │
│  ├─ Amendment Checkbox             ├─ Amendment Checkbox        │
│  ├─ Amendment PDF Upload           ├─ Amendment PDF Upload      │
│  ├─ Generation Settings            ├─ Generation Settings       │
│  └─ Submit Button                  └─ Generate Button           │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND PROCESSING                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Flask (flask_app.py)              Streamlit (app.py)           │
│  ├─ Extract Base PDF Text          ├─ Extract Base PDF Text     │
│  ├─ Extract Amendment PDF Text     ├─ Extract Amendment Text    │
│  ├─ Create Model Config            ├─ Create Model Config       │
│  ├─ Pass to Generation             ├─ Pass to Generation        │
│  └─ Cleanup Temp Files             └─ Cleanup Temp Files        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  MCQ GENERATION ENGINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  mcq_generator.py                                               │
│  ├─ merge_texts_for_amendment_analysis()                        │
│  │  └─ Merge original + amendment with markers                  │
│  ├─ create_amendment_prompt_section()                           │
│  │  └─ Generate amendment-specific instructions                 │
│  ├─ generate_mcq_questions_advanced()                           │
│  │  ├─ Include amendment prompt section                         │
│  │  ├─ Update system message                                    │
│  │  └─ Send to AI model                                         │
│  └─ AI Model (OpenRouter/OpenAI/DeepSeek)                       │
│     └─ Generate amendment-focused questions                     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    QUESTION OUTPUT                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Questions with:                                                │
│  ├─ Amendment-focused content                                   │
│  ├─ Original/Amendment references                               │
│  ├─ Change descriptions                                         │
│  ├─ Difference explanations                                     │
│  └─ All 7 quality rules applied                                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Input
    ↓
┌─────────────────────────────────────────┐
│ Base PDF + Amendment PDF (Optional)     │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Extract Text from Both PDFs             │
│ - Base PDF → original_text              │
│ - Amendment PDF → amendment_text        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Check Amendment Mode                    │
│ - use_amendment = True/False            │
└─────────────────────────────────────────┘
    ↓
    ├─ If use_amendment = False
    │  └─ Use original_text only
    │
    └─ If use_amendment = True
       ├─ Merge texts:
       │  ├─ === ORIGINAL DOCUMENT ===
       │  ├─ [original_text]
       │  ├─ === AMENDMENT DOCUMENT ===
       │  ├─ [amendment_text]
       │  └─ === ANALYSIS INSTRUCTIONS ===
       │
       └─ Create model_config:
          ├─ use_amendment: True
          ├─ amendment_text: [merged_text]
          └─ [other config]
    ↓
┌─────────────────────────────────────────┐
│ Generate MCQ Questions                  │
│ - Include amendment prompt section      │
│ - Update system message                 │
│ - Send to AI model                      │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ AI Model Response                       │
│ - Amendment-focused questions           │
│ - Original/Amendment references         │
│ - Change descriptions                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Return Questions to User                │
│ - Display in UI                         │
│ - Export to formats                     │
│ - Cleanup temp files                    │
└─────────────────────────────────────────┘
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                             │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────┐         ┌─────────────────┐             │
│  │  Flask HTML UI  │         │  Streamlit UI   │             │
│  │  - Checkbox     │         │  - Checkbox     │             │
│  │  - File Upload  │         │  - File Upload  │             │
│  │  - Settings     │         │  - Settings     │             │
│  └────────┬────────┘         └────────┬────────┘             │
│           │                           │                       │
│           └───────────────┬───────────┘                       │
│                           ↓                                    │
│                  ┌─────────────────┐                          │
│                  │  Form Data      │                          │
│                  │  - Base PDF     │                          │
│                  │  - Amendment    │                          │
│                  │  - Settings     │                          │
│                  └────────┬────────┘                          │
│                           │                                    │
└───────────────────────────┼────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│                   BACKEND LAYER                               │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  File Processing (flask_app.py / app.py)            │    │
│  │  ├─ Extract base PDF text                           │    │
│  │  ├─ Extract amendment PDF text                      │    │
│  │  ├─ Create model_config                             │    │
│  │  └─ Pass to generation                              │    │
│  └──────────────────┬───────────────────────────────────┘    │
│                     ↓                                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  MCQ Generation (mcq_generator.py)                  │    │
│  │  ├─ merge_texts_for_amendment_analysis()            │    │
│  │  ├─ create_amendment_prompt_section()               │    │
│  │  ├─ generate_mcq_questions_advanced()               │    │
│  │  └─ Include amendment instructions                  │    │
│  └──────────────────┬───────────────────────────────────┘    │
│                     ↓                                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  AI Model Integration                               │    │
│  │  ├─ System Message (amendment-aware)                │    │
│  │  ├─ User Prompt (with amendment section)            │    │
│  │  └─ Generate Questions                              │    │
│  └──────────────────┬───────────────────────────────────┘    │
│                     ↓                                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Post-Processing                                    │    │
│  │  ├─ Parse AI response                               │    │
│  │  ├─ Validate questions                              │    │
│  │  ├─ Cleanup temp files                              │    │
│  │  └─ Return to frontend                              │    │
│  └──────────────────┬───────────────────────────────────┘    │
│                     │                                          │
└─────────────────────┼──────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────────────────┐
│                   RESPONSE LAYER                              │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Questions with Amendment Focus                    │    │
│  │  ├─ Question text                                  │    │
│  │  ├─ Options (A, B, C, D)                           │    │
│  │  ├─ Correct answer                                 │    │
│  │  ├─ Explanation with references                    │    │
│  │  │  └─ "Reference: Original Section X /            │    │
│  │  │     Amendment Section Y"                        │    │
│  │  └─ Difficulty level                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

## Key Functions & Their Roles

```
┌─────────────────────────────────────────────────────────────┐
│  merge_texts_for_amendment_analysis()                       │
│  ├─ Input: original_text, amendment_text                   │
│  ├─ Process: Merge with clear markers                      │
│  └─ Output: Combined text for analysis                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  create_amendment_prompt_section()                          │
│  ├─ Input: use_amendment (bool)                            │
│  ├─ Process: Generate amendment instructions               │
│  └─ Output: Prompt section string                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  generate_mcq_questions_advanced()                          │
│  ├─ Input: text, model_config                              │
│  ├─ Process: Include amendment section in prompt           │
│  ├─ Process: Update system message                         │
│  └─ Output: Generated questions                            │
└─────────────────────────────────────────────────────────────┘
```

## Quality Assurance Flow

```
Generated Questions
    ↓
┌─────────────────────────────────────────┐
│ Apply 7 Mandatory Quality Rules         │
├─────────────────────────────────────────┤
│ 1. Single correct answer                │
│ 2. No conditional language              │
│ 3. Verified options                     │
│ 4. Paragraph references                 │
│ 5. Independent verifiability            │
│ 6. Exclusivity guarantee                │
│ 7. Coverage and distribution            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ Apply Amendment-Specific Rules          │
├─────────────────────────────────────────┤
│ - Focus on changes                      │
│ - Specify Original/Amendment            │
│ - Test understanding                    │
│ - Cover all major changes               │
│ - 50% amendment-focused                 │
└─────────────────────────────────────────┘
    ↓
Quality-Assured Questions
```

