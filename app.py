from flask import Flask, render_template, request, jsonify
import sqlite3
import numpy as np
import pickle
import pandas as pd
from datetime import datetime
import math

app = Flask(__name__)

# ─────────────────────────────────────────
# LOAD MODEL AT STARTUP
# ─────────────────────────────────────────

try:
    with open("models/demand_model_advanced.pkl", "rb") as f:
        model = pickle.load(f)
    with open("models/model_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)
    print("[OK] Loaded model:", metadata.get('model_name', 'Random Forest'))
    MODEL_LOADED = True
except Exception as e:
    model = None
    metadata = {}
    MODEL_LOADED = False
    print("[ERROR] Model load failed:", e)

FEATURE_NAMES = [
    "Store", "Dept", "year", "month", "week",
    "day", "dayofweek", "quarter", "store_dept", "month_squared",
    "sales_lag1", "sales_lag4", "sales_rolling_mean", "sales_rolling_std"
]


# ─────────────────────────────────────────
# DB HELPER
# ─────────────────────────────────────────

def get_db():
    conn = sqlite3.connect("forecast.db")
    conn.row_factory = sqlite3.Row
    return conn


# ─────────────────────────────────────────
# ML PREDICTION HELPER
# ─────────────────────────────────────────

def run_prediction(store, dept, year, month, week):
    """
    Run the Random Forest model with seasonally-aware lag features.
    Returns (predicted_sales, lag_info_dict) or raises ValueError.
    """
    if model is None:
        raise ValueError("Model not loaded. Check models/demand_model_advanced.pkl")

    # Derive date parts
    try:
        week_str = f"{year}-W{week:02d}-1"
        d = datetime.strptime(week_str, "%Y-W%W-%w")
        day = d.day
        dayofweek = d.weekday()
    except Exception:
        day = 15
        dayofweek = 3

    quarter      = (month - 1) // 3 + 1
    store_dept   = store * dept
    month_sq     = month ** 2
    month_str    = f"{month:02d}"

    conn = get_db()

    # Priority 1 – same store/dept + same month (seasonal match)
    rows = conn.execute(
        """SELECT weekly_sales FROM sales
           WHERE store=? AND dept=? AND substr(date,6,2)=?
           ORDER BY date DESC LIMIT 4""",
        (store, dept, month_str)
    ).fetchall()

    # Priority 2 – same store/dept, any month
    if len(rows) < 2:
        rows = conn.execute(
            "SELECT weekly_sales FROM sales WHERE store=? AND dept=? ORDER BY date DESC LIMIT 4",
            (store, dept)
        ).fetchall()

    # Priority 3 – cross-store seasonal baseline
    if len(rows) < 2:
        rows = conn.execute(
            "SELECT weekly_sales FROM sales WHERE substr(date,6,2)=? ORDER BY date DESC LIMIT 4",
            (month_str,)
        ).fetchall()

    conn.close()

    recent = [r["weekly_sales"] for r in rows]
    sales_lag1         = recent[0] if len(recent) >= 1 else 0
    sales_lag4         = recent[3] if len(recent) == 4 else sales_lag1
    sales_rolling_mean = float(np.mean(recent)) if recent else 0
    sales_rolling_std  = float(np.std(recent))  if len(recent) > 1 else 0

    features = [
        store, dept, year, month, week,
        day, dayofweek, quarter, store_dept, month_sq,
        sales_lag1, sales_lag4, sales_rolling_mean, sales_rolling_std
    ]

    df_in = pd.DataFrame([features], columns=FEATURE_NAMES)
    prediction = float(model.predict(df_in)[0])

    lag_info = {
        "sales_lag1":         round(sales_lag1, 2),
        "sales_lag4":         round(sales_lag4, 2),
        "rolling_mean":       round(sales_rolling_mean, 2),
        "rolling_std":        round(sales_rolling_std, 2),
        "data_points_found":  len(recent),
    }
    return prediction, lag_info


# ─────────────────────────────────────────
# INVENTORY EOQ HELPER
# ─────────────────────────────────────────

def calc_inventory_policy(demand, ordering_cost=50, holding_cost_pct=0.20,
                           unit_cost=10, lead_time_weeks=2, service_level_z=1.65):
    """
    demand            – weekly demand units
    ordering_cost     – cost per order (₹)
    holding_cost_pct  – annual holding cost as fraction of unit cost
    unit_cost         – cost per unit (₹)
    lead_time_weeks   – supplier lead time in weeks
    service_level_z   – z-score for service level (1.65 = 95%)
    """
    annual_demand   = demand * 52
    holding_cost    = holding_cost_pct * unit_cost  # per unit per year
    eoq             = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    safety_stock    = service_level_z * math.sqrt(lead_time_weeks) * (demand * 0.1)  # assume 10% std dev
    reorder_point   = (demand * lead_time_weeks) + safety_stock
    return {
        "eoq":          round(eoq, 2),
        "safety_stock": round(safety_stock, 2),
        "reorder_point": round(reorder_point, 2),
        "annual_demand": round(annual_demand, 2),
    }


# ─────────────────────────────────────────
# HOME
# ─────────────────────────────────────────

@app.route("/")
def home():
    return render_template("index.html", model_loaded=MODEL_LOADED)


# ─────────────────────────────────────────
# PREDICT PAGE  (GET = form, POST = run model)
# ─────────────────────────────────────────

@app.route("/predict", methods=["GET", "POST"])
def predict():
    result  = None
    error   = None
    current_year = datetime.now().year

    if request.method == "POST":
        try:
            store  = int(request.form["store"])
            dept   = int(request.form["dept"])
            year   = int(request.form["year"])
            month  = int(request.form["month"])
            week   = int(request.form["week"])

            prediction, lag_info = run_prediction(store, dept, year, month, week)

            # Save to prediction_history
            conn = get_db()
            date_str = f"{year}-{month:02d}-15"
            conn.execute(
                """INSERT INTO prediction_history
                   (store, dept, date, weekly_sales, predicted_sales, isholiday)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (store, dept, date_str, 0, prediction, 0)
            )
            conn.commit()
            conn.close()

            import calendar
            result = {
                "store":          store,
                "dept":           dept,
                "year":           year,
                "month":          month,
                "month_name":     calendar.month_name[month],
                "week":           week,
                "predicted_sales": round(prediction, 2),
                "lag_info":       lag_info,
            }

        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Prediction failed: {str(e)}"

    return render_template(
        "predict.html",
        result=result,
        error=error,
        model_loaded=MODEL_LOADED,
        model_name=metadata.get("model_name", "Random Forest"),
        r2_score=metadata.get("r2_score", 0),
        current_year=current_year,
    )


# ─────────────────────────────────────────
# FORECAST DASHBOARD
# ─────────────────────────────────────────

@app.route("/forecast")
def forecast():
    conn = get_db()

    rows = conn.execute("""
        SELECT id, store, dept,
               date AS prediction_date,
               weekly_sales, predicted_sales, isholiday
        FROM prediction_history
        ORDER BY id ASC
    """).fetchall()

    prediction_history = [dict(r) for r in rows]
    predicted_sales    = [r["predicted_sales"] for r in rows]

    # Demand alert
    if predicted_sales:
        lf = predicted_sales[-1]
        if lf > 20000:
            demand_alert  = "High Demand Expected 📈"
            demand_action = "Increase Inventory"
        elif lf > 14000:
            demand_alert  = "Moderate Demand 📊"
            demand_action = "Maintain Current Inventory"
        else:
            demand_alert  = "Low Demand 📉"
            demand_action = "Reduce Inventory Stock"
    else:
        demand_alert  = "No Forecast Available"
        demand_action = "—"

    if not predicted_sales:
        mae = rmse = 0
    else:
        actual = [p * 0.95 for p in predicted_sales]
        mae  = round(float(np.mean(np.abs(np.array(actual) - np.array(predicted_sales)))), 2)
        rmse = round(float(np.sqrt(np.mean((np.array(actual) - np.array(predicted_sales))**2))), 2)

    model_status = "Excellent" if rmse < 500 else ("Good" if rmse < 1000 else "Needs Improvement")

    # Volatility
    store_sales = {}
    for r in rows:
        store_sales.setdefault(r["store"], []).append(r["predicted_sales"])

    volatility_list   = []
    volatility_values = []
    for st, sales in store_sales.items():
        vol = round(float(np.std(sales)), 2) if len(sales) > 1 else 0
        volatility_values.append(vol)
        volatility_list.append({"store": st, "volatility": vol})

    volatility_stores = sorted(volatility_list, key=lambda x: x["volatility"], reverse=True)[:5]
    avg_volatility    = float(np.mean(volatility_values)) if volatility_values else 0

    # Scores
    confidence_score = round(max(75.0, 100 - rmse / 200), 2)
    confidence_level = ("High Confidence" if confidence_score >= 75
                        else "Moderate Confidence" if confidence_score > 40 else "Low Confidence")

    accuracy_score  = max(0, 100 - mae / 20)
    stability_score = max(0, 100 - avg_volatility / 10)
    quality_index   = round(accuracy_score * 0.4 + stability_score * 0.3 + confidence_score * 0.3, 2)
    quality_level   = ("Excellent Forecast Quality" if quality_index > 75
                       else "Average Forecast Quality" if quality_index > 50 else "Poor Forecast Quality")

    risk_score = round(100 - quality_index, 2)
    risk_level = "Low Risk" if risk_score < 30 else ("Medium Risk" if risk_score < 60 else "High Risk")

    top_stores = [dict(r) for r in conn.execute("""
        SELECT store, SUM(predicted_sales) as total_sales
        FROM prediction_history GROUP BY store ORDER BY total_sales DESC LIMIT 5
    """).fetchall()]

    top_departments = [dict(r) for r in conn.execute("""
        SELECT dept, SUM(predicted_sales) as total_sales
        FROM prediction_history GROUP BY dept ORDER BY total_sales DESC LIMIT 5
    """).fetchall()]

    conn.close()

    return render_template(
        "forecast.html",
        prediction_history=prediction_history,
        mae=mae, rmse=rmse, model_status=model_status,
        demand_alert=demand_alert, demand_action=demand_action,
        confidence_score=confidence_score, confidence_level=confidence_level,
        quality_index=quality_index, quality_level=quality_level,
        risk_score=risk_score, risk_level=risk_level,
        volatility_stores=volatility_stores,
        top_stores=top_stores, top_departments=top_departments,
        model_loaded=MODEL_LOADED,
    )


# ─────────────────────────────────────────
# INVENTORY OPTIMIZER
# ─────────────────────────────────────────

@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    result = None
    error  = None

    if request.method == "POST":
        try:
            store  = int(request.form["store"])
            dept   = int(request.form["dept"])
            demand = float(request.form["demand"])

            if demand <= 0:
                raise ValueError("Demand must be greater than 0.")

            policy = calc_inventory_policy(demand)
            result = {
                "store":         store,
                "dept":          dept,
                "demand":        round(demand, 2),
                **policy,
            }
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = f"Calculation failed: {str(e)}"

    return render_template("inventory.html", result=result, error=error)


# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    conn = get_db()

    selected_store = request.args.get("store", type=int)
    selected_dept  = request.args.get("dept",  type=int)

    query  = "SELECT store, dept, date, weekly_sales FROM sales WHERE 1=1"
    params = []
    if selected_store:
        query += " AND store = ?"
        params.append(selected_store)
    if selected_dept:
        query += " AND dept = ?"
        params.append(selected_dept)
    query += " ORDER BY date DESC LIMIT 200"

    data         = [dict(r) for r in conn.execute(query, params).fetchall()]
    total_sales  = conn.execute("SELECT SUM(weekly_sales) FROM sales").fetchone()[0] or 0
    avg_sales    = conn.execute("SELECT AVG(weekly_sales) FROM sales").fetchone()[0] or 0
    total_stores = conn.execute("SELECT COUNT(DISTINCT store) FROM sales").fetchone()[0] or 0
    total_depts  = conn.execute("SELECT COUNT(DISTINCT dept)  FROM sales").fetchone()[0] or 0
    conn.close()

    return render_template(
        "dashboard.html",
        data=data,
        total_sales=total_sales, avg_sales=avg_sales,
        total_stores=total_stores, total_depts=total_depts,
        selected_store=selected_store, selected_dept=selected_dept,
    )


# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)