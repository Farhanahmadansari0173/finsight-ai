from groq import Groq
from database import get_db
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_financial_context():
    db = get_db()
    transactions = await db.transactions.find().sort("date", -1).to_list(100)
    pipeline = [
        {"$match": {"amount": {"$lt": 0}}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
        {"$sort": {"total": 1}}
    ]
    spending_by_category = await db.transactions.aggregate(pipeline).to_list(20)
    total_income = 0
    total_expenses = 0
    for t in transactions:
        if t["amount"] > 0:
            total_income += t["amount"]
        else:
            total_expenses += abs(t["amount"])
    budgets = await db.budgets.find().to_list(20)
    context = {
        "transactions": [
            {
                "description": t["description"],
                "amount": t["amount"],
                "category": t["category"],
                "date": t["date"].strftime("%Y-%m-%d") if isinstance(t["date"], datetime) else str(t["date"])
            }
            for t in transactions
        ],
        "spending_by_category": [
            {"category": s["_id"], "total_spent": abs(s["total"]), "transactions": s["count"]}
            for s in spending_by_category
        ],
        "summary": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_savings": total_income - total_expenses
        },
        "budgets": [
            {"category": b["category"], "limit": b["limit"], "month": b["month"]}
            for b in budgets
        ]
    }
    return context

async def ask_agent(user_question: str) -> str:
    context = await get_financial_context()
    prompt = f"""You are FinSight AI, an intelligent personal finance agent.
You have access to the user's real financial data from MongoDB.

FINANCIAL DATA:
{json.dumps(context, indent=2)}

USER QUESTION: {user_question}

Instructions:
- Answer based on the actual data provided
- Be specific with numbers and amounts (use ₹ for Indian Rupees)
- Detect anomalies and warn about overspending
- Give actionable advice
- Be conversational but precise
- Highlight any subscriptions or recurring charges

Answer:"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

async def get_anomalies() -> str:
    context = await get_financial_context()
    prompt = f"""You are FinSight AI. Analyze this financial data and detect anomalies.

FINANCIAL DATA:
{json.dumps(context, indent=2)}

Detect and list:
1. Unusual spending spikes in any category
2. Subscriptions that might be forgotten
3. Categories where spending exceeds budget
4. Any concerning patterns

Be specific with amounts in ₹. Format as a clear bullet-point list."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content

async def get_forecast() -> str:
    context = await get_financial_context()
    prompt = f"""You are FinSight AI. Based on this financial data, provide a spending forecast.

FINANCIAL DATA:
{json.dumps(context, indent=2)}

Provide:
1. Projected monthly expenses based on current trends
2. Which categories are on track vs overspending
3. Estimated savings at end of month
4. Top 3 recommendations to save money

Use ₹ for amounts. Be specific and actionable."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )
    return response.choices[0].message.content