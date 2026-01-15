# 🚀 MindEase Deployment Guide

Complete guide to deploying MindEase to various platforms.

## 📋 Table of Contents

- [Quick Deploy (Streamlit Cloud)](#streamlit-cloud-recommended)
- [Heroku Deployment](#heroku-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Platforms (AWS/GCP/Azure)](#cloud-platforms)
- [Troubleshooting](#deployment-troubleshooting)

---

## 🌟 Streamlit Cloud (Recommended)

**Best for:** Demos, portfolios, free hosting

### Advantages
- ✅ **100% Free** for public repos
- ✅ **Zero configuration** needed
- ✅ **Auto-deploys** on git push
- ✅ **Built-in secrets** management
- ✅ **Perfect for demos** and showcasing

### Prerequisites
- GitHub account
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Step 1: Prepare Your Repository

```bash
# Navigate to MindEase folder
cd "E:\vs\Subham\projects\IBM SkillsBuild Applied AI Internship 2025  Capstone Project\MindEase"

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment setup"
```

### Step 2: Push to GitHub

**Option A: Using GitHub Desktop**
1. Open GitHub Desktop
2. Add this folder as repository
3. Publish to GitHub
4. Make repository public

**Option B: Using Command Line**
```bash
# Create new repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/mindease.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/mindease`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Advanced settings"**
6. In **Secrets** section, paste:
   ```toml
   GOOGLE_API_KEY = "AIzaSyC...your_actual_key_here"
   ```
7. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Initial deployment: 3-5 minutes
- Watch logs for any errors
- App will be live at: `https://YOUR_USERNAME-mindease.streamlit.app`

### Post-Deployment

**Share your app:**
- URL: `https://YOUR_USERNAME-mindease.streamlit.app`
- Add to README.md
- Share on LinkedIn/portfolio

**Auto-updates:**
- Every `git push` triggers redeployment
- Changes go live in 2-3 minutes

**Known Limitations:**
- Voice input (microphone) may not work (browser permissions)
- Voice output (TTS) works perfectly
- 1 GB RAM limit (sufficient for 10-50 users)

---

## 🟣 Heroku Deployment

**Best for:** More control, custom domains, production apps

### Prerequisites
- Heroku account ([sign up free](https://signup.heroku.com/))
- Heroku CLI installed
- Git repository

### Step 1: Install Heroku CLI

**Windows:**
```powershell
# Download and run installer from:
# https://devcenter.heroku.com/articles/heroku-cli
```

**macOS:**
```bash
brew tap heroku/brew && brew install heroku
```

**Linux:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create new app (name must be unique)
heroku create mindease-wellness-app

# Verify app created
heroku apps
```

### Step 3: Configure Environment

```bash
# Set API key
heroku config:set GOOGLE_API_KEY=AIzaSyC...your_key_here

# Verify
heroku config
```

### Step 4: Deploy

```bash
# Push to Heroku
git push heroku main

# Or if on different branch:
git push heroku your-branch:main

# Open app in browser
heroku open
```

### Step 5: Monitor Logs

```bash
# View real-time logs
heroku logs --tail

# View recent logs
heroku logs --num 100
```

### Heroku-Specific Files

All files already created:
- ✅ `Procfile` - Tells Heroku how to run app
- ✅ `setup.sh` - Configures Streamlit
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Dependencies

### Scaling on Heroku

```bash
# Check current dynos
heroku ps

# Scale up (for more users)
heroku ps:scale web=1

# Upgrade to hobby dyno ($7/month)
heroku dyno:type hobby
```

### Custom Domain

```bash
# Add custom domain
heroku domains:add www.mindease.com

# Get DNS target
heroku domains
```

---

## 🐳 Docker Deployment

**Best for:** Portability, local testing, cloud deployment

### Prerequisites
- Docker Desktop installed ([download](https://www.docker.com/products/docker-desktop))
- Docker account (for Docker Hub)

### Option 1: Docker Run

**Build image:**
```bash
cd "E:\vs\Subham\projects\IBM SkillsBuild Applied AI Internship 2025  Capstone Project\MindEase"

# Build
docker build -t mindease:latest .

# List images
docker images
```

**Run container:**
```bash
# Run with API key
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=AIzaSyC...your_key \
  mindease:latest

# Access at: http://localhost:8501
```

**Stop container:**
```bash
# List running containers
docker ps

# Stop container
docker stop <container_id>
```

### Option 2: Docker Compose

**Start services:**
```bash
# Create .env file first with:
# GOOGLE_API_KEY=AIzaSyC...your_key

# Start
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f
```

**Stop services:**
```bash
docker-compose down
```

### Publish to Docker Hub

```bash
# Login
docker login

# Tag image
docker tag mindease:latest YOUR_DOCKERHUB_USERNAME/mindease:latest

# Push
docker push YOUR_DOCKERHUB_USERNAME/mindease:latest

# Now anyone can run:
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_key \
  YOUR_DOCKERHUB_USERNAME/mindease:latest
```

---

## ☁️ Cloud Platforms

### AWS Elastic Beanstalk

**1. Install EB CLI:**
```bash
pip install awsebcli
```

**2. Initialize:**
```bash
eb init -p python-3.11 mindease-app --region us-east-1
```

**3. Create environment:**
```bash
eb create mindease-env
```

**4. Set environment variable:**
```bash
eb setenv GOOGLE_API_KEY=AIzaSyC...your_key
```

**5. Deploy:**
```bash
eb deploy
```

**6. Open app:**
```bash
eb open
```

### Google Cloud Run

**1. Install gcloud CLI**

**2. Deploy:**
```bash
gcloud run deploy mindease \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=AIzaSyC...your_key
```

**3. Access:**
```
Service URL: https://mindease-xxxxx-uc.a.run.app
```

### Azure App Service

**1. Install Azure CLI**

**2. Create app:**
```bash
az webapp up --name mindease-app --runtime "PYTHON|3.11"
```

**3. Set environment:**
```bash
az webapp config appsettings set \
  --name mindease-app \
  --resource-group <your-resource-group> \
  --settings GOOGLE_API_KEY=AIzaSyC...your_key
```

**4. Configure startup:**
```bash
az webapp config set \
  --name mindease-app \
  --startup-file "python -m streamlit run app.py --server.port=8000"
```

---

## 🔧 Deployment Troubleshooting

### Issue: App Not Starting

**Check logs:**
```bash
# Streamlit Cloud: View in dashboard
# Heroku: heroku logs --tail
# Docker: docker logs <container_id>
```

**Common causes:**
- Missing `GOOGLE_API_KEY` environment variable
- Port configuration issues
- Dependency installation failures

**Fix:**
```bash
# Verify environment variable set
heroku config  # Heroku
docker exec <container_id> env  # Docker

# Rebuild with clean cache
docker build --no-cache -t mindease:latest .
```

### Issue: PyAudio Installation Fails

**Cloud deployments may fail on PyAudio.**

**Solution:** App works without PyAudio - voice input disabled, all other features functional.

**In Dockerfile/buildpack, ensure:**
```bash
# Add system dependencies
apt-get install portaudio19-dev python3-pyaudio
```

### Issue: Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'streamlit'
```

**Fix:**
```bash
# Ensure requirements.txt is committed
git add requirements.txt
git commit -m "Add requirements"
git push

# For Heroku, trigger rebuild
heroku repo:purge_cache -a mindease-app
git commit --allow-empty -m "Rebuild"
git push heroku main
```

### Issue: Environment Variable Not Loading

**Check:**
1. Variable name exactly matches code: `GOOGLE_API_KEY`
2. No quotes in Streamlit Cloud secrets
3. Restart app after setting variable

**Streamlit Cloud:**
```toml
# Correct:
GOOGLE_API_KEY = "AIzaSy..."

# Wrong:
'GOOGLE_API_KEY' = 'AIzaSy...'
```

### Issue: Slow Performance

**Causes:**
- Free tier resource limits
- High traffic
- Large model responses

**Solutions:**
- Upgrade to paid tier
- Implement caching
- Optimize AI prompts for shorter responses

---

## 📊 Deployment Comparison

| Platform | Cost | Setup Time | Best For | Limitations |
|----------|------|------------|----------|-------------|
| **Streamlit Cloud** | Free | 5 min | Demos, portfolios | Public repos only, 1GB RAM |
| **Heroku** | Free-$7/mo | 15 min | Small apps | Sleeps after 30min inactivity |
| **Docker** | Varies | 30 min | Flexible deployment | Need hosting platform |
| **AWS/GCP/Azure** | Pay-as-go | 1-2 hours | Production | Complex setup |

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] `.env` in `.gitignore` (NEVER commit API keys!)
- [ ] `GOOGLE_API_KEY` ready to set in secrets
- [ ] All files committed to git
- [ ] Tested locally: `streamlit run app.py`
- [ ] `requirements.txt` up to date
- [ ] Deployment files present (Procfile, Dockerfile, etc.)
- [ ] Removed debug code/print statements

---

## 🎯 Quick Deploy Commands

**Streamlit Cloud:**
```bash
git push origin main
# Then deploy via web UI
```

**Heroku:**
```bash
git push heroku main
```

**Docker:**
```bash
docker-compose up -d
```

**Google Cloud:**
```bash
gcloud run deploy mindease --source .
```

---

## 📞 Support

**Deployment Help:**
- Streamlit: [discuss.streamlit.io](https://discuss.streamlit.io)
- Heroku: [help.heroku.com](https://help.heroku.com)
- Docker: [forums.docker.com](https://forums.docker.com)

**MindEase Issues:**
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review logs carefully
- Ensure all environment variables set

---

**🎉 Happy Deploying!**

Once deployed, share your MindEase app with the world! 🌍
