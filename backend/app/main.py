from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from backend.app.agent import get_migru_agent
from backend.app.tools import get_forecast, log_attack, get_status, update_status
import inspect

app = FastAPI(title="Migru Agent Backend")

agent = get_migru_agent()

# --- Request Models ---

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict

# --- Routes ---

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Migru Agent Backend"}

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
        "update_status": update_status
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
