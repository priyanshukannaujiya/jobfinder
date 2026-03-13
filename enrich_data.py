import sqlite3
import random

def update_db():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    # 1. Update fresher status based on titles
    fresher_keywords = ['intern', 'junior', 'entry', 'trainee', 'trainee', 'grad', 'student']
    for kw in fresher_keywords:
        cursor.execute(f"UPDATE jobs SET is_fresher = 1 WHERE job_title LIKE '%{kw}%'")
    
    # 2. Add some dummy recruiter info
    names = ["Sarah Johnson", "Michael Smith", "Emily Davis", "David Wilson", "Jessica Brown"]
    links = [
        "https://www.linkedin.com/in/sarah-recruiter/",
        "https://www.linkedin.com/in/michael-smith-hr/",
        "https://www.linkedin.com/in/emily-talent-acquisition/",
        "https://www.linkedin.com/in/david-wilson-hire/",
        "https://www.linkedin.com/in/jessica-brown-recruiting/"
    ]
    
    cursor.execute("SELECT id FROM jobs")
    ids = [row[0] for row in cursor.fetchall()]
    
    for i in ids:
        if i % 4 == 0:
            idx = random.randint(0, len(names)-1)
            cursor.execute("UPDATE jobs SET recruiter_name = ?, recruiter_link = ? WHERE id = ?", (names[idx], links[idx], i))
            
    conn.commit()
    conn.close()
    print("Database data enriched for demo!")

if __name__ == "__main__":
    update_db()
