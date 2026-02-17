# Vercel Deployment Guide - PDF MCQ Generator 🚀

Complete step-by-step guide to deploy your PDF MCQ Generator to Vercel.

## Prerequisites

- GitHub account with your repository pushed
- Vercel account (free at https://vercel.com)
- API keys for your chosen provider (OpenAI, OpenRouter, or DeepSeek)

## Step 1: Prepare Your Repository

### Verify All Files Are Committed

```bash
cd /Volumes/sathish/pdfmcq

# Check git status
git status

# Add all changes
git add .

# Commit with message
git commit -m "Prepare for Vercel deployment: Update vercel.json, add serverless configuration, and optimize for serverless environment"

# Push to GitHub
git push origin main
```

### Files That Should Be Committed

✅ **vercel.json** - Updated with serverless configuration
✅ **requirements-vercel.txt** - Lightweight dependencies
✅ **.env.example** - Environment variable template
✅ **flask_app.py** - Updated for serverless compatibility
✅ **api/index.py** - Vercel entry point
✅ **templates/** - HTML templates
✅ **static/** - CSS and JavaScript files

❌ **.env** - DO NOT commit (contains API keys)
❌ **uploads/** - DO NOT commit (temporary files)
❌ **models/** - DO NOT commit (too large)

## Step 2: Connect GitHub to Vercel

### Option A: Using Vercel Dashboard (Recommended)

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Click "Import Git Repository"
4. Search for "pdfmcq" and select your repository
5. Click "Import"

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
cd /Volumes/sathish/pdfmcq
vercel
```

## Step 3: Configure Environment Variables

### In Vercel Dashboard:

1. Go to your project settings
2. Click "Environment Variables"
3. Add the following variables:

```
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key (if using OpenAI)
DEEPSEEK_API_KEY=your_deepseek_api_key (if using DeepSeek)
VERCEL_DEPLOYMENT=True
USE_TEMP_DIRECTORY=True
FLASK_ENV=production
```

### Getting API Keys:

**OpenRouter (Recommended - Cost Effective):**
1. Go to https://openrouter.ai
2. Sign up and get your API key
3. Add to Vercel environment variables

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Add to Vercel environment variables

**DeepSeek:**
1. Go to https://platform.deepseek.com
2. Create API key
3. Add to Vercel environment variables

## Step 4: Configure Build Settings

### In Vercel Dashboard:

1. Go to Project Settings → Build & Development Settings
2. Set the following:

```
Framework Preset: Other
Build Command: pip install -r requirements.txt
Output Directory: .
Install Command: pip install -r requirements.txt
```

### Or in vercel.json (Already Configured):

The vercel.json file is already configured with:
- Python 3.10 runtime
- 60-second function timeout
- 3008MB memory allocation
- Proper routes for static files and API

## Step 5: Deploy

### Automatic Deployment

Once connected to GitHub, Vercel will automatically deploy when you push to main:

```bash
git push origin main
```

### Manual Deployment

```bash
vercel --prod
```

## Step 6: Verify Deployment

### Check Deployment Status

1. Go to https://vercel.com/dashboard
2. Click on your project
3. Check the "Deployments" tab
4. Look for green checkmark indicating successful deployment

### Test Your Application

1. Click the deployment URL
2. You should see the PDF MCQ Generator interface
3. Try uploading a test PDF
4. Verify MCQ generation works

### Common Issues and Solutions

**Issue: "Module not found" error**
- Solution: Ensure all imports in flask_app.py are correct
- Check requirements.txt has all dependencies

**Issue: "Timeout" error**
- Solution: Increase timeout in vercel.json (already set to 60s)
- Try with smaller PDF files first

**Issue: "API key not found" error**
- Solution: Verify environment variables are set in Vercel dashboard
- Check variable names match exactly

**Issue: "File upload not working"**
- Solution: Vercel uses temporary directories
- This is handled automatically in updated flask_app.py

## Step 7: Monitor and Maintain

### View Logs

```bash
vercel logs <project-url>
```

### Redeploy

```bash
vercel --prod
```

### Update Environment Variables

1. Go to Project Settings → Environment Variables
2. Update the variable
3. Redeploy the project

## Step 8: Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions
4. Wait for DNS propagation (usually 24-48 hours)

## Troubleshooting

### Deployment Fails

1. Check build logs in Vercel dashboard
2. Verify all files are committed to GitHub
3. Ensure requirements.txt has all dependencies
4. Check for syntax errors in Python files

### Application Crashes

1. Check function logs in Vercel dashboard
2. Verify environment variables are set
3. Test locally first: `python flask_app.py`
4. Check API key validity

### Slow Performance

1. Optimize PDF processing
2. Reduce number of questions generated
3. Use lighter models (DeepSeek instead of GPT-4)
4. Consider caching results

## Performance Tips

1. **Use OpenRouter** - More cost-effective than OpenAI
2. **Limit Questions** - Start with 5-10 questions
3. **Optimize PDFs** - Use smaller, well-formatted PDFs
4. **Cache Results** - Store generated questions in database
5. **Monitor Usage** - Check API usage regularly

## Cost Estimation

**Vercel Hosting:** Free tier (up to 100GB bandwidth/month)

**API Costs (per 1000 requests):**
- OpenRouter: $0.14 - $2.00 (depending on model)
- OpenAI: $0.50 - $15.00 (depending on model)
- DeepSeek: $0.14 - $0.28 (most cost-effective)

## Next Steps

1. ✅ Commit changes to GitHub
2. ✅ Connect repository to Vercel
3. ✅ Configure environment variables
4. ✅ Deploy application
5. ✅ Test functionality
6. ✅ Monitor performance
7. ✅ Share deployment URL

## Useful Links

- Vercel Dashboard: https://vercel.com/dashboard
- Vercel Documentation: https://vercel.com/docs
- Python on Vercel: https://vercel.com/docs/functions/serverless-functions/python
- Flask on Vercel: https://vercel.com/docs/frameworks/flask

## Support

For issues or questions:
1. Check Vercel logs
2. Review this guide
3. Check GitHub issues
4. Contact Vercel support

---

**Your PDF MCQ Generator is now deployed on Vercel! 🎉**

**Deployment URL:** https://your-project.vercel.app

