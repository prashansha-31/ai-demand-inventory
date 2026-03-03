import pandas as pd
import sqlite3
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Connect to database
conn = sqlite3.connect("inventory.db")

# Load data
df = pd.read_sql_query("SELECT * FROM sales", conn)

# Feature Engineering
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["week"] = df["date"].dt.isocalendar().week

# Features & Target
X = df[["store", "dept", "year", "month", "week"]]
y = df["weekly_sales"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Model Evaluation:")
print("MAE:", mae)
print("RMSE:", rmse)

# Save model
with open("models/demand_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully.")