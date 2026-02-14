# PDF MCQ Generator

This application generates multiple-choice questions (MCQs) from PDF documents using AI models. It provides two interfaces:

1. **Streamlit Web App** (`app.py`) - A modern web interface with built-in PDF download
2. **Flask Web App** (`flask_app.py`) - A traditional HTML interface with PDF download functionality

## Features

- Upload PDF documents
- Extract text from PDFs
- Generate MCQ questions using various AI models (OpenRouter, OpenAI, DeepSeek)
- Download questions in CSV and PDF formats
- Configurable difficulty levels and question counts

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

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
