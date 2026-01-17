# Migru App 🧠

**Migru** is a modern, intelligent migraine tracking and relief application. It combines a sleek SvelteKit frontend with a powerful AI agent backend (powered by Agno and Hume EVI) to help users forecast risks, log attacks, and find active relief.

![Migru App](https://via.placeholder.com/800x400?text=Migru+App+Preview)

## ✨ Features

-   **🔍 Forecast:** Personalized migraine risk prediction.
-   **📝 Log:** Easy logging of migraine attacks, symptoms, and severity.
-   **🛡️ Active Relief:** Guidance and tools to manage ongoing attacks.
-   **🤖 AI Companion:** Voice-enabled and intelligent agent interactions using **Hume EVI** and **Agno**.
-   **📱 PWA Ready:** Installable on mobile devices for quick access.

## 🛠️ Tech Stack

### Frontend
-   **Framework:** [SvelteKit](https://kit.svelte.dev/) (Svelte 5)
-   **Styling:** [TailwindCSS v4](https://tailwindcss.com/) & [DaisyUI](https://daisyui.com/)
-   **Language:** TypeScript

### Backend
-   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
-   **AI/Agent:** [Agno](https://github.com/agno-agi/agno) & [Hume AI](https://hume.ai/)
-   **Server:** Uvicorn

## 🚀 Getting Started

### Prerequisites
-   Node.js (v20+)
-   Python (v3.10+)

### 1. Frontend Setup

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (ensure you have a requirements.txt, or install manually for now)
pip install fastapi uvicorn agno pydantic

# Start the server
python -m app.main
```

The backend API will be available at `http://localhost:8000`.

## 📂 Project Structure

```
migru-app/
├── backend/            # Python FastAPI backend
│   └── app/            # Application logic (agents, tools, main)
├── src/                # SvelteKit source code
│   ├── lib/            # Shared components and stores
│   └── routes/         # Application pages (forecast, log, etc.)
├── static/             # Static assets (manifest, icons)
└── ...config files
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

[MIT](LICENSE)