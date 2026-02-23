# Cache Clearing Instructions for PDF MCQ Generator v2.1.0

## Issue
The "📝 Generate Notes" button and PDF download features are not visible in production due to browser/CDN caching.

## Solution

### Step 1: Clear Browser Cache
Choose your browser:

#### Chrome/Edge (Windows/Linux)
1. Press `Ctrl + Shift + Delete`
2. Select "All time" from the time range
3. Check "Cookies and other site data" and "Cached images and files"
4. Click "Clear data"

#### Chrome/Edge (Mac)
1. Press `Cmd + Shift + Delete`
2. Select "All time" from the time range
3. Check "Cookies and other site data" and "Cached images and files"
4. Click "Clear data"

#### Firefox (All OS)
1. Press `Ctrl + Shift + Delete` (Windows/Linux) or `Cmd + Shift + Delete` (Mac)
2. Select "Everything" from the time range
3. Click "Clear Now"

#### Safari (Mac)
1. Click "Safari" menu → "Preferences"
2. Go to "Privacy" tab
3. Click "Manage Website Data"
4. Find the website and click "Remove"

### Step 2: Hard Refresh the Page
After clearing cache, do a hard refresh:

#### Windows/Linux
- Press `Ctrl + F5` or `Ctrl + Shift + R`

#### Mac
- Press `Cmd + Shift + R` or `Cmd + Option + R`

### Step 3: Verify Changes
After hard refresh, you should see:
1. ✅ "📝 Generate Notes" radio button option
2. ✅ "📄 Download as PDF" button for notes
3. ✅ Model selection dropdown for notes generation

## What Was Fixed

### Backend Changes (Vercel)
- Added cache-control headers to `vercel.json`
- Prevents caching of HTML files
- Ensures latest version is always served

### Frontend Changes
- Added cache-control meta tags to HTML
- Updated page title to include version number (v2.1.0)
- Forces browser to fetch fresh copy

## If Still Not Working

1. **Wait 5-10 minutes** - Vercel deployment may still be in progress
2. **Try a different browser** - Check if it's browser-specific
3. **Check browser console** - Press F12 and look for errors
4. **Disable browser extensions** - Some extensions cache aggressively
5. **Try incognito/private mode** - Bypasses most caching

## Latest Commits
- `88b9519` - fix: Add cache-control headers to vercel.json
- `5648519` - fix: Add cache-control headers and version to force browser cache refresh
- `cf9883d` - docs: Add deployment notes for v2.1.0 release
- `3f29767` - chore: Force Vercel redeploy for PDF notes export feature
- `e14e94c` - feat: Add PDF export for notes and allow user model selection

## Expected Features After Cache Clear

### Generate Notes Mode
- Select "📝 Generate Notes" from mode selector
- Choose any OpenRouter model from dropdown
- Upload PDF and click "Generate Notes"
- Notes will be generated using selected model

### Download Options
- 📋 Copy Notes - Copy to clipboard
- 📥 Download as Text - Download as .txt file
- 📄 Download as PDF - **NEW** - Download as formatted PDF

## Support
If issues persist after following these steps, check:
1. Browser developer console (F12) for JavaScript errors
2. Network tab to verify files are being fetched
3. Application tab to see what's cached

