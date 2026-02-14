# ⚡ Rate Limit Management Guide

## 🚨 **Problem: Rate Limit Errors (429)**

When you see errors like:
```
Error code: 429 - Rate limit exceeded: limit_rpm/google/gemini-2.0-flash-exp
High demand for google/gemini-2.0-flash-exp:free - limited to 4 requests per minute
```

This means you've hit the rate limit for free models on OpenRouter.

## 📊 **Rate Limits by Model (Updated - 13 Free Models Available!)**

### **🥇 BEST FREE MODELS - REASONING (Highest Quality)**
| Model | Rate Limit | Best For |
|-------|------------|----------|
| **DeepSeek R1 Distill Llama 70B (Free)** | 20 req/min | Complex MCQs, best reasoning |
| **DeepSeek R1 Distill Qwen 32B (Free)** | 20 req/min | Good reasoning + speed balance |
| **DeepSeek R1 Distill Qwen 14B (Free)** | 20 req/min | Fast reasoning |

### **🎯 GENERAL PURPOSE MODELS (Balanced)**
| Model | Rate Limit | Best For |
|-------|------------|----------|
| **Llama 3.1 70B (Free)** | 20 req/min | High quality general content |
| **Llama 3.3 70B (Free)** | 20 req/min | Latest Llama, general content |
| **Llama 3.1 8B (Free)** | 20 req/min | Very fast, good quality |
| **DeepSeek V3** | 50 req/day | Excellent all-round |

### **⚡ SPECIALIZED MODELS**
| Model | Rate Limit | Best For |
|-------|------------|----------|
| **Qwen 2.5 Coder 32B (Free)** | 20 req/min | Programming/Technical content |
| **Qwen 2.5 72B (Free)** | 20 req/min | High quality general content |
| **Qwen 2.5 7B (Free)** | 20 req/min | Fast processing |
| **Phi-3 Medium 128K (Free)** | 20 req/min | Long PDFs (128K context) |
| **Mistral 7B (Free)** | 20 req/min | Efficient, lightweight |

### **⚠️ LIMITED FREE MODELS (Avoid for Large PDFs)**
| Model | Rate Limit | Issue |
|-------|------------|-------|
| **Gemini 2.0 Flash (Free)** | 4 req/min | Too slow for large PDFs |

## 🚀 **Solutions**

### **Solution 1: Use Better Free Models (Recommended)**

**🥇 Best Choice - DeepSeek R1 Distill Llama 70B (Free):**
1. In the web interface, select **"OpenRouter"** as provider
2. Choose **"DeepSeek R1 Distill Llama 70B (Free)"** as model
3. Upload your PDF - excellent reasoning for complex MCQs!

**Why DeepSeek R1 Distill is Better:**
- ✅ 20 requests/min (vs 4 for Gemini)
- ✅ Advanced reasoning capabilities
- ✅ Produces highest quality MCQs
- ✅ Automatic rate limiting built-in

**🥈 Alternative - Qwen 2.5 Coder 32B (Free):**
- Best for programming/technical PDFs
- Fast and efficient
- 20 requests/min rate limit

### **Solution 2: Add Credits to OpenRouter**

**Quick Fix:**
1. Go to https://openrouter.ai/settings/credits
2. Add $5-10 in credits
3. Unlocks 1000+ requests per day
4. Continue using any model you prefer

### **Solution 3: Use Direct DeepSeek API**

**Higher Limits:**
1. Get API key from https://platform.deepseek.com/
2. Update your `.env` file
3. Select **"DeepSeek"** (not OpenRouter) as provider
4. Much higher rate limits

## 🔧 **Automatic Rate Limiting (Built-in)**

The app now automatically handles rate limits:

### **Smart Delays Between Chunks:**
- **Gemini 2.0 Flash:** 15 seconds between chunks
- **Qwen Models:** 3 seconds between chunks  
- **DeepSeek:** 1 second between chunks
- **First chunk:** No delay

### **What You'll See:**
```
📊 Text analysis: 35,000 tokens, limit: 4800 (free tier, rate limit: 20/min)
📦 Created 8 chunks
📤 Sending prompt for chunk 1...
✅ Chunk 1 completed
⏳ Rate limit delay: waiting 3 seconds before chunk 2...
📤 Sending prompt for chunk 2...
✅ Chunk 2 completed
...
```

## 🎯 **Recommendations by Use Case**

### **For Complex/Academic PDFs:**
**Best Choice:** DeepSeek R1 Distill Llama 70B (Free)
- Advanced reasoning capabilities
- Best for complex questions
- 20 requests/min rate limit
- Highest quality MCQs

### **For Programming/Technical PDFs:**
**Best Choice:** Qwen 2.5 Coder 32B (Free)
- Specialized for code and technical content
- 20 requests/min rate limit
- Excellent accuracy for programming topics

### **For General Content PDFs:**
**Best Choice:** Llama 3.1 70B (Free) or Qwen 2.5 72B (Free)
- Great general performance
- 20 requests/min rate limit
- Good for academic/business content

### **For Very Large PDFs (50+ pages):**
**Best Choice:** Phi-3 Medium 128K (Free)
- 128K context window (vs 8K for others)
- Can handle much larger chunks
- 20 requests/min rate limit
- Fewer chunks needed

### **For Speed (Small PDFs):**
**Best Choice:** Llama 3.1 8B (Free) or Qwen 2.5 7B (Free)
- Fastest processing
- 20 requests/min rate limit
- Good quality for simple content

### **For Regular Heavy Use:**
**Best Choice:** Add $5 credits to OpenRouter
- Removes rate limits
- Use any model you prefer
- Fastest processing
- Or use Direct DeepSeek API (highest rate limits)

## ⏱️ **Processing Time Estimates**

### **With Rate Limiting (Free Models):**
- **Small PDF (1-5 pages):** 30 seconds - 2 minutes
- **Medium PDF (6-20 pages):** 2-8 minutes
- **Large PDF (20+ pages):** 8-20 minutes

### **With Credits (Paid):**
- **Small PDF (1-5 pages):** 10-30 seconds
- **Medium PDF (6-20 pages):** 30 seconds - 2 minutes
- **Large PDF (20+ pages):** 1-5 minutes

## 🛠️ **How to Switch Models**

### **In the Web Interface:**
1. **AI Model Provider:** Select "OpenRouter"
2. **Model:** Choose from dropdown (13 free models available!):

**🥇 Top Recommendations:**
   - **DeepSeek R1 Distill Llama 70B (Free)** ← Best for complex MCQs
   - **Qwen 2.5 Coder 32B (Free)** ← Best for programming
   - **Llama 3.1 70B (Free)** ← Best for general content
   - **Phi-3 Medium 128K (Free)** ← Best for large PDFs

**⚠️ Avoid:**
   - ~~Gemini 2.0 Flash (Free)~~ ← Only 4 req/min, too slow

### **Model Selection Tips:**
- **Complex/Academic content:** Use DeepSeek R1 Distill Llama 70B
- **Programming/Technical content:** Use Qwen 2.5 Coder 32B
- **General content:** Use Llama 3.1 70B or Qwen 2.5 72B
- **Large PDFs (50+ pages):** Use Phi-3 Medium 128K
- **Speed priority:** Use Llama 3.1 8B or Qwen 2.5 7B
- **Mixed content:** Use DeepSeek R1 Distill Qwen 32B

## 🚨 **Troubleshooting Rate Limits**

### **Still Getting 429 Errors?**

1. **Check your model selection:**
   - Avoid Gemini 2.0 Flash for large PDFs
   - Use Qwen or Llama models instead

2. **Wait for rate limit reset:**
   - Rate limits reset every minute
   - Try again after 1-2 minutes

3. **Use smaller PDFs:**
   - Split large PDFs into smaller sections
   - Process them separately

4. **Add credits (permanent fix):**
   - $5 gives you 1000+ requests/day
   - Removes all rate limit issues

## ✅ **Success Indicators**

After switching to better models, you should see:
- ✅ No more 429 rate limit errors
- ✅ Automatic delays between chunks
- ✅ Faster overall processing
- ✅ Better question quality (especially with Qwen Coder)

The app now intelligently manages rate limits and recommends the best models for your use case! 🎉
