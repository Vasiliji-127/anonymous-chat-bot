import aiosqlite as lite


class DatabaseManager:
    def __init__(self, path):
        self.path = path
        self.conn = None

    async def init_db(self):
        self.conn = await lite.connect(self.path)
        await self.conn.execute('pragma foreign_keys = on')
        await self.conn.execute(
            "CREATE TABLE IF NOT EXISTS 'users' ('tg_id' INTEGER, 'interests' TEXT NOT NULL, PRIMARY KEY('tg_id'))")
        await self.conn.commit()

    async def query(self, arg, values=None):
        if values is None:
            await self.conn.execute(arg)
        else:
            await self.conn.execute(arg, values)
        await self.conn.commit()

    async def fetchone(self, arg, values=None):
        if values is None:
            cur = await self.conn.execute(arg)
        else:
            cur = await self.conn.execute(arg, values)
        return await cur.fetchone()

    async def fetchall(self, arg, values=None):
        if values is None:
            cur = await self.conn.execute(arg)
        else:
            cur = await self.conn.execute(arg, values)
        return await cur.fetchall()

    async def close_db(self):
        await self.conn.close()
