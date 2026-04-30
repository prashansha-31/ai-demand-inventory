# ⚡ NeuralStock: AI Demand & Inventory Intelligence

A stunning, AI-powered demand forecasting and inventory intelligence dashboard built using **Flask, Python, Machine Learning (Random Forest)**, and a **modern Glassmorphism UI**.

NeuralStock predicts product demand with high accuracy and provides advanced analytics including stability analysis, confidence scoring, quality indexing, risk assessment, and automated inventory policy generation (EOQ & Safety Stock).

---

## 🚀 The Solution

Retail businesses often face the expensive challenges of **overstocking**, **stockouts**, and **poor demand estimation**. NeuralStock solves these problems by providing:
1. **Machine Learning Forecasting:** A Random Forest model trained on 421,500+ historical records, utilizing seasonally-aware lag features.
2. **Actionable Inventory Math:** Translating pure demand predictions into real-world purchasing policies (Economic Order Quantity & Reorder Points).
3. **Beautiful Analytics:** A highly visual, neon-themed dashboard designed to give executives and store managers immediate clarity.

---

## ✨ Core Features

### 🔮 AI Demand Predictor (`/predict`)
- Enter Store ID, Department ID, Year, Month, and Week.
- The backend automatically queries the SQLite database to build advanced rolling features (`sales_lag1`, `sales_lag4`, `rolling_mean`, `rolling_std`).
- Instantly returns the predicted weekly sales in a glowing, interactive UI.

### 📊 Forecast Dashboard (`/forecast`)
- **Chart.js Visualizations**: Line and bar graphs mapping predicted sales across time, stores, and departments.
- **Model Confidence Score**: Generates a dynamic confidence score (~75-95%) based on Root Mean Square Error (RMSE).
- **Demand Volatility Analysis**: Evaluates stability using standard deviation.
- **Quality & Risk Index**: A combined metric evaluating the operational risk of using forecasts for inventory planning.

### 📋 Global Sales Dashboard (`/dashboard`)
- A filterable, interactive data table to explore the entire 421,570-row historical sales database.
- View total sales, average weekly sales, and active department counts.

### 📦 Inventory Optimizer (`/inventory`)
- Instantly calculate **Economic Order Quantity (EOQ)**.
- Calculate **Safety Stock** and **Reorder Points** using an AI-driven service level of 95% (z-score 1.65).

---

## 🎨 UI / UX Design

The frontend was completely overhauled to feature a sophisticated, AI-themed dark aesthetic:
- **Neon Glow Effects:** Cyan and Purple linear gradients with CSS drop-shadows.
- **Glassmorphism:** Semi-transparent frosted glass cards (`rgba(0, 245, 255, 0.04)`) with backdrop filters.
- **Animated Backgrounds:** Floating blurred CSS orbs and dynamic scanline effects.
- **Micro-interactions:** Smooth hover states, glowing borders, and pulsating status indicators.

---

## 🛠 Technology Stack

- **Backend:** Python 3.12, Flask, SQLite3, Gunicorn
- **Machine Learning:** Scikit-Learn (Random Forest), Pandas, NumPy, Pickle
- **Frontend:** HTML5, Vanilla CSS3, Chart.js, Google Fonts (Inter & JetBrains Mono)
- **Deployment:** Docker, Render

---

## ⚙️ Installation & Local Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/prashansha-31/ai-demand-inventory.git
cd ai-demand-inventory
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize Database
Run the setup script to create the SQLite DB and seed it with historical sales data.
```bash
python init_db.py
```

### 5️⃣ Run the App
```bash
python app.py
```
Open your browser to `http://127.0.0.1:5000`

---

## 🌍 Deployment (Render)

This project is fully Dockerized and ready for production deployment on Render.

1. Create a new **Web Service** on Render.
2. Select **Docker** as the environment.
3. Connect this GitHub repository.
4. Leave the Root Directory blank.
5. Add an Environment Variable: `PORT` = `8000`.
6. Click **Deploy**. Render will automatically install dependencies, build the SQLite database via `init_db.py`, and start the app using Gunicorn.

## Troubleshooting

- If the build fails, check the logs for missing dependencies or large files.
- Ensure the database is properly initialized by verifying `init_db.py` runs without errors.
- For frontend issues, confirm the build process completes successfully.

---

## 📈 Machine Learning Details
The core forecasting engine uses a **Random Forest Regressor**.
- **Features Used:** `Store`, `Dept`, `year`, `month`, `week`, `day`, `dayofweek`, `quarter`, `store_dept`, `month_squared`, `sales_lag1`, `sales_lag4`, `sales_rolling_mean`, `sales_rolling_std`
- **Inference Strategy:** When making a new prediction, the system looks up the most relevant recent historical data for that exact Store and Department to populate the lag and rolling mean features dynamically.