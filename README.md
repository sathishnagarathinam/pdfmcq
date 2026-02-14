# PDF MCQ Generator-sathish

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/pdf-mcq-generator-sathish)

This application generates multiple-choice questions (MCQs) from PDF documents using AI models. It provides two interfaces:

1. **Streamlit Web App** (`app.py`) - A modern web interface with built-in PDF download
2. **Flask Web App** (`flask_app.py`) - A traditional HTML interface with PDF download functionality

## Features

### Core Functionality
- Upload PDF documents and extract text
- **Multiple generation methods** - Choose from Enhanced Professional, Fast, Online, or Offline
- **Online AI models** - Full access to OpenAI, OpenRouter, DeepSeek, Anthropic (Original method)
- **Manual reference control** - Optional manual input fields for book name and chapter name that appear in explanations
- Download questions in CSV and PDF formats
- Configurable difficulty levels and question counts

### 🎯 NEW: Enhanced Professional MCQ Generation (Truly Professional Quality)
- **Academic-grade questions** - T5-Large model with professional language patterns
- **Multiple question types** - Definition, concept, and application questions
- **Professional scoring** - 85%+ quality scores suitable for academic/certification use
- **Advanced text analysis** - Extracts definitions, relationships, and key concepts
- **Publication-ready** - Appropriate for textbooks, exams, and professional assessments

### 🌐 Online MCQ Generation (Original Method - Always Available)
- **Latest AI models** - Access to GPT-4, Claude, and other cutting-edge models
- **Multiple providers** - OpenAI, OpenRouter, DeepSeek, Anthropic support
- **Flexible model selection** - Choose from basic or advanced models
- **No local storage** - No need to download large models
- **Variable quality** - Quality depends on selected model and provider
- **API key based** - Requires API keys for chosen providers

### 🔒 Offline MCQ Generation
- **No internet required** - Generate questions using local AI models
- **Enhanced estimation** - Advanced analysis to determine maximum possible questions
- **Multiple strategies** - Fact-based, concept-based, and transformer-based question generation
- **Smart fallback** - Automatically falls back to online models if offline fails
- **Maximum extraction** - Optimized algorithms to extract the maximum number of quality questions

### Advanced Features
- Intelligent text analysis and question potential estimation
- Hybrid online/offline generation with seamless switching
- Model caching and configuration management
- Performance optimization for large documents

## 🚀 Quick Deploy to Vercel

1. **One-Click Deploy**: Click the "Deploy with Vercel" button above
2. **Set Environment Variables** in Vercel dashboard:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `OPENAI_API_KEY`: Your OpenAI API key (optional)
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key (optional)
3. **Deploy**: Vercel will automatically build and deploy your app

## 💻 Local Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pdf-mcq-generator-sathish.git
cd pdf-mcq-generator-sathish
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Choose your generation method:**

   **Option A: Online Generation (Original - Easiest Setup)**
   ```bash
   # Create .env file with your API keys
   echo "OPENAI_API_KEY=your_openai_key" > .env
   echo "OPENROUTER_API_KEY=your_openrouter_key" >> .env
   echo "DEEPSEEK_API_KEY=your_deepseek_key" >> .env
   # Ready to use immediately!
   ```

   **Option B: Enhanced Professional (Best Quality)**
   ```bash
   python setup_enhanced_professional.py
   ```

   **Option C: Fast Generation (Best Speed)**
   ```bash
   python setup_fast_models.py
   ```

   **Option D: Offline Generation (Privacy)**
   ```bash
   python setup_offline.py
   ```

4. Set up environment variables (for online generation):
Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

> **Note**: API keys are optional if you're using offline generation only.

## Running the Applications

### Streamlit App (Recommended)
```bash
streamlit run app.py
```
The app will be available at `http://localhost:8501`

### Flask App (HTML Interface)
```bash
python flask_app.py
```
The app will be available at `http://localhost:5000`

## 🎯 Enhanced Professional MCQ Generation (Truly Professional Quality)

For academic-grade, publication-ready questions with professional language:

### Quick Setup
```bash
python setup_enhanced_professional.py
```

### Test Professional Quality
```bash
python test_enhanced_professional.py
```

### Usage
- Select "🎯 Professional (Best Quality)" in the web interface
- Get 85%+ professional quality scores suitable for academic/certification use
- Uses T5-Large with advanced text analysis and professional question patterns

### Features
- **Definition Questions**: Professional terminology with accurate definitions
- **Concept Questions**: Advanced understanding and relationships
- **Application Questions**: Practical knowledge and use cases
- **Professional Language**: Academic-appropriate phrasing and structure
- **Quality Scoring**: Professional standards validation

## 🔒 Offline MCQ Generation

For maximum question extraction without internet dependency:

### Quick Setup
```bash
python setup_offline.py
```

### Test Offline Functionality
```bash
python test_offline_comprehensive.py
```

### Usage
- Enable "🔒 Offline" mode in the web interface
- Use "Enhanced Estimation" for better question count prediction
- Works completely offline after initial setup

For detailed offline setup instructions, see [OFFLINE_MCQ_GUIDE.md](OFFLINE_MCQ_GUIDE.md)

## PDF Download Feature

Both applications support PDF download:

### Streamlit App
- PDF download is built into the interface
- Click "Download PDF" button after generating questions
- Uses FPDF library with proper font handling

### Flask App (HTML Interface)
- PDF download via AJAX request to `/download-pdf` endpoint
- Questions are sent as JSON to the backend
- PDF is generated server-side and downloaded automatically
- Uses Arial font (built-in) to avoid font path issues

## Manual Reference Control

The application provides manual control over source references in question explanations:

### Manual Input Fields
- **Book Name (optional)**: Enter the exact book or document name you want to appear in explanations
- **Chapter Name (optional)**: Enter the exact chapter, section, clause, or rule reference

### How It Works
1. **Upload PDF**: The system extracts text from your PDF document
2. **Manual Input**: Enter book name and/or chapter name in the optional fields
3. **Source Attribution**: Only manually entered information appears in explanations
4. **Clean Output**: No reference appears if fields are left empty

### Reference Behavior
- **Both Fields Filled**: `(Source: Book Name, Chapter Name)`
- **Book Name Only**: `(Source: Book Name)`
- **Chapter Name Only**: `(Source: Chapter Name)`
- **No Input**: No source reference in explanations

### Example Outputs
- **Complete Reference**: "...explanation... (Source: POST OFFICE GUIDE-Part-I, clause 108)"
- **Book Only**: "...explanation... (Source: POST OFFICE GUIDE-Part-I)"
- **Chapter Only**: "...explanation... (Source: clause 108)"
- **No Reference**: "...explanation..." (clean, no source)

## File Structure

```
├── app.py                 # Streamlit application
├── flask_app.py          # Flask application
├── mcq_generator.py      # Core MCQ generation logic
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # HTML template for Flask app
├── uploads/              # Temporary file storage
└── README.md            # This file
```

## API Endpoints (Flask App)

- `GET /` - Serve the main HTML page
- `POST /upload` - Upload PDF and generate questions
- `POST /download-csv` - Download questions as CSV
- `POST /download-pdf` - Download questions as PDF

## Troubleshooting

1. **Font Issues**: The Flask app uses Arial font (built-in) to avoid font path issues
2. **API Keys**: Make sure your API keys are properly set in the `.env` file
3. **File Uploads**: Ensure the `uploads/` directory exists and is writable
4. **Dependencies**: Run `pip install -r requirements.txt` to install all required packages
