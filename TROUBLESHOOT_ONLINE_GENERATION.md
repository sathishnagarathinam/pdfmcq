# 🔧 Troubleshooting Online MCQ Generation

## 🚨 **Issue: Online Generation Produces Blank Questions**

If you're experiencing blank or empty questions when using online generation at `http://localhost:5002`, follow this troubleshooting guide.

---

## 🔍 **Step 1: Quick Diagnosis**

Run the quick test to identify the issue:

```bash
python quick_online_test.py
```

This will immediately tell you if online generation is working or not.

---

## 🔧 **Step 2: Check API Configuration**

### **Verify API Keys**

1. **Check .env file exists:**
   ```bash
   ls -la .env
   ```

2. **Verify API keys are set:**
   ```bash
   cat .env
   ```

3. **Expected format:**
   ```bash
   OPENAI_API_KEY=sk-your-openai-key-here
   OPENROUTER_API_KEY=sk-your-openrouter-key-here
   DEEPSEEK_API_KEY=your-deepseek-key-here
   ANTHROPIC_API_KEY=sk-your-anthropic-key-here
   ```

### **Test API Key Validity**

Run the comprehensive debug tool:
```bash
python debug_online_generation.py
```

---

## 🌐 **Step 3: Test Different Providers**

### **OpenRouter (Recommended)**
```bash
# Add to .env
OPENROUTER_API_KEY=sk-your-openrouter-key
```

### **OpenAI**
```bash
# Add to .env  
OPENAI_API_KEY=sk-your-openai-key
```

### **DeepSeek**
```bash
# Add to .env
DEEPSEEK_API_KEY=your-deepseek-key
```

---

## 🐛 **Step 4: Enable Debug Mode**

1. **In Streamlit app:**
   - Go to "🔧 Advanced Options"
   - Check "🐛 Debug Mode"
   - Try generating questions again
   - Check the debug output

2. **Check terminal output:**
   - Look at the terminal where you ran `streamlit run app.py`
   - Look for error messages or debug information

---

## 🔍 **Step 5: Common Issues and Solutions**

### **Issue: "No API keys configured"**
**Solution:**
```bash
# Create .env file with at least one API key
echo "OPENROUTER_API_KEY=your_key_here" > .env
```

### **Issue: "JSON parsing failed"**
**Solution:**
- The AI model is returning invalid JSON
- Try a different model provider
- Try reducing the number of questions requested

### **Issue: "Invalid response format"**
**Solution:**
- The AI model is not following the expected format
- Try using "basic" model type instead of "advanced"
- Try a different provider

### **Issue: "API key invalid"**
**Solution:**
- Verify your API key is correct
- Check if your API key has sufficient credits
- Try generating a new API key

### **Issue: "Connection timeout"**
**Solution:**
- Check your internet connection
- Try a different provider
- Increase timeout in the code

---

## 🧪 **Step 6: Manual Testing**

### **Test 1: Direct API Call**
```python
from mcq_generator import generate_mcq_questions

result = generate_mcq_questions(
    text="Python is a programming language.",
    num_questions=1,
    model_provider="openrouter",  # or "openai", "deepseek"
    model_type="basic"
)

print(result)
```

### **Test 2: Simple Text**
Try with very simple text:
```
"Python is a programming language created by Guido van Rossum in 1991."
```

### **Test 3: Different Models**
- Try "basic" instead of "advanced"
- Try different providers
- Try fewer questions (1-2 instead of 10)

---

## 🔧 **Step 7: Advanced Debugging**

### **Check Network Issues**
```bash
# Test API connectivity
curl -H "Authorization: Bearer your_api_key" https://api.openai.com/v1/models
```

### **Check Streamlit Logs**
```bash
# Run Streamlit with verbose logging
streamlit run app.py --logger.level debug
```

### **Check Python Environment**
```bash
# Verify required packages
pip list | grep -E "(openai|requests|streamlit)"
```

---

## 🚀 **Step 8: Alternative Solutions**

### **Use Different Generation Method**
If online generation continues to fail:

1. **Fast Generation:**
   ```bash
   python setup_fast_models.py
   # Then select "⚡ Fast" in the app
   ```

2. **Enhanced Professional:**
   ```bash
   python setup_enhanced_professional.py
   # Then select "🎯 Professional" in the app
   ```

3. **Offline Generation:**
   ```bash
   python setup_offline.py
   # Then select "🔒 Offline" in the app
   ```

---

## 📋 **Step 9: Report Issues**

If none of the above solutions work, gather this information:

### **System Information**
```bash
python --version
pip list | grep -E "(openai|streamlit|requests)"
```

### **Error Messages**
- Copy any error messages from the terminal
- Copy any error messages from the web interface
- Note which provider you're trying to use

### **Debug Output**
```bash
# Run with full debug
python debug_online_generation.py > debug_output.txt 2>&1
```

---

## ✅ **Expected Working Behavior**

When online generation is working correctly, you should see:

1. **In Terminal:**
   ```
   🌐 Starting online generation with openrouter (basic)
   📝 Text length: 150 characters
   🎯 Requested questions: 5
   🔑 Getting AI client for openrouter
   🔑 OpenRouter API key: ✅ Found
   🤖 Using model: openai/gpt-3.5-turbo
   📤 Sending API request to openai/gpt-3.5-turbo
   📥 Raw API response: [{"question": "What is Python?"...
   ✅ Successfully parsed 5 questions
   ```

2. **In Web Interface:**
   - Questions appear with proper formatting
   - All fields are filled (question, options A-D, correct answer)
   - No error messages

---

## 🎯 **Quick Fixes Summary**

1. **Check API keys** - Most common issue
2. **Try different provider** - OpenRouter usually most reliable
3. **Use debug mode** - Shows exactly what's happening
4. **Try simpler text** - Complex text can cause issues
5. **Use fewer questions** - Start with 1-2 questions
6. **Check internet connection** - Required for online generation
7. **Use alternative methods** - Fast/Professional/Offline as backup

---

## 💡 **Prevention Tips**

1. **Always test API keys** before using
2. **Keep backup providers** configured
3. **Use debug mode** when troubleshooting
4. **Start with simple text** for testing
5. **Have offline methods** as backup

**Remember: Online generation requires working API keys and internet connection. If you continue having issues, the enhanced professional or fast generation methods provide excellent alternatives!** 🚀
