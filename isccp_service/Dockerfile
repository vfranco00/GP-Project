from python:3.9-slim
workdir /app
copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt
copy isccp_consumer.py .
cmd ["python", "isccp_consumer.py"]
