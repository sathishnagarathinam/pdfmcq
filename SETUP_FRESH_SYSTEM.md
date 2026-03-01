# 🚀 Running PDF MCQ Generator on a Fresh System (Without VS Code)

## ✅ Quick Answer to Your Questions

1. **Can it run without IDE?** ✅ YES - Completely IDE-independent
2. **Just Python + Terminal?** ✅ YES - No special tools needed
3. **Cross-platform?** ✅ YES - Windows, macOS, Linux all supported
4. **IDE-specific dependencies?** ✅ NO - Zero VS Code dependencies

---

## 📋 Minimum System Requirements

### Python Version
- **Python 3.8+** (Recommended: 3.10 or 3.11)
- Check: `python --version` or `python3 --version`

### Operating Systems
- ✅ Windows 10/11
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu, Debian, CentOS, etc.)

### Disk Space
- ~500MB for Python + dependencies
- ~100MB for project files
- ~1GB for optional offline models (if using offline generation)

### Internet Connection
- Required for: API keys (OpenAI, OpenRouter, DeepSeek)
- Optional for: Offline generation mode

---

## 🔧 Step-by-Step Setup Instructions

### Step 1: Install Python (if not already installed)

**Windows:**
```bash
# Download from https://www.python.org/downloads/
# Run installer, CHECK "Add Python to PATH"
# Verify installation:
python --version
```

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from https://www.python.org/downloads/
# Verify:
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

---

### Step 2: Clone/Download Project

```bash
# Option A: Clone from GitHub (if available)
git clone <your-repo-url>
cd pdfmcq

# Option B: Download ZIP and extract
# Then navigate to the folder:
cd pdfmcq
```

---

### Step 3: Create Virtual Environment (Recommended)

**Why?** Isolates project dependencies from system Python

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in terminal after activation.

---

### Step 4: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Expected output:** Shows packages being installed (Flask, PyPDF2, pandas, etc.)

---

### Step 5: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your API keys
# Windows: notepad .env
# macOS/Linux: nano .env
```

**Minimum required for online generation:**
```
OPENAI_API_KEY=your_key_here
# OR
OPENROUTER_API_KEY=your_key_here
# OR
DEEPSEEK_API_KEY=your_key_here
```

**For offline mode (no API keys needed):**
```
ENABLE_OFFLINE_GENERATION=True
```

---

## 🎯 Running the Application

### Option A: Flask Web App (Recommended)

```bash
# Activate virtual environment first (if not already)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run Flask app
python flask_app.py

# Output should show:
# * Running on http://127.0.0.1:5000
# * Open browser to http://localhost:5000
```

**Access:** Open browser → `http://localhost:5000`

---

### Option B: Streamlit App

```bash
# Activate virtual environment first

# Run Streamlit app
streamlit run app.py

# Output should show:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
```

**Access:** Open browser → `http://localhost:8501`

---

### Option C: Command Line (Python Script)

```bash
# Activate virtual environment

# Run a demo
python demo_mcq_generation.py

# Or use as Python module
python -c "from mcq_generator import extract_text_from_pdf; print(extract_text_from_pdf('your_file.pdf'))"
```

---

## 🔌 API Key Setup (For Online Generation)

### Get Free API Keys

**OpenRouter (Recommended - Cheapest):**
1. Visit https://openrouter.ai
2. Sign up free
3. Copy API key to `.env`

**OpenAI:**
1. Visit https://platform.openai.com/api-keys
2. Create API key
3. Copy to `.env`

**DeepSeek:**
1. Visit https://platform.deepseek.com
2. Create API key
3. Copy to `.env`

---

## 📦 Optional: Offline Generation (No API Keys)

```bash
# Install offline models (one-time setup)
python setup_offline.py

# Then set in .env:
ENABLE_OFFLINE_GENERATION=True

# Run app normally - it will use offline models
python flask_app.py
```

---

## 🐛 Troubleshooting

### "Python not found"
```bash
# Windows: Use python
python --version

# macOS/Linux: Use python3
python3 --version
```

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Use different port
python flask_app.py --port 8000
# Then visit http://localhost:8000
```

### "API key not working"
- Check `.env` file exists in project root
- Verify API key is correct (no extra spaces)
- Restart the app after changing `.env`

---

## 📁 Project Structure

```
pdfmcq/
├── flask_app.py          # Main Flask web app
├── app.py                # Streamlit app
├── mcq_generator.py      # Core MCQ generation logic
├── mcq_parser.py         # Parse existing MCQ PDFs
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual API keys (create this)
├── templates/            # HTML templates for Flask
├── uploads/              # Uploaded PDFs (auto-created)
└── models/               # Offline models (if using offline mode)
```

---

## ✨ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with API keys (or offline mode enabled)
- [ ] Flask app runs without errors
- [ ] Can upload PDF and generate MCQs
- [ ] Can export results to CSV/PDF

---

## 🎓 Next Steps

1. **Test with sample PDF:** Use any PDF with text content
2. **Explore features:** Try different generation methods
3. **Customize:** Edit `.env` for your preferences
4. **Deploy:** Use Vercel, Heroku, or your own server

---

## 📞 Common Commands Reference

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python flask_app.py

# Run Streamlit app
streamlit run app.py

# Check installed packages
pip list

# Upgrade pip
pip install --upgrade pip
```

---

**That's it! Your project is now ready to run on any system with Python.** 🎉

