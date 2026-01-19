# Full-Stack Deployment Guide for migru-app

## Overview

This guide covers deploying the migru-app full-stack application with:
- **Frontend (SvelteKit)**: Deployed on Vercel
- **Backend (FastAPI)**: Deployed on Fly.io

---

## Frontend Deployment (SvelteKit on Vercel)

### Already Completed ✓

Your SvelteKit frontend is already deployed on Vercel and configured with:
- Automatic deployments from the `main` branch
- Public API base URL environment variable set to `https://migru-backend.fly.dev`

**Frontend URL**: https://migru-app.vercel.app

---

## Backend Deployment (FastAPI on Fly.io)

### Prerequisites

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create Fly Account & Login**:
   ```bash
   flyctl auth login
   ```

3. **Add Payment Method** (required to deploy):
   - Visit https://fly.io/dashboard
   - Add a credit card (Free tier available with limits)

### Deployment Steps

1. **Clone/Navigate to Repo**:
   ```bash
   cd migru-app
   ```

2. **Deploy Backend**:
   ```bash
   flyctl launch
   ```
   When prompted:
   - App name: `migru-backend`
   - Region: Choose closest to you (e.g., `sjc` for US-West)
   - Use existing `fly.toml`? Yes
   - Postgres database? No (unless needed)

3. **Deploy**:
   ```bash
   flyctl deploy
   ```

4. **Get Your Backend URL**:
   ```bash
   flyctl info
   ```
   Your app will be at: `https://migru-backend.fly.dev` (or custom domain)

### Environment Variables (Optional)

If your FastAPI backend needs environment variables:

```bash
flyctl secrets set API_KEY=your_key
flyctl secrets set DATABASE_URL=your_db_url
```

---

## Connecting Frontend to Backend

### Current Configuration

The frontend is already configured to call your backend at:
```
https://migru-backend.fly.dev
```

This is set via the `PUBLIC_API_BASE_URL` environment variable in Vercel.

### Using in SvelteKit Code

```javascript
// In any SvelteKit component or endpoint
import { PUBLIC_API_BASE_URL } from '$env/static/public';

const response = await fetch(`${PUBLIC_API_BASE_URL}/your-endpoint`, {
  method: 'GET'
});
```

### If Backend URL Changes

1. Update the environment variable in Vercel:
   - Visit: https://vercel.com/kaizenlabs/migru-app/settings/environment-variables
   - Update `PUBLIC_API_BASE_URL` to your new backend URL
   - Vercel will auto-redeploy

2. Or update in `fly.toml` and redeploy:
   ```bash
   flyctl deploy
   ```

---

## Monitoring & Debugging

### View Backend Logs
```bash
flyctl logs
```

### View Backend Status
```bash
flyctl status
```

### SSH into Backend
```bash
flyctl ssh console
```

### Restart Backend
```bash
flyctl restart
```

---

## CORS Configuration

If you get CORS errors, ensure your FastAPI backend allows Vercel origin:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://migru-app.vercel.app", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Troubleshooting

### 404 Not Found from Frontend
- Check `PUBLIC_API_BASE_URL` is correct
- Verify backend is running: `flyctl status`
- Check backend logs: `flyctl logs`

### CORS Errors
- Add Vercel domain to FastAPI `allow_origins`
- Test backend directly: `curl https://migru-backend.fly.dev/health`

### Slow Response Times
- Check Fly region is close to users
- Monitor CPU/Memory: `flyctl status`
- Scale if needed: `flyctl scale vm shared-cpu-1x --count 2`

### Backend Won't Start
- Check Dockerfile: `Dockerfile.backend`
- Review logs: `flyctl logs --all`
- Test locally: `docker build -f Dockerfile.backend -t migru .`

---

## Cost Estimates (Fly.io Free Tier)

- **Free**: 3 shared-cpu-1x 256MB VMs
- **Includes**: 160GB bandwidth/month
- **Overage**: ~$0.15/GB after free tier

---

## Next Steps

1. ✓ Frontend deployed
2. → Backend deployment (follow above)
3. → Test full-stack integration
4. → Custom domain setup (optional)
5. → Database setup (if needed)

