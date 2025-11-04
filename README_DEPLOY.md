# 🚀 RL Reality Dashboard - Deployment Guide

## Quick Deploy on Render

### Method 1: Auto Deploy
1. Fork this repo
2. Connect to Render
3. Auto-detects `render.yaml`
4. Deploy! 🎉

### Method 2: Manual Setup
**Repository:** `https://github.com/rityadani/RL_REALITY_VL.git`

**Settings:**
- **Name:** `rl-reality-dashboard`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn dashboard:app`
- **Environment Variables:**
  - `FLASK_ENV` = `production`
  - `PORT` = `10000`

## Local Development
```bash
pip install -r requirements.txt
python dashboard.py
```
Visit: http://localhost:8080

## Production Features
- ✅ Gunicorn WSGI server
- ✅ Environment-based configuration
- ✅ Production-ready dependencies
- ✅ Auto port detection
- ✅ Error handling

## Live Demo
After deployment, your dashboard will be available at:
`https://your-app-name.onrender.com`

## Support
- Dashboard runs on port 8080 (local) or PORT env var (production)
- User/Developer mode toggle
- Real-time RL metrics
- Policy drift monitoring