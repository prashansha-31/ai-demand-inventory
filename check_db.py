import sqlite3
conn = sqlite3.connect('forecast.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tables:", [t[0] for t in tables])

# Create prediction_history if missing
conn.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store INTEGER NOT NULL,
        dept INTEGER NOT NULL,
        date TEXT NOT NULL,
        prediction_date TEXT,
        weekly_sales REAL,
        predicted_sales REAL NOT NULL,
        isholiday INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()

# Check columns
cols = conn.execute("PRAGMA table_info(prediction_history)").fetchall()
print("prediction_history columns:", [c[1] for c in cols])

# Check row count
count = conn.execute("SELECT COUNT(*) FROM prediction_history").fetchone()[0]
print("Rows in prediction_history:", count)
conn.close()
