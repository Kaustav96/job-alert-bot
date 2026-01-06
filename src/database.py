import sqlite3

DB = "data/jobs.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY)")
    conn.close()

def is_new(job_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT id FROM jobs WHERE id=?", (job_id,))
    exists = cur.fetchone()

    if not exists:
        cur.execute("INSERT INTO jobs VALUES (?)", (job_id,))
        conn.commit()

    conn.close()
    return not exists