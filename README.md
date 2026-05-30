# FinSight AI 💰
### AI-Powered Personal Finance Agent

> Built for the Google Cloud Rapid Agent Hackathon — MongoDB Track

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What is FinSight AI?

FinSight AI is an intelligent personal finance agent that goes beyond simple chatbots. It **reasons**, **plans**, and **executes** multi-step financial analysis tasks — all powered by real data from MongoDB Atlas.

Ask it anything:
- "How much did I spend on food this month?"
- "What subscriptions am I wasting money on?"
- "Will I save money this month?"
- "What are my biggest spending anomalies?"

---

## 🌐 Live Demo

Live App: https://glistening-taiyaki-f12b61.netlify.app
API: https://finsight-ai-backend-vris.onrender.com

---

## 🏗️ Architecture

User → React Frontend → FastAPI Backend → Groq LLaMA 70B
                                ↓
                      MongoDB Atlas (via MCP)
                                ↓
                    Financial Intelligence Engine

---

## 🔌 MongoDB MCP Integration

FinSight AI uses MongoDB's **Model Context Protocol (MCP)** server to give the AI agent direct access to financial data. The MCP server exposes 5 tools:

| Tool | Description |
|------|-------------|
| get_transactions | Fetch all transactions from MongoDB |
| get_spending_by_category | Aggregate spending by category |
| get_budget_status | Compare actual vs budgeted spending |
| add_transaction | Write new transactions to MongoDB |
| detect_anomalies | Detect budget overruns and patterns |

---

## ✨ Features

- 💬 **Natural Language Chat** — Ask questions in plain English
- 📊 **Live Dashboard** — Pie charts and bar charts of spending
- 🚨 **Anomaly Detection** — AI detects unusual spending patterns
- 📈 **Spending Forecast** — Projects end-of-month savings
- 📋 **Transaction History** — Full table with categories and amounts
- 🔴 **Budget Alerts** — Real-time budget vs actual comparison

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (free tier)
- Groq API key (free)

### Backend Setup

git clone https://github.com/Farhanahmadansari0173/finsight-ai.git
cd finsight-ai/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env file:

GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string

Seed the database:

python seed_data.py

Start the backend:

uvicorn main:app --reload

### Frontend Setup

cd ../frontend
npm install
npm run dev

Open http://localhost:5173

### MCP Server

cd ../backend
python mcp_server.py

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Agent | Groq LLaMA 3.3 70B |
| Database | MongoDB Atlas |
| MCP Server | MongoDB MCP Protocol |
| Backend | FastAPI + Python |
| Frontend | React + Vite + Tailwind |
| Charts | Recharts |

---

## 📹 Demo

Watch the demo video — Coming soon

---

## 🏆 Hackathon Track

**MongoDB Track** — Google Cloud Rapid Agent Hackathon 2026

---

## 📄 License

MIT License — see LICENSE for details.