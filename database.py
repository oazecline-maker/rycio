import aiosqlite


async def init_db():
    async with aiosqlite.connect("items.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price TEXT,
            photo TEXT
        )
        """)
        await db.commit()


async def add_item(name, description, price, photo):
    async with aiosqlite.connect("items.db") as db:
        await db.execute(
            "INSERT INTO items (name, description, price, photo) VALUES (?, ?, ?, ?)",
            (name, description, price, photo)
        )
        await db.commit()


async def get_items():
    async with aiosqlite.connect("items.db") as db:
        cursor = await db.execute("SELECT * FROM items")
        return await cursor.fetchall()


async def get_item(item_id):
    async with aiosqlite.connect("items.db") as db:
        cursor = await db.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return await cursor.fetchone()


async def delete_item(item_id):
    async with aiosqlite.connect("items.db") as db:
        await db.execute("DELETE FROM items WHERE id = ?", (item_id,))
        await db.commit()
