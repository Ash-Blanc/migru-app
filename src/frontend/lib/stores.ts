import { writable, get } from 'svelte/store';
import {
    VoiceClient,
    getAudioStream,
    getSupportedMimeType
} from '@humeai/voice';

// V2 API Configuration
const API_URL = 'http://localhost:8000';

// Type definitions (approximate, since exports are missing in current version)
interface ToolCallMessage {
    type: 'tool_call';
    name: string;
    parameters: string | Record<string, any>;
    tool_call_id: string;
}

interface ToolResponseMessage {
    type: 'tool_response';
    tool_call_id: string;
    content: string;
}

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

// --- Configuration ---
const getBackendUrl = () => {
    return 'http://localhost:8000';
};

// --- Data Fetching (Sync with Backend) ---
export const syncWithBackend = async () => {
    try {
        console.log("Syncing with V2 backend...");
        const token = typeof localStorage !== 'undefined' ? localStorage.getItem('clerk_token') || 'dev_token' : 'dev_token';
        const res = await fetch(`${API_URL}/api/status`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (res.ok) {
            const data = await res.json();
            userStatus.set(data.status);
            riskLevel.set(data.risk_level);
            hrv.set(data.hrv);
            console.log("✅ Synced V2:", data);
        } else {
            console.error("Sync failed:", res.status);
        }
    } catch (e) {
        console.error("Backend connection error:", e);
    }
};

// Initial sync on client load
if (typeof window !== 'undefined') {
    syncWithBackend();
    // Poll every 30 seconds to keep UI fresh
    setInterval(syncWithBackend, 30000);
}

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
    humeConfigId: createPersistentStore('migru_hume_config_id', ''),
    geminiKey: createPersistentStore('migru_gemini_key', ''),
    mistralKey: createPersistentStore('migru_mistral_key', '')
};

// --- Toast Notifications ---
export interface ToastNotification {
    message: string;
    type: 'success' | 'error' | 'info';
    id?: string;
}

export const toastStore = writable<ToastNotification | null>(null);

export const showToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
    toastStore.set({ message, type, id: crypto.randomUUID() });
    setTimeout(() => {
        toastStore.update(t => (t && t.message === message ? null : t));
    }, 3000);
};

// --- Hume EVI Client (SDK v0.1.x) ---
class HumeEVIClient {
    private client: VoiceClient | null = null;
    private audioContext: AudioContext | null = null;
    private stream: MediaStream | null = null;
    private processor: ScriptProcessorNode | null = null;
    private source: MediaStreamAudioSourceNode | null = null;
    private nextStartTime = 0;

    async connect() {
        if (this.client) {
            console.log("Hume client already exists");
            isAgentOpen.set(true);
            return;
        }

        console.log("--- Initializing Hume EVI ---");
        showToast("Connecting...", "info");

        // 1. Initialize AudioContext IMMEDIATELY to capture user gesture
        try {
            const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
            if (!this.audioContext || this.audioContext.state === 'closed') {
                this.audioContext = new AudioContextClass({ sampleRate: 24000 });
            }
            // Resume immediately in case it's suspended
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }
            console.log("✓ AudioContext Initialized");
        } catch (e) {
            console.error("AudioContext Init Failed:", e);
            agentState.set("error");
            agentMessage.set("Audio error: Click to retry.");
            return;
        }

        // 2. Check for Secure Context
        if (typeof window !== 'undefined' && !window.isSecureContext && window.location.hostname !== 'localhost') {
            console.error("❌ NOT A SECURE CONTEXT!");
            agentState.set("error");
            agentMessage.set("Security error: Use localhost or HTTPS.");
            return;
        }

        agentState.set("connecting");

        // 3. Get Auth Token
        let accessToken = '';
        const configId = get(apiKeys.humeConfigId);
        
        try {
            const hKey = get(apiKeys.humeKey);
            const hSecret = get(apiKeys.humeSecret);
            const headers: Record<string, string> = {};
            if (hKey) headers['x-hume-api-key'] = hKey;
            if (hSecret) headers['x-hume-secret-key'] = hSecret;

            const res = await fetch(`${getBackendUrl()}/hume/auth`, { headers });
            if (!res.ok) throw new Error(`Auth failed: ${res.status}`);
            const data = await res.json();
            accessToken = data.access_token;
        } catch (e) {
            console.error("❌ Token fetch failed:", e);
            agentState.set("error");
            agentMessage.set("Auth failed. Check API Keys.");
            return;
        }

        // 4. Initialize SDK
        try {
            console.log("Phase 2: Connecting to Hume EVI WebSocket...");

            // @ts-ignore
            this.client = new VoiceClient({
                hostname: 'api.hume.ai',
                auth: { type: 'accessToken', value: accessToken },
                configId: configId || undefined,
                
                onOpen: async () => {
                    console.log("✓ Hume EVI Connected!");
                    // Since startAudioSystem enables the mic, we should show listening state
                    agentState.set("listening"); 
                    isAgentOpen.set(true);
                    agentMessage.set("Connected. Listening...");
                    
                    // Configure Session
                    // @ts-ignore
                    const settings = {
                        audio: {
                            channels: 1,
                            encoding: 'linear16',
                            sampleRate: 24000
                        }
                    };
                    // @ts-ignore
                    if (this.client.sendSessionSettings) {
                        // @ts-ignore
                        this.client.sendSessionSettings(settings);
                    }

                    // Start Audio I/O (using the pre-initialized context)
                    try {
                        await this.startAudioSystem();
                    } catch (err) {
                        console.error("Audio Start Error:", err);
                        agentState.set("error");
                        agentMessage.set("Microphone error.");
                        showToast("Microphone access denied", "error");
                    }
                },

                onMessage: (msg: any) => {
                    if (!msg) return;
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
                            this.playPCM(msg.data);
                            break;
                        case "user_interruption":
                            agentState.set("listening");
                            this.clearAudioQueue();
                            break;
                        case "tool_call":
                            this.handleToolCall(msg);
                            break;
                        case "error":
                            console.error("EVI Error:", msg);
                            // Don't kill session on minor errors, but log them
                            if (msg.code === 'socket_error' || msg.code === 'connection_error') {
                                agentState.set("error");
                                agentMessage.set(`Error: ${msg.message}`);
                            }
                            break;
                    }
                },
                onError: (err: any) => {
                    console.error("Socket Error:", err);
                    agentState.set("error");
                    agentMessage.set("Connection error.");
                },
                onClose: () => {
                    this.cleanup();
                    agentState.set("disconnected");
                }
            });

            this.client?.connect();

        } catch (e) {
            console.error("SDK Init Error:", e);
            agentState.set("error");
            agentMessage.set(`SDK error: ${(e as Error).message}`);
        }
    }
    
    // --- Audio System (Web Audio API) ---
    private async startAudioSystem() {
        // Initialize AudioContext if not already
        const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
        if (!this.audioContext || this.audioContext.state === 'closed') {
             this.audioContext = new AudioContextClass({ sampleRate: 24000 });
        }
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }

        this.nextStartTime = this.audioContext.currentTime;

        // Stop existing stream if any
        if (this.stream) {
            this.stream.getTracks().forEach(t => t.stop());
        }

        // Get Mic Stream
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: {
            echoCancellation: true,
            noiseSuppression: true,
            sampleRate: 24000
        }});

        // Create Processing Node
        if (this.processor) {
            this.processor.disconnect();
        }
        if (this.source) {
            this.source.disconnect();
        }

        this.processor = this.audioContext.createScriptProcessor(2048, 1, 1);
        this.source = this.audioContext.createMediaStreamSource(this.stream);
        
        this.source.connect(this.processor);
        this.processor.connect(this.audioContext.destination);

        this.processor.onaudioprocess = (e) => {
            if (!this.client || this.client.readyState !== 1) return;
            
            const inputData = e.inputBuffer.getChannelData(0);
            
            // Convert Float32 to Int16 (Linear16 PCM)
            const buffer = new ArrayBuffer(inputData.length * 2);
            const view = new DataView(buffer);
            for (let i = 0; i < inputData.length; i++) {
                let s = Math.max(-1, Math.min(1, inputData[i]));
                view.setInt16(i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
            }
            
            // Send to Hume
            this.client.sendAudio(buffer);
        };
        
        console.log("✓ Audio System Started (PCM 24kHz)");
    }

    private playPCM(base64Data: string) {
        if (!this.audioContext) return;

        // Decode Base64
        const binaryString = window.atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) bytes[i] = binaryString.charCodeAt(i);
        
        // Create Buffer (Assuming Linear16 from server as requested)
        const int16 = new Int16Array(bytes.buffer);
        const float32 = new Float32Array(int16.length);
        
        for (let i = 0; i < int16.length; i++) {
            float32[i] = int16[i] / 32768.0;
        }

        const buffer = this.audioContext.createBuffer(1, float32.length, 24000);
        buffer.getChannelData(0).set(float32);

        // Play
        const source = this.audioContext.createBufferSource();
        source.buffer = buffer;
        source.connect(this.audioContext.destination);
        
        // Schedule for gapless playback
        const startTime = Math.max(this.audioContext.currentTime, this.nextStartTime);
        source.start(startTime);
        this.nextStartTime = startTime + buffer.duration;
    }

    private clearAudioQueue() {
        if (this.audioContext) {
            this.nextStartTime = this.audioContext.currentTime;
        }
    }

    private cleanup() {
        this.source?.disconnect();
        this.processor?.disconnect();
        this.stream?.getTracks().forEach(t => t.stop());
        // Do not close AudioContext immediately if we want to reuse it? 
        // But if we disconnect, we should probably close it to save resources.
        // We will re-create it in connect().
        this.audioContext?.close();
        
        this.source = null;
        this.processor = null;
        this.stream = null;
        this.audioContext = null;
        this.client = null;
    }

    disconnect() {
        this.client?.disconnect();
        this.cleanup();
        agentState.set("disconnected");
        isAgentOpen.set(false);
    }

    async toggleListening() {
        // Ensure connected first
        const currentState = get(agentState);
        if (!this.client || currentState === 'disconnected' || currentState === 'error') {
            await this.connect();
            return;
        }

        if (!this.stream) {
            console.warn("No stream to toggle, attempting to start audio system...");
            try {
                await this.startAudioSystem();
            } catch (e) {
                console.error("Failed to restart audio:", e);
                showToast("Microphone error", "error");
                return;
            }
        }
        
        const track = this.stream?.getAudioTracks()[0];
        if (track) {
            track.enabled = !track.enabled;
            if (track.enabled) {
                agentState.set("listening");
                showToast("Unmuted", "success");
            } else {
                agentState.set("idle");
                showToast("Muted", "info");
            }
        }
    }

    private async handleToolCall(message: ToolCallMessage) {
        agentState.set("processing");
        console.log("Tool execution:", message.name);
        try {
            let args = message.parameters;
            if (typeof args === 'string') {
                 try { args = JSON.parse(args); } catch (e) {}
            }

            const res = await fetch(`${getBackendUrl()}/hume/tool-call`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tool_name: message.name,
                    arguments: args
                })
            });
            const data = await res.json();
            
            if (message.name === 'log_attack' || message.name === 'update_status') {
                 syncWithBackend();
            }

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