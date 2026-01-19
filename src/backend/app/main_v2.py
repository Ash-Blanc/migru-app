"""
MIGRU Backend V2 - Unified API with 4-Agent System

Integrates:
- Voice Analysis Agent
- Pattern Recognition Agent
- Intervention Agent
- Hume Integration Agent

With proper database, authentication, and user isolation.
"""
from fastapi import FastAPI, Depends, Header, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import os
import numpy as np
import httpx
from dotenv import load_dotenv

# Database
from app.database import (
    get_db, init_db, User, MigraineLog, VoiceSession, Prediction, Intervention,
    HealthStatus, RiskLevel, calculate_user_analytics
)

# Authentication
from app.auth import get_current_user, get_current_user_optional

# Agents
from app.agents import (
    VoiceAnalysisAgent,
    PatternRecognitionAgent,
    InterventionAgent,
    HumeIntegrationAgent
)

load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="MIGRU API V2",
    description="Voice-first migraine AI agent with 4-agent system",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Lock down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
voice_agent = VoiceAnalysisAgent()
pattern_agent = PatternRecognitionAgent()
intervention_agent = InterventionAgent()
hume_agent = HumeIntegrationAgent()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("🚀 MIGRU Backend V2 initialized")
    print("📊 Database ready")
    print("🤖 4-Agent system active")


# ===== REQUEST MODELS =====

class LogAttackRequest(BaseModel):
    severity: int  # 1-10
    primary_symptoms: List[str] = []
    secondary_symptoms: List[str] = []
    triggers: List[str] = []
    notes: Optional[str] = None
    duration_minutes: Optional[int] = None


class UpdateStatusRequest(BaseModel):
    status: str  # Balanced, Prodromal, Attack, Postdromal, Recovery


class VoiceAnalysisRequest(BaseModel):
    audio_base64: str  # Base64 encoded PCM audio
    sample_rate: int = 24000


class InterventionRequest(BaseModel):
    intervention_type: Optional[str] = None  # Auto-select if None
    context: Dict = {}


class InterventionOutcomeRequest(BaseModel):
    engaged: bool
    completion_percentage: float
    rating: Optional[int] = None  # 1-5


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict


# ===== HEALTH STATUS & FORECAST =====

@app.get("/api/status")
async def get_status(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user health status"""
    return {
        "status": user.current_status.value,
        "hrv": user.current_hrv,
        "risk_level": user.current_risk_level.value,
        "logs_count": len(user.migraine_logs),
        "onboarding_status": user.onboarding_status.value
    }


@app.get("/api/forecast")
async def get_forecast(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get 48-hour migraine prediction"""
    prediction = pattern_agent.generate_48h_prediction(user, db)
    return prediction


# ===== MIGRAINE LOGGING =====

@app.post("/api/logs")
async def log_attack(
    request: LogAttackRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a migraine attack"""
    log = MigraineLog(
        user_id=user.id,
        severity=request.severity,
        duration_minutes=request.duration_minutes,
        primary_symptoms=request.primary_symptoms,
        secondary_symptoms=request.secondary_symptoms,
        triggers=request.triggers,
        notes=request.notes,
        status_before=user.current_status
    )

    # Auto-update user status based on severity
    if request.severity >= 7:
        user.current_status = HealthStatus.ATTACK
        user.current_risk_level = RiskLevel.HIGH
    elif request.severity >= 4:
        user.current_status = HealthStatus.ATTACK
    else:
        user.current_status = HealthStatus.PRODROMAL

    log.status_after = user.current_status

    db.add(log)
    db.commit()
    db.refresh(log)

    # Recalculate analytics
    calculate_user_analytics(db, user)

    return {
        "status": "success",
        "log_id": log.id,
        "message": f"Attack logged. Severity {request.severity}/10. Status updated to {user.current_status.value}",
        "new_status": user.current_status.value
    }


@app.get("/api/logs")
async def get_recent_logs(
    limit: int = 10,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent migraine logs"""
    logs = db.query(MigraineLog).filter(
        MigraineLog.user_id == user.id
    ).order_by(MigraineLog.created_at.desc()).limit(limit).all()

    return {
        "logs": [
            {
                "id": log.id,
                "date": log.created_at.isoformat(),
                "severity": log.severity,
                "duration_minutes": log.duration_minutes,
                "primary_symptoms": log.primary_symptoms,
                "secondary_symptoms": log.secondary_symptoms,
                "triggers": log.triggers,
                "notes": log.notes
            }
            for log in logs
        ]
    }


@app.put("/api/status")
async def update_status(
    request: UpdateStatusRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user health status"""
    try:
        user.current_status = HealthStatus(request.status)
        db.commit()
        return {
            "status": "success",
            "new_status": user.current_status.value
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {request.status}")


# ===== VOICE ANALYSIS =====

@app.post("/api/voice/analyze")
async def analyze_voice(
    request: VoiceAnalysisRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze voice biomarkers from audio"""
    import base64

    # Decode audio
    audio_bytes = base64.b64decode(request.audio_base64)
    audio_array = np.frombuffer(audio_bytes, dtype=np.float32)

    # Analyze
    analysis = voice_agent.analyze_audio_chunk(audio_array, user, db)

    return analysis


@app.get("/api/voice/trend")
async def get_voice_trend(
    days: int = 7,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get voice stress trend"""
    trend = voice_agent.get_recent_trend(user, db, days)
    return trend


@app.post("/api/voice/baseline")
async def establish_baseline(
    audio_chunks: List[str],  # List of base64 encoded audio
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Establish voice baseline (onboarding)"""
    import base64

    # Decode chunks
    audio_arrays = []
    for chunk in audio_chunks:
        audio_bytes = base64.b64decode(chunk)
        audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
        audio_arrays.append(audio_array)

    # Establish baseline
    result = voice_agent.establish_baseline(audio_arrays, user, db)

    return result


# ===== INTERVENTIONS =====

@app.post("/api/interventions")
async def start_intervention(
    request: InterventionRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a therapeutic intervention"""
    # Get current context
    context = request.context or {}

    # Get latest voice session for stress score
    latest_session = db.query(VoiceSession).filter(
        VoiceSession.user_id == user.id
    ).order_by(VoiceSession.started_at.desc()).first()

    if latest_session and latest_session.stress_score:
        context["stress_score"] = latest_session.stress_score

    context["risk_level"] = user.current_risk_level

    # Generate intervention
    intervention = intervention_agent.select_intervention(user, context, db)

    return intervention


@app.post("/api/interventions/{intervention_id}/outcome")
async def log_intervention_outcome(
    intervention_id: int,
    request: InterventionOutcomeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log intervention outcome"""
    result = intervention_agent.log_intervention_outcome(
        intervention_id,
        request.engaged,
        request.completion_percentage,
        request.rating,
        user.current_status,
        user.current_hrv,
        db
    )
    return result


@app.get("/api/interventions/best")
async def get_best_interventions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's most effective interventions"""
    best = intervention_agent.get_best_interventions(user, db)
    return {"interventions": best}


# ===== PATTERN RECOGNITION =====

@app.get("/api/patterns/performance")
async def get_pattern_performance(
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prediction model performance"""
    performance = pattern_agent.get_model_performance(user, db, days)
    return performance


# ===== ANALYTICS & KPIs =====

@app.get("/api/analytics")
async def get_analytics(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user analytics and KPIs"""
    # Recalculate first
    analytics = calculate_user_analytics(db, user)

    return {
        "onboarding": {
            "status": user.onboarding_status.value,
            "completion_rate": analytics.onboarding_completion_rate,
            "completed_at": analytics.onboarding_completed_at.isoformat() if analytics.onboarding_completed_at else None
        },
        "engagement": {
            "weekly_voice_checkins": analytics.weekly_voice_checkins,
            "total_voice_sessions": analytics.total_voice_sessions,
            "last_checkin": analytics.last_voice_checkin.isoformat() if analytics.last_voice_checkin else None,
            "current_streak": analytics.current_checkin_streak,
            "longest_streak": analytics.longest_checkin_streak
        },
        "health_outcomes": {
            "baseline_attack_frequency": analytics.baseline_attack_frequency,
            "current_attack_frequency": analytics.current_attack_frequency,
            "migraine_reduction_percentage": analytics.migraine_reduction_percentage,
            "achieved_40_percent_reduction": analytics.achieved_40_percent_reduction,
            "days_to_40_percent_reduction": analytics.days_to_40_percent_reduction
        },
        "nps": {
            "score": analytics.nps_score,
            "last_survey": analytics.last_nps_survey.isoformat() if analytics.last_nps_survey else None
        }
    }


# ===== HUME INTEGRATION =====

@app.get("/hume/auth")
async def hume_auth(
    x_hume_api_key: Optional[str] = Header(None),
    x_hume_secret_key: Optional[str] = Header(None),
    user: User = Depends(get_current_user_optional)
):
    """Get Hume access token"""
    user_id = user.id if user else 0
    result = await hume_agent.get_access_token(user_id, x_hume_api_key, x_hume_secret_key)
    return result


@app.get("/hume/tools")
def get_hume_tools():
    """Get tool definitions for Hume EVI configuration"""
    tools = hume_agent.create_tool_definitions()
    return tools


@app.get("/hume/prompt")
async def get_hume_prompt(
    user: User = Depends(get_current_user)
):
    """Get personalized system prompt for Hume"""
    prompt = hume_agent.create_system_prompt(user)
    return {"prompt": prompt}


@app.post("/hume/tool-call")
async def handle_hume_tool_call(
    request: ToolCallRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Handle tool calls from Hume EVI"""
    tool_name = request.tool_name
    args = request.arguments

    # Route to appropriate handler
    if tool_name == "get_forecast":
        return await get_forecast(user, db)

    elif tool_name == "get_status":
        return await get_status(user, db)

    elif tool_name == "log_attack":
        log_request = LogAttackRequest(
            severity=args["severity"],
            primary_symptoms=args.get("symptoms", []),
            notes=args.get("notes")
        )
        return await log_attack(log_request, user, db)

    elif tool_name == "update_status":
        status_request = UpdateStatusRequest(status=args["status"])
        return await update_status(status_request, user, db)

    elif tool_name == "get_recent_logs":
        limit = args.get("limit", 3)
        return await get_recent_logs(limit, user, db)

    elif tool_name == "start_intervention":
        intervention_request = InterventionRequest(
            intervention_type=args.get("intervention_type"),
            context={}
        )
        return await start_intervention(intervention_request, user, db)

    elif tool_name == "analyze_voice":
        # Return latest voice analysis
        latest_session = db.query(VoiceSession).filter(
            VoiceSession.user_id == user.id
        ).order_by(VoiceSession.started_at.desc()).first()

        if latest_session:
            return {
                "stress_score": latest_session.stress_score,
                "tremor_detected": latest_session.tremor_detected,
                "baseline_deviation": latest_session.deviation_from_baseline
            }
        return {"status": "no_data"}

    else:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")


@app.post("/hume/emotion-sync")
async def sync_emotion_data(
    session_id: int,
    emotion_data: Dict,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Sync emotion scores from Hume to database"""
    session = db.query(VoiceSession).filter(
        VoiceSession.id == session_id,
        VoiceSession.user_id == user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    result = hume_agent.process_emotion_scores(emotion_data, session, db)
    return result


@app.get("/hume/emotion-trend")
async def get_emotion_trend(
    days: int = 7,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get emotion trend analysis"""
    trend = hume_agent.get_emotion_trend(user, db, days)
    return trend


# ===== ONBOARDING =====

@app.get("/api/onboarding/status")
async def get_onboarding_status(
    user: User = Depends(get_current_user)
):
    """Get onboarding progress"""
    return {
        "status": user.onboarding_status.value,
        "completed": user.onboarding_status.value == "completed",
        "baseline_established": user.baseline_pitch_mean is not None,
        "tone_preference_set": user.tone_preference is not None
    }


@app.post("/api/onboarding/complete")
async def complete_onboarding(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark onboarding as complete"""
    from app.database import OnboardingStatus

    user.onboarding_status = OnboardingStatus.COMPLETED
    user.onboarding_completed_at = datetime.utcnow()
    db.commit()

    # Recalculate analytics
    calculate_user_analytics(db, user)

    return {
        "status": "success",
        "message": "Onboarding completed!"
    }


# ===== HEALTH CHECK =====

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "agents": {
            "voice_analysis": "active",
            "pattern_recognition": "active",
            "intervention": "active",
            "hume_integration": "active"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
