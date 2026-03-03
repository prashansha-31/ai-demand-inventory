# 🤖 AI-Based Demand Forecasting & Inventory Optimization Platform

## 📌 Overview

This project is a full-stack web application that integrates **machine learning-based demand forecasting** with **automated inventory optimization**.  

The system simulates a real-world retail decision-support platform where historical sales data is analyzed, future demand is predicted, and optimal inventory policies are generated automatically.

It demonstrates the integration of:

- 📊 Data Analytics  
- 🤖 Machine Learning  
- 📦 Inventory Optimization  
- 🗄 Database Management  
- 🌐 Web Application Development  

---

## 🎯 Objectives

- Analyze historical retail sales data.
- Predict weekly demand using a trained machine learning model.
- Automatically compute optimal inventory policies.
- Store forecast and optimization results in a relational database.
- Provide an interactive web-based dashboard for decision support.

---

## 🏗 System Architecture

```
Sales Data → ML Model → Demand Prediction → Inventory Optimization → Database Storage → Web Dashboard
```

### 🔹 Architecture Layers

### 1️⃣ Data Layer
- Cleaned historical sales dataset (CSV)
- SQLite database for persistent storage
- Automatic schema initialization

### 2️⃣ Machine Learning Layer
- Pre-trained regression model (Pickle)
- Time-based feature engineering (year, month, week)
- Real-time demand prediction

### 3️⃣ Optimization Layer
- 📐 Economic Order Quantity (EOQ)
- 📊 Safety Stock calculation
- 📍 Reorder Point computation
- Automated integration with forecast output

### 4️⃣ Application Layer
- Flask web framework
- Interactive sales dashboard
- Forecasting interface
- Inventory recommendation engine
- Historical tracking tables

---

## ✨ Key Features

### 📊 Sales Dashboard
- Filter by Store and Department
- Display recent sales records
- Calculate total and average weekly sales
- View distinct store and department counts

### 🔮 Demand Forecasting
- Input Store ID and Department ID
- Generate real-time weekly demand prediction
- Store predictions with timestamps
- Display forecast history

### 📦 Automated Inventory Optimization
- EOQ calculation
- Safety Stock estimation
- Reorder Point determination
- Automatic storage of inventory policies
- Inventory decision history tracking

### 🗂 Persistent Data Management
- SQLite integration
- Automatic table creation
- Forecast and policy logs
- Structured database design

---

## 📐 Inventory Optimization Formulas

### 📦 Economic Order Quantity (EOQ)

\[
EOQ = \sqrt{\frac{2DS}{H}}
\]

Where:
- D = Predicted Demand
- S = Ordering Cost
- H = Holding Cost

---

### 🛡 Safety Stock

\[
Safety\ Stock = Z \times \sqrt{Lead\ Time} \times Demand\ Variability
\]

---

### 📍 Reorder Point

\[
Reorder\ Point = (Demand \times Lead\ Time) + Safety\ Stock
\]

---

## 🔄 Workflow

1. 📥 Historical sales data loaded into database.
2. 🧑‍💼 User selects store and department.
3. 🤖 ML model predicts weekly demand.
4. 📦 Inventory engine calculates optimal policy.
5. 🗄 Forecast and optimization results stored.
6. 📊 Historical records displayed for monitoring.

---

## 🛠 Technology Stack

- 🐍 Python
- 🌐 Flask
- 🗄 SQLite
- 📊 Pandas
- 🔢 NumPy
- 🤖 Scikit-learn
- 🧾 HTML / CSS
- 📦 Pickle (Model Serialization)

---

## 📁 Project Structure

```
AI-Demand-Inventory/
│
├── 📁 data/
│   └── clean_sales.csv
│
├── 📁 models/
│   └── demand_model.pkl
│
├── 📁 templates/
│   ├── index.html
│   ├── dashboard.html
│   └── forecast.html
│
├── 📁 static/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ Installation & Setup

### 1️⃣ Clone Repository

```
git clone https://github.com/prashansha-31/ai-demand-inventory.git
cd AI-Demand-Inventory
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

**Windows**
```
venv\Scripts\activate
```

**Mac/Linux**
```
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run Application

```
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000/
```

---

## 🚀 Future Enhancements

- 📊 Interactive charts and visualization
- 📅 Multi-week forecasting
- 🔬 Advanced model tuning
- 🔐 User authentication
- 🌍 Cloud deployment
- 📈 Performance monitoring dashboard

---

## 🏁 Conclusion

This platform demonstrates how **Machine Learning and Inventory Optimization** can be integrated into a unified decision-support system.  

It highlights practical implementation of predictive analytics combined with operational models to improve supply chain efficiency and support data-driven retail management.