from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from backend.app.agent import get_migru_agent
from backend.app.tools import get_forecast, log_attack, get_status, update_status, get_recent_logs
import inspect
import os
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Migru Agent Backend")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = get_migru_agent()

# --- Request Models ---

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict

# --- Routes ---

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Migru Agent Backend"}

@app.get("/hume/auth")
async def hume_auth():
    """
    Generates a Hume Access Token using the API Key and Secret Key from env.
    """
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    HUME_SECRET_KEY = os.getenv("HUME_SECRET_KEY")
    
    if not HUME_API_KEY or not HUME_SECRET_KEY:
        # Fallback/Mock for demo if keys aren't present
        return {"access_token": "mock_token_for_demo_purposes", "note": "Set HUME_API_KEY/SECRET env vars for real token"}

    # Request a token from Hume API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.hume.ai/oauth2-cc/token",
            auth=(HUME_API_KEY, HUME_SECRET_KEY),
            data={"grant_type": "client_credentials"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch Hume token")

@app.post("/agent/chat")
def chat(message: str):
    """
    Direct chat endpoint for testing the Agno agent logic.
    """
    response = agent.run(message)
    return {"response": response.content}

@app.post("/hume/tool-call")
def handle_hume_tool_call(request: ToolCallRequest):
    """
    Generic webhook to handle tool calls coming from Hume EVI.
    Hume will send the tool name and arguments here.
    """
    tool_map = {
        "get_forecast": get_forecast,
        "log_attack": log_attack,
        "get_status": get_status,
        "update_status": update_status,
        "get_recent_logs": get_recent_logs
    }
    
    if request.tool_name not in tool_map:
        raise HTTPException(status_code=404, detail=f"Tool {request.tool_name} not found")
    
    func = tool_map[request.tool_name]
    
    try:
        # Call the function with unpacked arguments
        result = func(**request.arguments)
        return {"result": result}
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid arguments for {request.tool_name}: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hume/tools")
def get_hume_tool_definitions():
    """
    Returns the JSON schemas for the tools to configure Hume EVI.
    This helper generates the config needed for the frontend/Hume setup.
    """
    # Helper to generate Hume-compatible tool definitions from Python functions
    # (Simplified for this prototype)
    
    tools = [
        {
            "type": "function",
            "name": "get_forecast",
            "parameters": "{}",
            "description": "Get the migraine forecast and risk level."
        },
        {
            "type": "function",
            "name": "get_status",
            "parameters": "{}",
            "description": "Get the user's current health status."
        },
        {
            "type": "function",
            "name": "update_status",
            "parameters": "{\"type\": \"object\", \"properties\": {\"status\": {\"type\": \"string\", \"enum\": [\"Balanced\", \"Prodromal\", \"Attack\", \"Postdromal\"]}}, \"required\": [\"status\"]}",
            "description": "Update the user's current health status."
        },
        {
            "type": "function",
            "name": "log_attack",
            "parameters": "{\"type\": \"object\", \"properties\": {\"severity\": {\"type\": \"integer\", \"minimum\": 1, \"maximum\": 10}, \"symptoms\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}, \"notes\": {\"type\": \"string\"}}, \"required\": [\"severity\", \"symptoms\"]}",
            "description": "Log a migraine attack with severity and symptoms."
        }
    ]
    return tools

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
