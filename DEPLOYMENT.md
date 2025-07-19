# Deployment Guide for PDF MCQ Generator-sathish

## 🚀 Deploy to Vercel

### Prerequisites
- GitHub account
- Vercel account (free)
- OpenRouter API key (get from https://openrouter.ai/)

### Step-by-Step Deployment

#### 1. Upload to GitHub
```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: PDF MCQ Generator-sathish"

# Add GitHub remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/pdf-mcq-generator-sathish.git

# Push to GitHub
git push -u origin main
```

#### 2. Deploy to Vercel

1. **Go to Vercel**: Visit https://vercel.com/
2. **Sign in**: Use your GitHub account
3. **Import Project**: Click "New Project" → "Import Git Repository"
4. **Select Repository**: Choose your `pdf-mcq-generator-sathish` repository
5. **Configure Project**:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: pip install -r requirements.txt

#### 3. Set Environment Variables

In Vercel dashboard → Project Settings → Environment Variables, add:

| Name | Value | Environment | Required |
|------|-------|-------------|----------|
| `OPENROUTER_API_KEY` | `sk-or-v1-xxxxx` | Production, Preview, Development | ✅ Yes |
| `OPENAI_API_KEY` | `sk-xxxxx` | Production, Preview, Development | ❌ Optional |
| `DEEPSEEK_API_KEY` | `sk-xxxxx` | Production, Preview, Development | ❌ Optional |

**Important**: Make sure to select all three environments (Production, Preview, Development) for each variable.

#### 4. Deploy

1. Click **"Deploy"**
2. Wait for build to complete
3. Your app will be available at: `https://your-project-name.vercel.app`

### 🔧 Configuration Files

The project includes these Vercel-specific files:

- **`vercel.json`**: Vercel deployment configuration
- **`index.py`**: Entry point for Vercel
- **`requirements.txt`**: Python dependencies
- **`.gitignore`**: Files to exclude from Git

### 🌐 Usage After Deployment

1. **Access your app**: Visit your Vercel URL
2. **Enter references**: 
   - Book Name: `POST OFFICE GUIDE-Part-I`
   - Chapter Name: `clause 108`
3. **Upload PDF**: Select your PDF file
4. **Generate MCQs**: Click generate button
5. **Download**: Get results as PDF or CSV

### 🔍 Troubleshooting

#### Build Errors
- Check that all files are committed to GitHub
- Verify `requirements.txt` includes all dependencies
- Ensure environment variables are set correctly

#### Runtime Errors
- Check Vercel function logs in dashboard
- Verify API keys are valid and have sufficient credits
- Ensure PDF files are not corrupted

#### API Issues
- OpenRouter API key is required for basic functionality
- Check API key permissions and rate limits
- Verify network connectivity to AI services

### 📱 Features Available in Deployed Version

✅ **Web Interface**: Full HTML interface with file upload
✅ **Manual Reference Control**: Book name and chapter name fields
✅ **Multiple AI Models**: OpenRouter, OpenAI, DeepSeek support
✅ **PDF Download**: Generate and download MCQ PDFs
✅ **CSV Export**: Download questions in CSV format
✅ **Responsive Design**: Works on desktop and mobile

### 🎯 Example Usage

**For Post Office Guide documents:**
1. Book Name: `POST OFFICE GUIDE-Part-I`
2. Chapter Name: `clause 108`
3. Result: `(Source: POST OFFICE GUIDE-Part-I, clause 108)`

**For other documents:**
- Leave fields empty for clean explanations
- Fill only book name for book-only references
- Fill only chapter for chapter-only references

### 🔄 Updates and Maintenance

To update your deployed app:
1. Make changes to your local code
2. Commit and push to GitHub
3. Vercel automatically redeploys on push
4. Check deployment status in Vercel dashboard

### 💡 Tips for Success

- **API Keys**: Keep your API keys secure and never commit them to Git
- **File Size**: Large PDFs may take longer to process
- **Rate Limits**: Be aware of API rate limits for your chosen AI service
- **Monitoring**: Use Vercel analytics to monitor usage and performance

Your PDF MCQ Generator-sathish is now ready for production use! 🎉
