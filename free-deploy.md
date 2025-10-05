# 🆓 Free Hosting Guide for GalamseyWatch

## 🌐 Frontend - Vercel (Free)

### Deploy Steps
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "GalamseyWatch initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/galamsey-watch.git
git push -u origin main

# 2. Deploy on Vercel
# Go to vercel.com
# Connect GitHub repo
# Auto-deploy ✅
```

**Free Limits:** Unlimited personal projects, 100GB bandwidth/month

## 🔧 Backend - Railway (Free)

### Deploy Steps
```bash
# 1. Create railway.json
echo '{"build": {"builder": "NIXPACKS"}, "deploy": {"startCommand": "cd api && python simple_main.py"}}' > railway.json

# 2. Deploy
# Go to railway.app
# Connect GitHub repo
# Select api folder as root
# Auto-deploy ✅
```

**Free Limits:** $5 credit/month, 500 hours runtime

## 🔄 Alternative: Render (Free)

### Backend on Render
```bash
# 1. Create render.yaml
cat > render.yaml << EOF
services:
  - type: web
    name: galamsey-api
    env: python
    buildCommand: "cd api && pip install -r ../requirements.txt"
    startCommand: "cd api && python simple_main.py"
    envVars:
      - key: PORT
        value: 10000
EOF

# 2. Deploy at render.com
# Connect GitHub repo ✅
```

**Free Limits:** 750 hours/month, sleeps after 15min inactivity

## 🌟 Recommended Free Stack

**Frontend:** Vercel (Best Next.js support)
**Backend:** Railway (Best Python support)

## 🔗 Environment Variables

**Vercel:**
- `NEXT_PUBLIC_API_URL` = `https://your-app.up.railway.app`

**Railway:**
- `GOOGLE_APPLICATION_CREDENTIALS` = (Upload service account JSON)
- `PORT` = `${{PORT}}` (Auto-provided)

## 📱 Your Live URLs

**Frontend:** `https://galamsey-watch.vercel.app`
**Backend:** `https://galamsey-watch-api.up.railway.app`

## 💡 Cost: $0/month

Both services offer generous free tiers perfect for hackathon projects and demos!