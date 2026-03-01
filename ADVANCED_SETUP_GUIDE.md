# 🔧 Advanced Setup & Troubleshooting Guide

## Platform-Specific Detailed Instructions

### Windows Setup (Detailed)

**1. Install Python:**
```bash
# Download from https://www.python.org/downloads/
# Run installer
# ⚠️ IMPORTANT: Check "Add Python to PATH" during installation
# Verify:
python --version
pip --version
```

**2. Navigate to project:**
```bash
cd C:\Users\YourName\Downloads\pdfmcq
# or wherever you extracted the project
```

**3. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate
# You should see (venv) in your terminal
```

**4. Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**5. Create .env file:**
```bash
# Copy example
copy .env.example .env

# Edit with Notepad
notepad .env
```

**6. Run app:**
```bash
python flask_app.py
# Visit http://localhost:5000
```

---

### macOS Setup (Detailed)

**1. Install Python (if needed):**
```bash
# Check if Python 3 is installed
python3 --version

# If not, install via Homebrew
brew install python@3.11

# Or download from https://www.python.org/downloads/
```

**2. Navigate to project:**
```bash
cd ~/Downloads/pdfmcq
# or wherever you extracted it
```

**3. Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
# You should see (venv) in your terminal
```

**4. Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**5. Create .env file:**
```bash
cp .env.example .env
nano .env  # or use your favorite editor
```

**6. Run app:**
```bash
python flask_app.py
# Visit http://localhost:5000
```

---

### Linux Setup (Ubuntu/Debian)

**1. Install Python:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

**2. Navigate to project:**
```bash
cd ~/pdfmcq
```

**3. Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**4. Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**5. Create .env file:**
```bash
cp .env.example .env
nano .env
```

**6. Run app:**
```bash
python flask_app.py
# Visit http://localhost:5000
```

---

## 🔍 Detailed Troubleshooting

### Issue: "python: command not found"

**Windows:**
```bash
# Use python3 instead
python3 --version

# Or reinstall Python with PATH enabled
# Download from https://www.python.org/downloads/
```

**macOS/Linux:**
```bash
# Use python3
python3 --version

# Or create alias
alias python=python3
```

---

### Issue: "pip: command not found"

```bash
# Windows/macOS/Linux
python -m pip --version

# Use this instead of pip:
python -m pip install -r requirements.txt
```

---

### Issue: Virtual environment not activating

**Windows:**
```bash
# Try PowerShell instead of CMD
# In PowerShell:
venv\Scripts\Activate.ps1

# If error about execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Make sure you're in project directory
pwd  # should show pdfmcq directory

# Try:
source venv/bin/activate

# Or:
. venv/bin/activate
```

---

### Issue: "ModuleNotFoundError: No module named 'flask'"

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall all dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
pip list | grep Flask
```

---

### Issue: "Port 5000 already in use"

```bash
# Option 1: Use different port
python flask_app.py --port 8000
# Then visit http://localhost:8000

# Option 2: Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

---

### Issue: API key not working

**Check 1: .env file exists**
```bash
# Windows
dir .env

# macOS/Linux
ls -la .env
```

**Check 2: .env format is correct**
```bash
# Should look like:
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=sk-...

# NOT like:
OPENAI_API_KEY = sk-...  # No spaces!
OPENAI_API_KEY="sk-..."  # No quotes!
```

**Check 3: Restart app after changing .env**
```bash
# Stop current app (Ctrl+C)
# Then restart:
python flask_app.py
```

---

### Issue: "Permission denied" on macOS/Linux

```bash
# Make scripts executable
chmod +x flask_app.py
chmod +x app.py

# Then run
python flask_app.py
```

---

## 🚀 Performance Optimization

### For Faster Startup

```bash
# Install fast models (one-time)
python setup_fast_models.py

# Then set in .env:
DEFAULT_MODEL_PROVIDER=fast
```

---

### For Best Quality

```bash
# Install professional models (one-time)
python setup_enhanced_professional.py

# Then set in .env:
DEFAULT_MODEL_PROVIDER=professional
```

---

### For Offline Mode (No Internet)

```bash
# Install offline models (one-time, ~1GB)
python setup_offline.py

# Then set in .env:
ENABLE_OFFLINE_GENERATION=True
DEFAULT_MODEL_PROVIDER=offline
```

---

## 📊 Verifying Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list

# Check if Flask works
python -c "import flask; print(flask.__version__)"

# Check if PyPDF2 works
python -c "import PyPDF2; print('PyPDF2 OK')"

# Check if pandas works
python -c "import pandas; print(pandas.__version__)"
```

---

## 🔐 Security Notes

1. **Never commit .env file** - It contains API keys
2. **Keep API keys secret** - Don't share them
3. **Use .gitignore** - Already configured to ignore .env
4. **Rotate keys regularly** - If compromised

---

## 📱 Running on Different Machines

**To move project to another computer:**

```bash
# On new computer:
1. Install Python 3.8+
2. Clone/download project
3. Create virtual environment: python -m venv venv
4. Activate: source venv/bin/activate (or venv\Scripts\activate on Windows)
5. Install deps: pip install -r requirements.txt
6. Copy .env file (or create new one with API keys)
7. Run: python flask_app.py
```

**No IDE needed - just Python!**

---

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file created with API keys
- [ ] Flask app starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can upload PDF
- [ ] Can generate MCQs

---

## 📞 Getting Help

If you encounter issues:

1. Check error message carefully
2. Search this guide for the error
3. Try the troubleshooting steps
4. Check Python version: `python --version`
5. Verify virtual environment is activated
6. Reinstall dependencies: `pip install -r requirements.txt`

---

**Your project is completely IDE-independent and runs on any system with Python!** ✅

