FROM python:3.9-slim
workdir /app
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt
copy car_simulator.py .
cmd ["python", "car_simulator.py"]