# GitHub Upload - Visual Step-by-Step Guide 📸

## Step 1: Create Repository on GitHub

```
┌─────────────────────────────────────────────────────────┐
│  GitHub.com                                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Click "+" icon (top right)                          │
│  2. Select "New repository"                             │
│  3. Fill in details:                                    │
│     ├─ Repository name: pdfmcq                          │
│     ├─ Description: PDF MCQ Generator...                │
│     ├─ Visibility: Public                               │
│     └─ Initialize: Leave unchecked                      │
│  4. Click "Create repository"                           │
│  5. Copy HTTPS URL                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 2: Open Terminal

```
┌─────────────────────────────────────────────────────────┐
│  Terminal / Command Prompt                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ cd /Volumes/sathish/pdfmcq                           │
│                                                          │
│  You should see your project files                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 3: Initialize Git

```
┌─────────────────────────────────────────────────────────┐
│  Terminal Commands                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ git init                                             │
│  Initialized empty Git repository                       │
│                                                          │
│  $ git config user.name "Your Name"                     │
│  $ git config user.email "your.email@example.com"       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 4: Add Files

```
┌─────────────────────────────────────────────────────────┐
│  Terminal Commands                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ git add .                                            │
│                                                          │
│  This stages all files for commit                       │
│  (except those in .gitignore)                           │
│                                                          │
│  Files added:                                           │
│  ├─ flask_app.py                                        │
│  ├─ app.py                                              │
│  ├─ mcq_generator.py                                    │
│  ├─ templates/                                          │
│  ├─ static/                                             │
│  ├─ README.md                                           │
│  └─ ... (and more)                                      │
│                                                          │
│  Files NOT added (in .gitignore):                       │
│  ├─ .env                                                │
│  ├─ __pycache__/                                        │
│  ├─ venv/                                               │
│  └─ uploads/                                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 5: Create Commit

```
┌─────────────────────────────────────────────────────────┐
│  Terminal Commands                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ git commit -m "Initial commit: PDF MCQ Generator     │
│    with amendment analysis"                             │
│                                                          │
│  Output:                                                │
│  [main (root-commit) abc1234] Initial commit...         │
│   50 files changed, 5000+ insertions(+)                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 6: Add Remote Repository

```
┌─────────────────────────────────────────────────────────┐
│  Terminal Commands                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ git remote add origin                                │
│    https://github.com/yourusername/pdfmcq.git          │
│                                                          │
│  This connects your local repo to GitHub                │
│                                                          │
│  Verify:                                                │
│  $ git remote -v                                        │
│  origin  https://github.com/yourusername/pdfmcq.git    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 7: Push to GitHub

```
┌─────────────────────────────────────────────────────────┐
│  Terminal Commands                                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  $ git branch -M main                                   │
│  $ git push -u origin main                              │
│                                                          │
│  When prompted:                                         │
│  Username: yourusername                                 │
│  Password: your_personal_access_token                   │
│                                                          │
│  Output:                                                │
│  Enumerating objects: 50, done.                         │
│  Counting objects: 100% (50/50), done.                  │
│  ...                                                    │
│  To https://github.com/yourusername/pdfmcq.git         │
│   * [new branch]      main -> main                      │
│  Branch 'main' set up to track remote branch 'main'     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Step 8: Verify on GitHub

```
┌─────────────────────────────────────────────────────────┐
│  GitHub.com                                             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Visit: https://github.com/yourusername/pdfmcq         │
│                                                          │
│  You should see:                                        │
│  ├─ File list (flask_app.py, app.py, etc.)             │
│  ├─ README.md displayed with formatting                │
│  ├─ Commit history showing your commit                 │
│  ├─ Branch: main                                        │
│  └─ "X commits" in the top bar                          │
│                                                          │
│  ✅ Success!                                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Complete Command Flow

```
┌──────────────────────────────────────────────────────────┐
│                                                           │
│  1. GitHub.com                                           │
│     └─ Create repository                                │
│        └─ Copy HTTPS URL                                │
│                                                           │
│  2. Terminal                                             │
│     ├─ cd /Volumes/sathish/pdfmcq                       │
│     ├─ git init                                          │
│     ├─ git config user.name "Your Name"                │
│     ├─ git config user.email "your.email@example.com"  │
│     ├─ git add .                                         │
│     ├─ git commit -m "Initial commit..."                │
│     ├─ git remote add origin [HTTPS URL]                │
│     ├─ git branch -M main                               │
│     └─ git push -u origin main                          │
│        └─ Enter credentials                             │
│                                                           │
│  3. GitHub.com                                           │
│     └─ Verify files are uploaded                        │
│                                                           │
│  ✅ Done!                                                │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## File Structure After Upload

```
GitHub Repository
│
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 flask_app.py
├── 📄 app.py
├── 📄 mcq_generator.py
├── 📄 mcq_parser.py
│
├── 📁 templates/
│   ├── index.html
│   ├── results.html
│   └── styles.css
│
├── 📁 static/
│   └── js/
│       └── script.js
│
├── 📁 Documentation/
│   ├── GITHUB_QUICK_START.md
│   ├── GITHUB_UPLOAD_GUIDE.md
│   ├── AMENDMENT_FEATURE_QUICK_START.md
│   └── ... (more docs)
│
└── 📁 pdfmcq1/
    ├── mcq_generator.py
    └── ... (other files)

NOT uploaded (in .gitignore):
├── .env
├── __pycache__/
├── venv/
├── uploads/
└── *.pyc
```

## Troubleshooting Visual Guide

```
Problem: "fatal: not a git repository"
Solution:
  $ cd /Volumes/sathish/pdfmcq
  $ git init

Problem: "remote origin already exists"
Solution:
  $ git remote remove origin
  $ git remote add origin https://github.com/yourusername/pdfmcq.git

Problem: "Authentication failed"
Solution:
  1. Generate personal access token at:
     https://github.com/settings/tokens
  2. Use token as password (not your GitHub password)
  3. Ensure token has 'repo' scope

Problem: ".env file is visible on GitHub"
Solution:
  $ git rm --cached .env
  $ git commit -m "Remove .env from tracking"
  $ git push
  (Then regenerate any exposed credentials)
```

## Success Checklist

```
✅ Repository created on GitHub
✅ Local git initialized
✅ Files added and committed
✅ Remote repository connected
✅ Files pushed to GitHub
✅ All files visible on GitHub
✅ README displays correctly
✅ No .env file visible
✅ Commit history shows your commit
✅ Repository URL works

🎉 Your project is on GitHub!
```

## Next Steps

```
After successful upload:

1. Share the URL
   https://github.com/yourusername/pdfmcq

2. Add collaborators (optional)
   Settings → Collaborators

3. Enable features (optional)
   Settings → Features → Discussions

4. Create releases (optional)
   Releases tab → Create new release

5. Keep updating
   Make commits as you improve the project
```

---

**Visual Guide Complete!** 📸

For detailed information, see:
- GITHUB_QUICK_START.md - Quick reference
- GITHUB_UPLOAD_GUIDE.md - Detailed guide
- GITHUB_UPLOAD_CHECKLIST.md - Verification

