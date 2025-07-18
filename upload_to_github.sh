#!/bin/bash

# Upload PDF MCQ Generator-sathish to GitHub
echo "🚀 Uploading PDF MCQ Generator-sathish to GitHub"
echo "=================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing Git repository..."
    git init
fi

# Add all files
echo "📁 Adding files to Git..."
git add .

# Check git status
echo "📋 Git status:"
git status

# Commit files
echo "💾 Committing files..."
git commit -m "Initial commit: PDF MCQ Generator-sathish with manual reference control

Features:
- Manual book name and chapter name input
- Multiple AI model support (OpenRouter, OpenAI, DeepSeek)
- PDF and CSV download functionality
- Clean explanations with user-controlled source references
- Vercel deployment ready

Project: PDF MCQ Generator-sathish"

echo "✅ Files committed successfully!"
echo ""
echo "🌐 Next Steps:"
echo "1. Create a new repository on GitHub named 'pdf-mcq-generator-sathish'"
echo "2. Copy the repository URL"
echo "3. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/pdf-mcq-generator-sathish.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Then deploy to Vercel:"
echo "   - Go to https://vercel.com/"
echo "   - Import your GitHub repository"
echo "   - Set environment variables (OPENROUTER_API_KEY, etc.)"
echo "   - Deploy!"
echo ""
echo "🎉 Your PDF MCQ Generator-sathish will be live on Vercel!"
