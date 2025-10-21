import sqlite3

class Database:
    def __init__(self, path="gifts.db"):
        self.path = path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS gifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                person TEXT,
                occasion TEXT,
                priority INTEGER,
                purchased INTEGER DEFAULT 0
            )
            """)
            con.commit()

    def fetch_all(self):
        with sqlite3.connect(self.path) as con:
            return con.execute("SELECT * FROM gifts").fetchall()

    def add(self, title, person, occasion, priority, purchased):
        with sqlite3.connect(self.path) as con:
            con.execute(
                "INSERT INTO gifts (title, person, occasion, priority, purchased) VALUES (?, ?, ?, ?, ?)",
                (title, person, occasion, priority, purchased)
            )
            con.commit()

    def update(self, gift_id, title, person, occasion, priority, purchased):
        with sqlite3.connect(self.path) as con:
            con.execute("""
                UPDATE gifts SET title=?, person=?, occasion=?, priority=?, purchased=?
                WHERE id=?
            """, (title, person, occasion, priority, purchased, gift_id))
            con.commit()

    def delete(self, gift_id):
        with sqlite3.connect(self.path) as con:
            con.execute("DELETE FROM gifts WHERE id=?", (gift_id,))
            con.commit()
