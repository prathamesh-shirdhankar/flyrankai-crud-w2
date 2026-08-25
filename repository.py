import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
    count = cursor.fetchone()["count"]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Buy milk", False),
                ("Walk the dog", False),
                ("Write README", True),
            ],
        )

    conn.commit()
    cursor.close()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_task_by_id(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def create_task(title: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *",
        (title, False),
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return row


def update_task(task_id: int, title: str, done: bool):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *",
        (title, done, task_id),
    )
    row = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return row


def delete_task(task_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    cursor.close()
    conn.close()
    return deleted