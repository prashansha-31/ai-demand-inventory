from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import pickle
import datetime

app = Flask(__name__)

# Load Trained ML Model
with open("models/demand_model.pkl", "rb") as f:
    model = pickle.load(f)


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn


# DATABASE INITIALIZATION
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sales Table
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

    # Forecasts Table (Single Clean Version)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            predicted_sales REAL,
            prediction_date TEXT
        )
    """)

    # Inventory Policy Table
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


# ROUTES

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    store = request.args.get("store")
    dept = request.args.get("dept")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT store, dept, date, weekly_sales FROM sales"
    conditions = []
    params = []

    if store:
        conditions.append("store = ?")
        params.append(store)

    if dept:
        conditions.append("dept = ?")
        params.append(dept)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " LIMIT 20"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Analytics
    analytics_query = "SELECT SUM(weekly_sales), AVG(weekly_sales) FROM sales"
    if conditions:
        analytics_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(analytics_query, params)
    result = cursor.fetchone()

    total_sales = result[0] if result[0] else 0
    avg_sales = result[1] if result[1] else 0

    cursor.execute("SELECT COUNT(DISTINCT store) FROM sales")
    total_stores = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT dept) FROM sales")
    total_depts = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        data=rows,
        total_sales=total_sales,
        avg_sales=avg_sales,
        total_stores=total_stores,
        total_depts=total_depts,
        selected_store=store,
        selected_dept=dept
    )


@app.route("/forecast", methods=["GET", "POST"])
def forecast():

    prediction = None
    selected_store = None
    selected_dept = None

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        selected_store = request.form["store"]
        selected_dept = request.form["dept"]

        store = int(selected_store)
        dept = int(selected_dept)

        today = datetime.datetime.now()
        year = today.year
        month = today.month
        week = today.isocalendar()[1]

        features = [[store, dept, year, month, week]]

        prediction = model.predict(features)[0]

        # Save prediction into database
        cursor.execute("""
            INSERT INTO forecasts (store, dept, predicted_sales, prediction_date)
            VALUES (?, ?, ?, ?)
        """, (store, dept, float(prediction),
              today.strftime("%Y-%m-%d %H:%M:%S")))

        conn.commit()

    # Fetch last 10 predictions
    cursor.execute("""
        SELECT * FROM forecasts
        ORDER BY id DESC
        LIMIT 10
    """)
    prediction_history = cursor.fetchall()

    conn.close()

    return render_template(
        "forecast.html",
        prediction=prediction,
        selected_store=selected_store,
        selected_dept=selected_dept,
        prediction_history=prediction_history
    )


@app.route("/check-data")
def check_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]
    conn.close()
    return f"Total rows in sales table: {count}"


# MAIN
if __name__ == "__main__":
    init_db()
    app.run(debug=True)