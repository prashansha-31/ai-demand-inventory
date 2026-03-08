# 📊 AI Demand Forecasting & Inventory Intelligence System

An **AI-powered demand forecasting and inventory intelligence dashboard** built using **Flask, Python, and Machine Learning**.

This system predicts product demand and provides **advanced analytics including stability analysis, confidence scoring, quality index, risk assessment, and AI recommendations** to support better inventory decisions.

---

# 🚀 Project Overview

Retail businesses face major challenges such as:

- 📦 Overstocking
- ❌ Stockouts
- 📉 Poor demand estimation

This project solves those problems using **AI-driven forecasting and analytics dashboards**.

The system predicts demand and evaluates **forecast reliability**, helping businesses make **data-driven inventory decisions**.

---

# ✨ Key Features

## 🔮 Demand Forecasting
Predicts weekly demand based on:

- Store ID
- Department ID

---

## 📊 Interactive Dashboard

The dashboard includes:

- Forecast trend visualization
- Forecast history tracking
- Performance analytics
- Risk evaluation

---

## 📈 Forecast Trend Visualization

Interactive **Chart.js line graph** showing demand trends over time.

Helps identify:

- Rising demand
- Demand drops
- Seasonal patterns

---

## 📋 Forecast History Tracking

All predictions are stored in **SQLite database**.

Allows:

- Historical analysis
- Model evaluation
- Trend monitoring

---

# 🧠 Advanced Forecast Analytics

## 📉 Model Performance Metrics

The system evaluates prediction accuracy using:

### MAE (Mean Absolute Error)

Measures average error in predictions.

Lower MAE = Better model accuracy

### RMSE (Root Mean Square Error)

Penalizes large prediction errors.

Lower RMSE = More reliable predictions

---

## 📊 Forecast Stability Analysis

Measures **volatility in predicted demand**.

Calculated using **standard deviation**.

Stability levels:

- 🟢 Highly Stable
- 🟡 Moderately Stable
- 🔴 Unstable

Higher volatility indicates unstable demand patterns.

---

## 🎯 Forecast Confidence Analysis

Generates a **confidence score based on model error**.

Confidence levels:

- 🟢 High Confidence
- 🟡 Moderate Confidence
- 🔴 Low Confidence

Low confidence suggests unreliable predictions.

---

## 🏆 Forecast Quality Index

A combined metric evaluating:

- Model accuracy
- Forecast stability
- Confidence score

Range:

```
0 – 100
```

Quality Levels:

- 🟢 Excellent Forecast Quality
- 🟡 Good Forecast Quality
- 🟠 Average Forecast Quality
- 🔴 Poor Forecast Quality

Displayed with a **visual quality meter** in the dashboard.

---

## ⚠️ Forecast Risk Assessment

Evaluates the **operational risk of using forecasts** for inventory planning.

Risk score combines:

- Forecast volatility
- Quality index
- Confidence score

Risk Levels:

- 🟢 Low Risk
- 🟡 Medium Risk
- 🔴 High Risk

Lower risk indicates **more reliable forecasts**.

---

## 🤖 AI Forecast Recommendations

The system generates automatic recommendations such as:

- High volatility detected in forecasts
- Model accuracy needs improvement
- Forecast suitable for short-term planning
- Risk level warning for inventory decisions

This makes the system a **decision-support tool for inventory management**.

---

# 🛠 Technology Stack

## 💻 Backend
- Python
- Flask

## 🎨 Frontend
- HTML
- CSS
- Chart.js

## 🗄 Database
- SQLite

## 📊 Data Processing
- Pandas
- NumPy

---

# 📦 Project Structure

```
AI-DEMAND-INVENTORY/
│
├── 📁 data
│   ├── 📊 sales.csv
│   └── 📊 clean_sales.csv
│
├── 📁 models
│   ├── 🧠 demand_model.pkl
│   ├── 📈 forecast_model.py
│   └── 🔍 eda_analysis.py
│
├── 📁 templates
│   ├── 🖥 index.html
│   ├── 📊 dashboard.html
│   ├── 🔮 forecast.html
│   └── 📦 inventory.html
│
├── 📁 static
│   └── 🎨 styles.css
│
├── 🐍 app.py
├── 🗄 forecast.db
├── 🗄 inventory.db
├── 📦 requirements.txt
├── 📄 README.md
└── 🚫 .gitignore
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/ai-demand-inventory.git
```

---

## 2️⃣ Navigate to Project

```
cd ai-demand-inventory
```

---

## 3️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate environment

### Windows

```
venv\Scripts\activate
```

### Mac/Linux

```
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 5️⃣ Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📊 Dashboard Modules

The dashboard provides:

- 📈 Forecast Trend Chart
- 📋 Forecast History Table
- 📊 KPI Summary Cards
- 📉 Model Performance Metrics
- 📊 Stability Analysis
- 🎯 Confidence Score
- 🏆 Forecast Quality Index
- ⚠️ Risk Assessment
- 🤖 AI Recommendations

---

# 📊 Example Output

### Forecast Quality Index

```
53.53 / 100
```

Quality Level

```
Average Forecast Quality
```

---

### Risk Assessment

Risk Score

```
50.21 / 100
```

Risk Level

```
Medium Risk
```

---

### AI Recommendations

- High volatility detected in forecasts  
- Forecast suitable mainly for short-term planning

---

# 🔮 Future Improvements 

Planned enhancements:

- 📊 Department demand ranking
- 🏬 Store performance comparison
- 📈 Demand volatility ranking
- 🌡 Forecast heatmap visualization
- 🤖 Automated model retraining alerts
- 📉 Advanced ML forecasting models

---

# 🎯 Learning Outcomes

This project demonstrates real-world skills in:

- Machine Learning forecasting
- Business analytics dashboards
- Decision support systems
- Data visualization
- Supply chain analytics

---

# ✅ Conclusion

The **AI Demand Forecasting & Inventory Intelligence System** demonstrates how machine learning and data analytics can be used to improve inventory planning and demand prediction.

This project combines **forecasting models, data visualization, and analytics metrics** to provide a comprehensive decision-support dashboard. By analyzing model performance, forecast stability, confidence levels, quality index, and risk assessment, the system helps users better understand the reliability of predictions.

The dashboard transforms raw predictions into **actionable insights**, enabling smarter inventory decisions and reducing the risks of overstocking or stockouts.

Overall, this project highlights the practical application of:

- 📊 Data analytics
- 🤖 Machine learning forecasting
- 📈 Business intelligence dashboards
- 🧠 Decision-support systems

It serves as a strong example of how **AI-driven insights can enhance supply chain and inventory management systems**.