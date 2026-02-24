# 🔧 Vercel maxDuration Fix - Free Plan Compatibility

## ❌ Problem

You received this error:
```
The value for maxDuration must be between 1 second and 300 seconds, 
in order to increase this limit upgrade your plan: https://vercel.com/pricing
```

## 🎯 Root Cause

The `vercel.json` configuration had `maxDuration` set to **900 seconds (15 minutes)**, but Vercel's **free plan only allows up to 300 seconds (5 minutes)**.

## ✅ Solution Applied

Changed `vercel.json` line 27:

**Before:**
```json
"maxDuration": 900,
```

**After:**
```json
"maxDuration": 300,
```

## 📊 Vercel Plan Limits

| Plan | Max Duration | Max Memory |
|------|-------------|-----------|
| **Free** | 300 seconds (5 min) | 3008 MB |
| **Pro** | 900 seconds (15 min) | 3008 MB |
| **Enterprise** | Custom | Custom |

## 🚀 What This Means

### ✅ What Works (Within 5 minutes)
- ✅ Login
- ✅ MCQ generation (small PDFs)
- ✅ Notes generation (small PDFs)
- ✅ PDF download
- ✅ PDF parsing
- ✅ PDF splitting

### ⚠️ What Might Timeout (Large PDFs)
- ⚠️ Very large PDF processing (>50 pages)
- ⚠️ Complex MCQ generation
- ⚠️ Large batch operations

## 💡 Tips for Staying Within 5-Minute Limit

1. **Use smaller PDFs** - Keep PDFs under 50 pages
2. **Reduce question count** - Generate 5-10 questions instead of 50
3. **Use faster models** - OpenRouter free models are optimized for speed
4. **Avoid complex operations** - Don't combine multiple features

## 💳 Upgrade Options

If you need longer timeouts:

### Option 1: Vercel Pro Plan
- **Cost:** $20/month
- **Max Duration:** 900 seconds (15 minutes)
- **Memory:** 3008 MB
- **Other benefits:** More deployments, analytics, etc.

### Option 2: Vercel Enterprise
- **Cost:** Custom pricing
- **Max Duration:** Custom
- **Memory:** Custom
- **Other benefits:** Dedicated support, SLA, etc.

**Upgrade:** https://vercel.com/pricing

## 📝 Configuration Details

**File:** `vercel.json`

**Current Configuration:**
```json
{
  "functions": {
    "api/index.py": {
      "maxDuration": 300,
      "memory": 3008
    }
  }
}
```

## ✅ Status

**✅ FIXED** - `maxDuration` set to 300 seconds for free plan compatibility

**Commit:** `8e14b62` - fix: Set maxDuration to 300 seconds for Vercel free plan compatibility

## 🔄 Next Steps

1. **Redeploy** - Vercel will auto-deploy the fix
2. **Wait 2-5 minutes** - For deployment to complete
3. **Test** - Try uploading a PDF and generating MCQs
4. **Monitor** - Check if operations complete within 5 minutes

## 🆘 If You Still Get Timeout Errors

### Option 1: Optimize Your PDFs
- Use smaller PDFs (< 50 pages)
- Reduce question count
- Use faster models

### Option 2: Upgrade Plan
- Go to https://vercel.com/pricing
- Select Pro plan ($20/month)
- Upgrade your project
- Change `maxDuration` back to 900 seconds

### Option 3: Use Different Provider
- Deploy on a different platform with longer timeouts
- Examples: AWS Lambda, Google Cloud Run, Heroku

## 📞 Support

If you need help:
1. Check Vercel logs: Settings → Function Logs
2. Try with a smaller PDF
3. Reduce question count
4. Consider upgrading plan

---

**Your application is now compatible with Vercel's free plan!** 🎉

