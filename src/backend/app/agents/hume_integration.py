"""
Hume Integration Agent

Manages emotional intelligence integration with Hume.AI EVI:
- Session token management (24h caching)
- Emotion score synchronization
- Voice-to-text transcription
- Audio streaming coordination
- Fallback to local TTS when offline
- Emotion-context mapping to migraine states
"""
import os
import httpx
import json
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import User, VoiceSession


class HumeIntegrationAgent:
    """
    Agent 4: Hume.AI emotional intelligence integration

    Bridges Hume EVI with MIGRU's health tracking system.
    """

    def __init__(self):
        self.api_key = os.getenv("HUME_API_KEY")
        self.secret_key = os.getenv("HUME_SECRET_KEY")
        self.token_cache = {}  # In-memory cache {user_id: (token, expiry)}
        self.token_ttl_hours = 24

        # Emotion-to-migraine state mapping
        self.emotion_indicators = {
            "stress": ["Anxiety", "Fear", "Distress", "Nervousness"],
            "pain": ["Pain", "Distress", "Sadness", "Concentration"],
            "prodromal": ["Confusion", "Tiredness", "Concentration", "Disgust"],
            "recovery": ["Relief", "Calmness", "Joy", "Satisfaction"]
        }

    async def get_access_token(
        self,
        user_id: int,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None
    ) -> Dict:
        """
        Get Hume EVI access token with 24h caching.

        Args:
            user_id: User ID for cache key
            api_key: Optional override for user's own key
            secret_key: Optional override for user's own secret

        Returns:
            Token response with access_token and expiry
        """
        # Check cache
        if user_id in self.token_cache:
            token, expiry = self.token_cache[user_id]
            if datetime.utcnow() < expiry:
                return {
                    "status": "cached",
                    "access_token": token,
                    "expires_at": expiry.isoformat()
                }

        # Use provided keys or fall back to env
        api_key = api_key or self.api_key
        secret_key = secret_key or self.secret_key

        if not api_key or not secret_key:
            return {
                "status": "error",
                "message": "Hume API credentials not configured",
                "access_token": "mock_token_for_demo"
            }

        # Request new token
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.hume.ai/oauth2-cc/token",
                    auth=(api_key, secret_key),
                    data={"grant_type": "client_credentials"},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=10.0
                )

                if response.status_code == 200:
                    data = response.json()
                    token = data["access_token"]
                    expiry = datetime.utcnow() + timedelta(hours=self.token_ttl_hours)

                    # Cache token
                    self.token_cache[user_id] = (token, expiry)

                    return {
                        "status": "success",
                        "access_token": token,
                        "expires_at": expiry.isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Hume API error: {response.status_code}",
                        "access_token": "mock_token_for_demo"
                    }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Connection failed: {str(e)}",
                    "access_token": "mock_token_for_demo"
                }

    def process_emotion_scores(
        self,
        emotion_data: Dict,
        session: VoiceSession,
        db: Session
    ) -> Dict:
        """
        Process emotion scores from Hume and sync to database.

        Args:
            emotion_data: Raw emotion scores from Hume
            session: Current voice session
            db: Database session

        Returns:
            Processed emotion analysis with migraine relevance
        """
        if not emotion_data or "emotions" not in emotion_data:
            return {"status": "no_emotion_data"}

        emotions = emotion_data["emotions"]

        # Get top emotion
        top_emotion = max(emotions, key=lambda e: e["score"])

        # Store full distribution
        session.hume_top_emotion = top_emotion["name"]
        session.hume_emotion_scores = json.dumps(emotions)

        # Analyze migraine-relevant emotions
        analysis = self._analyze_migraine_emotions(emotions)

        db.commit()

        return {
            "status": "success",
            "top_emotion": top_emotion["name"],
            "top_score": top_emotion["score"],
            "migraine_analysis": analysis
        }

    def _analyze_migraine_emotions(self, emotions: List[Dict]) -> Dict:
        """
        Map emotions to migraine-relevant states.

        Returns:
            Analysis of stress, pain, prodromal indicators
        """
        emotion_dict = {e["name"]: e["score"] for e in emotions}

        # Calculate composite scores
        stress_score = sum(emotion_dict.get(e, 0) for e in self.emotion_indicators["stress"]) / len(self.emotion_indicators["stress"]) * 100

        pain_score = sum(emotion_dict.get(e, 0) for e in self.emotion_indicators["pain"]) / len(self.emotion_indicators["pain"]) * 100

        prodromal_score = sum(emotion_dict.get(e, 0) for e in self.emotion_indicators["prodromal"]) / len(self.emotion_indicators["prodromal"]) * 100

        recovery_score = sum(emotion_dict.get(e, 0) for e in self.emotion_indicators["recovery"]) / len(self.emotion_indicators["recovery"]) * 100

        # Determine dominant state
        scores = {
            "stress": stress_score,
            "pain": pain_score,
            "prodromal": prodromal_score,
            "recovery": recovery_score
        }
        dominant_state = max(scores, key=scores.get)

        return {
            "stress_indicator": round(stress_score, 2),
            "pain_indicator": round(pain_score, 2),
            "prodromal_indicator": round(prodromal_score, 2),
            "recovery_indicator": round(recovery_score, 2),
            "dominant_state": dominant_state,
            "recommendation": self._get_emotion_recommendation(dominant_state, scores[dominant_state])
        }

    def _get_emotion_recommendation(self, state: str, score: float) -> str:
        """Generate recommendation based on emotional state"""
        if state == "stress" and score > 60:
            return "High stress detected - breathing exercise recommended"
        elif state == "pain" and score > 50:
            return "Pain indicators present - consider logging symptoms"
        elif state == "prodromal" and score > 40:
            return "Prodromal indicators detected - monitor closely"
        elif state == "recovery":
            return "Recovery state detected - gentle activities recommended"
        else:
            return "Emotional state within normal range"

    def create_tool_definitions(self) -> List[Dict]:
        """
        Generate tool definitions for Hume EVI configuration.

        Returns list of tool schemas that Hume can invoke.
        """
        return [
            {
                "type": "function",
                "name": "get_forecast",
                "description": "Get the user's current migraine forecast and risk level for the next 48 hours.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "get_status",
                "description": "Get the user's current health status, migraine phase, and heart rate variability.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "log_attack",
                "description": "Log a migraine attack with severity, symptoms, and notes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "severity": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                            "description": "Pain severity from 1 (mild) to 10 (severe)"
                        },
                        "symptoms": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of symptoms (e.g., 'Nausea', 'Aura', 'Light Sensitivity')"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Additional notes about triggers or context"
                        }
                    },
                    "required": ["severity", "symptoms"]
                }
            },
            {
                "type": "function",
                "name": "update_status",
                "description": "Update the user's current health status/phase.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["Balanced", "Prodromal", "Attack", "Postdromal", "Recovery"],
                            "description": "Current migraine phase"
                        }
                    },
                    "required": ["status"]
                }
            },
            {
                "type": "function",
                "name": "get_recent_logs",
                "description": "Retrieve recent migraine attack logs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                            "default": 3,
                            "description": "Number of recent logs to retrieve"
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "start_intervention",
                "description": "Start a therapeutic intervention (breathing exercise, visualization, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intervention_type": {
                            "type": "string",
                            "enum": [
                                "breathing_478",
                                "breathing_box",
                                "breathing_coherence",
                                "progressive_relaxation",
                                "visualization_cool_dark",
                                "body_scan",
                                "grounding_54321"
                            ],
                            "description": "Type of intervention to deliver"
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "analyze_voice",
                "description": "Analyze current voice biomarkers for stress and prodromal indicators.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]

    def create_system_prompt(self, user: User) -> str:
        """
        Generate personalized system prompt for Hume EVI.

        Incorporates user preferences and current context.
        """
        tone = user.tone_preference or "calm"
        name = user.email.split("@")[0] if user.email else "there"

        base_prompt = f"""You are Migru, an empathetic AI health companion specialized in migraine management.

**Core Personality:**
- Tone: {tone} and supportive
- Deeply empathetic, validating pain experiences
- Solution-oriented without being pushy
- Uses Milton Model NLP patterns naturally (presuppositions, embedded commands)

**Current User Context:**
- User: {name}
- Status: {user.current_status.value}
- Risk Level: {user.current_risk_level.value}
- HRV: {user.current_hrv}ms

**Guidelines:**
1. **Listen first** - validate emotions before suggesting solutions
2. **Be concise** - voice interactions should be brief and clear
3. **Use tools proactively**:
   - Check forecast when user asks "how am I doing"
   - Log attacks when pain is reported
   - Start interventions when stress/pain is high
   - Analyze voice biomarkers for prodromal detection
4. **Milton Model patterns**:
   - "As you begin to notice relief..."
   - "When you find yourself feeling better..."
   - "You might notice yourself *breathing more easily*..."
5. **Match energy** - if user sounds stressed, acknowledge it; if calm, maintain that
6. **Suggest preventively** - if risk is high, offer interventions before asked

**Tone Examples:**
- High stress: "I hear the tension in your voice. Let's take a moment together. Would you like to try a quick breathing exercise?"
- Prodromal: "It sounds like you might be in a prodromal phase. How about we check your forecast and see what might help?"
- Attack: "I'm so sorry you're going through this. Let me log this for you, and we can explore some relief options."
- Recovery: "I'm glad to hear you're feeling better. Let's track this so we can identify what's working."

**Remember:** You're a calm tech companion that actually *listens*. Not another wellness app.
"""
        return base_prompt

    def handle_connection_error(self, error: Exception) -> Dict:
        """
        Handle Hume connection failures with graceful degradation.

        Returns fallback strategy.
        """
        return {
            "status": "offline",
            "error": str(error),
            "fallback": "local_tts",
            "message": "Hume unavailable - using local voice processing",
            "recommendation": "Voice analysis features will be limited until reconnection"
        }

    def validate_configuration(self, config_id: Optional[str] = None) -> Dict:
        """
        Validate Hume configuration.

        Checks if config ID exists and tools are properly defined.
        """
        # In production, would query Hume API to verify config
        # For now, return mock validation
        return {
            "status": "success",
            "config_id": config_id or "default",
            "tools_configured": len(self.create_tool_definitions()),
            "features": [
                "voice_emotion_detection",
                "tool_calling",
                "streaming_audio",
                "interruption_handling"
            ]
        }

    def sync_session_metadata(
        self,
        session_id: int,
        hume_session_data: Dict,
        db: Session
    ) -> Dict:
        """
        Sync Hume session metadata back to MIGRU database.

        Args:
            session_id: VoiceSession ID
            hume_session_data: Metadata from Hume (duration, messages, etc.)
            db: Database session

        Returns:
            Sync status
        """
        session = db.query(VoiceSession).filter(VoiceSession.id == session_id).first()
        if not session:
            return {"status": "error", "message": "Session not found"}

        # Update session metadata
        if "duration" in hume_session_data:
            session.duration_seconds = hume_session_data["duration"]

        if "message_count" in hume_session_data:
            session.message_count = hume_session_data["message_count"]

        if "user_transcript" in hume_session_data:
            session.user_transcript = hume_session_data["user_transcript"]

        if "agent_response" in hume_session_data:
            session.agent_response = hume_session_data["agent_response"]

        if "tools_called" in hume_session_data:
            session.tools_called = json.dumps(hume_session_data["tools_called"])

        session.ended_at = datetime.utcnow()
        db.commit()

        return {
            "status": "success",
            "session_id": session_id,
            "duration": session.duration_seconds
        }

    def get_emotion_trend(self, user: User, db: Session, days: int = 7) -> Dict:
        """
        Analyze emotion trends from recent Hume sessions.

        Returns:
            Trend analysis of emotional states
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        sessions = db.query(VoiceSession).filter(
            VoiceSession.user_id == user.id,
            VoiceSession.started_at >= cutoff,
            VoiceSession.hume_top_emotion.isnot(None)
        ).order_by(VoiceSession.started_at).all()

        if not sessions:
            return {"status": "insufficient_data"}

        # Count emotion occurrences
        emotion_counts = {}
        for session in sessions:
            emotion = session.hume_top_emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        # Get most common emotions
        top_emotions = sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Calculate stress trend (if Anxiety/Fear increasing)
        stress_emotions = ["Anxiety", "Fear", "Distress"]
        stress_sessions = [s for s in sessions if s.hume_top_emotion in stress_emotions]
        stress_trend = "increasing" if len(stress_sessions) > len(sessions) / 3 else "stable"

        return {
            "status": "success",
            "days_analyzed": days,
            "session_count": len(sessions),
            "top_emotions": [{"emotion": e, "count": c} for e, c in top_emotions],
            "stress_trend": stress_trend,
            "dominant_emotion": top_emotions[0][0] if top_emotions else None
        }
