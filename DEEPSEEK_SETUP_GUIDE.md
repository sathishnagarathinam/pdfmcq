# 🚀 DeepSeek Direct API Setup Guide

## 🎯 **Why Use Direct DeepSeek API?**

**OpenRouter Free Tier Issues:**
- ❌ Only 50 requests per day
- ❌ Rate limit errors (429)
- ❌ Shared rate limits across all users

**Direct DeepSeek API Benefits:**
- ✅ Much higher rate limits
- ✅ Better performance
- ✅ More reliable service
- ✅ Often free or very low cost

## 🔑 **Step 1: Get Your DeepSeek API Key**

1. **Visit DeepSeek Platform**
   - Go to: https://platform.deepseek.com/
   - Click "Sign Up" or "Login"

2. **Create Account**
   - Sign up with email or GitHub
   - Verify your email if required

3. **Get API Key**
   - Navigate to "API Keys" section
   - Click "Create New Key"
   - Copy the API key (starts with `sk-` but NOT `sk-or-v1-`)
   - Save it securely

## ⚙️ **Step 2: Update Your Configuration**

1. **Update .env file**
   ```bash
   # Replace 'your-direct-deepseek-api-key-here' with your actual key
   DEEPSEEK_API_KEY='sk-your-actual-deepseek-key-here'
   ```

2. **Restart your Flask app**
   ```bash
   python flask_app.py
   ```

## 🎮 **Step 3: Use Direct DeepSeek in the App**

1. **In the web interface:**
   - Select **"DeepSeek"** as the AI Model Provider (not OpenRouter)
   - Choose model: **"DeepSeek Chat"** or **"DeepSeek Coder"**
   - Upload your PDF and generate questions

2. **Model Options:**
   - **DeepSeek Chat**: Best for general MCQ generation
   - **DeepSeek Coder**: Better for technical/programming content

## 🔧 **Step 4: Verify Setup**

Test with a small PDF first:
- Upload a 1-2 page PDF
- Select "DeepSeek" provider
- Choose "DeepSeek Chat" model
- Generate 2-3 questions

**Expected Result:**
- ✅ No rate limit errors
- ✅ Fast generation
- ✅ High-quality questions

## 🆘 **Troubleshooting**

### **Issue: "Authentication Fails"**
**Solution:**
- Double-check your API key in .env file
- Make sure it starts with `sk-` (not `sk-or-v1-`)
- Restart the Flask app after updating .env

### **Issue: "Model not found"**
**Solution:**
- Use "deepseek-chat" or "deepseek-coder" as model names
- Make sure you selected "DeepSeek" as provider (not OpenRouter)

### **Issue: Still getting rate limits**
**Solution:**
- Make sure you're using "DeepSeek" provider, not "OpenRouter"
- Check that DEEPSEEK_API_KEY is set correctly
- Verify the API key is from platform.deepseek.com

## 💡 **Alternative: Add Credits to OpenRouter**

If you prefer to stick with OpenRouter:
1. Go to https://openrouter.ai/settings/credits
2. Add $5-10 in credits
3. This unlocks 1000+ free model requests per day
4. Continue using "OpenRouter" provider with "DeepSeek V3"

## 📊 **Rate Limit Comparison**

| Provider | Free Tier Limit | Cost | Setup Difficulty |
|----------|----------------|------|------------------|
| OpenRouter Free | 50 requests/day | Free | Easy |
| OpenRouter Paid | 1000+ requests/day | $5-10 | Easy |
| Direct DeepSeek | Much higher | Free/Low cost | Medium |

## 🎯 **Recommendation**

**For regular use:** Get direct DeepSeek API key
**For testing:** Add $5 credits to OpenRouter

Both options will solve the rate limit issue and give you reliable MCQ generation!
