from flask import Flask, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            date TEXT,
            weekly_sales REAL,
            is_holiday INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            forecast_date TEXT,
            predicted_sales REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_policy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            safety_stock REAL,
            reorder_point REAL,
            eoq REAL
        )
    """)

    conn.commit()
    conn.close()

# -----------------------------
# LOAD DATA INTO DATABASE
# -----------------------------
def load_data():
    df = pd.read_csv("data/clean_sales.csv")

    conn = get_db_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO sales (store, dept, date, weekly_sales, is_holiday)
            VALUES (?, ?, ?, ?, ?)
        """, (
            int(row["store"]),
            int(row["dept"]),
            str(row["date"]),
            float(row["weekly_sales"]),
            int(row["isholiday"])
        ))

    conn.commit()
    conn.close()

# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/test-db")
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return str(tables)

@app.route("/check-data")
def check_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()
    conn.close()
    return f"Total rows in sales table: {count[0]}"

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)