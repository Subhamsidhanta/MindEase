# 🚀 Quick Deployment Reference

## One-Command Deploy

### Streamlit Cloud (Easiest - 5 minutes)
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy MindEase"
git remote add origin https://github.com/YOUR_USERNAME/mindease.git
git push -u origin main

# 2. Go to share.streamlit.io and deploy
# 3. Add secret: GOOGLE_API_KEY = "your_key"
# ✅ Done! App live at https://YOUR_USERNAME-mindease.streamlit.app
```

### Docker (Run Locally)
```bash
# Build and run
docker-compose up -d

# Access at http://localhost:8501
```

### Heroku (Production Ready)
```bash
# Deploy
heroku create mindease-app
heroku config:set GOOGLE_API_KEY=your_key
git push heroku main
heroku open
```

---

## 📁 Required Files (All Included)

- ✅ `Dockerfile` - Docker container config
- ✅ `docker-compose.yml` - Docker Compose config  
- ✅ `Procfile` - Heroku config
- ✅ `setup.sh` - Heroku setup script
- ✅ `runtime.txt` - Python 3.11 specification
- ✅ `packages.txt` - System dependencies
- ✅ `.streamlit/config.toml` - Streamlit settings
- ✅ `.gitignore` - Prevents committing secrets
- ✅ `.env.example` - Environment template

---

## 🔑 Environment Variables

**All platforms need:**
```
GOOGLE_API_KEY=AIzaSyC...your_actual_key_here
```

**Get free key:** https://aistudio.google.com/app/apikey

---

## ✅ Pre-Deploy Checklist

- [ ] API key ready
- [ ] `.env` in `.gitignore` 
- [ ] Tested locally: `streamlit run app.py`
- [ ] All files committed to git

---

## 🌐 Platform URLs

| Platform | URL Format | Time |
|----------|------------|------|
| Streamlit Cloud | `https://username-mindease.streamlit.app` | 5 min |
| Heroku | `https://mindease-app.herokuapp.com` | 15 min |
| Docker | `http://localhost:8501` | 10 min |

---

## 🆘 Quick Troubleshooting

**App won't start?**
```bash
# Check logs
heroku logs --tail  # Heroku
docker logs <container_id>  # Docker
```

**Missing API key?**
```bash
# Verify environment variable
heroku config  # Heroku
docker exec <container_id> env  # Docker
```

**PyAudio fails?**
- App still works (voice input disabled, TTS works)
- Solution: Included in `packages.txt` and `Dockerfile`

---

**Full guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)
