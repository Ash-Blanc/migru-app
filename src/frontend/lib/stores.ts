import { writable, get } from 'svelte/store';
import {
    VoiceClient,
    type ToolCallMessage,
    type ToolResponseMessage
} from '@humeai/voice';

// --- Helper for Persistence ---
const createPersistentStore = <T>(key: string, startValue: T) => {
    if (typeof window === 'undefined' || typeof localStorage === 'undefined') {
        return writable(startValue);
    }
    const json = localStorage.getItem(key);
    let initial: T = startValue;
    if (json) {
        try {
            initial = JSON.parse(json);
        } catch (e) {
            console.error(`Failed to parse stored key "${key}"`, e);
        }
    }
    const store = writable(initial);
    store.subscribe(value => {
        localStorage.setItem(key, JSON.stringify(value));
        if (key === 'migru_theme' && typeof document !== 'undefined') {
            const theme = value as string;
            let appliedTheme = theme;

            if (theme === 'light') {
                appliedTheme = 'nord';
            } else if (theme === 'dark') {
                appliedTheme = 'sunset';
            } else if (theme === 'system') {
                const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                appliedTheme = isDark ? 'sunset' : 'nord';
            }

            document.documentElement.setAttribute('data-theme', appliedTheme);
        }
    });
    return store;
};

// --- App State ---
export const userStatus = createPersistentStore<string>("migru_status", "Balanced");
export const riskLevel = createPersistentStore<string>("migru_risk", "Moderate");
export const hrv = createPersistentStore<number>("migru_hrv", 65);
export const userTheme = createPersistentStore<string>("migru_theme", "light");
export const notificationsEnabled = createPersistentStore<boolean>("migru_notifications", true);
export const logs = createPersistentStore<any[]>("migru_logs", []);

// --- Voice Agent State ---
export type AgentState = "disconnected" | "connecting" | "idle" | "listening" | "processing" | "speaking" | "error";
export const agentState = writable<AgentState>("disconnected");
export const agentMessage = writable<string | null>(null);
export const userTranscript = writable<string | null>(null);
export const isAgentOpen = writable<boolean>(false);

// --- API Keys ---
export const apiKeys = {
    humeKey: createPersistentStore('migru_hume_key', ''),
    humeSecret: createPersistentStore('migru_hume_secret', ''),
    geminiKey: createPersistentStore('migru_gemini_key', ''),
    mistralKey: createPersistentStore('migru_mistral_key', '')
};

// --- Hume EVI Client (SDK v0.1.x) ---
class HumeEVIClient {
    private client: VoiceClient | null = null;

    async connect() {
        if (this.client) {
            console.log("Hume client already exists");
            isAgentOpen.set(true);
            return;
        }

        console.log("--- Initializing Hume EVI ---");

        // 1. Check for Secure Context (Required for Mic)
        if (typeof window !== 'undefined' && !window.isSecureContext) {
            console.error("❌ NOT A SECURE CONTEXT! Microphone access will be blocked.");
            console.warn("Please use http://localhost:5173 or HTTPS if using an IP/Domain.");
            agentState.set("error");
            agentMessage.set("Security error: Use localhost or HTTPS for voice chat.");
            return;
        }

        // 2. Check for MediaDevices
        if (typeof navigator === 'undefined' || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.error("❌ MediaDevices / getUserMedia not supported in this browser.");
            agentState.set("error");
            agentMessage.set("Voice chat not supported on this browser.");
            return;
        }

        agentState.set("connecting");

        // 3. Get Auth Token
        let accessToken = '';
        try {
            const hKey = get(apiKeys.humeKey);
            const hSecret = get(apiKeys.humeSecret);
            const headers: Record<string, string> = {};
            if (hKey) headers['x-hume-api-key'] = hKey;
            if (hSecret) headers['x-hume-secret-key'] = hSecret;

            console.log("Phase 1: Fetching access token...");
            const res = await fetch('http://localhost:8000/hume/auth', { headers });
            if (!res.ok) throw new Error(`Auth backend failed: ${res.status}`);
            const data = await res.json();
            accessToken = data.access_token;
            console.log("✓ Access token received");
        } catch (e) {
            console.error("❌ Token fetch failed:", e);
            agentState.set("error");
            agentMessage.set("Auth failed. Check backend connection.");
            return;
        }

        // 4. Initialize SDK
        try {
            console.log("Phase 2: Connecting to Hume EVI WebSocket...");

            // In v0.1.x, we use the constructor directly
            this.client = new VoiceClient({
                hostname: 'api.hume.ai',
                auth: { type: 'accessToken', value: accessToken },

                onOpen: () => {
                    console.log("✓ Hume EVI Connected!");
                    agentState.set("idle");
                    isAgentOpen.set(true);
                    agentMessage.set("Connected and ready!");
                },

                onMessage: (msg: any) => {
                    if (!msg) return;
                    console.log("Hume message:", msg.type);

                    switch (msg.type) {
                        case "user_message":
                            if (msg.message?.content) userTranscript.set(msg.message.content);
                            agentState.set("processing");
                            break;
                        case "assistant_message":
                            if (msg.message?.content) {
                                agentMessage.set(msg.message.content);
                                agentState.set("speaking");
                            }
                            break;
                        case "audio_output":
                            agentState.set("speaking");
                            break;
                        case "user_interruption":
                            agentState.set("listening");
                            break;
                        case "tool_call":
                            this.handleToolCall(msg);
                            break;
                        case "error":
                            console.error("EVI Server Error:", msg.message);
                            agentState.set("error");
                            agentMessage.set(`Error: ${msg.message}`);
                            break;
                    }
                },

                onError: (err: any) => {
                    console.error("❌ WebSocket Error:", err);
                    agentState.set("error");
                    agentMessage.set("Connection lost. Retrying...");
                },

                onClose: () => {
                    console.log("EVI Connection CLOSED");
                    this.client = null;
                    agentState.set("disconnected");
                }
            });

            console.log("Phase 3: Handshaking...");
            this.client.connect();

        } catch (e) {
            console.error("❌ SDK Initialization failed:", e);
            agentState.set("error");
            agentMessage.set(`SDK error: ${(e as Error).message}`);
        }
    }

    disconnect() {
        if (this.client) {
            this.client.disconnect();
            this.client = null;
        }
        agentState.set("disconnected");
        isAgentOpen.set(false);
    }

    toggleListening() {
        console.log("toggleListening called - SDK handles VAD automatically.");
    }

    private async handleToolCall(message: ToolCallMessage) {
        agentState.set("processing");
        console.log("Tool execution:", message.name);
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
            this.client?.sendToolMessage({
                type: 'tool_response',
                tool_call_id: message.tool_call_id,
                content: JSON.stringify(data.result)
            } as ToolResponseMessage);
        } catch (e) {
            console.error("Tool execution error:", e);
            this.client?.sendToolMessage({
                type: 'tool_response',
                tool_call_id: message.tool_call_id,
                content: "Error executing tool"
            } as ToolResponseMessage);
        }
    }
}

export const humeClient = new HumeEVIClient();