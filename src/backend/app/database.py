"""
Database models and connection management for MIGRU.
Uses SQLAlchemy with SQLite for development, easily swappable to PostgreSQL for production.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import enum
import os
from typing import Optional

# Database URL - defaults to SQLite, set DATABASE_URL env var for PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./migru.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Set to True for SQL debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- Enums ---

class HealthStatus(str, enum.Enum):
    BALANCED = "Balanced"
    PRODROMAL = "Prodromal"
    ATTACK = "Attack"
    POSTDROMAL = "Postdromal"
    RECOVERY = "Recovery"


class RiskLevel(str, enum.Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"


class OnboardingStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    VOICE_BASELINE = "voice_baseline"
    MIGRAINE_HISTORY = "migraine_history"
    TONE_PREFERENCE = "tone_preference"
    COMPLETED = "completed"


# --- Models ---

class User(Base):
    """User model with Clerk integration"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Onboarding
    onboarding_status = Column(SQLEnum(OnboardingStatus), default=OnboardingStatus.NOT_STARTED)
    onboarding_completed_at = Column(DateTime, nullable=True)

    # Voice baseline
    baseline_pitch_mean = Column(Float, nullable=True)
    baseline_pitch_variance = Column(Float, nullable=True)
    baseline_tempo = Column(Float, nullable=True)  # words per minute
    baseline_energy = Column(Float, nullable=True)
    baseline_jitter = Column(Float, nullable=True)  # vocal stability
    baseline_shimmer = Column(Float, nullable=True)  # amplitude variation

    # Preferences
    tone_preference = Column(String, default="calm")  # calm, energetic, neutral
    notification_enabled = Column(Boolean, default=True)
    theme_preference = Column(String, default="dark")

    # Current health state
    current_status = Column(SQLEnum(HealthStatus), default=HealthStatus.BALANCED)
    current_hrv = Column(Integer, default=65)
    current_risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.MODERATE)

    # Relationships
    migraine_logs = relationship("MigraineLog", back_populates="user", cascade="all, delete-orphan")
    voice_sessions = relationship("VoiceSession", back_populates="user", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("UserAnalytics", back_populates="user", uselist=False, cascade="all, delete-orphan")


class MigraineLog(Base):
    """Individual migraine attack records"""
    __tablename__ = "migraine_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Attack details
    severity = Column(Integer, nullable=False)  # 1-10
    duration_minutes = Column(Integer, nullable=True)

    # Symptoms (JSON array)
    primary_symptoms = Column(JSON, default=list)  # ["Nausea", "Aura", "Light Sensitivity", etc.]
    secondary_symptoms = Column(JSON, default=list)

    # Triggers (JSON array)
    triggers = Column(JSON, default=list)  # ["Poor sleep", "Stress", etc.]

    # Environmental context
    weather_condition = Column(String, nullable=True)
    barometric_pressure = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)

    # Notes
    notes = Column(Text, nullable=True)

    # Voice biomarkers at time of logging
    voice_stress_score = Column(Float, nullable=True)  # 0-100
    voice_tremor_detected = Column(Boolean, default=False)

    # Intervention effectiveness
    intervention_used = Column(String, nullable=True)
    intervention_effectiveness = Column(Integer, nullable=True)  # 1-5

    # Status before/after
    status_before = Column(SQLEnum(HealthStatus), nullable=True)
    status_after = Column(SQLEnum(HealthStatus), nullable=True)

    user = relationship("User", back_populates="migraine_logs")


class VoiceSession(Base):
    """Voice interaction sessions with biomarker analysis"""
    __tablename__ = "voice_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Voice biomarkers
    pitch_mean = Column(Float, nullable=True)
    pitch_variance = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)  # words per minute
    energy_mean = Column(Float, nullable=True)
    jitter = Column(Float, nullable=True)  # vocal stability
    shimmer = Column(Float, nullable=True)  # amplitude variation

    # Computed stress indicators
    stress_score = Column(Float, nullable=True)  # 0-100
    deviation_from_baseline = Column(Float, nullable=True)  # percentage
    tremor_detected = Column(Boolean, default=False)

    # Hume emotion analysis
    hume_top_emotion = Column(String, nullable=True)
    hume_emotion_scores = Column(JSON, nullable=True)  # Full emotion distribution

    # Conversation metadata
    message_count = Column(Integer, default=0)
    user_transcript = Column(Text, nullable=True)
    agent_response = Column(Text, nullable=True)

    # Tools called during session
    tools_called = Column(JSON, default=list)

    user = relationship("User", back_populates="voice_sessions")


class Prediction(Base):
    """48-hour migraine predictions from pattern recognition"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    predicted_for = Column(DateTime, nullable=False, index=True)  # Target timestamp

    # Prediction details
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    probability = Column(Float, nullable=False)  # 0-100
    confidence = Column(Float, nullable=False)  # 0-100

    # Contributing factors (JSON)
    temporal_patterns = Column(JSON, nullable=True)  # Time-of-day, day-of-week patterns
    environmental_factors = Column(JSON, nullable=True)  # Weather, pressure
    physiological_indicators = Column(JSON, nullable=True)  # HRV, sleep, stress

    # Model metadata
    model_version = Column(String, default="v1.0")
    feature_importance = Column(JSON, nullable=True)

    # Outcome tracking
    actual_occurred = Column(Boolean, nullable=True)  # Set after prediction window
    actual_severity = Column(Integer, nullable=True)  # If occurred
    prediction_accuracy = Column(Float, nullable=True)  # Calculated post-facto

    user = relationship("User", back_populates="predictions")


class Intervention(Base):
    """Intervention delivery tracking with efficacy logging"""
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    delivered_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Intervention details
    intervention_type = Column(String, nullable=False)  # "breathing", "nlp_reframe", "guided_meditation", etc.
    content = Column(Text, nullable=False)  # The actual intervention text/script

    # Context
    triggered_by = Column(String, nullable=True)  # "high_stress", "prodromal_detection", "user_request"
    risk_level_at_delivery = Column(SQLEnum(RiskLevel), nullable=True)
    stress_score_at_delivery = Column(Float, nullable=True)

    # Milton Model NLP patterns used
    nlp_patterns = Column(JSON, nullable=True)  # ["presupposition", "embedded_command", "sensory_language"]
    tone_matched = Column(Boolean, default=False)

    # Efficacy tracking
    user_engaged = Column(Boolean, nullable=True)
    completion_percentage = Column(Float, nullable=True)  # 0-100
    user_rating = Column(Integer, nullable=True)  # 1-5

    # Outcome
    status_before = Column(SQLEnum(HealthStatus), nullable=True)
    status_after = Column(SQLEnum(HealthStatus), nullable=True)
    hrv_before = Column(Integer, nullable=True)
    hrv_after = Column(Integer, nullable=True)
    stress_reduction = Column(Float, nullable=True)  # Percentage change

    user = relationship("User", back_populates="interventions")


class UserAnalytics(Base):
    """KPI tracking per user"""
    __tablename__ = "user_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    # Onboarding KPIs
    onboarding_started_at = Column(DateTime, nullable=True)
    onboarding_completed_at = Column(DateTime, nullable=True)
    onboarding_completion_rate = Column(Float, default=0.0)  # 0-100

    # Engagement KPIs
    weekly_voice_checkins = Column(Integer, default=0)
    last_voice_checkin = Column(DateTime, nullable=True)
    total_voice_sessions = Column(Integer, default=0)
    total_interactions = Column(Integer, default=0)

    # Health outcome KPIs
    baseline_attack_frequency = Column(Float, nullable=True)  # Attacks per month (first 30 days)
    current_attack_frequency = Column(Float, nullable=True)  # Rolling 30-day average
    migraine_reduction_percentage = Column(Float, nullable=True)

    # Days to 40% reduction (target KPI)
    days_to_40_percent_reduction = Column(Integer, nullable=True)
    achieved_40_percent_reduction = Column(Boolean, default=False)

    # NPS and satisfaction
    nps_score = Column(Integer, nullable=True)  # -100 to 100
    last_nps_survey = Column(DateTime, nullable=True)

    # Streaks
    current_checkin_streak = Column(Integer, default=0)
    longest_checkin_streak = Column(Integer, default=0)

    # Updated timestamp
    last_calculated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="analytics")


# --- Database Utilities ---

def get_db():
    """Dependency for FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully")


def get_or_create_user(db, clerk_id: str, email: Optional[str] = None) -> User:
    """Get existing user or create new one from Clerk ID"""
    user = db.query(User).filter(User.clerk_id == clerk_id).first()
    if not user:
        user = User(clerk_id=clerk_id, email=email)
        db.add(user)

        # Create analytics record
        analytics = UserAnalytics(user=user)
        db.add(analytics)

        db.commit()
        db.refresh(user)
    return user


def calculate_user_analytics(db, user: User):
    """Recalculate all KPIs for a user"""
    analytics = user.analytics
    if not analytics:
        analytics = UserAnalytics(user=user)
        db.add(analytics)

    now = datetime.utcnow()

    # Onboarding metrics
    if user.onboarding_completed_at:
        analytics.onboarding_completion_rate = 100.0
    elif user.onboarding_status != OnboardingStatus.NOT_STARTED:
        # Partial completion based on status
        status_map = {
            OnboardingStatus.VOICE_BASELINE: 25.0,
            OnboardingStatus.MIGRAINE_HISTORY: 50.0,
            OnboardingStatus.TONE_PREFERENCE: 75.0,
        }
        analytics.onboarding_completion_rate = status_map.get(user.onboarding_status, 0.0)

    # Voice engagement
    week_ago = now - timedelta(days=7)
    analytics.weekly_voice_checkins = db.query(VoiceSession).filter(
        VoiceSession.user_id == user.id,
        VoiceSession.started_at >= week_ago
    ).count()

    analytics.total_voice_sessions = db.query(VoiceSession).filter(
        VoiceSession.user_id == user.id
    ).count()

    last_session = db.query(VoiceSession).filter(
        VoiceSession.user_id == user.id
    ).order_by(VoiceSession.started_at.desc()).first()
    if last_session:
        analytics.last_voice_checkin = last_session.started_at

    # Migraine frequency
    thirty_days_ago = now - timedelta(days=30)
    recent_attacks = db.query(MigraineLog).filter(
        MigraineLog.user_id == user.id,
        MigraineLog.created_at >= thirty_days_ago
    ).count()
    analytics.current_attack_frequency = recent_attacks

    # Calculate baseline (first 30 days after account creation)
    baseline_end = user.created_at + timedelta(days=30)
    baseline_attacks = db.query(MigraineLog).filter(
        MigraineLog.user_id == user.id,
        MigraineLog.created_at >= user.created_at,
        MigraineLog.created_at <= baseline_end
    ).count()

    if baseline_attacks > 0:
        analytics.baseline_attack_frequency = baseline_attacks

        # Calculate reduction
        if analytics.current_attack_frequency is not None:
            reduction = ((analytics.baseline_attack_frequency - analytics.current_attack_frequency) /
                        analytics.baseline_attack_frequency * 100)
            analytics.migraine_reduction_percentage = max(0, reduction)

            # Check if 40% reduction achieved
            if reduction >= 40 and not analytics.achieved_40_percent_reduction:
                analytics.achieved_40_percent_reduction = True
                days_since_signup = (now - user.created_at).days
                analytics.days_to_40_percent_reduction = days_since_signup

    analytics.last_calculated = now
    db.commit()
    return analytics


if __name__ == "__main__":
    init_db()
