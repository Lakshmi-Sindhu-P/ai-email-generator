import sqlite3
from datetime import datetime

DB_PATH = "ai_email_generator.db"  # Place db in project root

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject_context TEXT,
            tone TEXT,
            purpose TEXT,
            bullet_points TEXT,
            length TEXT,
            additional_notes TEXT,
            subjects TEXT,
            draft1 TEXT,
            draft2 TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_email_log(inputs, subjects, drafts):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO email_logs (
            recipient, subject_context, tone, purpose, bullet_points, length,
            additional_notes, subjects, draft1, draft2, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inputs['recipient'],
        inputs['subject_context'],
        inputs['tone'],
        inputs['purpose'],
        "; ".join(inputs['bullet_points']),
        inputs['length'],
        inputs['additional_notes'],
        "; ".join(subjects),
        drafts[0],
        drafts[1],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
