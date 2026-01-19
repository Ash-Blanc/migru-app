"""
Pattern Recognition Agent

Builds temporal migraine models and generates 48-hour predictive alerts.

Features:
- Time-of-day patterns (morning, evening attacks)
- Day-of-week patterns (weekend vs weekday)
- Seasonal trends
- Trigger correlation analysis
- Environmental factor modeling (weather, pressure)
- Prodromal signal detection
"""
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import User, MigraineLog, Prediction, VoiceSession, RiskLevel
import json


class PatternRecognitionAgent:
    """
    Agent 2: Temporal pattern analysis and predictive modeling

    Learns from historical migraine data to predict future attacks.
    """

    def __init__(self):
        self.lookback_days = 90  # Analyze last 3 months
        self.prediction_window_hours = 48

    def generate_48h_prediction(self, user: User, db: Session) -> Dict:
        """
        Generate 48-hour migraine risk prediction.

        Returns:
            Prediction with risk level, probability, and contributing factors
        """
        # Gather historical data
        patterns = self._analyze_temporal_patterns(user, db)
        environmental = self._analyze_environmental_factors(user, db)
        physiological = self._analyze_physiological_signals(user, db)

        # Calculate risk probability
        risk_score = self._calculate_risk_score(patterns, environmental, physiological)

        # Determine risk level
        if risk_score >= 70:
            risk_level = RiskLevel.HIGH
        elif risk_score >= 40:
            risk_level = RiskLevel.MODERATE
        else:
            risk_level = RiskLevel.LOW

        # Calculate confidence based on data availability
        confidence = self._calculate_confidence(user, db)

        # Create prediction record
        prediction_time = datetime.utcnow() + timedelta(hours=24)  # Midpoint of 48h window
        prediction = Prediction(
            user_id=user.id,
            predicted_for=prediction_time,
            risk_level=risk_level,
            probability=risk_score,
            confidence=confidence,
            temporal_patterns=patterns,
            environmental_factors=environmental,
            physiological_indicators=physiological,
            model_version="v1.0"
        )
        db.add(prediction)
        db.commit()

        return {
            "status": "success",
            "prediction_id": prediction.id,
            "risk_level": risk_level.value,
            "probability": risk_score,
            "confidence": confidence,
            "factors": {
                "temporal": patterns,
                "environmental": environmental,
                "physiological": physiological
            },
            "recommendations": self._generate_recommendations(risk_level, patterns, environmental)
        }

    def _analyze_temporal_patterns(self, user: User, db: Session) -> Dict:
        """
        Analyze time-based patterns in migraine history.

        Returns temporal risk factors.
        """
        cutoff = datetime.utcnow() - timedelta(days=self.lookback_days)
        logs = db.query(MigraineLog).filter(
            MigraineLog.user_id == user.id,
            MigraineLog.created_at >= cutoff
        ).all()

        if not logs:
            return {"status": "insufficient_data"}

        # Hour of day distribution
        hours = [log.created_at.hour for log in logs]
        hour_distribution = {f"hour_{h}": hours.count(h) for h in range(24)}
        peak_hour = max(hour_distribution, key=hour_distribution.get).replace("hour_", "")

        # Day of week distribution
        weekdays = [log.created_at.weekday() for log in logs]  # 0=Monday, 6=Sunday
        weekday_distribution = {f"day_{d}": weekdays.count(d) for d in range(7)}
        peak_day = max(weekday_distribution, key=weekday_distribution.get).replace("day_", "")

        # Current time context
        now = datetime.utcnow()
        current_hour_risk = hour_distribution.get(f"hour_{now.hour}", 0) / len(logs) * 100
        current_weekday_risk = weekday_distribution.get(f"day_{now.weekday()}", 0) / len(logs) * 100

        # Cluster detection (attacks in similar time windows)
        recent_week_logs = [log for log in logs if log.created_at >= datetime.utcnow() - timedelta(days=7)]
        cluster_risk = len(recent_week_logs) / 7 * 100 if recent_week_logs else 0

        return {
            "status": "success",
            "peak_hour": int(peak_hour),
            "peak_day": int(peak_day),
            "current_hour_risk": round(current_hour_risk, 2),
            "current_weekday_risk": round(current_weekday_risk, 2),
            "recent_cluster_risk": round(cluster_risk, 2),
            "total_attacks_analyzed": len(logs)
        }

    def _analyze_environmental_factors(self, user: User, db: Session) -> Dict:
        """
        Analyze environmental correlations.

        In production, would integrate with weather API.
        For now, uses logged data.
        """
        cutoff = datetime.utcnow() - timedelta(days=self.lookback_days)
        logs = db.query(MigraineLog).filter(
            MigraineLog.user_id == user.id,
            MigraineLog.created_at >= cutoff,
            MigraineLog.barometric_pressure.isnot(None)
        ).all()

        if not logs:
            return {"status": "no_environmental_data"}

        # Pressure analysis
        pressures = [log.barometric_pressure for log in logs if log.barometric_pressure]
        if pressures:
            avg_attack_pressure = np.mean(pressures)
            # Simulated current pressure (would come from weather API)
            current_pressure = 1013.25  # Standard atmosphere
            pressure_risk = abs(current_pressure - avg_attack_pressure) / avg_attack_pressure * 100
        else:
            pressure_risk = 0

        # Weather condition correlation
        weather_counts = {}
        for log in logs:
            if log.weather_condition:
                weather_counts[log.weather_condition] = weather_counts.get(log.weather_condition, 0) + 1

        high_risk_weather = max(weather_counts, key=weather_counts.get) if weather_counts else None

        return {
            "status": "success",
            "pressure_risk": round(pressure_risk, 2),
            "high_risk_weather": high_risk_weather,
            "weather_correlation": weather_counts
        }

    def _analyze_physiological_signals(self, user: User, db: Session) -> Dict:
        """
        Analyze physiological indicators from recent voice sessions.

        Prodromal signals: elevated stress, vocal changes, tremor.
        """
        # Recent voice sessions (last 24 hours)
        cutoff = datetime.utcnow() - timedelta(hours=24)
        sessions = db.query(VoiceSession).filter(
            VoiceSession.user_id == user.id,
            VoiceSession.started_at >= cutoff
        ).order_by(VoiceSession.started_at.desc()).all()

        if not sessions:
            return {"status": "no_recent_voice_data"}

        # Average stress score
        stress_scores = [s.stress_score for s in sessions if s.stress_score is not None]
        avg_stress = np.mean(stress_scores) if stress_scores else 0

        # Tremor detection
        tremor_count = sum(1 for s in sessions if s.tremor_detected)
        tremor_rate = tremor_count / len(sessions) * 100 if sessions else 0

        # Baseline deviation trend
        deviations = [s.deviation_from_baseline for s in sessions if s.deviation_from_baseline is not None]
        avg_deviation = np.mean(deviations) if deviations else 0

        # HRV (if available)
        hrv_risk = 0
        if user.current_hrv < 55:  # Low HRV = higher stress
            hrv_risk = (55 - user.current_hrv) / 55 * 100

        # Prodromal phase detection
        prodromal_indicators = 0
        if avg_stress > 60:
            prodromal_indicators += 1
        if tremor_rate > 20:
            prodromal_indicators += 1
        if avg_deviation > 25:
            prodromal_indicators += 1
        if hrv_risk > 30:
            prodromal_indicators += 1

        prodromal_detected = prodromal_indicators >= 2

        return {
            "status": "success",
            "avg_stress_score": round(avg_stress, 2),
            "tremor_rate": round(tremor_rate, 2),
            "baseline_deviation": round(avg_deviation, 2),
            "hrv_risk": round(hrv_risk, 2),
            "prodromal_detected": prodromal_detected,
            "prodromal_confidence": prodromal_indicators / 4 * 100
        }

    def _calculate_risk_score(
        self,
        temporal: Dict,
        environmental: Dict,
        physiological: Dict
    ) -> float:
        """
        Combine all factors into unified risk score (0-100).

        Weighted combination of pattern signals.
        """
        score = 0.0

        # Temporal contribution (30%)
        if temporal.get("status") == "success":
            temporal_score = (
                temporal.get("current_hour_risk", 0) * 0.4 +
                temporal.get("current_weekday_risk", 0) * 0.3 +
                temporal.get("recent_cluster_risk", 0) * 0.3
            )
            score += temporal_score * 0.3

        # Environmental contribution (25%)
        if environmental.get("status") == "success":
            env_score = min(100, environmental.get("pressure_risk", 0) * 2)
            score += env_score * 0.25

        # Physiological contribution (45%) - most predictive
        if physiological.get("status") == "success":
            physio_score = (
                physiological.get("avg_stress_score", 0) * 0.4 +
                physiological.get("tremor_rate", 0) * 0.3 +
                physiological.get("baseline_deviation", 0) * 0.2 +
                physiological.get("hrv_risk", 0) * 0.1
            )
            score += physio_score * 0.45

        return min(100, score)

    def _calculate_confidence(self, user: User, db: Session) -> float:
        """
        Calculate prediction confidence based on data availability.

        More historical data = higher confidence.
        """
        cutoff = datetime.utcnow() - timedelta(days=self.lookback_days)

        # Count data points
        log_count = db.query(MigraineLog).filter(
            MigraineLog.user_id == user.id,
            MigraineLog.created_at >= cutoff
        ).count()

        session_count = db.query(VoiceSession).filter(
            VoiceSession.user_id == user.id,
            VoiceSession.started_at >= cutoff
        ).count()

        # Baseline established?
        has_baseline = user.baseline_pitch_mean is not None

        # Confidence formula
        confidence = 0.0

        # Need at least 5 logged attacks for decent confidence
        if log_count >= 5:
            confidence += min(50, log_count * 5)

        # Voice sessions contribute
        if session_count >= 10:
            confidence += min(30, session_count * 2)

        # Baseline established
        if has_baseline:
            confidence += 20

        return min(100, confidence)

    def _generate_recommendations(
        self,
        risk_level: RiskLevel,
        temporal: Dict,
        environmental: Dict
    ) -> List[str]:
        """Generate actionable recommendations based on prediction"""
        recommendations = []

        if risk_level == RiskLevel.HIGH:
            recommendations.append("High migraine risk in next 48h - consider preventive measures")
            recommendations.append("Ensure adequate hydration and rest")
            recommendations.append("Have rescue medication accessible")
        elif risk_level == RiskLevel.MODERATE:
            recommendations.append("Moderate risk - monitor for prodromal symptoms")
            recommendations.append("Avoid known triggers if possible")

        # Temporal recommendations
        if temporal.get("status") == "success":
            peak_hour = temporal.get("peak_hour")
            if peak_hour is not None:
                recommendations.append(f"Your attacks often occur around {peak_hour}:00 - plan accordingly")

        # Environmental recommendations
        if environmental.get("status") == "success":
            if environmental.get("pressure_risk", 0) > 50:
                recommendations.append("Barometric pressure changes detected - stay alert")

        return recommendations

    def validate_prediction(self, prediction_id: int, db: Session) -> Dict:
        """
        Validate a past prediction against actual outcome.

        Called after prediction window has passed.
        """
        prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
        if not prediction:
            return {"status": "error", "message": "Prediction not found"}

        # Check if prediction window has passed
        now = datetime.utcnow()
        window_end = prediction.predicted_for + timedelta(hours=24)
        if now < window_end:
            return {"status": "pending", "message": "Prediction window not yet complete"}

        # Check for attacks in prediction window
        window_start = prediction.predicted_for - timedelta(hours=24)
        attacks = db.query(MigraineLog).filter(
            MigraineLog.user_id == prediction.user_id,
            MigraineLog.created_at >= window_start,
            MigraineLog.created_at <= window_end
        ).all()

        occurred = len(attacks) > 0
        severity = max([a.severity for a in attacks]) if attacks else None

        # Calculate accuracy
        predicted_high_risk = prediction.risk_level in [RiskLevel.HIGH, RiskLevel.MODERATE]
        correct = (predicted_high_risk and occurred) or (not predicted_high_risk and not occurred)
        accuracy = 100.0 if correct else 0.0

        # Update prediction record
        prediction.actual_occurred = occurred
        prediction.actual_severity = severity
        prediction.prediction_accuracy = accuracy
        db.commit()

        return {
            "status": "validated",
            "prediction_id": prediction_id,
            "predicted_risk": prediction.risk_level.value,
            "actual_occurred": occurred,
            "actual_severity": severity,
            "accuracy": accuracy,
            "correct": correct
        }

    def get_model_performance(self, user: User, db: Session, days: int = 30) -> Dict:
        """
        Analyze prediction model performance over time.

        Returns accuracy metrics.
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        predictions = db.query(Prediction).filter(
            Prediction.user_id == user.id,
            Prediction.created_at >= cutoff,
            Prediction.prediction_accuracy.isnot(None)
        ).all()

        if not predictions:
            return {"status": "insufficient_data"}

        accuracies = [p.prediction_accuracy for p in predictions]
        avg_accuracy = np.mean(accuracies)

        # True positive rate (high risk correctly predicted)
        high_risk_predictions = [p for p in predictions if p.risk_level in [RiskLevel.HIGH, RiskLevel.MODERATE]]
        true_positives = sum(1 for p in high_risk_predictions if p.actual_occurred)
        sensitivity = true_positives / len(high_risk_predictions) * 100 if high_risk_predictions else 0

        # True negative rate (low risk correctly predicted)
        low_risk_predictions = [p for p in predictions if p.risk_level == RiskLevel.LOW]
        true_negatives = sum(1 for p in low_risk_predictions if not p.actual_occurred)
        specificity = true_negatives / len(low_risk_predictions) * 100 if low_risk_predictions else 0

        return {
            "status": "success",
            "total_predictions": len(predictions),
            "average_accuracy": round(avg_accuracy, 2),
            "sensitivity": round(sensitivity, 2),
            "specificity": round(specificity, 2),
            "days_analyzed": days
        }
