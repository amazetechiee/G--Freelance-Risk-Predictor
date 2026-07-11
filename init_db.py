import sqlite3, os
def run_init():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/freelance.db")
    conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS contract_audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp_utc TEXT DEFAULT CURRENT_TIMESTAMP,
        developer_experience REAL,
        tech_stack TEXT,
        duration_days INTEGER,
        total_budget_inr REAL,
        calculated_risk_score REAL,
        final_prediction_status TEXT
    )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database verified via external execution configuration.")

if __name__ == '__main__':
    run_init()