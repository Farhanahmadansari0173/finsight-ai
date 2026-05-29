import asyncio
from database import connect_db, get_db
from datetime import datetime, timedelta
import random

transactions = [
    {"description": "Swiggy Food Order", "amount": -450, "category": "Food", "date": datetime.now() - timedelta(days=1)},
    {"description": "Zomato Food Order", "amount": -320, "category": "Food", "date": datetime.now() - timedelta(days=2)},
    {"description": "Salary Credit", "amount": 85000, "category": "Income", "date": datetime.now() - timedelta(days=3)},
    {"description": "Amazon Purchase", "amount": -2300, "category": "Shopping", "date": datetime.now() - timedelta(days=4)},
    {"description": "Netflix Subscription", "amount": -649, "category": "Subscriptions", "date": datetime.now() - timedelta(days=5)},
    {"description": "Uber Ride", "amount": -180, "category": "Transport", "date": datetime.now() - timedelta(days=6)},
    {"description": "Electricity Bill", "amount": -1200, "category": "Utilities", "date": datetime.now() - timedelta(days=7)},
    {"description": "Spotify Subscription", "amount": -119, "category": "Subscriptions", "date": datetime.now() - timedelta(days=8)},
    {"description": "Swiggy Food Order", "amount": -550, "category": "Food", "date": datetime.now() - timedelta(days=9)},
    {"description": "Amazon Prime", "amount": -299, "category": "Subscriptions", "date": datetime.now() - timedelta(days=10)},
    {"description": "Petrol", "amount": -3000, "category": "Transport", "date": datetime.now() - timedelta(days=11)},
    {"description": "Gym Membership", "amount": -999, "category": "Health", "date": datetime.now() - timedelta(days=12)},
    {"description": "Freelance Payment", "amount": 15000, "category": "Income", "date": datetime.now() - timedelta(days=13)},
    {"description": "Zomato Food Order", "amount": -780, "category": "Food", "date": datetime.now() - timedelta(days=14)},
    {"description": "Mobile Recharge", "amount": -239, "category": "Utilities", "date": datetime.now() - timedelta(days=15)},
    {"description": "Swiggy Food Order", "amount": -890, "category": "Food", "date": datetime.now() - timedelta(days=16)},
    {"description": "YouTube Premium", "amount": -189, "category": "Subscriptions", "date": datetime.now() - timedelta(days=17)},
    {"description": "Uber Ride", "amount": -250, "category": "Transport", "date": datetime.now() - timedelta(days=18)},
    {"description": "Grocery Store", "amount": -3400, "category": "Groceries", "date": datetime.now() - timedelta(days=19)},
    {"description": "Swiggy Food Order", "amount": -1200, "category": "Food", "date": datetime.now() - timedelta(days=20)},
]

async def seed():
    await connect_db()
    db = get_db()
    
    # Clear existing data
    await db.transactions.delete_many({})
    await db.budgets.delete_many({})
    
    # Insert transactions
    await db.transactions.insert_many(transactions)
    print(f"✅ Inserted {len(transactions)} transactions")
    
    # Insert budgets
    budgets = [
        {"category": "Food", "limit": 3000, "month": "2026-05"},
        {"category": "Shopping", "limit": 5000, "month": "2026-05"},
        {"category": "Transport", "limit": 2000, "month": "2026-05"},
        {"category": "Subscriptions", "limit": 1000, "month": "2026-05"},
        {"category": "Utilities", "limit": 2000, "month": "2026-05"},
    ]
    await db.budgets.insert_many(budgets)
    print(f"✅ Inserted {len(budgets)} budgets")
    print("🎉 Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())