from fastapi import Header, Optional, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from src.backend.app.agent import get_migru_agent
from src.backend.app.tools import get_forecast, log_attack, get_status, update_status, get_recent_logs
from agno.os import AgentOS
import os
from fastapi.middleware.cors import CORSMiddleware
import httpx

# 1. Initialize the Migru Agent
migru_agent = get_migru_agent()

# 2. Create the AgentOS instance
# This automatically creates a FastAPI app with agentic endpoints
agent_os = AgentOS(
    id="migru-os",
    name="Migru Agent OS",
    agents=[migru_agent],
)

# 3. Get the FastAPI app from AgentOS
app = agent_os.get_app()

# Allow CORS for frontend (AgentOS might already handle this, but we'll be explicit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Models ---

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict

# --- Custom Routes (Hume Integration) ---

@app.get("/hume/auth")
async def hume_auth(
    x_hume_api_key: Optional[str] = Header(None), 
    x_hume_secret_key: Optional[str] = Header(None)
):
    """
    Generates a Hume Access Token.
    Prioritizes headers, then environment variables.
    """
    HUME_API_KEY = x_hume_api_key or os.getenv("HUME_API_KEY")
    HUME_SECRET_KEY = x_hume_secret_key or os.getenv("HUME_SECRET_KEY")
    
    if not HUME_API_KEY or not HUME_SECRET_KEY:
        return {"access_token": "mock_token_for_demo_purposes", "note": "Set HUME_API_KEY/SECRET in Settings or env vars"}

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
def chat(
    message: str, 
    x_gemini_api_key: Optional[str] = Header(None),
    x_mistral_api_key: Optional[str] = Header(None)
):
    """
    Direct chat endpoint for testing.
    Dynamically instantiates the agent based on provided keys.
    """
    agent = get_migru_agent(gemini_key=x_gemini_api_key, mistral_key=x_mistral_api_key)
    response = agent.run(message)
    return {"response": response.content}

@app.post("/hume/tool-call")
def handle_hume_tool_call(request: ToolCallRequest):
    """
    Generic webhook to handle tool calls coming from Hume EVI.
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
        result = func(**request.arguments)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hume/tools")
def get_hume_tool_definitions():
    """
    Returns the JSON schemas for the tools to configure Hume EVI.
    """
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
        },
        {
            "type": "function",
            "name": "get_recent_logs",
            "parameters": "{\"type\": \"object\", \"properties\": {\"limit\": {\"type\": \"integer\"}}}",
            "description": "Get the most recent health logs."
        }
    ]
    return tools

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
