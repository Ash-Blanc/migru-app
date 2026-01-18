import { writable } from 'svelte/store';

// --- App State ---
export const userStatus = writable("Balanced"); // Balanced, Prodromal, Attack, Postdromal
export const riskLevel = writable("Moderate");
export const hrv = writable(65);

// --- Voice Agent State ---
export type AgentState = "disconnected" | "connecting" | "idle" | "listening" | "processing" | "speaking" | "error";

export const agentState = writable<AgentState>("disconnected");
export const agentMessage = writable<string | null>(null); // Last message from agent
export const userTranscript = writable<string | null>(null); // Real-time user transcript

// --- Mock Hume Client (simulating the SDK) ---
class MockHumeClient {
    async connect() {
        agentState.set("connecting");
        setTimeout(() => {
            agentState.set("idle");
            agentMessage.set("Hello! I'm Migru. How are you feeling today?");
        }, 1500);
    }

    async disconnect() {
        agentState.set("disconnected");
        agentMessage.set(null);
    }

    async toggleListening() {
        // In a real app, this would toggle the microphone
        agentState.update(s => {
            if (s === "idle") return "listening";
            if (s === "listening") {
                // Simulate processing
                setTimeout(() => {
                    agentState.set("processing");
                    setTimeout(() => {
                        agentState.set("speaking");
                        agentMessage.set("I understand. I've logged that for you. Is there anything else?");
                        setTimeout(() => agentState.set("idle"), 3000);
                    }, 1000);
                }, 1000);
                return "processing"; // Immediate transition to processing simulation
            }
            return s;
        });
    }
}

export const humeClient = new MockHumeClient();