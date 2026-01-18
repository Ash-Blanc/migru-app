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

- [Bun](https://bun.sh/) (Fast all-in-one JavaScript runtime)

- [uv](https://github.com/astral-sh/uv) (Extremely fast Python package installer and resolver)



### 1. Frontend Setup



```bash

# Install dependencies

bun install



# Start the development server

bun run dev

```



The frontend will be available at `http://localhost:5173`.



### 2. Backend Setup



```bash

# uv will automatically manage the virtual environment and dependencies

uv run python -m src.backend.app.main

```



The backend API will be available at `http://localhost:8000`.



## 📂 Project Structure

```
migru-app/
├── src/
│   ├── backend/        # Python FastAPI backend
│   │   └── app/        # Application logic (agents, tools, main)
│   └── frontend/       # SvelteKit source code
│       ├── lib/        # Shared components and stores
│       └── routes/     # Application pages (forecast, log, etc.)
└── ...config files
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📄 License

[MIT](LICENSE)