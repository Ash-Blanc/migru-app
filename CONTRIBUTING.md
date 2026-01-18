# Contributing to Migru App 🧠

Welcome! We're thrilled you're interested in contributing to Migru. Whether you're a seasoned pro or just starting out, we want to make your experience as smooth as possible.

Migru is a migraine tracking and relief app that combines a beautiful UI with powerful AI agents to help users manage their health.

## 🚀 Quick Start

You can get the whole app running in about 5 minutes.

### Prerequisites
1.  **[Bun](https://bun.sh/)**: A fast JavaScript runtime (for the frontend).
2.  **[uv](https://github.com/astral-sh/uv)**: A fast Python package installer (for the backend).

### 1. Set up the Backend (Python)
The backend handles the AI agents and data processing.

```bash
# From the project root
uv run python -m src.backend.app.main
```
*   The API will start at `http://localhost:8000`.
*   **Note:** You might need to create a `.env` file with API keys (see [Configuration](#-configuration-api-keys)).

### 2. Set up the Frontend (SvelteKit)
The frontend is the user interface you interact with.

```bash
# Open a new terminal
bun install
bun run dev
```
*   The app will open at `http://localhost:5173`.

---

## 🗺️ Navigation Guide

Here's where everything lives so you don't get lost:

*   **`src/frontend/`**: The SvelteKit application.
    *   **`routes/`**: The pages of the app (Home, Log, Active Relief, Settings).
    *   **`lib/components/`**: Reusable UI blocks (like `VoiceAgent.svelte`, `ForecastCard.svelte`).
    *   **`lib/stores.ts`**: The "brain" of the frontend. It handles state (user status, logs) and the **Hume AI client logic**.
*   **`src/backend/`**: The FastAPI application.
    *   **`app/main.py`**: The server entry point and API routes.
    *   **`app/agent.py`**: Logic for the Agno/Mistral agents.

---

## 🎯 Focus Areas (Where we need help!)

If you're looking for something to work on, here are the areas that "lowkey need improvement":

### 1. 🎨 UI/UX Polish
The app uses **Tailwind CSS v4** and **DaisyUI**. We want it to feel calm, smooth, and modern.
*   **Responsiveness:** Check how pages look on mobile vs. desktop. Some layouts might need tweaking.
*   **Animations:** We use `svelte/transition` (fly, fade) but could use more subtle interactions.
*   **Theming:** The theme switcher logic resides in `stores.ts`. Feel free to add better color palettes for migraine sensitivity (e.g., lower contrast or warmer tones).

### 2. 🤖 Hume AI Integration
The Voice Agent (the microphone button) uses **Hume EVI** to talk to users. It's cool but can be tricky.
*   **Where is the code?**
    *   Frontend logic: `src/frontend/lib/stores.ts` (look for `HumeEVIClient` class) and `src/frontend/lib/components/VoiceAgent.svelte`.
    *   Backend auth: `src/backend/app/main.py` (look for `/hume/auth`).
*   **Common "It's not working" fixes:**
    *   **Secure Context:** Voice features *only* work on `localhost` or `https`. If you access via IP address, the mic won't work.
    *   **API Keys:** You need a Hume API Key and Secret. You can put them in a `.env` file for the backend OR enter them in the App Settings page (which saves to local storage).
    *   **Backend Connection:** If `fetch('http://localhost:8000/hume/auth')` fails, the agent won't start. Ensure the Python backend is running.

### 3. 🐛 General Bugs
*   Check the console for errors.
*   If you see "mock_token_for_demo_purposes", it means valid API keys haven't been provided yet.

---

## 🔑 Configuration (API Keys)

To fully test the AI features, you'll need API keys. You can get them from [Hume AI](https://hume.ai/) and [Google AI Studio](https://aistudio.google.com/) (or Mistral).

**Option A: `.env` file (Backend)**
Create a `.env` file in the root:
```bash
HUME_API_KEY=your_key
HUME_SECRET_KEY=your_secret
GOOGLE_API_KEY=your_gemini_key
```

**Option B: In-App Settings (Frontend)**
Go to the **Settings** page in the app and paste your keys. This is great for quick testing without restarting servers.

---

## 🤝 How to Submit Changes

1.  **Fork** the repository.
2.  **Create a Branch** for your feature (`git checkout -b fix/voice-agent-connection`).
3.  **Commit** your changes (`git commit -m "fix: handle mic permission errors gracefully"`).
4.  **Push** to your fork.
5.  **Open a Pull Request**. We'll review it ASAP!

---

**Questions?**
Feel free to open an issue if you get stuck. Happy coding! 🚀
