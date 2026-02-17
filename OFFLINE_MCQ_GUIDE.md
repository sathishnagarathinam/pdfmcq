# Offline MCQ Generation Guide

This guide explains how to set up and use the offline MCQ generation functionality that allows you to extract the maximum number of questions from PDFs without requiring an internet connection.

## 🚀 Quick Start

### 1. Install Dependencies

Run the setup script to install all required dependencies:

```bash
python setup_offline.py
```

Or install manually:

```bash
pip install transformers>=4.30.0 torch>=2.0.0 sentence-transformers>=2.2.0 spacy>=3.6.0 nltk>=3.8.0 scikit-learn>=1.3.0 numpy>=1.24.0 datasets>=2.12.0
python -m spacy download en_core_web_sm
```

### 2. Test Installation

```bash
python test_offline.py
```

### 3. Use in Your Applications

```python
from mcq_generator import generate_mcq_questions_with_offline_fallback

# Generate questions with offline preference
questions = generate_mcq_questions_with_offline_fallback(
    text="Your PDF text here",
    num_questions=10,
    prefer_offline=True
)
```

## 🔧 Features

### Enhanced Question Estimation

The offline system provides much more accurate estimation of the maximum number of questions that can be generated from a PDF:

- **Fact-based analysis**: Identifies factual statements that can become questions
- **Concept extraction**: Uses TF-IDF to find key concepts
- **Semantic analysis**: Analyzes text structure and meaning
- **Confidence scoring**: Provides confidence levels for estimates

### Multiple Generation Strategies

1. **Fact-to-Question Conversion**: Converts factual statements into questions
2. **Concept-based Questions**: Generates questions about key concepts
3. **T5 Model Generation**: Uses transformer models for natural question generation
4. **Hybrid Approach**: Combines multiple strategies for maximum coverage

### Smart Fallback System

- Tries offline generation first if preferred
- Falls back to online models if offline fails
- Provides seamless user experience
- Maintains compatibility with existing code

## 📁 File Structure

```
├── offline_mcq_generator.py    # Main offline generation logic
├── offline_config.py           # Configuration and model management
├── setup_offline.py           # Setup script
├── test_offline.py            # Test script (created by setup)
├── offline_config.json        # Configuration file (created automatically)
└── models/                    # Model cache directory
    ├── question_generation/
    ├── sentence_transformer/
    └── spacy/
```

## ⚙️ Configuration

The system uses `offline_config.json` for configuration:

```json
{
  "models": {
    "question_generation": {
      "name": "valhalla/t5-small-qg-hl",
      "type": "t5",
      "size": "small"
    },
    "sentence_transformer": {
      "name": "all-MiniLM-L6-v2",
      "type": "sentence_transformer", 
      "size": "small"
    },
    "spacy": {
      "name": "en_core_web_sm",
      "type": "spacy",
      "size": "small"
    }
  },
  "cache_dir": "./models",
  "max_cache_size_gb": 5,
  "auto_download": true
}
```

## 🎯 Usage Examples

### Basic Offline Generation

```python
from offline_mcq_generator import generate_mcq_questions_offline

questions = generate_mcq_questions_offline(
    text="Your text here",
    num_questions=5,
    difficulty="medium"
)
```

### Enhanced Estimation

```python
from mcq_generator import estimate_max_questions_detailed

result = estimate_max_questions_detailed(text)
print(f"Max questions: {result['max_questions']}")
print(f"Confidence: {result['confidence']}")
print(f"Breakdown: {result['breakdown']}")
```

### Flask App Integration

The Flask app automatically supports offline generation:

```python
# In your form, add:
prefer_offline = request.form.get('preferOffline') == 'on'
use_offline_estimation = request.form.get('useOfflineEstimation') == 'on'
```

### Streamlit App Integration

The Streamlit app includes offline options:

```python
prefer_offline = st.checkbox("🔒 Prefer Offline Generation")
use_offline_estimation = st.checkbox("Use Enhanced Estimation")
```

## 🔍 Model Information

### Question Generation Model
- **Model**: valhalla/t5-small-qg-hl
- **Type**: T5-based transformer
- **Size**: ~250MB
- **Purpose**: Generates natural questions from text

### Sentence Transformer
- **Model**: all-MiniLM-L6-v2
- **Type**: Sentence embedding model
- **Size**: ~90MB
- **Purpose**: Semantic analysis and similarity

### spaCy Model
- **Model**: en_core_web_sm
- **Type**: English language model
- **Size**: ~50MB
- **Purpose**: NLP processing and entity recognition

## 🚨 Troubleshooting

### Common Issues

1. **Models not downloading**
   ```bash
   # Check internet connection and try manual download
   python setup_offline.py --skip-deps
   ```

2. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Out of memory errors**
   ```python
   # Reduce batch size or use smaller models
   # Edit offline_config.json to use smaller models
   ```

4. **Cache size issues**
   ```python
   from offline_config import get_model_manager
   manager = get_model_manager()
   manager.cleanup_cache(force=True)
   ```

### Performance Tips

1. **First run is slow**: Models need to be downloaded and cached
2. **Subsequent runs are fast**: Models are loaded from cache
3. **Memory usage**: ~2-3GB RAM for all models
4. **Disk space**: ~500MB for all models

## 🔄 API Compatibility

The offline system maintains full compatibility with the existing API:

```python
# These functions now support offline fallback
generate_mcq_questions_with_offline_fallback()
estimate_max_questions()  # Enhanced with offline analysis
estimate_max_questions_detailed()  # New detailed analysis
```

## 📊 Performance Comparison

| Method | Speed | Quality | Internet Required | Max Questions |
|--------|-------|---------|-------------------|---------------|
| Online Only | Fast | High | Yes | 100+ |
| Offline Only | Medium | Good | No | 50+ |
| Hybrid | Fast | High | Preferred | 100+ |

## 🛠️ Advanced Configuration

### Custom Models

You can configure custom models by editing `offline_config.json`:

```json
{
  "models": {
    "question_generation": {
      "name": "your-custom-model",
      "type": "t5"
    }
  }
}
```

### Cache Management

```python
from offline_config import get_model_manager

manager = get_model_manager()

# Check status
status = manager.get_status()

# Clean cache
manager.cleanup_cache()

# Download specific model
manager.download_model("question_generation")
```

## 🤝 Contributing

To contribute to the offline functionality:

1. Test your changes with `python test_offline.py`
2. Ensure backward compatibility
3. Update documentation
4. Add appropriate error handling

## 📝 License

This offline functionality is part of the PDF MCQ Generator project and follows the same license terms.
