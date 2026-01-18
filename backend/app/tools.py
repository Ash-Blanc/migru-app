from typing import List, Optional
from pydantic import BaseModel
import datetime
import random

# --- In-Memory State (Mock DB) ---
class AppState(BaseModel):
    status: str = "Balanced"
    hrv: int = 65
    risk_level: str = "Moderate"
    logs: List[dict] = []

db = AppState()

# --- Tool Functions ---

def get_forecast() -> str:
    """
    Retrieves the current migraine forecast, risk level, and environmental factors.
    """
    # Simulate dynamic data
    weather = random.choice(["Cloudy", "Sunny", "Rainy", "Stormy"])
    pressure = random.choice(["Stable", "Falling Rapidly", "Rising"])
    
    return (
        f"Current Risk: {db.risk_level}. "
        f"Weather is {weather} with {pressure} barometric pressure. "
        "HRV is slightly lower than your baseline."
    )

def log_attack(severity: int, symptoms: List[str], notes: str = "") -> str:
    """
    Logs a migraine attack with details.
    
    Args:
        severity: Pain level from 1 to 10.
        symptoms: List of symptoms experienced (e.g., 'Nausea', 'Aura', 'Light Sensitivity').
        notes: Any additional notes or potential triggers.
    """
    entry = {
        "date": datetime.datetime.now().isoformat(),
        "type": "attack",
        "severity": severity,
        "symptoms": symptoms,
        "notes": notes
    }
    db.logs.insert(0, entry) # Add to top
    
    # Auto-update status if severe
    if severity >= 4:
        db.status = "Attack"
    elif severity > 0:
        db.status = "Prodromal"
        
    return f"I've logged that for you. Severity {severity}/10. Status is now '{db.status}'."

def get_status() -> str:
    """
    Gets the user's current health status and HRV.
    """
    return f"You are currently in the '{db.status}' phase. Your Heart Rate Variability (HRV) is {db.hrv}ms."

def update_status(status: str) -> str:
    """
    Updates the user's current status.
    Allowed values: "Balanced", "Prodromal", "Attack", "Postdromal", "Recovery".
    """
    db.status = status
    return f"Status updated to {status}."

def get_recent_logs(limit: int = 3) -> str:
    """
    Retrieves the most recent health logs.
    """
    if not db.logs:
        return "No recent logs found."
    
    recent = db.logs[:limit]
    summary = []
    for log in recent:
        date_str = log["date"].split("T")[0]
        if log["type"] == "attack":
            summary.append(f"- {date_str}: Attack (Severity {log['severity']}), Symptoms: {', '.join(log['symptoms'])}")
    
    return "\n".join(summary)
