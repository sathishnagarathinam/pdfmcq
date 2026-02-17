# GitHub Upload - Quick Start 🚀

**5-Minute Quick Reference for Uploading to GitHub**

## 1️⃣ Create Repository on GitHub

Visit: https://github.com/new

```
Repository name: pdfmcq
Description: PDF MCQ Generator with amendment analysis
Visibility: Public
Initialize: Leave unchecked
```

Click "Create repository" and copy the HTTPS URL

## 2️⃣ Open Terminal

```bash
cd /Volumes/sathish/pdfmcq
```

## 3️⃣ Initialize Git

```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 4️⃣ Add and Commit Files

```bash
git add .
git commit -m "Initial commit: PDF MCQ Generator with amendment analysis"
```

## 5️⃣ Add Remote and Push

Replace `yourusername` with your GitHub username:

```bash
git remote add origin https://github.com/yourusername/pdfmcq.git
git branch -M main
git push -u origin main
```

## 6️⃣ Enter Credentials

When prompted:
- **Username:** Your GitHub username
- **Password:** Your personal access token (not password!)

## 7️⃣ Verify

Visit: https://github.com/yourusername/pdfmcq

✅ All files should be visible!

---

## 📝 Complete Command Sequence

Copy and paste this entire block:

```bash
cd /Volumes/sathish/pdfmcq

git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: PDF MCQ Generator with amendment analysis"
git remote add origin https://github.com/yourusername/pdfmcq.git
git branch -M main
git push -u origin main
```

**Replace:**
- `Your Name` - Your actual name
- `your.email@example.com` - Your email
- `yourusername` - Your GitHub username

---

## 🔑 Getting Personal Access Token

If you don't have a token:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token"
3. Name: `pdfmcq-upload`
4. Select: `repo` and `workflow`
5. Click "Generate token"
6. Copy the token (you won't see it again!)
7. Use as password when prompted

---

## ✅ Verification Checklist

After pushing:

- [ ] Visit https://github.com/yourusername/pdfmcq
- [ ] See all your files listed
- [ ] README.md displays correctly
- [ ] No sensitive files visible (.env, API keys)
- [ ] Commit message visible in history

---

## 🆘 Common Issues

### "fatal: not a git repository"
```bash
cd /Volumes/sathish/pdfmcq
git init
```

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/yourusername/pdfmcq.git
```

### "Authentication failed"
- Use personal access token, not password
- Token must have `repo` scope
- Check token hasn't expired

### ".env file visible"
- Add to .gitignore
- Remove from history: `git rm --cached .env`
- Commit: `git commit -m "Remove .env from tracking"`

---

## 📚 Next Steps

After successful upload:

1. **Share the link:** https://github.com/yourusername/pdfmcq
2. **Add collaborators:** Settings → Collaborators
3. **Enable discussions:** Settings → Features
4. **Create releases:** Releases tab
5. **Add topics:** About section

---

## 🎯 What Gets Uploaded

✅ **Included:**
- All Python files (.py)
- HTML/CSS/JS files
- Documentation (.md)
- Configuration files
- Requirements.txt

❌ **Excluded (by .gitignore):**
- .env files
- __pycache__/
- venv/
- uploads/
- *.pyc
- .DS_Store

---

## 💡 Pro Tips

1. **Commit often** - Small, focused commits are better
2. **Write good messages** - Describe what and why
3. **Use branches** - Create feature branches for new work
4. **Pull before push** - Avoid conflicts
5. **Review before commit** - Check what you're committing

---

**Your project is now on GitHub! 🎉**

For detailed guide, see: `GITHUB_UPLOAD_GUIDE.md`

