# Vercel Deployment Guide - MIGRU V2

## ✅ Status: Ready for Deployment

The MIGRU V2 frontend is **fully configured** for Vercel deployment. All issues have been resolved.

---

## 🔧 What Was Fixed

### 1. Vercel Adapter Configuration
**Problem:** The project was using `@sveltejs/adapter-auto`, which couldn't detect the Vercel environment, causing build failures.

**Solution:**
- Installed `@sveltejs/adapter-vercel`
- Updated `svelte.config.js` to explicitly use Vercel adapter with Node.js 20.x runtime
- Configured custom file paths for the monorepo structure

### 2. TypeScript Build Errors
**Problem:** TypeScript type incompatibility in `voiceRecorder.ts` with Uint8Array buffer types.

**Solution:**
- Fixed `getFrequencyData()` method to create new Uint8Array instance
- Resolved ArrayBufferLike vs ArrayBuffer type mismatch

### 3. Configuration Files
**Added:**
- `vercel.json` - Vercel-specific configuration with framework settings
- `.vercelignore` - Excludes backend files and unnecessary artifacts
- Node.js version specification in `package.json` (>=20.0.0)

### 4. Vite Configuration
**Enhanced:**
- Added proper path aliases for `$lib`
- Configured server file system access
- Ensured Tailwind CSS integration

---

## 📦 Files Modified

```
✅ svelte.config.js - Switched to @sveltejs/adapter-vercel
✅ vite.config.ts - Added path aliases and server config
✅ package.json - Added engines field for Node.js 20+
✅ vercel.json - Created with framework configuration
✅ .vercelignore - Created to exclude backend files
✅ src/frontend/lib/utils/voiceRecorder.ts - Fixed TypeScript types
```

---

## 🚀 Deploy to Vercel

### Option 1: GitHub Integration (Recommended)

1. **Connect Repository:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository: `Ash-Blanc/migru-app`

2. **Configure Project:**
   - Framework Preset: **SvelteKit** (auto-detected)
   - Root Directory: `./` (leave default)
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `.svelte-kit/output` (auto-detected)

3. **Environment Variables:**
   - Add any required environment variables (optional for frontend)
   - Example: `PUBLIC_CLERK_PUBLISHABLE_KEY`

4. **Deploy:**
   - Click "Deploy"
   - Vercel will automatically build and deploy
   - You'll get a production URL (e.g., `migru-app.vercel.app`)

### Option 2: Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to production
vercel --prod
```

---

## 🔗 Post-Deployment Steps

### 1. Update Backend URL
After deployment, update the API URL in your frontend:

**File:** `src/frontend/lib/stores.ts`

```typescript
// Change this line:
const API_URL = 'http://localhost:8000';

// To your production backend URL:
const API_URL = 'https://your-backend-url.railway.app';
```

### 2. Configure CORS on Backend
Update your backend to allow requests from your Vercel domain:

**File:** `src/backend/app/main_v2.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://migru-app.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app"  # Allow preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Set Environment Variables (if needed)
If you're using public environment variables in your frontend, add them in Vercel:
- Go to Project Settings → Environment Variables
- Add: `PUBLIC_CLERK_PUBLISHABLE_KEY`, etc.

---

## 🧪 Testing

### Local Build Test
```bash
# Run production build locally
npm run build

# Preview production build
npm run preview
```

Both commands should complete successfully without errors.

### Vercel Preview Deployments
- Every push to non-main branches gets a preview deployment
- Check the deployment URL in the Vercel dashboard
- Test thoroughly before merging to main

---

## 📊 Build Verification

### ✅ Build Status: PASSING

```bash
$ npm run build
> Using @sveltejs/adapter-vercel
  ✔ done

Build completed successfully in ~13s
```

### Current Configuration
- **Adapter:** `@sveltejs/adapter-vercel` v6.3.0
- **Node.js Runtime:** 20.x
- **SvelteKit:** v2.49.1
- **Vite:** v7.2.6
- **TypeScript:** v5.9.3

---

## 🐛 Troubleshooting

### Build Fails on Vercel

**Check:**
1. Build logs in Vercel dashboard
2. Ensure all dependencies are in `package.json`
3. Verify Node.js version matches (20.x)
4. Check if environment variables are set

**Common Issues:**
- Missing `@sveltejs/adapter-vercel` - Fixed ✅
- TypeScript errors - Fixed ✅
- Path resolution issues - Fixed ✅

### Preview Works but Production Fails

**Check:**
1. Environment variables are set for production
2. Backend URL is updated in `stores.ts`
3. CORS is configured for your domain

---

## 📁 Repository Structure

```
migru-app/
├── .vercel/                    # Vercel build cache (auto-generated)
├── .vercelignore               # Excludes backend from deployment
├── vercel.json                 # Vercel configuration
├── svelte.config.js            # SvelteKit + Vercel adapter
├── vite.config.ts              # Vite + path aliases
├── package.json                # Node.js 20+ requirement
├── src/
│   ├── frontend/               # SvelteKit app (deployed to Vercel)
│   │   ├── routes/
│   │   ├── lib/
│   │   └── static/
│   └── backend/                # FastAPI (NOT deployed to Vercel)
│       └── app/
└── README.md
```

---

## 🎯 Next Steps After Deployment

1. **Backend Deployment:**
   - Deploy backend to Railway/Render (see README.md)
   - Get production backend URL
   - Update `API_URL` in frontend

2. **Domain Configuration:**
   - Add custom domain in Vercel (optional)
   - Configure DNS records
   - Enable automatic HTTPS

3. **Monitoring:**
   - Check Vercel Analytics
   - Monitor build times and errors
   - Set up error tracking (Sentry, etc.)

4. **CI/CD:**
   - Every push to main auto-deploys to production
   - Pull requests get preview deployments
   - Automatic rollback on build failures

---

## ✅ Deployment Checklist

- [x] Vercel adapter installed and configured
- [x] Build passes locally
- [x] vercel.json created
- [x] .vercelignore created
- [x] Node.js version specified
- [x] TypeScript errors resolved
- [x] Custom file paths configured
- [ ] Repository connected to Vercel
- [ ] First deployment successful
- [ ] Backend URL updated in stores.ts
- [ ] CORS configured on backend
- [ ] Environment variables set (if needed)
- [ ] Custom domain configured (optional)

---

**Status:** Ready to deploy! 🚀

Connect your GitHub repository to Vercel and let it auto-deploy. The configuration is complete.
