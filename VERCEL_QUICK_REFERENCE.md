# ⚡ Vercel Environment Variables - Quick Reference

## 🎯 MINIMUM REQUIRED (Copy & Paste)

```
SECRET_KEY = your-super-secret-key-change-this-to-something-random-and-long-12345678
OPENROUTER_API_KEY = sk-or-v1-your-openrouter-api-key-here
```

---

## 📋 ALL VARIABLES (Complete Setup)

### 1. Flask Configuration
```
SECRET_KEY = your-super-secret-key-change-this-to-something-random-and-long-12345678
FLASK_ENV = production
FLASK_DEBUG = False
```

### 2. API Keys (Choose at least ONE)

**Option A: OpenRouter (RECOMMENDED)**
```
OPENROUTER_API_KEY = sk-or-v1-your-openrouter-api-key-here
```

**Option B: OpenAI**
```
OPENAI_API_KEY = sk-proj-your-openai-api-key-here
```

**Option C: DeepSeek**
```
DEEPSEEK_API_KEY = sk-your-deepseek-api-key-here
```

### 3. Vercel Configuration
```
VERCEL_DEPLOYMENT = True
USE_TEMP_DIRECTORY = True
```

---

## 🔑 How to Get API Keys

### OpenRouter (FREE - Recommended)
1. Go to https://openrouter.ai
2. Sign up (free)
3. Settings → API Keys
4. Copy key starting with `sk-or-v1-`

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy key starting with `sk-proj-`

### DeepSeek
1. Go to https://platform.deepseek.com
2. Create account
3. Create API key
4. Copy key starting with `sk-`

---

## 🔐 How to Generate SECRET_KEY

Run this command in terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use as `SECRET_KEY` value.

---

## 📝 Step-by-Step Vercel Setup

### Step 1: Go to Vercel
- https://vercel.com/dashboard
- Select your project
- Click **Settings**

### Step 2: Add Variables
- Click **Environment Variables**
- For each variable:
  - Enter **Key** (e.g., `SECRET_KEY`)
  - Enter **Value** (e.g., your secret key)
  - Select: **Production**, **Preview**, **Development**
  - Click **Add**

### Step 3: Redeploy
- Go to **Deployments**
- Click three dots on latest deployment
- Click **Redeploy**

### Step 4: Wait & Test
- Wait 2-5 minutes for deployment
- Test login: username `sathishsat04`
- Test features

---

## ✅ Checklist

- [ ] Generated `SECRET_KEY`
- [ ] Got API key from OpenRouter/OpenAI/DeepSeek
- [ ] Added `SECRET_KEY` to Vercel
- [ ] Added API key to Vercel
- [ ] Added optional variables (optional)
- [ ] Redeployed
- [ ] Waited 2-5 minutes
- [ ] Tested login
- [ ] Tested MCQ generation
- [ ] Tested notes generation

---

## 🚀 You're Ready!

Your application should now work on Vercel! 🎉

