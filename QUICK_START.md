# MIGRU V2 - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites
- **uv** (Python 3.11 package manager) - [Install here](https://github.com/astral-sh/uv)
- **Node.js 18+** - [Install here](https://nodejs.org)

### Step 1: Install Backend Dependencies
```bash
cd src/backend
uv sync
```
uv will automatically set up a virtual environment with Python 3.11 and install all dependencies.

### Step 2: Initialize Database
```bash
uv run python -c "from app.database import init_db; init_db()"
```
This creates `migru.db` with all tables.

### Step 3: Set Environment Variables
Create `src/backend/.env`:
```env
DEV_MODE=true
CLERK_PUBLISHABLE_KEY=your_key_here
HUME_API_KEY=your_hume_key (optional)
HUME_SECRET_KEY=your_hume_secret (optional)
```

### Step 4: Start Backend
```bash
cd src/backend
uv run uvicorn app.main_v2:app --reload --port 8000
```

Visit http://localhost:8000/health to verify.

### Step 5: Install Frontend Dependencies
```bash
cd src/frontend
npm install
```

### Step 6: Start Frontend
```bash
npm run dev
```

Visit http://localhost:5173

---

## 🎯 Test the New Features

### 1. Test Analytics Dashboard
Navigate to `/analytics` - you'll see:
- Weekly voice check-in progress
- Migraine reduction tracking
- Streak visualization
- Engagement metrics

### 2. Test Onboarding Flow
Navigate to `/onboarding` - 4-step wizard:
1. Welcome screen
2. Voice baseline (placeholder - needs Web Audio API implementation)
3. Migraine history intake
4. Tone preference selection

### 3. Test Voice Analysis API
```bash
# Get user status
curl http://localhost:8000/api/status \
  -H "Authorization: Bearer dev_token"

# Get 48h forecast
curl http://localhost:8000/api/forecast \
  -H "Authorization: Bearer dev_token"

# Log attack
curl -X POST http://localhost:8000/api/logs \
  -H "Authorization: Bearer dev_token" \
  -H "Content-Type: application/json" \
  -d '{
    "severity": 7,
    "primary_symptoms": ["Nausea", "Light Sensitivity"],
    "triggers": ["Stress"],
    "notes": "Started after stressful meeting"
  }'

# Get analytics
curl http://localhost:8000/api/analytics \
  -H "Authorization: Bearer dev_token"
```

### 4. Test Intervention System
```bash
# Start intervention
curl -X POST http://localhost:8000/api/interventions \
  -H "Authorization: Bearer dev_token" \
  -H "Content-Type: application/json" \
  -d '{"context": {"stress_score": 75}}'
```

You'll get a Milton Model NLP script with breathing instructions!

---

## 📊 What Got Built

### Database (SQLite)
✅ 6 tables with proper relationships:
- `users` - user profiles with Clerk ID, onboarding status, voice baseline
- `migraine_logs` - attack records with symptoms/triggers
- `voice_sessions` - biomarker analysis per session
- `predictions` - 48h forecasts with validation tracking
- `interventions` - therapeutic delivery with efficacy logging
- `user_analytics` - KPI tracking

### Backend (Python/FastAPI)
✅ 4-agent system:
1. **Voice Analysis Agent** - biomarker extraction (pitch, tempo, jitter, shimmer, tremor)
2. **Pattern Recognition Agent** - temporal patterns, 48h predictions
3. **Intervention Agent** - Milton Model NLP scripts, tone matching
4. **Hume Integration Agent** - emotion sync, token management

✅ 30+ API endpoints for health tracking, voice analysis, interventions, analytics

### Frontend (SvelteKit)
✅ New pages:
- `/onboarding` - 4-step wizard
- `/analytics` - KPI dashboard

✅ Existing pages enhanced:
- Dashboard, Log, Active Relief, Settings, Diagnostics

---

## 🔧 What Still Needs Implementation

### High Priority
1. **Voice Recording in Onboarding**
   - Implement Web Audio API in `/onboarding` page
   - Capture 30s baseline audio
   - Send to `/api/voice/baseline` endpoint

2. **Hume EVI Full Integration**
   - Update `VoiceAgent.svelte` to use V2 endpoints
   - Sync emotion scores to database
   - Use personalized system prompts

3. **Intervention Audio Playback**
   - TTS for intervention scripts
   - Breathing timer with visual/audio cues

### Medium Priority
4. **Charts & Visualizations**
   - Migraine frequency over time
   - Stress score trends
   - Prediction accuracy graphs

5. **Notifications**
   - Push notifications for high-risk predictions
   - Daily check-in reminders
   - Streak celebration

6. **Data Export**
   - CSV export of logs
   - PDF health reports

### Low Priority
7. **Weather API Integration**
   - Real-time barometric pressure
   - Weather correlation analysis

8. **Advanced Voice Analysis**
   - Upgrade to ONNX Runtime models
   - More sophisticated pitch tracking (librosa/parselmouth)

---

## 🎓 Learning Resources

### Milton Model NLP
See examples in `app/agents/intervention.py`:
- Presuppositions: "As you begin to notice..."
- Embedded commands: "*feeling more comfortable*"
- Sensory language: "feel", "hear", "see"

### Voice Biomarkers
See `app/agents/voice_analysis.py`:
- Jitter = pitch stability (vocal tremor)
- Shimmer = amplitude variation
- Stress score = weighted combination of features

### Pattern Recognition
See `app/agents/pattern_recognition.py`:
- Temporal patterns (hour/day clustering)
- Physiological signals (stress, HRV, tremor)
- Risk scoring formula

---

## 📞 Need Help?

**Common Issues:**

1. **Database locked error**
   - Close other connections to `migru.db`
   - Or switch to PostgreSQL (production-ready)

2. **Clerk auth failing**
   - Set `DEV_MODE=true` in `.env` to use demo user
   - Or configure proper Clerk keys

3. **Hume token errors**
   - System works without Hume (uses mock tokens)
   - Add real keys for full emotion detection

4. **Frontend can't reach backend**
   - Check backend is running on port 8000
   - Update `BACKEND_URL` in `lib/stores.ts` if needed

---

## 🎯 Next Steps

### For Development
1. Implement voice recording UI
2. Add chart visualizations
3. Integrate weather API
4. Build notification system

### For Production
1. Switch to PostgreSQL
2. Implement proper JWT verification
3. Lock down CORS
4. Add rate limiting
5. Set up monitoring (Sentry)
6. Deploy to cloud (Vercel frontend + Railway backend)

---

## 💡 Pro Tips

- Use `DEV_MODE=true` to bypass auth during development
- Check `migru.db` with SQLite browser to see data
- Voice analysis works on any audio - test with music!
- Milton Model scripts are in plain text - customize them
- Analytics recalculate on every request - add caching for scale

---

**You now have a production-quality foundation for MIGRU!** 🎉

The 4-agent system, database, auth, and KPI tracking are all in place. Focus on UI polish and user testing next.
