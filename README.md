---
title: AI Research Agent
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 8501
pinned: false
---

# 🔬 AI Research Agent
### Multi-Agent LLM System for Autonomous Research Discovery

> Built by **Vaibhav Mishra** | RGIPT Amethi

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Groq](https://img.shields.io/badge/LLM-Groq%20Llama3-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What It Does

A researcher types a question like:

> *"How can federated learning be applied to EV battery monitoring?"*

The system automatically:

1. 🧠 **Plans** — breaks the question into targeted search strategies
2. 🔍 **Searches** — fetches real papers from Arxiv API
3. 📊 **Indexes** — embeds papers into a FAISS vector store
4. 📖 **Reads** — extracts methods, results, and contributions
5. 💡 **Ideates** — generates 3 novel research directions
6. 🧪 **Designs** — proposes concrete experiments with datasets and metrics

---

## 🏗️ Agent Architecture
```
User Query
    ↓
┌─────────────────┐
│  Planner Agent  │  → breaks query into 3 targeted search strategies
└────────┬────────┘
         ↓
┌─────────────────┐
│  Search Agent   │  → fetches papers from Arxiv API
└────────┬────────┘
         ↓
┌─────────────────┐
│  RAG Pipeline   │  → FAISS + sentence-transformers embeddings
└────────┬────────┘
         ↓
┌─────────────────┐
│  Reader Agent   │  → extracts problem, method, results per paper
└────────┬────────┘
         ↓
┌─────────────────┐
│  Idea Agent     │  → generates novel research directions
└────────┬────────┘
         ↓
┌──────────────────────┐
│ Experiment Designer  │  → proposes datasets, models, metrics
└────────┬─────────────┘
         ↓
┌─────────────────┐
│  Streamlit UI   │  → interactive dashboard
└─────────────────┘
```

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq API — Llama 3.3 70B |
| Agent Orchestration | Custom Python pipeline |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| Paper Search | Arxiv API |
| Frontend | Streamlit |
| Deployment | Docker + HuggingFace Spaces |

---

## 📁 Project Structure
```
ai-research-agent/
├── agents/
│   ├── planner_agent.py       # breaks query into search tasks
│   ├── search_agent.py        # fetches papers from Arxiv
│   ├── reader_agent.py        # analyzes papers via LLM
│   ├── idea_agent.py          # generates research ideas
│   └── experiment_agent.py    # designs experiment plans
├── rag/
│   ├── embeddings.py          # sentence-transformer embeddings
│   └── retriever.py           # FAISS vector store
├── frontend/
│   └── app.py                 # Streamlit dashboard
├── pipeline.py                # chains all agents together
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/regardsvaibhav/AI-Research-Agent.git
cd AI-Research-Agent
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add API key

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app
```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 🐳 Docker
```bash
docker-compose up --build
```

---

## 💡 Example Output

**Query:** `How can federated learning be applied to EV battery monitoring?`

**Planner Output:**
```
Search Queries:
- federated learning for IoT battery monitoring
- distributed ML for EV battery management
- privacy-preserving battery state estimation
```

**Generated Ideas:**
```
IDEA 1: Federated Battery Health Prediction
→ FedAvg + LSTM across EV fleets
→ NASA Battery Dataset

IDEA 2: Privacy-Preserving Degradation Modeling
→ Differential privacy + federated averaging
→ CALCE Battery Dataset

IDEA 3: Decentralized Charging Optimization
→ Central server-free FL + GCN
→ London EV Charging Dataset
```

**Experiment Design:**
```
DATASET: NASA Battery Dataset (3.6M data points, 41 batteries)
MODEL: FedAvg + LSTM
BASELINE: Centralized LSTM
METRICS: MAE, MSE, R-squared
```

---

## 🧠 Design Decisions

**Why FAISS over a vector database?**
Lightweight, no server needed, perfect for a self-contained research tool.

**Why Groq over OpenAI?**
Free tier, ~500 tokens/sec inference speed, sufficient quality for research tasks.

**Why separate agents instead of one big prompt?**
Single responsibility per agent makes the system easier to debug, test, and extend independently.

---

## 🔭 Roadmap

- [x] 5-agent pipeline
- [x] RAG with FAISS
- [x] Streamlit UI
- [x] Docker deployment
- [x] HuggingFace Spaces
- [ ] Finetuned Llama 3.2 1B for idea generation
- [ ] LangGraph orchestration
- [ ] Evaluation framework

---

## 📄 License

MIT
