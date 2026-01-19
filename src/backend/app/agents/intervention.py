"""
Intervention Agent

Delivers therapeutic interventions using:
- Milton Model NLP (presuppositions, embedded commands, sensory language)
- Tone matching (pitch/tempo mirroring)
- Smart response selection based on context
- Efficacy logging and A/B testing

Intervention types:
- Breathing exercises with entrainment
- Guided visualizations
- Reframing techniques
- Distraction strategies
- Progressive muscle relaxation
"""
import random
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import User, Intervention, HealthStatus, RiskLevel


class InterventionAgent:
    """
    Agent 3: Intelligent intervention delivery with Milton Model NLP

    Selects and delivers appropriate interventions based on user state,
    using advanced linguistic patterns for maximum effectiveness.
    """

    def __init__(self):
        self.milton_patterns = {
            "presupposition": [
                "As you begin to notice the relief...",
                "When you find yourself feeling calmer...",
                "Before you realize how much better you feel...",
                "While you continue to relax more deeply..."
            ],
            "embedded_command": [
                "You might notice yourself *feeling more comfortable* now",
                "It's possible to *let go of that tension* naturally",
                "You can *breathe more easily* with each moment",
                "Allow yourself to *release the discomfort*"
            ],
            "sensory_language": {
                "visual": ["notice", "see", "visualize", "imagine", "picture"],
                "auditory": ["hear", "listen", "sound", "quiet", "rhythm"],
                "kinesthetic": ["feel", "sense", "touch", "release", "relax", "soften"]
            },
            "pacing_leading": [
                "You're feeling {current_state}, and as you focus on your breath, you can begin to feel {desired_state}",
                "Right now there's {current_state}, and with each breath, there's more {desired_state}"
            ],
            "metaphor": [
                "Like waves gently washing away tension from the shore...",
                "As clouds slowly drift across a peaceful sky...",
                "Like a tight knot gradually loosening...",
                "As darkness fades with the coming dawn..."
            ]
        }

    def select_intervention(
        self,
        user: User,
        context: Dict,
        db: Session
    ) -> Dict:
        """
        Select optimal intervention based on current state.

        Args:
            user: User object
            context: Current context (stress_score, risk_level, trigger, etc.)
            db: Database session

        Returns:
            Intervention details with NLP-enhanced content
        """
        stress_score = context.get("stress_score", 50)
        risk_level = context.get("risk_level", RiskLevel.MODERATE)
        trigger = context.get("trigger")
        prodromal = context.get("prodromal_detected", False)

        # Select intervention type
        intervention_type = self._select_type(stress_score, risk_level, prodromal)

        # Generate content with Milton Model patterns
        content = self._generate_intervention_content(
            intervention_type,
            user,
            stress_score,
            context
        )

        # Select NLP patterns to use
        patterns_used = self._select_nlp_patterns(intervention_type, stress_score)

        # Store intervention
        intervention = Intervention(
            user_id=user.id,
            intervention_type=intervention_type,
            content=content["script"],
            triggered_by=context.get("triggered_by", "user_request"),
            risk_level_at_delivery=risk_level,
            stress_score_at_delivery=stress_score,
            nlp_patterns=patterns_used,
            tone_matched=context.get("tone_matched", False),
            status_before=user.current_status,
            hrv_before=user.current_hrv
        )
        db.add(intervention)
        db.commit()

        return {
            "status": "success",
            "intervention_id": intervention.id,
            "type": intervention_type,
            "content": content,
            "nlp_patterns": patterns_used,
            "estimated_duration_seconds": content["duration"],
            "instructions": content["instructions"]
        }

    def _select_type(
        self,
        stress_score: float,
        risk_level: RiskLevel,
        prodromal: bool
    ) -> str:
        """
        Decision tree for intervention type selection.
        """
        if prodromal or risk_level == RiskLevel.HIGH:
            # Urgent interventions for prodromal/high risk
            return random.choice(["breathing_478", "progressive_relaxation", "visualization_cool_dark"])

        elif stress_score > 70:
            # High stress but not prodromal
            return random.choice(["breathing_box", "grounding_54321", "bilateral_stimulation"])

        elif stress_score > 50:
            # Moderate stress
            return random.choice(["breathing_coherence", "body_scan", "positive_affirmations"])

        else:
            # Preventive/maintenance
            return random.choice(["mindful_breathing", "gratitude_practice", "gentle_movement"])

    def _generate_intervention_content(
        self,
        intervention_type: str,
        user: User,
        stress_score: float,
        context: Dict
    ) -> Dict:
        """
        Generate intervention script with Milton Model NLP patterns.
        """
        # Get user's preferred tone
        tone = user.tone_preference or "calm"

        # Base scripts by type
        scripts = {
            "breathing_478": self._breathing_478_script(tone, stress_score),
            "breathing_box": self._box_breathing_script(tone),
            "breathing_coherence": self._coherence_breathing_script(tone),
            "progressive_relaxation": self._progressive_relaxation_script(tone),
            "visualization_cool_dark": self._cool_dark_visualization_script(tone),
            "body_scan": self._body_scan_script(tone),
            "grounding_54321": self._grounding_54321_script(tone),
            "mindful_breathing": self._mindful_breathing_script(tone)
        }

        return scripts.get(intervention_type, self._default_script(tone))

    def _breathing_478_script(self, tone: str, stress_score: float) -> Dict:
        """4-7-8 breathing with Milton Model patterns"""
        # Select presupposition based on stress level
        presup = random.choice(self.milton_patterns["presupposition"])

        script = f"""{presup}

Let's do the 4-7-8 breathing together. This powerful technique *calms your nervous system* naturally.

**As you begin, you might notice** yourself settling into a comfortable position...

*Breathe in* through your nose for 4... feel your lungs filling...

*Hold* for 7... notice the stillness...

*Exhale slowly* through your mouth for 8... releasing all tension...

{random.choice(self.milton_patterns['metaphor'])}

We'll repeat this cycle **as your body remembers** how to relax deeply.

*Inhale* for 4... 2... 3... 4...

*Hold* for 7... 2... 3... 4... 5... 6... 7...

*Exhale* for 8... 2... 3... 4... 5... 6... 7... 8...

**And you can continue at your own pace**, knowing that each breath brings more comfort."""

        return {
            "script": script,
            "duration": 180,  # 3 minutes
            "instructions": "Follow the breathing pattern: 4 counts in, 7 counts hold, 8 counts out",
            "target_breaths_per_minute": 6
        }

    def _box_breathing_script(self, tone: str) -> Dict:
        """Box breathing (4-4-4-4)"""
        presup = random.choice(self.milton_patterns["presupposition"])

        script = f"""{presup}

Box breathing, used by Navy SEALs to stay calm under pressure. Simple, yet profound.

**As you settle in**, picture a square...

*Breathe in* for 4 counts... traveling up the first side...

*Hold* for 4... across the top...

*Breathe out* for 4... down the other side...

*Hold* for 4... completing the box...

{random.choice(self.milton_patterns['embedded_command'])}

Let's continue...

*In* 2-3-4... *Hold* 2-3-4... *Out* 2-3-4... *Hold* 2-3-4...

**Perfect.** You're doing great. Continue for a few more cycles **at your own rhythm**."""

        return {
            "script": script,
            "duration": 120,
            "instructions": "Equal counts: 4 in, 4 hold, 4 out, 4 hold",
            "target_breaths_per_minute": 6
        }

    def _coherence_breathing_script(self, tone: str) -> Dict:
        """Coherence breathing (5-5-5-5) for HRV optimization"""
        script = f"""Before you realize how much better you feel, let's try coherence breathing.

This rhythm synchronizes your heart and mind.

**Breathe in** through your nose for 5... feeling your chest expand...

**Breathe out** through your nose for 5... naturally, easily...

{random.choice(self.milton_patterns['metaphor'])}

Continue this gentle rhythm...

*In* 2-3-4-5... *Out* 2-3-4-5...

**Notice** how your body settles into this comfortable pattern...

*In* 2-3-4-5... *Out* 2-3-4-5...

You can continue **as long as feels right**."""

        return {
            "script": script,
            "duration": 300,  # 5 minutes
            "instructions": "Breathe in for 5, out for 5. Aim for 6 breaths per minute.",
            "target_breaths_per_minute": 6
        }

    def _progressive_relaxation_script(self, tone: str) -> Dict:
        """Progressive muscle relaxation with embedded commands"""
        script = f"""As you begin to notice the relief spreading through your body...

We'll systematically **release tension** from each muscle group.

Start by *making a fist* with both hands... tighter... tighter...

**And release.** *Notice the difference* between tension and relaxation...

Now *scrunch your shoulders* up toward your ears... hold...

**And let them drop.** Feel that wave of relief...

{random.choice(self.milton_patterns['metaphor'])}

*Clench your jaw*... hold... **and soften it completely.**

With each release, you might notice yourself *feeling more comfortable*, more at ease.

Your forehead... *tense*... **and smooth.**

Your whole body **remembering** how to let go..."""

        return {
            "script": script,
            "duration": 240,
            "instructions": "Tense each muscle group for 5 seconds, then release and notice the difference",
            "target_breaths_per_minute": 8
        }

    def _cool_dark_visualization_script(self, tone: str) -> Dict:
        """Visualization for migraine relief"""
        script = f"""**While you continue to relax**, let me guide you to a healing space...

*Imagine* a cool, dark room... peaceful and quiet...

A soft pillow supporting your head...

{random.choice(self.milton_patterns['metaphor'])}

*Feel* the coolness on your forehead... soothing...

*Hear* the gentle silence... wrapping around you...

With each breath, the discomfort **begins to fade**, like shadows dissolving in moonlight...

You're safe here... comfortable... **allowing** your body to heal...

Stay in this space **as long as you need**..."""

        return {
            "script": script,
            "duration": 180,
            "instructions": "Close your eyes and follow the visualization",
            "target_breaths_per_minute": 8
        }

    def _body_scan_script(self, tone: str) -> Dict:
        """Mindful body scan"""
        script = f"""As you settle into stillness...

Let's **scan through** your body with gentle awareness...

*Notice* your feet... without changing anything... just aware...

Your calves... knees... thighs... **softening** naturally...

{random.choice(self.milton_patterns['embedded_command'])}

Your hips and lower back... *releasing* any holding...

Your belly... chest... shoulders... **letting go**...

Down your arms to your fingertips...

Your neck... jaw... face... **completely relaxed**...

You might notice yourself *feeling lighter*, more present..."""

        return {
            "script": script,
            "duration": 300,
            "instructions": "Bring gentle awareness to each body part without trying to change anything",
            "target_breaths_per_minute": 8
        }

    def _grounding_54321_script(self, tone: str) -> Dict:
        """5-4-3-2-1 grounding technique"""
        script = f"""When stress feels overwhelming, this technique **brings you back** to the present.

**Look around** and name 5 things you can *see*...

Now 4 things you can *feel* or *touch*...

3 things you can *hear*...

{random.choice(self.milton_patterns['embedded_command'])}

2 things you can *smell* (or imagine smelling)...

And 1 thing you can *taste*...

**And already**, you might notice yourself *feeling more grounded*, more here..."""

        return {
            "script": script,
            "duration": 120,
            "instructions": "Use your senses to anchor yourself in the present moment",
            "target_breaths_per_minute": 10
        }

    def _mindful_breathing_script(self, tone: str) -> Dict:
        """Simple mindful breathing"""
        script = f"""{random.choice(self.milton_patterns['presupposition'])}

Simply *notice* your breath... no need to change it...

**Feel** the air entering your nose... filling your lungs...

**Notice** the pause at the top...

**Sense** the exhale... the natural release...

{random.choice(self.milton_patterns['metaphor'])}

Thoughts will come... that's okay... just gently return to the breath...

**Each moment**, you can *feel more present*, more at peace..."""

        return {
            "script": script,
            "duration": 300,
            "instructions": "Simply observe your natural breathing without trying to control it",
            "target_breaths_per_minute": 12
        }

    def _default_script(self, tone: str) -> Dict:
        """Fallback script"""
        return {
            "script": "Take a moment to breathe deeply and notice how you're feeling right now.",
            "duration": 60,
            "instructions": "Pause and check in with yourself",
            "target_breaths_per_minute": 10
        }

    def _select_nlp_patterns(self, intervention_type: str, stress_score: float) -> List[str]:
        """
        Select which Milton Model patterns are used.
        """
        patterns = ["presupposition"]  # Always include

        if stress_score > 60:
            patterns.append("embedded_command")
            patterns.append("pacing_leading")

        if "visualization" in intervention_type or "relaxation" in intervention_type:
            patterns.append("sensory_language")
            patterns.append("metaphor")

        return patterns

    def log_intervention_outcome(
        self,
        intervention_id: int,
        user_engaged: bool,
        completion_percentage: float,
        user_rating: Optional[int],
        status_after: HealthStatus,
        hrv_after: int,
        db: Session
    ) -> Dict:
        """
        Log intervention outcome for efficacy tracking.
        """
        intervention = db.query(Intervention).filter(Intervention.id == intervention_id).first()
        if not intervention:
            return {"status": "error", "message": "Intervention not found"}

        intervention.user_engaged = user_engaged
        intervention.completion_percentage = completion_percentage
        intervention.user_rating = user_rating
        intervention.status_after = status_after
        intervention.hrv_after = hrv_after

        # Calculate stress reduction
        if intervention.hrv_before and hrv_after:
            hrv_change = ((hrv_after - intervention.hrv_before) / intervention.hrv_before) * 100
            intervention.stress_reduction = hrv_change

        db.commit()

        return {
            "status": "success",
            "intervention_id": intervention_id,
            "effectiveness": user_rating,
            "hrv_change": intervention.stress_reduction
        }

    def get_best_interventions(self, user: User, db: Session, limit: int = 3) -> List[Dict]:
        """
        Retrieve most effective interventions for this user.

        Based on historical ratings and outcomes.
        """
        interventions = db.query(Intervention).filter(
            Intervention.user_id == user.id,
            Intervention.user_rating.isnot(None)
        ).order_by(Intervention.user_rating.desc()).limit(limit).all()

        return [
            {
                "type": i.intervention_type,
                "rating": i.user_rating,
                "times_used": db.query(Intervention).filter(
                    Intervention.user_id == user.id,
                    Intervention.intervention_type == i.intervention_type
                ).count()
            }
            for i in interventions
        ]

    def generate_tone_matched_response(
        self,
        base_script: str,
        user_pitch: float,
        user_tempo: float
    ) -> Dict:
        """
        Modify response to match user's vocal characteristics.

        For TTS generation (would integrate with Hume EVI settings).
        """
        # Pitch matching (Hz)
        target_pitch = user_pitch * 0.95  # Slightly lower for calming effect

        # Tempo matching (words per minute)
        target_tempo = user_tempo * 0.85  # 15% slower to induce calm

        return {
            "script": base_script,
            "tts_settings": {
                "pitch_hz": target_pitch,
                "tempo_wpm": target_tempo,
                "energy": "soft",  # Always calm for interventions
                "prosody": "soothing"
            }
        }
