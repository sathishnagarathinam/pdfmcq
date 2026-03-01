# ⚡ Quick Start: Terminal-Only Setup (5 Minutes)

## Copy-Paste Commands for Each OS

### 🪟 Windows (Command Prompt)

```bash
# 1. Navigate to project
cd C:\path\to\pdfmcq

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env

# 6. Edit .env (add your API key)
notepad .env

# 7. Run Flask app
python flask_app.py

# 8. Open browser to http://localhost:5000
```

---

### 🍎 macOS (Terminal)

```bash
# 1. Navigate to project
cd ~/Downloads/pdfmcq

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Edit .env (add your API key)
nano .env
# Press Ctrl+X, then Y, then Enter to save

# 7. Run Flask app
python flask_app.py

# 8. Open browser to http://localhost:5000
```

---

### 🐧 Linux (Terminal)

```bash
# 1. Navigate to project
cd ~/pdfmcq

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Edit .env (add your API key)
nano .env
# Press Ctrl+X, then Y, then Enter to save

# 7. Run Flask app
python flask_app.py

# 8. Open browser to http://localhost:5000
```

---

## 🔑 Getting an API Key (2 Minutes)

### Easiest Option: OpenRouter (Free Tier)

1. Go to https://openrouter.ai
2. Click "Sign Up" (free)
3. Copy your API key
4. In `.env` file, add:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
5. Save and restart app

---

## 🎯 What Each Command Does

| Command | Purpose |
|---------|---------|
| `cd ...` | Navigate to project folder |
| `python -m venv venv` | Create isolated Python environment |
| `activate` / `source venv/bin/activate` | Enable virtual environment |
| `pip install -r requirements.txt` | Install all dependencies |
| `copy/cp .env.example .env` | Create configuration file |
| `python flask_app.py` | Start the web app |

---

## ✅ Success Indicators

When you run `python flask_app.py`, you should see:

```
 * Serving Flask app 'flask_app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Then open your browser to `http://localhost:5000` and you should see the web interface.

---

## 🚨 Common Issues & Quick Fixes

### "python: command not found"
```bash
# Try python3 instead
python3 --version
python3 -m venv venv
```

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### "Port 5000 already in use"
```bash
# Use different port
python flask_app.py --port 8000
# Then visit http://localhost:8000
```

### "API key not working"
```bash
# 1. Check .env file exists in project root
# 2. Check API key is correct (no extra spaces)
# 3. Restart the app (Ctrl+C, then python flask_app.py)
```

---

## 🎮 Using the App

1. **Upload PDF** - Click "Choose File" and select a PDF
2. **Select Options** - Choose number of questions, difficulty, etc.
3. **Generate** - Click "Generate MCQs"
4. **Download** - Export as CSV or PDF

---

## 🔄 Next Time You Use It

```bash
# Just activate and run (no reinstall needed)
cd pdfmcq
source venv/bin/activate  # or venv\Scripts\activate on Windows
python flask_app.py
```

---

## 📚 Alternative: Streamlit App

If you prefer a different interface:

```bash
# Make sure virtual environment is activated
pip install streamlit

# Run Streamlit app
streamlit run app.py

# Visit http://localhost:8501
```

---

## 🌐 Offline Mode (No API Key Needed)

```bash
# Install offline models (one-time, ~1GB download)
python setup_offline.py

# Edit .env:
ENABLE_OFFLINE_GENERATION=True

# Run normally
python flask_app.py
```

---

## 📦 What Gets Installed

- **Flask** - Web framework
- **PyPDF2** - PDF reading
- **pandas** - Data handling
- **fpdf2** - PDF generation
- **OpenAI/OpenRouter** - API clients
- **python-dotenv** - Environment variables

Total: ~200MB

---

## 🎓 That's It!

Your project is now running completely independently without any IDE. You can:

✅ Run on any computer with Python  
✅ Use just terminal/command prompt  
✅ Works on Windows, macOS, Linux  
✅ No VS Code or IDE needed  
✅ Share with others easily  

---

**Happy MCQ generating!** 🎉

