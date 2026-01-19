# MIGRU V2: Complete Implementation Guide

## 🎉 What's New

MIGRU V2 is a complete revamp with enterprise-grade architecture and the full 4-agent system described in the brief.

### Major Improvements

#### ✅ **1. Database Architecture with User Isolation**
- **SQLAlchemy ORM** with SQLite (dev) / PostgreSQL (production) support
- **Full user isolation** - each user's data is completely separated
- **Comprehensive models**:
  - `User` - user profiles with Clerk integration, onboarding status, voice baseline
  - `MigraineLog` - detailed attack records with symptoms, triggers, environmental data
  - `VoiceSession` - voice biomarker analysis per session
  - `Prediction` - 48-hour predictions with outcome tracking
  - `Intervention` - intervention delivery with efficacy logging
  - `UserAnalytics` - KPI tracking (onboarding, engagement, health outcomes, NPS)

#### ✅ **2. Four-Agent System**

**Agent 1: Voice Analysis Agent** (`app/agents/voice_analysis.py`)
- Real-time vocal biomarker extraction:
  - Pitch (mean, variance)
  - Tempo (words per minute)
  - Energy (RMS amplitude)
  - Jitter (vocal stability)
  - Shimmer (amplitude variation)
  - Micro-tremor detection (4-12 Hz modulation)
- Baseline deviation calculation
- Stress score (0-100)
- Prodromal risk assessment
- Trend analysis over time

**Agent 2: Pattern Recognition Agent** (`app/agents/pattern_recognition.py`)
- Temporal pattern analysis:
  - Hour-of-day patterns
  - Day-of-week patterns
  - Recent clustering detection
- Environmental factor correlation (weather, barometric pressure)
- Physiological signal analysis (stress, tremor, HRV)
- 48-hour risk prediction with confidence scoring
- Model performance tracking (accuracy, sensitivity, specificity)
- Prediction validation against actual outcomes

**Agent 3: Intervention Agent** (`app/agents/intervention.py`)
- **Milton Model NLP patterns**:
  - Presuppositions ("As you begin to notice the relief...")
  - Embedded commands ("You might notice yourself *feeling more comfortable*")
  - Sensory language (visual, auditory, kinesthetic)
  - Pacing and leading
  - Metaphors
- **Intervention types**:
  - 4-7-8 breathing
  - Box breathing
  - Coherence breathing (HRV optimization)
  - Progressive muscle relaxation
  - Cool dark visualization
  - Body scan
  - 5-4-3-2-1 grounding
- Smart selection based on stress score, risk level, prodromal state
- Tone matching for TTS (pitch/tempo mirroring)
- Efficacy tracking with user ratings
- Best intervention recommendations

**Agent 4: Hume Integration Agent** (`app/agents/hume_integration.py`)
- OAuth2 token management with 24h caching
- Emotion score processing and migraine-state mapping
- Tool definition generation for Hume EVI
- Personalized system prompt generation
- Emotion trend analysis
- Graceful degradation when offline
- Session metadata synchronization

#### ✅ **3. Backend Authentication**
- Clerk JWT validation middleware
- User-specific data isolation
- Development mode with demo user
- Production-ready token verification (TODO: implement JWKS verification)

#### ✅ **4. Unified Backend API** (`app/main_v2.py`)

**Health Status & Forecast**
- `GET /api/status` - Current user health status
- `GET /api/forecast` - 48-hour migraine prediction

**Migraine Logging**
- `POST /api/logs` - Log migraine attack
- `GET /api/logs` - Get recent logs
- `PUT /api/status` - Update health status

**Voice Analysis**
- `POST /api/voice/analyze` - Analyze audio chunk
- `GET /api/voice/trend` - Get stress trend
- `POST /api/voice/baseline` - Establish baseline (onboarding)

**Interventions**
- `POST /api/interventions` - Start intervention
- `POST /api/interventions/{id}/outcome` - Log outcome
- `GET /api/interventions/best` - Get most effective

**Pattern Recognition**
- `GET /api/patterns/performance` - Model accuracy metrics

**Analytics & KPIs**
- `GET /api/analytics` - Complete user analytics dashboard

**Hume Integration**
- `GET /hume/auth` - Get access token (24h cached)
- `GET /hume/tools` - Tool definitions
- `GET /hume/prompt` - Personalized system prompt
- `POST /hume/tool-call` - Handle tool invocations
- `POST /hume/emotion-sync` - Sync emotion data
- `GET /hume/emotion-trend` - Emotion trend analysis

**Onboarding**
- `GET /api/onboarding/status` - Onboarding progress
- `POST /api/onboarding/complete` - Mark complete

#### ✅ **5. Frontend Enhancements**

**New Pages**
- `/onboarding` - 4-step onboarding flow:
  1. Welcome
  2. Voice baseline (30s capture)
  3. Migraine history intake
  4. Tone preference selection
- `/analytics` - KPI dashboard with:
  - Weekly check-in progress
  - Migraine reduction percentage
  - Streak tracking
  - Engagement metrics
  - Health outcomes
  - Actionable insights

**Updated Components**
- Enhanced navigation to include Analytics
- Integration with V2 API endpoints

#### ✅ **6. KPI Tracking System**

The system tracks and calculates:

**Onboarding KPIs**
- Completion rate (target: 50%+)
- Time to completion

**Engagement KPIs**
- Weekly voice check-ins (target: 5+)
- Total sessions
- Current streak
- Longest streak
- Last check-in date

**Health Outcome KPIs**
- Baseline attack frequency (first 30 days)
- Current attack frequency (rolling 30 days)
- Migraine reduction percentage
- 40% reduction achievement flag
- Days to 40% reduction

**NPS Tracking**
- NPS score storage
- Last survey date

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Clerk account with API keys
- Hume.AI account with API keys (optional for full voice features)

### Backend Setup

1. **Install dependencies**
```bash
cd src/backend
pip install -e .
```

2. **Environment variables**
Create `.env` file:
```env
# Clerk Authentication
CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Hume.AI
HUME_API_KEY=your_hume_api_key
HUME_SECRET_KEY=your_hume_secret_key

# LLM (choose one)
GOOGLE_API_KEY=your_gemini_key
# OR
MISTRAL_API_KEY=your_mistral_key

# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///./migru.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/migru

# Development mode
DEV_MODE=true
```

3. **Initialize database**
```bash
python -c "from app.database import init_db; init_db()"
```

4. **Run server**
```bash
# V2 API (recommended)
uvicorn app.main_v2:app --reload --port 8000

# Or original API
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. **Install dependencies**
```bash
cd src/frontend
npm install
```

2. **Environment variables**
Create `.env`:
```env
PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
```

3. **Update API endpoint**
In `src/frontend/lib/stores.ts`, update backend URL if needed:
```typescript
const BACKEND_URL = 'http://localhost:8000';
```

4. **Run development server**
```bash
npm run dev
```

5. **Access app**
Open http://localhost:5173

---

## 📊 Database Schema

### User Table
```sql
users (
  id INTEGER PRIMARY KEY,
  clerk_id STRING UNIQUE,
  email STRING,
  onboarding_status ENUM,
  baseline_pitch_mean FLOAT,
  baseline_tempo FLOAT,
  tone_preference STRING,
  current_status ENUM,
  current_hrv INTEGER,
  current_risk_level ENUM,
  created_at DATETIME
)
```

### MigraineLog Table
```sql
migraine_logs (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FK,
  severity INTEGER,
  duration_minutes INTEGER,
  primary_symptoms JSON,
  secondary_symptoms JSON,
  triggers JSON,
  notes TEXT,
  voice_stress_score FLOAT,
  voice_tremor_detected BOOLEAN,
  created_at DATETIME
)
```

### VoiceSession Table
```sql
voice_sessions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FK,
  pitch_mean FLOAT,
  tempo FLOAT,
  jitter FLOAT,
  shimmer FLOAT,
  stress_score FLOAT,
  tremor_detected BOOLEAN,
  hume_top_emotion STRING,
  hume_emotion_scores JSON,
  started_at DATETIME
)
```

### Prediction Table
```sql
predictions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FK,
  predicted_for DATETIME,
  risk_level ENUM,
  probability FLOAT,
  confidence FLOAT,
  temporal_patterns JSON,
  environmental_factors JSON,
  actual_occurred BOOLEAN,
  prediction_accuracy FLOAT,
  created_at DATETIME
)
```

### Intervention Table
```sql
interventions (
  id INTEGER PRIMARY KEY,
  user_id INTEGER FK,
  intervention_type STRING,
  content TEXT,
  nlp_patterns JSON,
  tone_matched BOOLEAN,
  user_rating INTEGER,
  stress_reduction FLOAT,
  delivered_at DATETIME
)
```

---

## 🧪 Testing

### Backend API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get status (requires auth)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/status

# Get forecast
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/forecast

# Log attack
curl -X POST http://localhost:8000/api/logs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "severity": 7,
    "primary_symptoms": ["Nausea", "Light Sensitivity"],
    "triggers": ["Stress"],
    "notes": "Started suddenly at work"
  }'

# Get analytics
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/analytics
```

### Voice Analysis Testing

```python
import numpy as np
import base64
from app.agents import VoiceAnalysisAgent
from app.database import SessionLocal, User

# Create agent
agent = VoiceAnalysisAgent()

# Generate sample audio (1 second of 440Hz sine wave)
sample_rate = 24000
duration = 1.0
t = np.linspace(0, duration, int(sample_rate * duration))
audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

# Analyze
db = SessionLocal()
user = db.query(User).first()
result = agent.analyze_audio_chunk(audio, user, db)
print(result)
```

---

## 🔧 Configuration

### Switching Between V1 and V2 APIs

**V1 API** (original): `app/main.py`
- Single shared database (JSON file)
- No authentication
- Basic agent with Agno

**V2 API** (new): `app/main_v2.py`
- SQL database with user isolation
- Clerk authentication
- 4-agent system
- Full KPI tracking

To use V2, ensure your frontend points to V2 endpoints or update `main.py` to import from `main_v2`.

### Database Migration

To migrate from V1 (JSON) to V2 (SQL):

```python
import json
from app.database import SessionLocal, User, MigraineLog, get_or_create_user

# Load old data
with open('migru_data.json') as f:
    old_data = json.load(f)

# Create session
db = SessionLocal()

# Create demo user
user = get_or_create_user(db, "migrated_user", "user@example.com")

# Migrate logs
for log in old_data.get('logs', []):
    migraine_log = MigraineLog(
        user_id=user.id,
        severity=log['severity'],
        primary_symptoms=log.get('symptoms', []),
        notes=log.get('notes', ''),
        created_at=log['date']
    )
    db.add(migraine_log)

db.commit()
print("Migration complete!")
```

---

## 🎨 Frontend Customization

### Updating Voice Agent Prompts

Edit `src/backend/app/agents/hume_integration.py`, method `create_system_prompt()`:

```python
def create_system_prompt(self, user: User) -> str:
    return f"""You are Migru, an empathetic AI health companion.

    Tone: {user.tone_preference}
    Current Status: {user.current_status.value}

    [Your custom instructions here]
    """
```

### Adding New Intervention Types

1. Add intervention script in `src/backend/app/agents/intervention.py`:
```python
def _my_new_intervention_script(self, tone: str) -> Dict:
    script = """Your intervention script here..."""
    return {
        "script": script,
        "duration": 180,
        "instructions": "Instructions for user"
    }
```

2. Update intervention type selection:
```python
def _select_type(self, stress_score, risk_level, prodromal):
    # Add your intervention to the pool
    return random.choice(["breathing_478", "my_new_intervention"])
```

3. Register in scripts dictionary:
```python
scripts = {
    # ...
    "my_new_intervention": self._my_new_intervention_script(tone)
}
```

---

## 📈 Performance Optimization

### Database Indexing
The schema includes indexes on:
- `user.clerk_id` (unique)
- `migraine_logs.created_at`
- `migraine_logs.user_id`
- `voice_sessions.started_at`
- `predictions.predicted_for`

### Caching Strategy
- Hume tokens cached 24h (in-memory)
- Consider adding Redis for production:
  - Session token cache
  - Frequently accessed predictions
  - User analytics (recalculate every 5min)

### Scaling Considerations
- **Database**: Migrate to PostgreSQL for production
- **File storage**: Store audio samples in S3/MinIO instead of base64
- **Async workers**: Use Celery for:
  - Pattern recognition model training
  - Prediction validation
  - Analytics calculation
- **API rate limiting**: Add rate limiting middleware

---

## 🔐 Security Notes

### Current Status
- ✅ User isolation via Clerk ID
- ✅ JWT validation on all authenticated routes
- ⚠️ JWKS signature verification not implemented (DEV_MODE bypass)
- ⚠️ CORS open to all origins (development)

### Production Checklist
- [ ] Implement proper JWKS verification in `app/auth.py`
- [ ] Lock down CORS to specific domains
- [ ] Add rate limiting (e.g., slowapi)
- [ ] Enable HTTPS only
- [ ] Encrypt sensitive data at rest
- [ ] Add audit logging for data access
- [ ] Implement data retention policies
- [ ] Add GDPR compliance features (data export/deletion)

---

## 🐛 Known Issues & TODOs

### Backend
- [ ] Voice baseline recording not implemented in onboarding flow
- [ ] Weather API integration for environmental factors
- [ ] ONNX Runtime for advanced voice analysis (optional upgrade)
- [ ] Proper JWKS verification for Clerk tokens
- [ ] Background jobs for prediction validation
- [ ] Email/SMS notifications for high-risk predictions
- [ ] Export data to CSV/PDF

### Frontend
- [ ] Voice recording UI in onboarding
- [ ] Real-time waveform during interventions
- [ ] Haptic feedback integration
- [ ] Offline mode with service worker
- [ ] Charts for migraine trends
- [ ] Intervention audio playback
- [ ] Push notifications

### System
- [ ] Automated testing suite
- [ ] CI/CD pipeline
- [ ] Monitoring and logging (Sentry, DataDog)
- [ ] Performance profiling
- [ ] Load testing

---

## 📚 Key Files Reference

### Backend
- `app/database.py` - Database models and utilities
- `app/auth.py` - Authentication middleware
- `app/main_v2.py` - V2 API endpoints
- `app/agents/voice_analysis.py` - Voice biomarker analysis
- `app/agents/pattern_recognition.py` - Predictive modeling
- `app/agents/intervention.py` - Milton Model NLP interventions
- `app/agents/hume_integration.py` - Hume.AI integration

### Frontend
- `routes/onboarding/+page.svelte` - Onboarding flow
- `routes/analytics/+page.svelte` - KPI dashboard
- `lib/stores.ts` - State management
- `lib/components/VoiceAgent.svelte` - Voice interface

---

## 🎯 Achieving Target KPIs

### 50%+ Onboarding Completion
**Strategy**: 4-step flow with clear progress indicators
- Each step < 1 minute
- Voice baseline is engaging (gamified)
- Skip options for advanced users
- Progress saved between sessions

**Tracking**: `UserAnalytics.onboarding_completion_rate`

### 5+ Weekly Voice Check-ins
**Strategy**: Daily notifications + streak rewards
- Push reminder at user's peak migraine time
- Streak visualization in app
- Weekly summary emails

**Tracking**: `UserAnalytics.weekly_voice_checkins`

### 40% Migraine Reduction in 30 Days
**Strategy**: Pattern recognition + proactive interventions
- 48h predictions trigger preventive actions
- Intervention efficacy tracking shows what works
- Personalized trigger avoidance

**Tracking**: `UserAnalytics.migraine_reduction_percentage`

### NPS > 50
**Strategy**: Deliver real value, not another app
- Voice-first reduces friction
- Predictive alerts feel magical
- Milton Model NLP builds trust
- Track intervention effectiveness

**Tracking**: `UserAnalytics.nps_score`

---

## 🤝 Contributing

### Code Style
- Backend: Black formatter, type hints
- Frontend: Prettier, TypeScript
- Commits: Conventional commits (feat:, fix:, docs:)

### Adding Features
1. Update database schema if needed (`database.py`)
2. Create agent methods or API endpoints
3. Add frontend UI components
4. Update this documentation
5. Add tests
6. Submit PR with description

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/yourusername/migru-app/issues
- Email: support@migru.app

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

- **Hume.AI** for emotional intelligence API
- **Clerk** for authentication
- **SvelteKit** for the amazing framework
- **Agno** for agent orchestration
- **Milton Erickson** for NLP patterns that actually work

---

**Built with ❤️ for people who deserve calm tech that listens.**
