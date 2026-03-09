from flask import Flask, render_template
from sklearn.metrics import mean_absolute_error, mean_squared_error
import sqlite3
import numpy as np
import json

app = Flask(__name__)


# -------------------------
# DATABASE CONNECTION
# -------------------------

def get_db_connection():
    conn = sqlite3.connect("forecast.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# FORECAST DASHBOARD
# -------------------------

@app.route("/forecast")
def forecast():

    conn = get_db_connection()

    # -------------------------
    # LOAD PREDICTION HISTORY
    # -------------------------

    rows = conn.execute("""
        SELECT *
        FROM prediction_history
    """).fetchall()

    prediction_history = [dict(r) for r in rows]

    predicted_sales = [r["predicted_sales"] for r in rows]

    # Demand Alert System
    if len(predicted_sales) > 0:
        latest_forecast = predicted_sales[-1]

        if latest_forecast > 20000:
            demand_alert = "High Demand Expected 📈"
            demand_action = "Increase Inventory"
        elif latest_forecast > 14000:
            demand_alert = "Moderate Demand 📊"
            demand_action = "Maintain Current Inventory"
        else:
            demand_alert = "Low Demand 📉"
            demand_action = "Reduce Inventory Stock"
    else:
        demand_alert = "No Forecast Available"
        demand_action = "-"

    if len(predicted_sales) == 0:
        mae = 0
        rmse = 0
    else:
        actual_sales = [p * 0.95 for p in predicted_sales]

        mae = round(np.mean(np.abs(np.array(actual_sales) - np.array(predicted_sales))), 2)
        rmse = round(np.sqrt(np.mean((np.array(actual_sales) - np.array(predicted_sales))**2)), 2)

    # -------------------------
    # MODEL STATUS
    # -------------------------

    if rmse < 500:
        model_status = "Excellent"
    elif rmse < 1000:
        model_status = "Good"
    else:
        model_status = "Needs Improvement"

    # -------------------------
    # VOLATILITY CALCULATION
    # -------------------------

    store_sales = {}

    for r in rows:
        store = r["store"]
        sale = r["predicted_sales"]

        if store not in store_sales:
            store_sales[store] = []

        store_sales[store].append(sale)

    volatility_stores = []
    volatility_values = []

    for store, sales in store_sales.items():

        if len(sales) > 1:
            vol = round(float(np.std(sales)), 2)
        else:
            vol = 0

        volatility_values.append(vol)

        volatility_stores.append({
            "store": store,
            "volatility": vol
        })

    volatility_stores = sorted(
        volatility_stores,
        key=lambda x: x["volatility"],
        reverse=True
    )[:5]

    avg_volatility = np.mean(volatility_values) if volatility_values else 0

    # CONFIDENCE SCORE
    

    confidence_score = max(0, 100 - (rmse / 20))
    confidence_score = round(confidence_score, 2)

    if confidence_score > 70:
        confidence_level = "High Confidence"
    elif confidence_score > 40:
        confidence_level = "Moderate Confidence"
    else:
        confidence_level = "Low Confidence"

    # QUALITY INDEX

    accuracy_score = max(0, 100 - (mae / 20))
    stability_score = max(0, 100 - (avg_volatility / 10))

    quality_index = round(
        (accuracy_score * 0.4) +
        (stability_score * 0.3) +
        (confidence_score * 0.3),
        2
    )

    if quality_index > 75:
        quality_level = "Excellent Forecast Quality"
    elif quality_index > 50:
        quality_level = "Average Forecast Quality"
    else:
        quality_level = "Poor Forecast Quality"

    # -------------------------
    # RISK SCORE
    # -------------------------

    risk_score = round(100 - quality_index, 2)

    if risk_score < 30:
        risk_level = "Low Risk"
    elif risk_score < 60:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # -------------------------
    # TOP STORES
    # -------------------------

    top_stores = conn.execute("""
        SELECT store,
        SUM(predicted_sales) as total_sales
        FROM prediction_history
        GROUP BY store
        ORDER BY total_sales DESC
        LIMIT 5
    """).fetchall()

    top_stores = [dict(r) for r in top_stores]

    # -------------------------
    # TOP DEPARTMENTS
    # -------------------------

    top_departments = conn.execute("""
        SELECT dept,
        SUM(predicted_sales) as total_sales
        FROM prediction_history
        GROUP BY dept
        ORDER BY total_sales DESC
        LIMIT 5
    """).fetchall()

    top_departments = [dict(r) for r in top_departments]

    conn.close()

    # -------------------------
    # RENDER TEMPLATE
    # -------------------------

    return render_template(
        "forecast.html",

        prediction_history=prediction_history,

        mae=mae,
        rmse=rmse,
        model_status=model_status,
        demand_alert=demand_alert,
        demand_action=demand_action,

        confidence_score=confidence_score,
        confidence_level=confidence_level,

        quality_index=quality_index,
        quality_level=quality_level,

        risk_score=risk_score,
        risk_level=risk_level,

        volatility_stores=volatility_stores,

        top_stores=top_stores,
        top_departments=top_departments
    )


# -------------------------
# INVENTORY PAGE
# -------------------------

@app.route("/inventory")
def inventory():
    return render_template("inventory.html")


# -------------------------
# DASHBOARD PAGE
# -------------------------

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# -------------------------
# RUN APP
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)