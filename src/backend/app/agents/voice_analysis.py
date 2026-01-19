"""
Voice Analysis Agent

Analyzes vocal biomarkers for stress detection and migraine onset prediction:
- Pitch (mean, variance, range)
- Tempo (words per minute)
- Energy (amplitude)
- Jitter (vocal stability)
- Shimmer (amplitude variation)
- Micro-tremor detection

Uses lightweight signal processing (no ML dependencies for now, can upgrade to ONNX later).
"""
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import User, VoiceSession


class VoiceAnalysisAgent:
    """
    Agent 1: Real-time voice biomarker analysis

    Extracts vocal features from audio and compares to user baseline
    to detect stress, fatigue, and potential migraine prodrome.
    """

    def __init__(self):
        self.sample_rate = 24000  # Hume uses 24kHz
        self.min_speech_duration = 2.0  # seconds

    def analyze_audio_chunk(
        self,
        audio_data: np.ndarray,
        user: User,
        db: Session
    ) -> Dict:
        """
        Analyze audio chunk and extract biomarkers.

        Args:
            audio_data: NumPy array of audio samples (float32, mono, 24kHz)
            user: User object with baseline metrics
            db: Database session

        Returns:
            Dictionary with biomarker analysis
        """
        if len(audio_data) < self.sample_rate * self.min_speech_duration:
            return {
                "status": "insufficient_data",
                "message": "Audio too short for analysis"
            }

        # Extract features
        features = self._extract_features(audio_data)

        # Compare to baseline
        deviation = self._calculate_baseline_deviation(features, user)

        # Calculate stress score
        stress_score = self._calculate_stress_score(features, user)

        # Detect micro-tremor
        tremor_detected = self._detect_tremor(audio_data)

        # Store session
        session = VoiceSession(
            user_id=user.id,
            pitch_mean=features['pitch_mean'],
            pitch_variance=features['pitch_variance'],
            tempo=features['tempo'],
            energy_mean=features['energy_mean'],
            jitter=features['jitter'],
            shimmer=features['shimmer'],
            stress_score=stress_score,
            deviation_from_baseline=deviation,
            tremor_detected=tremor_detected
        )
        db.add(session)
        db.commit()

        return {
            "status": "success",
            "session_id": session.id,
            "features": features,
            "stress_score": stress_score,
            "baseline_deviation": deviation,
            "tremor_detected": tremor_detected,
            "prodromal_risk": "high" if stress_score > 70 or deviation > 30 else "low",
            "recommendations": self._generate_recommendations(stress_score, tremor_detected)
        }

    def _extract_features(self, audio: np.ndarray) -> Dict:
        """
        Extract vocal biomarkers from audio signal.

        Simplified feature extraction - can be enhanced with librosa or parselmouth.
        """
        # Energy (RMS amplitude)
        energy = np.sqrt(np.mean(audio ** 2))

        # Simple pitch estimation via zero-crossing rate
        # Note: This is a rough estimate. For production, use librosa.pyin() or parselmouth
        zero_crossings = np.where(np.diff(np.sign(audio)))[0]
        zcr = len(zero_crossings) / len(audio) * self.sample_rate

        # Rough pitch estimate (assumes voice is 80-300 Hz)
        pitch_estimate = zcr / 2 if 80 <= zcr / 2 <= 300 else 150

        # Jitter (pitch stability) - variance of frame-level pitch
        frame_length = int(0.03 * self.sample_rate)  # 30ms frames
        frames = [audio[i:i+frame_length] for i in range(0, len(audio) - frame_length, frame_length)]
        frame_zcrs = [len(np.where(np.diff(np.sign(f)))[0]) / len(f) * self.sample_rate / 2 for f in frames if len(f) > 0]
        jitter = np.std(frame_zcrs) if len(frame_zcrs) > 0 else 0

        # Shimmer (amplitude stability) - variance of frame-level energy
        frame_energies = [np.sqrt(np.mean(f ** 2)) for f in frames if len(f) > 0]
        shimmer = np.std(frame_energies) if len(frame_energies) > 0 else 0

        # Tempo (rough estimate based on energy envelope changes)
        # In real implementation, would use speech-to-text word count / duration
        envelope = np.abs(audio)
        smoothed = np.convolve(envelope, np.ones(int(0.1 * self.sample_rate)) / int(0.1 * self.sample_rate), mode='same')
        peaks = len(np.where(np.diff(np.sign(np.diff(smoothed))) < 0)[0])
        tempo = peaks / (len(audio) / self.sample_rate) * 60  # peaks per minute (rough proxy for syllables)

        return {
            "pitch_mean": float(pitch_estimate),
            "pitch_variance": float(jitter),
            "tempo": float(tempo),
            "energy_mean": float(energy),
            "jitter": float(jitter),
            "shimmer": float(shimmer)
        }

    def _calculate_baseline_deviation(self, features: Dict, user: User) -> float:
        """
        Calculate percentage deviation from user's baseline.

        Returns average deviation across all features.
        """
        if not user.baseline_pitch_mean:
            return 0.0  # No baseline yet

        deviations = []

        # Pitch deviation
        if user.baseline_pitch_mean > 0:
            pitch_dev = abs(features['pitch_mean'] - user.baseline_pitch_mean) / user.baseline_pitch_mean * 100
            deviations.append(pitch_dev)

        # Tempo deviation
        if user.baseline_tempo and user.baseline_tempo > 0:
            tempo_dev = abs(features['tempo'] - user.baseline_tempo) / user.baseline_tempo * 100
            deviations.append(tempo_dev)

        # Energy deviation
        if user.baseline_energy and user.baseline_energy > 0:
            energy_dev = abs(features['energy_mean'] - user.baseline_energy) / user.baseline_energy * 100
            deviations.append(energy_dev)

        return np.mean(deviations) if deviations else 0.0

    def _calculate_stress_score(self, features: Dict, user: User) -> float:
        """
        Calculate stress score (0-100) based on vocal features.

        Higher pitch, faster tempo, increased jitter = higher stress.
        """
        score = 0.0

        # Pitch contribution (stressed voice often has higher pitch)
        if user.baseline_pitch_mean and user.baseline_pitch_mean > 0:
            pitch_increase = (features['pitch_mean'] - user.baseline_pitch_mean) / user.baseline_pitch_mean
            score += min(30, max(0, pitch_increase * 100))

        # Jitter contribution (stressed voice is less stable)
        if user.baseline_jitter and user.baseline_jitter > 0:
            jitter_increase = (features['jitter'] - user.baseline_jitter) / user.baseline_jitter
            score += min(30, max(0, jitter_increase * 100))

        # Tempo contribution (stressed speech often faster or erratic)
        if user.baseline_tempo and user.baseline_tempo > 0:
            tempo_change = abs(features['tempo'] - user.baseline_tempo) / user.baseline_tempo
            score += min(20, max(0, tempo_change * 50))

        # Shimmer contribution
        if user.baseline_shimmer and user.baseline_shimmer > 0:
            shimmer_increase = (features['shimmer'] - user.baseline_shimmer) / user.baseline_shimmer
            score += min(20, max(0, shimmer_increase * 100))

        return min(100, score)

    def _detect_tremor(self, audio: np.ndarray) -> bool:
        """
        Detect micro-tremor in voice (potential prodromal indicator).

        Looks for high-frequency amplitude modulation (4-12 Hz range).
        """
        # Extract amplitude envelope
        envelope = np.abs(audio)

        # Smooth envelope
        window_size = int(0.05 * self.sample_rate)  # 50ms window
        smoothed = np.convolve(envelope, np.ones(window_size) / window_size, mode='same')

        # FFT of envelope to detect modulation frequency
        fft = np.fft.rfft(smoothed)
        freqs = np.fft.rfftfreq(len(smoothed), 1/self.sample_rate)

        # Check for peak in tremor range (4-12 Hz)
        tremor_band = (freqs >= 4) & (freqs <= 12)
        tremor_power = np.sum(np.abs(fft[tremor_band]) ** 2)
        total_power = np.sum(np.abs(fft) ** 2)

        # Tremor detected if >10% of power in tremor band
        return (tremor_power / total_power) > 0.1 if total_power > 0 else False

    def _generate_recommendations(self, stress_score: float, tremor_detected: bool) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []

        if stress_score > 70:
            recommendations.append("High stress detected - consider a breathing exercise")
        elif stress_score > 50:
            recommendations.append("Moderate stress - may benefit from a short break")

        if tremor_detected:
            recommendations.append("Vocal tremor detected - possible prodromal phase, stay hydrated")

        return recommendations

    def establish_baseline(
        self,
        audio_chunks: List[np.ndarray],
        user: User,
        db: Session
    ) -> Dict:
        """
        Establish user's vocal baseline from multiple audio samples.

        Should be called during onboarding (30-second baseline capture).

        Args:
            audio_chunks: List of audio samples from relaxed state
            user: User object
            db: Database session

        Returns:
            Baseline metrics
        """
        if not audio_chunks or len(audio_chunks) < 3:
            return {
                "status": "error",
                "message": "Need at least 3 audio samples to establish baseline"
            }

        all_features = []
        for chunk in audio_chunks:
            if len(chunk) >= self.sample_rate * self.min_speech_duration:
                features = self._extract_features(chunk)
                all_features.append(features)

        if not all_features:
            return {
                "status": "error",
                "message": "Insufficient valid audio data"
            }

        # Calculate averages
        user.baseline_pitch_mean = np.mean([f['pitch_mean'] for f in all_features])
        user.baseline_pitch_variance = np.mean([f['pitch_variance'] for f in all_features])
        user.baseline_tempo = np.mean([f['tempo'] for f in all_features])
        user.baseline_energy = np.mean([f['energy_mean'] for f in all_features])
        user.baseline_jitter = np.mean([f['jitter'] for f in all_features])
        user.baseline_shimmer = np.mean([f['shimmer'] for f in all_features])

        db.commit()

        return {
            "status": "success",
            "message": "Baseline established",
            "baseline": {
                "pitch_mean": user.baseline_pitch_mean,
                "tempo": user.baseline_tempo,
                "energy": user.baseline_energy,
                "jitter": user.baseline_jitter,
                "shimmer": user.baseline_shimmer
            }
        }

    def get_recent_trend(self, user: User, db: Session, days: int = 7) -> Dict:
        """
        Analyze stress score trend over recent sessions.

        Returns:
            Trend analysis with direction and slope
        """
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)

        sessions = db.query(VoiceSession).filter(
            VoiceSession.user_id == user.id,
            VoiceSession.started_at >= cutoff,
            VoiceSession.stress_score.isnot(None)
        ).order_by(VoiceSession.started_at).all()

        if len(sessions) < 2:
            return {"status": "insufficient_data", "trend": "unknown"}

        scores = [s.stress_score for s in sessions]
        timestamps = [(s.started_at - cutoff).total_seconds() for s in sessions]

        # Simple linear regression
        slope = np.polyfit(timestamps, scores, 1)[0]

        trend = "increasing" if slope > 1 else "decreasing" if slope < -1 else "stable"

        return {
            "status": "success",
            "trend": trend,
            "slope": float(slope),
            "current_score": scores[-1],
            "average_score": float(np.mean(scores)),
            "session_count": len(sessions)
        }
