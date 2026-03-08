from flask import Flask, render_template, request
import sqlite3
import numpy as np
from datetime import datetime

app = Flask(__name__)

# -------------------------------
# CREATE DATABASE TABLE
# -------------------------------

def init_db():
    conn = sqlite3.connect("forecast.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prediction_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store INTEGER,
        dept INTEGER,
        predicted_sales REAL,
        prediction_date TEXT
    )
    """)

    conn.commit()
    conn.close()


# run when app starts
init_db()

DATABASE = "forecast.db"


# -------------------------------
# DATABASE CONNECTION
# -------------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------
# SIMPLE PREDICTION FUNCTION
# (Replace with ML model later)
# -------------------------------

def predict_sales(store, dept):
    base = 12000
    prediction = base + (store * 120) + (dept * 80)
    return round(prediction, 2)


# -------------------------------
# FORECAST ROUTE
# -------------------------------

@app.route("/", methods=["GET", "POST"])
def forecast():

    conn = get_db_connection()

    prediction = None
    selected_store = None
    selected_dept = None

    if request.method == "POST":

        store = int(request.form["store"])
        dept = int(request.form["dept"])

        selected_store = store
        selected_dept = dept

        prediction = predict_sales(store, dept)

        conn.execute(
            """
            INSERT INTO prediction_history (store, dept, predicted_sales, prediction_date)
            VALUES (?, ?, ?, ?)
            """,
            (store, dept, prediction, datetime.now())
        )

        conn.commit()

    # -------------------------------
    # LOAD HISTORY
    # -------------------------------

    rows = conn.execute(
        "SELECT * FROM prediction_history ORDER BY id DESC LIMIT 20"
    ).fetchall()

    prediction_history = [dict(row) for row in rows]

    conn.close()

    sales_list = [row["predicted_sales"] for row in prediction_history]

    # -------------------------------
    # KPI CALCULATIONS
    # -------------------------------

    if sales_list:

        latest_forecast = sales_list[0]
        average_forecast = round(np.mean(sales_list), 2)
        total_predictions = len(sales_list)

        # Dummy MAE / RMSE for demonstration
        actuals = [x * 0.9 for x in sales_list]

        errors = [abs(a - p) for a, p in zip(actuals, sales_list)]
        mae = round(np.mean(errors), 2)

        rmse = round(np.sqrt(np.mean([(a - p) ** 2 for a, p in zip(actuals, sales_list)])), 2)

        # -------------------------------
        # STABILITY (VOLATILITY)
        # -------------------------------

        volatility_score = round(np.std(sales_list), 2)

        if volatility_score < 300:
            stability_level = "Highly Stable"
        elif volatility_score < 700:
            stability_level = "Moderately Stable"
        else:
            stability_level = "Unstable"

        # -------------------------------
        # CONFIDENCE SCORE
        # -------------------------------

        confidence_score = round(max(0, 100 - (rmse / 500)), 2)

        if confidence_score > 80:
            confidence_level = "High Confidence"
        elif confidence_score > 50:
            confidence_level = "Moderate Confidence"
        else:
            confidence_level = "Low Confidence"

        # -------------------------------
        # QUALITY INDEX
        # -------------------------------

        quality_index = round(
            (confidence_score + (100 - volatility_score / 10) + (100 - mae / 100)) / 3, 2
        )

        if quality_index > 80:
            quality_status = "Excellent Forecast Quality"
        elif quality_index > 60:
            quality_status = "Good Forecast Quality"
        elif quality_index > 40:
            quality_status = "Average Forecast Quality"
        else:
            quality_status = "Poor Forecast Quality"

        # -------------------------------
        # RISK ASSESSMENT
        # -------------------------------

        normalized_volatility = max(0, 100 - (volatility_score / 10))

        risk_score = (confidence_score + quality_index + normalized_volatility) / 3
        risk_score = max(0, min(100, risk_score))

        if risk_score < 30:
            risk_level = "High Risk"
        elif risk_score < 60:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"

        # -------------------------------
        # AI RECOMMENDATION ENGINE
        # -------------------------------

        recommendations = []

        if mae > 10000 or rmse > 20000:
            recommendations.append(
                "Model accuracy is low. Consider retraining the forecasting model."
            )

        if confidence_score < 50:
            recommendations.append(
                "Forecast confidence is low. Predictions may be unreliable."
            )

        if volatility_score > 700:
            recommendations.append(
                "High volatility detected in forecasts. Demand may fluctuate significantly."
            )

        if risk_level == "High Risk":
            recommendations.append(
                "Forecast risk is high. Use caution when planning inventory."
            )

        if risk_level == "Medium Risk":
            recommendations.append(
                "Forecast risk is moderate. Suitable mainly for short-term planning."
            )

        if quality_index > 70:
            recommendations.append(
                "Forecast quality is strong. Model performing well."
            )

    else:

        latest_forecast = 0
        average_forecast = 0
        total_predictions = 0
        mae = 0
        rmse = 0
        volatility_score = 0
        stability_level = "N/A"
        confidence_score = 0
        confidence_level = "N/A"
        quality_index = 0
        quality_status = "N/A"
        risk_score = 0
        risk_level = "N/A"
        recommendations = []

    # -------------------------------
    # RENDER TEMPLATE
    # -------------------------------

    return render_template(
        "forecast.html",
        prediction=prediction,
        selected_store=selected_store,
        selected_dept=selected_dept,
        prediction_history=prediction_history,
        latest_forecast=latest_forecast,
        average_forecast=average_forecast,
        total_predictions=total_predictions,
        mae=mae,
        rmse=rmse,
        volatility_score=volatility_score,
        stability_level=stability_level,
        confidence_score=confidence_score,
        confidence_level=confidence_level,
        quality_index=quality_index,
        quality_status=quality_status,
        risk_score=round(risk_score, 2),
        risk_level=risk_level,
        recommendations=recommendations
    )


# -------------------------------
# RUN APP
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)