# 🚀 Vercel Environment Variables - Complete Setup Guide

## 📋 Required Environment Variables for Vercel Deployment

Add these variables to your Vercel project settings:

### 1. **SECRET_KEY** (REQUIRED - For Flask Session Management)

**Key:** `SECRET_KEY`

**Value:** Generate a secure random string (at least 32 characters)

**Example:**
```
your-super-secret-key-change-this-to-something-random-and-long-12345678
```

**How to generate:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🔑 API Keys (Choose at least ONE)

### Option 1: OpenRouter (RECOMMENDED - Free & Cost-Effective)

**Key:** `OPENROUTER_API_KEY`

**Value:** Your OpenRouter API key

**How to get:**
1. Go to https://openrouter.ai
2. Sign up for free account
3. Go to Settings → API Keys
4. Copy your API key
5. Paste in Vercel

**Example:**
```
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Option 2: OpenAI

**Key:** `OPENAI_API_KEY`

**Value:** Your OpenAI API key

**How to get:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy and paste in Vercel

**Example:**
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Option 3: DeepSeek

**Key:** `DEEPSEEK_API_KEY`

**Value:** Your DeepSeek API key

**How to get:**
1. Go to https://platform.deepseek.com
2. Sign up for account
3. Create API key
4. Copy and paste in Vercel

**Example:**
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📝 Optional Configuration Variables

### Flask Configuration

**Key:** `FLASK_ENV`
**Value:** `production`

**Key:** `FLASK_DEBUG`
**Value:** `False`

---

### Vercel Specific

**Key:** `VERCEL_DEPLOYMENT`
**Value:** `True`

**Key:** `USE_TEMP_DIRECTORY`
**Value:** `True`

---

## 🎯 Minimum Setup (Quick Start)

For the application to work, you MUST set:

1. **SECRET_KEY** - Required for Flask sessions
2. **At least ONE API Key** - Choose from:
   - `OPENROUTER_API_KEY` (Recommended)
   - `OPENAI_API_KEY`
   - `DEEPSEEK_API_KEY`

---

## 📊 Complete Setup (All Variables)

For full functionality, set all of these:

| Key | Value | Required |
|-----|-------|----------|
| `SECRET_KEY` | Your secret key | ✅ YES |
| `OPENROUTER_API_KEY` | Your OpenRouter key | ⭕ At least 1 |
| `OPENAI_API_KEY` | Your OpenAI key | ⭕ At least 1 |
| `DEEPSEEK_API_KEY` | Your DeepSeek key | ⭕ At least 1 |
| `FLASK_ENV` | `production` | ❌ Optional |
| `FLASK_DEBUG` | `False` | ❌ Optional |
| `VERCEL_DEPLOYMENT` | `True` | ❌ Optional |
| `USE_TEMP_DIRECTORY` | `True` | ❌ Optional |

---

## 🔧 How to Add Variables to Vercel

### Step 1: Go to Vercel Dashboard
1. Go to https://vercel.com/dashboard
2. Select your project
3. Click **Settings**

### Step 2: Navigate to Environment Variables
1. Click **Environment Variables** (left sidebar)
2. You'll see a form to add variables

### Step 3: Add Each Variable
1. Enter **Key** (e.g., `SECRET_KEY`)
2. Enter **Value** (e.g., your secret key)
3. Select environments: **Production**, **Preview**, **Development**
4. Click **Add**

### Step 4: Redeploy
1. Go to **Deployments**
2. Click the three dots on latest deployment
3. Click **Redeploy**

---

## ✅ Verification Checklist

After adding variables:

- [ ] Added `SECRET_KEY`
- [ ] Added at least one API key (OpenRouter/OpenAI/DeepSeek)
- [ ] All variables set for Production environment
- [ ] Redeployed the application
- [ ] Waited 2-5 minutes for deployment
- [ ] Tested login (username: `sathishsat04`, password: your password)
- [ ] Tested MCQ generation
- [ ] Tested notes generation
- [ ] Tested PDF download

---

## 🆘 Troubleshooting

### "API key not found" error
- Check that API key variable name is EXACTLY correct
- Verify value is not empty
- Redeploy after adding variable

### "Secret key error" or "Session error"
- Make sure `SECRET_KEY` is set
- Value should be at least 32 characters
- Redeploy after adding

### "Feature not working"
- Check Vercel logs: Settings → Function Logs
- Verify all required variables are set
- Try redeploying

---

## 📞 Support

If you need help:
1. Check Vercel logs for error messages
2. Verify all variables are set correctly
3. Try redeploying
4. Clear browser cache and hard refresh

---

**Your application is ready to deploy!** 🚀

