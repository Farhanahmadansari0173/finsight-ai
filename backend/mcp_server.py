from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import pymongo
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Server("finsight-mongodb-mcp")
client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = client["finsight"]

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_transactions",
            description="Get all financial transactions from MongoDB",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_spending_by_category",
            description="Get total spending grouped by category",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_budget_status",
            description="Get budget limits and current spending status",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="add_transaction",
            description="Add a new transaction to MongoDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "amount": {"type": "number"},
                    "category": {"type": "string"}
                },
                "required": ["description", "amount", "category"]
            }
        ),
        Tool(
            name="detect_anomalies",
            description="Detect spending anomalies and budget overruns",
            inputSchema={"type": "object", "properties": {}, "required": []}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_transactions":
        transactions = list(db.transactions.find().sort("date", -1).limit(50))
        for t in transactions:
            t["_id"] = str(t["_id"])
            if isinstance(t.get("date"), datetime):
                t["date"] = t["date"].strftime("%Y-%m-%d")
        return [TextContent(type="text", text=json.dumps(transactions, indent=2))]

    elif name == "get_spending_by_category":
        pipeline = [
            {"$match": {"amount": {"$lt": 0}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}},
            {"$sort": {"total": 1}}
        ]
        result = list(db.transactions.aggregate(pipeline))
        spending = [{"category": r["_id"], "total_spent": abs(r["total"]), "transactions": r["count"]} for r in result]
        return [TextContent(type="text", text=json.dumps(spending, indent=2))]

    elif name == "get_budget_status":
        budgets = list(db.budgets.find())
        pipeline = [
            {"$match": {"amount": {"$lt": 0}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
        ]
        spending = {r["_id"]: abs(r["total"]) for r in db.transactions.aggregate(pipeline)}
        status = []
        for b in budgets:
            spent = spending.get(b["category"], 0)
            status.append({
                "category": b["category"],
                "budget": b["limit"],
                "spent": spent,
                "remaining": b["limit"] - spent,
                "status": "OVERSPENT" if spent > b["limit"] else "ON TRACK"
            })
        return [TextContent(type="text", text=json.dumps(status, indent=2))]

    elif name == "add_transaction":
        transaction = {
            "description": arguments["description"],
            "amount": arguments["amount"],
            "category": arguments["category"],
            "date": datetime.now()
        }
        result = db.transactions.insert_one(transaction)
        return [TextContent(type="text", text=json.dumps({"success": True, "id": str(result.inserted_id)}))]

    elif name == "detect_anomalies":
        pipeline = [
            {"$match": {"amount": {"$lt": 0}}},
            {"$group": {"_id": "$category", "total": {"$sum": "$amount"}, "count": {"$sum": 1}}}
        ]
        spending = list(db.transactions.aggregate(pipeline))
        budgets = {b["category"]: b["limit"] for b in db.budgets.find()}
        anomalies = []
        for s in spending:
            cat = s["_id"]
            spent = abs(s["total"])
            if cat in budgets and spent > budgets[cat]:
                anomalies.append({
                    "category": cat,
                    "spent": spent,
                    "budget": budgets[cat],
                    "overspent_by": spent - budgets[cat]
                })
        return [TextContent(type="text", text=json.dumps(anomalies, indent=2))]

    return [TextContent(type="text", text="Tool not found")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())