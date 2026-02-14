# 🚀 Redeploy to Vercel - Quick Guide

## What Happened?
Your deployment failed because `requirements.txt` had heavy ML libraries (4GB+).

## What's Fixed?
✅ Updated to use lightweight `requirements-vercel.txt` (200MB)
✅ Pushed to GitHub (commit b13abd7)
✅ Ready to redeploy!

## 3-Step Redeploy Process

### Step 1: Go to Vercel Dashboard
```
https://vercel.com/dashboard
```

### Step 2: Redeploy Your Project
1. Click on "pdfmcq" project
2. Go to "Deployments" tab
3. Find the failed deployment
4. Click "Redeploy" button
5. Wait 2-3 minutes for build

### Step 3: Configure Environment Variables
If not already set, add these in Vercel:

**Settings → Environment Variables:**
```
OPENROUTER_API_KEY = your_api_key_here
VERCEL_DEPLOYMENT = True
USE_TEMP_DIRECTORY = True
FLASK_ENV = production
```

## Get API Key (2 minutes)

### Option 1: OpenRouter (Cheapest)
1. Go to https://openrouter.ai
2. Sign up (free)
3. Copy API key from Account → API Keys
4. Paste in Vercel environment variables

### Option 2: OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create API key
3. Paste in Vercel environment variables

### Option 3: DeepSeek
1. Go to https://platform.deepseek.com
2. Create API key
3. Paste in Vercel environment variables

## Expected Results

✅ Build completes in 2-3 minutes
✅ Deployment succeeds
✅ Application is live
✅ PDF upload works
✅ MCQ generation works

## Verify Deployment

1. Visit your Vercel deployment URL
2. Upload a PDF
3. Generate MCQ questions
4. Test export (CSV/PDF)

## If Build Fails Again

1. Check build logs in Vercel
2. Look for error messages
3. Verify environment variables
4. Check API key is valid

## Files Changed

- ✅ vercel.json (buildCommand updated)
- ✅ Pushed to GitHub
- ✅ Ready for redeploy

## Status

**Current:** Ready to redeploy
**Next:** Click "Redeploy" in Vercel dashboard
**Time:** 2-3 minutes to deploy

---

**That's it! Your app is ready to deploy! 🎉**

Go to Vercel dashboard and click "Redeploy" now!

