import { writable, get } from 'svelte/store';
import { 
    VoiceClient, 
    type VoiceEventMap, 
    type ToolCallMessage,
    type ToolResponseMessage 
} from '@humeai/voice-embed';

// --- App State ---
export const userStatus = writable("Balanced"); // Balanced, Prodromal, Attack, Postdromal
export const riskLevel = writable("Moderate");
export const hrv = writable(65);

// --- Voice Agent State ---
export type AgentState = "disconnected" | "connecting" | "idle" | "listening" | "processing" | "speaking" | "error";

export const agentState = writable<AgentState>("disconnected");
export const agentMessage = writable<string | null>(null); // Last message from agent
export const userTranscript = writable<string | null>(null); // Real-time user transcript

// --- API Keys ---
// Helper to persist to localStorage
const createPersistentStore = (key: string, startValue: string) => {
    let initialValue = startValue;
    if (typeof localStorage !== 'undefined') {
        const storedValue = localStorage.getItem(key);
        if (storedValue) {
            initialValue = storedValue;
        }
    }

    const { subscribe, set, update } = writable(initialValue);
    
    if (typeof localStorage !== 'undefined') {
        subscribe(current => {
            localStorage.setItem(key, current);
        });
    }

    return { subscribe, set, update };
};

export const apiKeys = {
    humeKey: createPersistentStore('migru_hume_key', ''),
    humeSecret: createPersistentStore('migru_hume_secret', ''),
    geminiKey: createPersistentStore('migru_gemini_key', ''),
    mistralKey: createPersistentStore('migru_mistral_key', '')
};

// --- Real Hume Client (using SDK) ---
class RealHumeClient {
    private client: VoiceClient | null = null;

    async connect() {
        if (this.client) return;

        agentState.set("connecting");

        // Fetch access token from our backend (which handles the secret key)
        const humeKey = get(apiKeys.humeKey);
        const humeSecret = get(apiKeys.humeSecret);
        
        let accessToken = '';

        try {
            const headers: Record<string, string> = {};
            if (humeKey) headers['x-hume-api-key'] = humeKey;
            if (humeSecret) headers['x-hume-secret-key'] = humeSecret;

            const res = await fetch('http://localhost:8000/hume/auth', { headers });
            if (!res.ok) throw new Error("Failed to get Hume token");
            const data = await res.json();
            accessToken = data.access_token;
        } catch (e) {
            console.error(e);
            agentState.set("error");
            agentMessage.set("Authentication failed. Please check your settings.");
            return;
        }
        
        // Initialize the SDK
        this.client = await VoiceClient.create({
            hostname: 'https://api.hume.ai',
            accessToken,
            // You can also provide 'configId' if you have a specific EVI configuration ID
            // configId: "...", 
            
            // Handlers
            onOpen: () => {
                agentState.set("idle");
                console.log("Hume Connected");
            },
            onMessage: (message) => {
                switch (message.type) {
                    case "user_message":
                        userTranscript.set(message.message.content);
                        agentState.set("processing"); // User finished speaking
                        break;
                    case "assistant_message":
                        agentMessage.set(message.message.content);
                        agentState.set("speaking");
                        break;
                    case "audio_output":
                        // SDK handles playback, but we can update state
                        agentState.set("speaking");
                        break;
                    case "user_interruption":
                        agentState.set("listening");
                        break;
                    case "tool_call":
                        this.handleToolCall(message);
                        break;
                    case "error":
                        console.error("Hume Error:", message);
                        agentState.set("error");
                        break;
                }
            },
            onClose: () => {
                agentState.set("disconnected");
                this.client = null;
            }
        });

        // Start the session
        this.client.connect();
    }

    async disconnect() {
        if (this.client) {
            this.client.disconnect();
            this.client = null;
        }
        agentState.set("disconnected");
    }

    async toggleListening() {
        // The SDK manages the mic state mostly automatically, but you can pause/resume audio input
        // For EVI, "toggle listening" usually means mute/unmute or interrupting
        // But simply, we rely on VAD (Voice Activity Detection).
        
        // If we want to force "stop listening" (mute mic):
        // this.client?.mute(); 
        // this.client?.unmute();
        
        // For this demo, let's treat the mic button as a way to force-stop or interrupt if needed,
        // or just let the VAD handle it.
        console.log("Toggle listening (SDK handles VAD)");
    }

    private async handleToolCall(message: ToolCallMessage) {
        agentState.set("processing");
        console.log("Tool Call:", message);
        
        // Execute tool on our backend
        try {
            const res = await fetch('http://localhost:8000/hume/tool-call', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tool_name: message.name,
                    arguments: JSON.parse(message.parameters)
                })
            });
            
            const data = await res.json();
            
            // Send result back to Hume
            const responseMessage: ToolResponseMessage = {
                type: 'tool_response',
                tool_call_id: message.tool_call_id,
                content: JSON.stringify(data.result)
            };
            
            this.client?.sendToolMessage(responseMessage);
            
        } catch (e) {
            console.error("Tool execution failed", e);
            const errorMessage: ToolResponseMessage = {
                type: 'tool_response',
                tool_call_id: message.tool_call_id,
                content: "Error executing tool"
            };
            this.client?.sendToolMessage(errorMessage);
        }
    }
}

export const humeClient = new RealHumeClient();