# 👔 Gucci Group HR Simulation — AI NPC Engine

> **Take-home Assignment for AI Engineer Intern @ Edtronaut**
>
> A dynamic, multi-agent AI simulation designed to train HR Strategy and Stakeholder Management skills through real-time, stateful interactions with an AI CEO.

---

## 🌟 Project Overview

Unlike traditional "static" simulations (e.g., reading PDFs and submitting forms), this project introduces a **Dynamic AI Simulation Engine**. Users interact with the *CEO of Gucci Group* to propose HR transformations. The NPC has a **memory**, **emotional states**, and acts as an **autonomous agent** capable of using business tools and enforcing corporate guidelines.

---

## ✨ Key Features

### 🎭 Stateful Role-Playing (Sentiment Tracking)
The CEO agent maintains a hidden **Sentiment Score (1–10)**. If the user disrespects the *Group DNA*, the score drops and the CEO becomes cold and rejects proposals. If the user acts strategically, the CEO becomes a collaborative partner.

### 👁️ Invisible Supervisor (The "Director" Layer)
A secondary background agent that monitors the **last 3 turns** of the conversation. If the user gets "stuck" or violates core guidelines, the Director injects a subtle hint into the CEO's prompt to seamlessly guide the user back on track.

### 🛠️ Agentic Tool Use
The AI doesn't just chat — it **executes Python functions**. Included tools:
- **KPI Calculator**
- **HR A/B Strategy Simulator**
- **Portfolio Exporter**

### 📚 RAG-Enabled Knowledge
Integrated with **FAISS** and **Google Generative AI Embeddings** (`text-embedding-004`) to ground the CEO's responses strictly in the Gucci Brand Guidelines.

### 🛡️ Safety Guardrails
Robust prompt engineering and custom **Regex parsers** prevent jailbreaks, prompt injections, and handle unpredictable LLM structured outputs.

---

## 🏗️ System Architecture

The system utilizes a **Multi-Agent Orchestration Pipeline**:

```
User Input
    │
    ▼
FastAPI Endpoint
    │
    ▼
Director Agent  ──────────────────────────────────┐
(reads last 3 turns, generates Hint if needed)    │
    │                                             │
    ▼                                             │
Prompt Manager                                    │
(injects Hint + Sentiment Score into context) ◄───┘
    │
    ▼
CEO Agent
(retrieves docs via FAISS, calls Tools, generates response)
    │
    ▼
Regex Parser
(extracts [SENTIMENT: X] tag, updates state, cleans output)
    │
    ▼
Clean Response → User Interface
```

---

## 🚀 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | LangChain (Core Orchestration & Tool Binding) |
| **LLM** | Google Gemini 2.5 Flash (optimized for low-latency chat) |
| **Embeddings** | E5-base-v2 (`intfloat/e5-base-v2`) |
| **Vector DB** | FAISS (in-memory, zero network latency) |
| **Backend API** | FastAPI & Uvicorn |

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gucci-hr-simulation.git
cd gucci-hr-simulation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory and add your API key:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 4. Run the API Server

```bash
python main.py
```

The server will start at **http://localhost:8000**.

### 5. Chat with the CEO Agent

Open a **new terminal** and run:

```bash
python chat.py
```

You will enter an interactive session where you can converse directly with the AI CEO of Gucci Group. Type your HR proposals and observe how the CEO's sentiment shifts in real time.

---

## 🧪 Evaluation Criteria Addressed

This prototype was built specifically to address the Edtronaut evaluation criteria:

| Criterion | Implementation |
|---|---|
| **Role-Playing Fidelity** | Stateful Sentiment tracking + strict Group DNA adherence |
| **Architecture Soundness** | Decoupled Multi-Agent (Director + CEO) design + LangChain integration |
| **Problem Solving** | Zero-shot prompt injection protection, out-of-domain redirection, and custom parsers for LLM function-calling edge cases |

---

*Developed by Tran Le Gia Thoai*