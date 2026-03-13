import sqlite3
try:
    conn = sqlite3.connect('jobs.db', timeout=2)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM jobs")
    print("Jobs count:", c.fetchone()[0])
    conn.close()
except Exception as e:
    print("Error:", e)
