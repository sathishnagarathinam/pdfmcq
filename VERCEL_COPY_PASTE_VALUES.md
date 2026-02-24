# 📋 Vercel Environment Variables - Copy & Paste Values

## 🎯 MINIMUM SETUP (2 Variables)

### Variable 1: SECRET_KEY

**In Vercel, enter:**

```
Key:   SECRET_KEY
Value: (Generate using Python command below)
```

**Generate the value using this command:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Example output (copy this format):**
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

---

### Variable 2: API Key (Choose ONE)

#### Option A: OpenRouter (RECOMMENDED ⭐)

**In Vercel, enter:**
```
Key:   OPENROUTER_API_KEY
Value: sk-or-v1-your-actual-key-here
```

**How to get:**
1. Go to https://openrouter.ai
2. Sign up (free)
3. Click Settings
4. Click API Keys
5. Copy your key (starts with `sk-or-v1-`)
6. Paste in Vercel

---

#### Option B: OpenAI

**In Vercel, enter:**
```
Key:   OPENAI_API_KEY
Value: sk-proj-your-actual-key-here
```

**How to get:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy key (starts with `sk-proj-`)
4. Paste in Vercel

---

#### Option C: DeepSeek

**In Vercel, enter:**
```
Key:   DEEPSEEK_API_KEY
Value: sk-your-actual-key-here
```

**How to get:**
1. Go to https://platform.deepseek.com
2. Create account
3. Create API key
4. Copy key (starts with `sk-`)
5. Paste in Vercel

---

## ⭕ OPTIONAL SETUP (4 Additional Variables)

### Variable 3: Flask Environment

**In Vercel, enter:**
```
Key:   FLASK_ENV
Value: production
```

---

### Variable 4: Flask Debug

**In Vercel, enter:**
```
Key:   FLASK_DEBUG
Value: False
```

---

### Variable 5: Vercel Deployment

**In Vercel, enter:**
```
Key:   VERCEL_DEPLOYMENT
Value: True
```

---

### Variable 6: Temp Directory

**In Vercel, enter:**
```
Key:   USE_TEMP_DIRECTORY
Value: True
```

---

## 📝 Step-by-Step Instructions

### Step 1: Generate SECRET_KEY (2 min)
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output

### Step 2: Get API Key (5 min)
Choose ONE and copy the key:
- OpenRouter: https://openrouter.ai → Settings → API Keys
- OpenAI: https://platform.openai.com/api-keys
- DeepSeek: https://platform.deepseek.com

### Step 3: Go to Vercel (1 min)
1. https://vercel.com/dashboard
2. Select project
3. Settings → Environment Variables

### Step 4: Add Variables (5 min)
For each variable:
1. Paste **Key** (e.g., `SECRET_KEY`)
2. Paste **Value** (e.g., your secret key)
3. Check: ✓ Production ✓ Preview ✓ Development
4. Click **Add**

### Step 5: Redeploy (1 min)
1. Deployments tab
2. Click three dots (•••)
3. Click **Redeploy**

### Step 6: Wait & Test (5 min)
1. Wait 2-5 minutes
2. Visit your Vercel URL
3. Login: `sathishsat04`
4. Test features

---

## ✅ Checklist

- [ ] Generated `SECRET_KEY` using Python
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

## 🚀 Ready!

Your application is ready to deploy! 🎉

