# 🚀 PDF MCQ Generator - Setup & Deployment Guide

## ⚡ TL;DR (Too Long; Didn't Read)

**Your project runs on ANY computer with Python. No IDE needed.**

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
notepad .env  # Add API key
python flask_app.py

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env  # Add API key
python flask_app.py

# Then open: http://localhost:5000
```

---

## 📚 Complete Documentation

We've created 6 comprehensive guides for you:

### 1. **ANSWERS_TO_YOUR_QUESTIONS.md** ✅
Direct answers to your 5 specific questions with proof and examples.

### 2. **QUICK_START_TERMINAL.md** ⚡
Copy-paste commands for Windows, macOS, and Linux. Get running in 5 minutes.

### 3. **SETUP_FRESH_SYSTEM.md** 📋
Comprehensive step-by-step guide with detailed explanations.

### 4. **ADVANCED_SETUP_GUIDE.md** 🔧
Platform-specific detailed instructions and troubleshooting.

### 5. **TECHNICAL_DETAILS.md** 🔬
Architecture, dependencies, and how it works without IDE.

### 6. **VISUAL_SETUP_GUIDE.md** 📊
Diagrams, flowcharts, and visual explanations.

### 7. **SETUP_GUIDE_INDEX.md** 📚
Navigation guide to help you choose the right guide.

---

## ✅ Your Questions Answered

### Q1: Can it run without IDE?
**✅ YES** - Pure Python, zero IDE dependencies

### Q2: Just Python + terminal?
**✅ YES** - That's all you need

### Q3: Minimum requirements?
**Python 3.8+** - 5-10 minute setup

### Q4: Cross-platform?
**✅ YES** - Windows, macOS, Linux

### Q5: IDE-specific dependencies?
**❌ NO** - Zero IDE dependencies

---

## 🎯 Quick Start (Choose Your Path)

### Path 1: I want to start NOW (5 minutes)
→ Open **QUICK_START_TERMINAL.md**
→ Copy-paste commands for your OS
→ Done!

### Path 2: I want detailed explanations
→ Open **SETUP_FRESH_SYSTEM.md**
→ Follow step-by-step
→ Understand everything

### Path 3: I'm having issues
→ Open **ADVANCED_SETUP_GUIDE.md**
→ Find your issue in troubleshooting
→ Follow the fix

### Path 4: I want to understand the architecture
→ Open **TECHNICAL_DETAILS.md**
→ Learn how it works
→ Understand the design

### Path 5: I want visual guides
→ Open **VISUAL_SETUP_GUIDE.md**
→ See diagrams and flowcharts
→ Follow the visuals

---

## 📋 System Requirements

**Minimum:**
- Python 3.8+
- 500MB disk space
- 2GB RAM
- Terminal/Command Prompt
- Text editor

**Optional:**
- Internet (for API keys)
- Git (for cloning)

**NOT needed:**
- ❌ VS Code
- ❌ PyCharm
- ❌ Any IDE
- ❌ IDE extensions

---

## 🔧 Installation Summary

**Step 1:** Install Python 3.8+
**Step 2:** Download/clone project
**Step 3:** Create virtual environment
**Step 4:** Activate virtual environment
**Step 5:** Install dependencies
**Step 6:** Create .env file
**Step 7:** Add API key
**Step 8:** Run app
**Step 9:** Open browser

**Total time:** 5-10 minutes

---

## 🌐 Running the App

### Flask Web App (Recommended)
```bash
python flask_app.py
# Visit http://localhost:5000
```

### Streamlit App
```bash
streamlit run app.py
# Visit http://localhost:8501
```

### Command Line
```bash
python -c "from mcq_generator import extract_text_from_pdf; ..."
```

---

## 🔑 API Keys

**Get free API keys from:**
- OpenRouter: https://openrouter.ai (recommended)
- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com

**Add to .env:**
```
OPENROUTER_API_KEY=your_key_here
```

**Or use offline mode (no API key needed):**
```
ENABLE_OFFLINE_GENERATION=True
```

---

## 🎓 What You Get

✅ Web interface for PDF upload
✅ MCQ generation from PDFs
✅ Multiple generation methods
✅ Export to CSV/PDF
✅ Offline mode support
✅ API integration
✅ Cross-platform compatibility
✅ No IDE required

---

## 📁 Project Structure

```
pdfmcq/
├── flask_app.py          # Main web app
├── app.py                # Streamlit app
├── mcq_generator.py      # Core logic
├── mcq_parser.py         # PDF parsing
├── requirements.txt      # Dependencies
├── .env.example          # Config template
├── .env                  # Your config (create)
├── templates/            # HTML files
├── uploads/              # Uploaded PDFs
└── models/               # Offline models
```

---

## 🚀 Deployment Options

### Local Machine
```bash
python flask_app.py
```

### Remote Server (SSH)
```bash
ssh user@server.com
cd pdfmcq
source venv/bin/activate
python flask_app.py
```

### Vercel (Serverless)
```bash
vercel deploy
```

### Docker
```bash
docker build -t pdfmcq .
docker run -p 5000:5000 pdfmcq
```

---

## 🐛 Troubleshooting

**"python: command not found"**
→ Use `python3` instead

**"ModuleNotFoundError"**
→ Activate venv + reinstall dependencies

**"Port 5000 already in use"**
→ Use different port: `python flask_app.py --port 8000`

**"API key not working"**
→ Check .env file + restart app

**More issues?**
→ See ADVANCED_SETUP_GUIDE.md

---

## ✨ Key Features

- 🎯 Generate MCQs from PDFs
- 📊 Parse existing MCQ PDFs
- 🔄 Multiple generation methods
- 📥 Export to CSV/PDF
- 🌐 Web interface
- 💻 Command-line interface
- 🔌 API integration
- 📱 Cross-platform
- 🚀 Serverless ready
- 🔐 Secure (API keys in .env)

---

## 📞 Support

1. **Check the guides** - Most answers are there
2. **Read error messages** - They're helpful
3. **Try troubleshooting** - See ADVANCED_SETUP_GUIDE.md
4. **Verify setup** - Follow the checklist

---

## 🎯 Next Steps

1. Choose a guide above
2. Follow the instructions
3. Run the app
4. Upload a PDF
5. Generate MCQs
6. Download results
7. Enjoy! 🎉

---

## 📚 Guide Selection Matrix

| Need | Guide |
|------|-------|
| Quick start | QUICK_START_TERMINAL.md |
| Detailed setup | SETUP_FRESH_SYSTEM.md |
| Troubleshooting | ADVANCED_SETUP_GUIDE.md |
| Architecture | TECHNICAL_DETAILS.md |
| Visual guide | VISUAL_SETUP_GUIDE.md |
| Your Q&A | ANSWERS_TO_YOUR_QUESTIONS.md |
| Navigation | SETUP_GUIDE_INDEX.md |

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file created
- [ ] API key added
- [ ] Flask app runs
- [ ] Browser opens to http://localhost:5000
- [ ] Can upload PDF
- [ ] Can generate MCQs

---

**Your project is completely IDE-independent and ready to run anywhere!** 🚀

**Choose a guide above and get started in 5-10 minutes.** ⚡
