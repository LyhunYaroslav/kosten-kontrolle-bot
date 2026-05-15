import aiosqlite
from datetime import datetime

DB_NAME = "expenses.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def add_expense(user_id: int, amount: float, description: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO expenses (user_id, amount, description, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, amount, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()


async def get_expenses(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id, amount, description, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )
        rows = await cursor.fetchall()
        return rows


async def delete_expense(user_id: int, expense_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            DELETE FROM expenses
            WHERE user_id = ? AND id = ?
            """,
            (user_id, expense_id)
        )
        await db.commit()