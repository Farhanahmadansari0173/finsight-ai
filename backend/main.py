from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import connect_db, close_db
from agent import ask_agent, get_anomalies, get_forecast
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="FinSight AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.get("/")
async def root():
    return {"message": "FinSight AI is running!", "status": "ok"}

@app.post("/ask")
async def ask(request: QuestionRequest):
    answer = await ask_agent(request.question)
    return {"question": request.question, "answer": answer}

@app.get("/anomalies")
async def anomalies():
    result = await get_anomalies()
    return {"anomalies": result}

@app.get("/forecast")
async def forecast():
    result = await get_forecast()
    return {"forecast": result}

@app.get("/transactions")
async def get_transactions():
    from database import get_db
    db = get_db()
    transactions = await db.transactions.find().sort("date", -1).to_list(100)
    for t in transactions:
        t["_id"] = str(t["_id"])
        if hasattr(t["date"], "strftime"):
            t["date"] = t["date"].strftime("%Y-%m-%d")
    return {"transactions": transactions}

@app.get("/summary")
async def get_summary():
    from database import get_db
    db = get_db()
    pipeline = [
        {"$match": {"amount": {"$lt": 0}}},
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$sort": {"total": 1}}
    ]
    spending = await db.transactions.aggregate(pipeline).to_list(20)
    return {
        "spending_by_category": [
            {"category": s["_id"], "total": abs(s["total"])}
            for s in spending
        ]
    }