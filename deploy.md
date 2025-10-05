# 🚀 GalamseyWatch Deployment Guide

## 🌐 Frontend Deployment (Vercel)

### 1. Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
vercel --prod
```

### 2. Environment Variables
Set in Vercel dashboard:
- `NEXT_PUBLIC_API_URL` = `https://your-backend-url.herokuapp.com`

## 🔧 Backend Deployment (Heroku)

### 1. Setup Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create galamsey-watch-api

# Set Python buildpack
heroku buildpacks:set heroku/python -a galamsey-watch-api
```

### 2. Environment Variables
```bash
# Set Earth Engine credentials
heroku config:set GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json -a galamsey-watch-api

# Set NASA credentials (if needed)
heroku config:set NASA_USERNAME=your_username -a galamsey-watch-api
heroku config:set NASA_PASSWORD=your_password -a galamsey-watch-api
```

### 3. Deploy Backend
```bash
# From api directory
cd api
git init
git add .
git commit -m "Initial commit"
heroku git:remote -a galamsey-watch-api
git push heroku main
```

## 🔗 Alternative: Railway Deployment

### Backend (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Environment Variables
Set in Railway dashboard:
- `GOOGLE_APPLICATION_CREDENTIALS`
- `NASA_USERNAME`
- `NASA_PASSWORD`

## 📱 Access Your App

**Frontend:** https://galamsey-watch.vercel.app
**Backend:** https://galamsey-watch-api.herokuapp.com

## 🛠️ Local Development
```bash
# Frontend
npm run dev

# Backend
source venv/bin/activate && cd api && python simple_main.py
```