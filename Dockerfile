# Python environment for Flask app
FROM python:3.12-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Initialize the database with historical data
RUN python init_db.py

EXPOSE 8000

# Start Gunicorn to serve the Flask app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
