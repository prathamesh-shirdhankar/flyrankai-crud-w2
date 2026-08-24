import sqlite3

DB_FILE = "tasks.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Buy milk", False),
                ("Walk the dog", False),
                ("Write README", True),
            ],
        )

    conn.commit()
    conn.close()