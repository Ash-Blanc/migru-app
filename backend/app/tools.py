from typing import List, Optional
from pydantic import BaseModel
import datetime

# --- In-Memory State (Mock DB) ---
class AppState(BaseModel):
    status: str = "Balanced"
    hrv: str = "65ms"
    risk_level: str = "Moderate"
    logs: List[dict] = []

db = AppState()

# --- Tool Functions ---

def get_forecast() -> str:
    """
    Retrieves the current migraine forecast and risk level.
    """
    return f"The current risk level is {db.risk_level}. Barometric pressure is falling, which might trigger symptoms. Humidity is at 45%."

def log_attack(severity: int, symptoms: List[str], notes: str = "") -> str:
    """
    Logs a migraine attack with details.
    
    Args:
        severity: Pain level from 1 to 10.
        symptoms: List of symptoms experienced (e.g., 'Nausea', 'Aura').
        notes: Any additional notes or potential triggers.
    """
    entry = {
        "date": datetime.datetime.now().isoformat(),
        "type": "attack",
        "severity": severity,
        "symptoms": symptoms,
        "notes": notes
    }
    db.logs.append(entry)
    
    # Auto-update status if severe
    if severity > 3:
        db.status = "Attack"
        
    return f"Attack logged. Severity: {severity}. Status updated to {db.status}."

def get_status() -> str:
    """
    Gets the user's current health status and HRV.
    """
    return f"Current status is {db.status}. HRV is {db.hrv}."

def update_status(status: str) -> str:
    """
    Updates the user's current status (e.g., Balanced, Attack, Recovery).
    """
    db.status = status
    return f"Status updated to {status}."
