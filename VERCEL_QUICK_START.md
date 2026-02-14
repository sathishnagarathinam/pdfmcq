# Vercel Deployment - Quick Start 🚀

Deploy your PDF MCQ Generator to Vercel in 5 minutes!

## Prerequisites

- GitHub repository with code pushed
- Vercel account (free at https://vercel.com)
- API key (OpenRouter, OpenAI, or DeepSeek)

## Step 1: Commit Changes (2 minutes)

```bash
cd /Volumes/sathish/pdfmcq

git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

## Step 2: Connect to Vercel (1 minute)

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Select your "pdfmcq" repository
5. Click "Import"

## Step 3: Configure Environment Variables (1 minute)

In Vercel Dashboard:

1. Go to Project Settings → Environment Variables
2. Add these variables:

```
OPENROUTER_API_KEY=your_api_key_here
VERCEL_DEPLOYMENT=True
USE_TEMP_DIRECTORY=True
FLASK_ENV=production
```

3. Click "Save"

## Step 4: Deploy (1 minute)

1. Click "Deploy" button
2. Wait for deployment to complete (usually 2-3 minutes)
3. You'll see a green checkmark when done

## Step 5: Test (Optional)

1. Click the deployment URL
2. Upload a test PDF
3. Generate MCQ questions
4. Verify it works!

---

## Getting API Keys

### OpenRouter (Recommended)
1. Go to https://openrouter.ai
2. Sign up
3. Copy your API key
4. Add to Vercel environment variables

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new key
3. Copy and add to Vercel

### DeepSeek
1. Go to https://platform.deepseek.com
2. Create API key
3. Copy and add to Vercel

---

## Troubleshooting

### Deployment Failed
- Check build logs in Vercel dashboard
- Verify all files are committed to GitHub
- Ensure requirements.txt is present

### Application Not Working
- Check environment variables are set
- Verify API key is correct
- Check function logs in Vercel dashboard

### Slow Performance
- Use smaller PDFs
- Reduce number of questions
- Use DeepSeek (faster and cheaper)

---

## Your Deployment URL

After successful deployment, your app will be at:

```
https://your-project.vercel.app
```

Share this URL with others!

---

**That's it! Your app is live on Vercel! 🎉**

For detailed guide, see: VERCEL_DEPLOYMENT_GUIDE.md

