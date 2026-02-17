# GitHub Upload Guide 🚀

Complete step-by-step guide to upload your PDF MCQ Generator project to GitHub.

## Prerequisites

- GitHub account (create at https://github.com if needed)
- Git installed on your machine
- Terminal/Command Prompt access

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name:** `pdfmcq`
   - **Description:** "PDF MCQ Generator - AI-powered question generation with amendment analysis"
   - **Visibility:** Public (recommended for open source)
   - **Initialize repository:** Leave unchecked
3. Click "Create repository"
4. Copy the HTTPS URL shown (e.g., `https://github.com/yourusername/pdfmcq.git`)

### Option B: Using GitHub CLI
```bash
gh repo create pdfmcq --public --source=. --remote=origin --push
```

## Step 2: Configure Git Locally

Open Terminal and navigate to your project:

```bash
cd /Volumes/sathish/pdfmcq
```

### Initialize Git Repository

```bash
# Initialize git
git init

# Configure git user (if not already configured)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Or configure globally
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Add Files and Create Initial Commit

```bash
# Check git status
git status

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: PDF MCQ Generator with amendment analysis feature

- Core MCQ generation from PDF documents
- Amendment analysis and comparison
- Multiple export formats (Web, CSV, PDF, JSON)
- 7 mandatory quality rules enforcement
- Support for multiple AI providers (OpenAI, OpenRouter, DeepSeek)
- Flask and Streamlit web interfaces"
```

## Step 4: Add Remote Repository

Replace `yourusername` with your GitHub username:

```bash
# Add remote origin
git remote add origin https://github.com/yourusername/pdfmcq.git

# Verify remote
git remote -v
```

## Step 5: Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main

# You'll be prompted for GitHub credentials
# Use your GitHub username and personal access token (not password)
```

## Creating GitHub Personal Access Token

If you get authentication errors:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. Use token as password when prompted

## Step 6: Verify Upload

1. Go to https://github.com/yourusername/pdfmcq
2. Verify all files are present
3. Check that README.md displays correctly

## Step 7: Add Additional Files (Optional)

### Create LICENSE File
```bash
# MIT License (recommended)
curl https://opensource.org/licenses/MIT > LICENSE
git add LICENSE
git commit -m "Add MIT License"
git push
```

### Create CONTRIBUTING.md
```bash
# Create contribution guidelines
cat > CONTRIBUTING.md << 'EOF'
# Contributing to PDF MCQ Generator

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Add docstrings to functions
- Include type hints where possible

## Testing

- Write tests for new features
- Run tests before submitting PR
- Ensure all tests pass

## Reporting Issues

- Use GitHub Issues for bug reports
- Include detailed description
- Provide steps to reproduce
- Include error messages and logs
EOF

git add CONTRIBUTING.md
git commit -m "Add contribution guidelines"
git push
```

## Step 8: Update Project Settings (Optional)

### Add Topics
1. Go to your repository
2. Click "About" (gear icon)
3. Add topics: `python`, `mcq`, `pdf`, `ai`, `education`

### Enable Discussions
1. Go to Settings → Features
2. Enable "Discussions"

### Add Branch Protection
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Require pull request reviews

## Subsequent Updates

After initial upload, to push new changes:

```bash
# Make your changes
# ...

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# View remote
git remote -v

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout branch-name

# Merge branch
git merge branch-name

# Delete branch
git branch -d branch-name

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View differences
git diff
```

## Troubleshooting

### Authentication Failed
- Use personal access token instead of password
- Check token has `repo` scope
- Regenerate token if expired

### Remote Already Exists
```bash
git remote remove origin
git remote add origin https://github.com/yourusername/pdfmcq.git
```

### Large Files
- Use `.gitignore` to exclude large files
- Consider Git LFS for large files
- Remove from history if accidentally added

### Merge Conflicts
```bash
# View conflicts
git status

# Resolve conflicts manually
# Then:
git add .
git commit -m "Resolve merge conflicts"
git push
```

## Best Practices

✅ **Do:**
- Write clear commit messages
- Use `.gitignore` properly
- Keep commits focused and small
- Write descriptive pull requests
- Document your code

❌ **Don't:**
- Commit sensitive data (.env files)
- Commit large binary files
- Force push to main branch
- Ignore merge conflicts
- Leave commented code

## Next Steps

1. ✅ Repository created
2. ✅ Files uploaded
3. ✅ README configured
4. 📋 Add GitHub Actions for CI/CD (optional)
5. 📋 Set up issue templates (optional)
6. 📋 Create release tags (optional)

## Resources

- [GitHub Docs](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)
- [Markdown Guide](https://www.markdownguide.org)

---

**Your project is now on GitHub! 🎉**

Share the repository URL with others:
`https://github.com/yourusername/pdfmcq`

