from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import pickle
import datetime
import json
import math

app = Flask(__name__)

# =========================
# LOAD ML MODEL
# =========================
with open("models/demand_model.pkl", "rb") as f:
    model = pickle.load(f)


# =========================
# DATABASE CONNECTION
# =========================
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# DATABASE INITIALIZATION
# =========================
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sales table
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

    # Forecast table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            predicted_sales REAL,
            prediction_date TEXT
        )
    """)

    # Inventory policy table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_policy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            predicted_sales REAL,
            eoq REAL,
            safety_stock REAL,
            reorder_point REAL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# DASHBOARD
# =========================
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

    cursor.execute("SELECT SUM(weekly_sales), AVG(weekly_sales) FROM sales")
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
        total_depts=total_depts
    )


# =========================
# FORECAST + INVENTORY
# =========================
@app.route("/forecast", methods=["GET", "POST"])
def forecast():

    prediction = None
    inventory_result = None
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
        prediction = float(model.predict(features)[0])

        # Save forecast
        cursor.execute("""
            INSERT INTO forecasts (store, dept, predicted_sales, prediction_date)
            VALUES (?, ?, ?, ?)
        """, (store, dept, prediction, today.strftime("%Y-%m-%d %H:%M:%S")))

        # =====================
        # INVENTORY CALCULATION
        # =====================
        ordering_cost = 50
        holding_cost = 2
        lead_time = 2
        z = 1.65
        demand_variability = 0.1 * prediction

        eoq = math.sqrt((2 * prediction * ordering_cost) / holding_cost)
        safety_stock = z * math.sqrt(lead_time) * demand_variability
        reorder_point = (prediction * lead_time) + safety_stock

        inventory_result = {
            "eoq": round(eoq, 2),
            "safety_stock": round(safety_stock, 2),
            "reorder_point": round(reorder_point, 2)
        }

        # Save inventory policy
        cursor.execute("""
            INSERT INTO inventory_policy
            (store, dept, predicted_sales, eoq, safety_stock, reorder_point, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            store,
            dept,
            prediction,
            inventory_result["eoq"],
            inventory_result["safety_stock"],
            inventory_result["reorder_point"],
            today.strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

    # Fetch history
    cursor.execute("SELECT * FROM forecasts ORDER BY id DESC LIMIT 10")
    prediction_rows = cursor.fetchall()

    prediction_history = [dict(row) for row in prediction_rows]

    cursor.execute("SELECT * FROM inventory_policy ORDER BY id DESC LIMIT 10")
    inventory_rows = cursor.fetchall()

    inventory_history = [dict(row) for row in inventory_rows]

    # Prepare JSON chart data
    forecast_chart_data = json.dumps([
        {"date": row["prediction_date"], "sales": row["predicted_sales"]}
        for row in prediction_history
    ])

    inventory_chart_data = json.dumps([
        {"date": row["created_at"], "reorder": row["reorder_point"]}
        for row in inventory_history
    ])

    conn.close()

    return render_template(
        "forecast.html",
        prediction=prediction,
        selected_store=selected_store,
        selected_dept=selected_dept,
        inventory_result=inventory_result,
        prediction_history=prediction_history,
        inventory_history=inventory_history,
        forecast_chart_data=forecast_chart_data,
        inventory_chart_data=inventory_chart_data
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)