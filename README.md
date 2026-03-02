# 📊 AI-Based Demand Forecasting & Inventory Optimization Platform

A full-stack AI-powered retail analytics system built using Flask and SQLite.

This project implements real-time sales analytics, dynamic filtering, and database integration as a foundation for demand forecasting and inventory optimization.

---

## 🚀 Project Overview

This platform allows users to:

- View real-time sales analytics
- Filter sales by Store and Department
- Analyze Total Sales & Average Weekly Sales
- Access a dynamic dashboard powered by SQL queries
- Prepare data for Machine Learning forecasting

The system integrates backend logic, database management, and frontend interaction into a scalable architecture.

---

## 🧱 System Architecture

Frontend (HTML + Bootstrap)  
⬇  
Flask Backend (Python)  
⬇  
SQLite Database  
⬇  
Sales Dataset (843,000+ records)

---

## 🛠 Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Data Processing:** Pandas
- **Frontend:** HTML, Bootstrap 5
- **Version Control:** Git & GitHub

---

## 📅 Development Progress

### ✅ Day 1 – Project Setup
- Flask initialization
- Project folder structure
- Virtual environment setup
- Basic routes (`/`, `/dashboard`)
- GitHub repository setup

---

### ✅ Day 2 – Database Integration
- SQLite database created
- Tables implemented:
  - `sales`
  - `forecasts`
  - `inventory_policy`
- Dataset cleaned using Pandas
- 843,000+ records inserted into database
- Backend successfully connected to database

---

### ✅ Day 3 – Analytics Dashboard
- Dynamic data fetching from SQLite
- SQL aggregation queries implemented:
  - Total Sales (SUM)
  - Average Weekly Sales (AVG)
  - Total Stores (COUNT DISTINCT)
  - Total Departments (COUNT DISTINCT)
- Professional summary cards added
- Real-time dashboard rendering

---

### ✅ Day 4 – Interactive Filtering System
- Dynamic filtering by:
  - Store
  - Department
- SQL WHERE clause generation
- Filter-based analytics recalculation
- Reset functionality implemented
- Fully interactive dashboard

---

## 📊 Current Features

✔ Live sales analytics  
✔ Dynamic filtering system  
✔ Real-time SQL aggregation  
✔ Professional Bootstrap UI  
✔ Scalable full-stack structure  
✔ Clean project architecture  

---

## 📂 Project Structure

```
ai-demand-inventory/
│
├── app.py
├── inventory.db
├── requirements.txt
├── README.md
│
├── data/
│   ├── sales.csv
│   └── clean_sales.csv
│
├── models/
│   └── eda_analysis.py
│
├── templates/
│   ├── index.html
│   └── dashboard.html
│
└── static/
```

---

## ▶ How to Run

1️⃣ Create virtual environment:

```
python -m venv venv
```

2️⃣ Activate environment (Windows):

```
venv\Scripts\activate
```

3️⃣ Install dependencies:

```
pip install -r requirements.txt
```

4️⃣ Run application:

```
python app.py
```

5️⃣ Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔮 Upcoming Features

- Machine Learning Demand Forecasting
- Sales Trend Visualization (Charts)
- Forecast storage in `forecasts` table
- Inventory Optimization (EOQ, Safety Stock, Reorder Point)
- Model performance evaluation

---

## 🎯 Academic Objective

This project demonstrates:

- End-to-end system design
- Backend + Database integration
- Data-driven analytics
- Interactive dashboard engineering
- Foundation for AI-powered retail forecasting

---

## 👥 Team T-24

- **Prashansha Maheshwari(Team Leader)** – Backend & Database Engineering  
- **Abhishek Verma** – Data Processing & Analytics  
- **Prateek Choudhary** – Frontend & UI Development  

---

⭐ Developed as part of 2nd Year AIML Mini Project