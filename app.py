from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import pickle
import datetime
import math

app = Flask(__name__)

# ==============================
# LOAD TRAINED MODEL
# ==============================
with open("models/demand_model.pkl", "rb") as f:
    model = pickle.load(f)


# ==============================
# DATABASE CONNECTION
# ==============================
def get_db_connection():
    conn = sqlite3.connect("inventory.db")
    conn.row_factory = sqlite3.Row
    return conn


# ==============================
# DATABASE INITIALIZATION
# ==============================
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SALES TABLE
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

    # FORECAST TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store INTEGER,
            dept INTEGER,
            predicted_sales REAL,
            prediction_date TEXT
        )
    """)

    # INVENTORY POLICY TABLE (CORRECT STRUCTURE)
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


# ==============================
# LOAD CLEAN DATA INTO SALES TABLE (RUN ONCE IF EMPTY)
# ==============================
def load_data_if_empty():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")
    count = cursor.fetchone()[0]

    if count == 0:
        df = pd.read_csv("data/clean_sales.csv")

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


# ==============================
# ROUTES
# ==============================

@app.route("/")
def home():
    return render_template("index.html")


# ==============================
# DASHBOARD ROUTE (NOT REMOVED)
# ==============================
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


# ==============================
# FORECAST + INVENTORY ROUTE
# ==============================
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

        # ==============================
        # INVENTORY CALCULATIONS
        # ==============================

        ordering_cost = 500
        holding_cost = 2
        lead_time = 2  # weeks
        service_level_z = 1.65

        eoq = math.sqrt((2 * prediction * ordering_cost) / holding_cost)
        safety_stock = service_level_z * math.sqrt(lead_time) * (prediction * 0.1)
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
    prediction_history = cursor.fetchall()

    cursor.execute("SELECT * FROM inventory_policy ORDER BY id DESC LIMIT 10")
    inventory_history = cursor.fetchall()

    conn.close()

    return render_template(
        "forecast.html",
        prediction=prediction,
        inventory_result=inventory_result,
        selected_store=selected_store,
        selected_dept=selected_dept,
        prediction_history=prediction_history,
        inventory_history=inventory_history
    )


# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    init_db()
    load_data_if_empty()
    app.run(debug=True)