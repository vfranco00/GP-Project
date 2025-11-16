from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo_host = os.getenv("MONGO_HOST", "localhost")
client = MongoClient(host=mongo_host, port=27017)
db = client["gp_db"]
collection = db["tire_data"]

@app.get("/")
def home():
    return {"message": "Vizualizaçao SSVCP"}

@app.get("/cars")
def get_active_cars():
    cars = collection.distinct("car_id")
    return {"cars": cars}

@app.get("/cars/{car_id}/latest")
def get_latest_telemetry(car_id: str):
    data = collection.find_one({"car_id": car_id}, sort=[("_id", -1)], projection={"_id": 0})
    if not data:
        return {"error": "Car not found"}
    return data

@app.get("/dashboard/all")
def get_all_latest():
    cars = collection.distinct("car_id")
    results = []
    for car in cars:
        data = collection.find_one({"car_id": car}, sort=[("_id", -1)], projection={"_id": 0})
        if data:
            results.append(data)
    return results