import sqlite3
from typing import List

DB_PATH = "sentinel.db"

def init_db():
    """Initialize the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS processed_papers (
            id TEXT PRIMARY KEY,
            processed_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_processed_ids() -> set:
    """Return a set of all paper IDs we have already seen."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM processed_papers')
    # usage of set for O(1) lookups
    ids = {row[0] for row in c.fetchall()}
    conn.close()
    return ids

def mark_as_processed(paper_ids: List[str]):
    """Save a batch of IDs to the database so we don't fetch them again."""
    if not paper_ids:
        return
        
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # data format: [(id, date), (id, date)...]
    data = [(pid, date_str) for pid in paper_ids]
    
    # INSERT OR IGNORE avoids crashing if we accidentally try to save a duplicate
    c.executemany('INSERT OR IGNORE INTO processed_papers (id, processed_date) VALUES (?, ?)', data)
    
    conn.commit()
    conn.close()
    print(f"🧠 Memory: Memorized {len(paper_ids)} paper IDs.")