import sqlite3
from datetime import datetime
import os

DB_PATH = "feedback_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            thread_id TEXT,
            user_input TEXT,
            agent_response TEXT,
            feedback_score INTEGER,
            optional_comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_feedback(thread_id, user_input, agent_response, feedback_score, optional_comment=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO feedback (timestamp, thread_id, user_input, agent_response, feedback_score, optional_comment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, thread_id, user_input, agent_response, feedback_score, optional_comment))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM feedback')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
