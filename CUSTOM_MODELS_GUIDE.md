# Custom Models Configuration Guide

## Overview

The PDF MCQ Generator now supports custom AI models with flexible API key management. You can use pre-configured models or add your own custom models with their respective API keys.

## Supported Model Providers

### 1. **OpenRouter** (Default)
- **Models Available:**
  - DeepSeek V3 (Free)
  - Llama 3.3 70B (Free)
  - Qwen 2.5 72B (Free)
  - Mistral 7B (Free)
  - Gemini 2.0 Flash (Free)
- **API Key:** Set `OPENROUTER_API_KEY` in `.env` file
- **Base URL:** `https://openrouter.ai/api/v1`

### 2. **OpenAI**
- **Models Available:**
  - GPT-3.5 Turbo
  - GPT-4
  - GPT-4 Turbo
  - GPT-4o
- **API Key:** Set `OPENAI_API_KEY` in `.env` file
- **Base URL:** `https://api.openai.com/v1` (default)

### 3. **Anthropic**
- **Models Available:**
  - Claude 3 Haiku
  - Claude 3 Sonnet
  - Claude 3 Opus
- **API Key:** Set `ANTHROPIC_API_KEY` in `.env` file
- **Base URL:** `https://api.anthropic.com/v1`

### 4. **DeepSeek**
- **Models Available:**
  - DeepSeek Chat
  - DeepSeek Coder
- **API Key:** Set `DEEPSEEK_API_KEY` in `.env` file
- **Base URL:** `https://api.deepseek.com`

### 5. **Custom Models**
- **Use any OpenAI-compatible API**
- **Provide custom API key and base URL**
- **Support for various providers like Groq, Mistral, Cohere, etc.**

## Setting Up API Keys

### Environment File (.env)
Create or update your `.env` file with the following structure:

```env
# AI Model API Keys
OPENROUTER_API_KEY='your-openrouter-api-key'
OPENAI_API_KEY='your-openai-api-key'
ANTHROPIC_API_KEY='your-anthropic-api-key'
DEEPSEEK_API_KEY='your-deepseek-api-key'

# Additional API Keys for Custom Models
HUGGINGFACE_API_KEY='your-huggingface-api-key'
COHERE_API_KEY='your-cohere-api-key'
MISTRAL_API_KEY='your-mistral-api-key'
GROQ_API_KEY='your-groq-api-key'
```

## Using Custom Models

### Step 1: Select "Custom Model" Provider
1. Open the web interface at `http://127.0.0.1:5000`
2. In the "AI Model Provider" dropdown, select "Custom Model"
3. The custom model configuration section will appear

### Step 2: Configure Custom Model
Fill in the following fields:

1. **Custom Model Name:** 
   - Example: `gpt-4`, `claude-3-opus`, `llama-2-70b-chat`
   - Use the exact model name as required by the API

2. **API Key:**
   - Enter your API key for the custom model provider
   - This will be used for authentication

3. **Base URL (Optional):**
   - Enter the base URL for the API endpoint
   - Examples:
     - Groq: `https://api.groq.com/openai/v1`
     - Mistral: `https://api.mistral.ai/v1`
     - Local models: `http://localhost:1234/v1`

### Step 3: Generate MCQs
1. Upload your PDF file
2. Configure other settings (questions count, difficulty)
3. Click "Generate MCQs"
4. Download results as PDF or CSV

## Example Custom Model Configurations

### Groq API
```
Model Name: llama3-70b-8192
API Key: gsk_your_groq_api_key
Base URL: https://api.groq.com/openai/v1
```

### Mistral API
```
Model Name: mistral-large-latest
API Key: your_mistral_api_key
Base URL: https://api.mistral.ai/v1
```

### Local Model (Ollama/LM Studio)
```
Model Name: llama2
API Key: not-needed (or any placeholder)
Base URL: http://localhost:1234/v1
```

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for production deployments**
3. **Rotate API keys regularly**
4. **Monitor API usage and costs**
5. **Use least-privilege API keys when possible**

## Troubleshooting

### Common Issues:

1. **"Invalid API Key" Error:**
   - Verify the API key is correct
   - Check if the key has necessary permissions
   - Ensure the key is not expired

2. **"Model Not Found" Error:**
   - Verify the model name is correct
   - Check if the model is available in your plan
   - Ensure the base URL is correct

3. **Connection Timeout:**
   - Check internet connectivity
   - Verify the base URL is accessible
   - Try with a different model or provider

4. **Rate Limiting:**
   - Wait before making another request
   - Consider upgrading your API plan
   - Use a different model with higher limits

## Advanced Features

### Model-Specific Optimizations
- Different models may perform better with specific prompt formats
- Adjust temperature and max_tokens based on model capabilities
- Some models may require specific system prompts

### Batch Processing
- For large documents, consider splitting into smaller chunks
- Use appropriate models for different content types
- Monitor token usage for cost optimization

## Support

For additional help:
1. Check the model provider's documentation
2. Verify API endpoint compatibility
3. Test with simple requests first
4. Contact the model provider's support if needed
