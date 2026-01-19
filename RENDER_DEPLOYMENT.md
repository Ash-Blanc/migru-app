# Deploy FastAPI Backend on Render.com (FREE - NO PAYMENT REQUIRED)

## Why Render?

✅ **Free tier** - Deploy without credit card  
✅ **Auto-deploy** from GitHub  
✅ **Automatic HTTPS** - SSL included  
✅ **Easy to use** - 5 minutes to deploy  
✅ **Docker support** - Simple container builds  

---

## Quick Start (5 minutes)

### Step 1: Sign Up with GitHub

1. Go to https://render.com
2. Click **"Sign up"** → **"GitHub"**
3. Authorize and complete GitHub OAuth
4. Email verification (check inbox)

### Step 2: Create New Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. **Select repository:** `migru-app`
3. Click **"Connect"**

### Step 3: Configure Service

**In the form, set:**

| Field | Value |
|-------|-------|
| **Name** | `migru-backend` |
| **Branch** | `main` |
| **Runtime** | `Python 3.11` |
| **Build Command** | `cd src/backend && pip install -r pyproject.toml` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| **Plan** | `Free` |

### Step 4: Set Environment Variables

Click **"Advanced"** and add variables if needed:

```
PORT=8000
PYTHONUNBUFFERED=1
```

### Step 5: Deploy

Click **"Create Web Service"** and wait ~3-5 minutes.

**Your backend URL:** `https://migru-backend.onrender.com` (or custom name)

---

## Alternative: Using render.yaml (Recommended)

You already have `render.yaml` in your repo! Just:

1. Go to https://render.com → **"Dashboard"**
2. Click **"New +"** → **"Web Service"**
3. Select `migru-app` repository
4. Render will auto-detect `render.yaml`
5. Click **"Deploy"**

That's it! Render reads all config from `render.yaml`.

---

## Update Frontend URL

Once backend is live, update Vercel environment:

1. Go to: https://vercel.com/kaizenlabs/migru-app/settings/environment-variables
2. Edit `PUBLIC_API_BASE_URL`
3. Change to: `https://migru-backend.onrender.com`
4. Save → Vercel auto-redeploys

---

## Testing Backend

Once deployed, test it:

```bash
curl https://migru-backend.onrender.com/health
# or check from Sveltekit:
# fetch('https://migru-backend.onrender.com/your-endpoint')
```

---

## Free Tier Limits

| Limit | Amount |
|-------|--------|
| **vCPU** | 0.5 |
| **RAM** | 512 MB |
| **Services** | 1 active web |
| **Bandwidth** | Unmetered |
| **Cold starts** | ~30s after 15 min inactivity |

### Cold Start Note:

After 15 minutes of no requests, Render puts services to sleep. First request takes ~30 seconds. Not an issue for active apps.

---

## Troubleshooting

### Deploy Failed

**Check logs:**
1. Render dashboard → Your service
2. Click **"Logs"** tab
3. Look for errors

### Common Issues

**"Build failed" → ModuleNotFoundError**
- Ensure `src/backend/pyproject.toml` exists with all dependencies
- Check build command: `cd src/backend && pip install -r pyproject.toml`

**"Port already in use"**
- Render auto-assigns port. Don't hardcode port 8000
- Use environment variable: `port = int(os.getenv('PORT', 8000))`

**"CORS Errors" from frontend**
- Add to `src/backend/app/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://migru-app.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Backend URL Shows Old Version**
- Render caches DNS. Wait 5 minutes or:
  - Go to service settings → **"Redeploy"**
  - Or push a new commit to trigger auto-deploy

---

## Auto-Deploy Setup

Render automatically deploys when you push to `main` branch. To disable:

1. Service settings → **"Auto-Deploy"**
2. Toggle **Off**
3. Manually deploy from **"Deploy"** button

---

## Upgrade (If Needed)

If you need more resources:
- Click **"Plan"** → Choose paid tier
- Billed hourly only while service is active
- Free tier will still be free for development

---

## Full Stack is Live! 🚀

✅ Frontend: `https://migru-app.vercel.app`  
✅ Backend: `https://migru-backend.onrender.com`  
✅ No payment needed  
✅ Auto-deploys on push
