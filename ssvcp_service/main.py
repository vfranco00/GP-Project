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

MONGO_URI = "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0"

try:
    client = MongoClient(MONGO_URI)
    db = client["gp_db"]
    collection = db["tire_data"]
    print(f"[SSVCP] Conectado ao Cluster MongoDB para leitura.")
except Exception as e:
    print(f"[SSVCP] Erro de conexão: {e}")

@app.get("/")
def home():
    return {"service": "SSVCP - API de Visualização"}

@app.get("/cars")
def get_active_cars():
    cars = collection.distinct("car_id")
    return {"cars": cars}

@app.get("/dashboard/all")
def get_all_latest():
    """ Traz o último dado de TODOS os carros """
    try:
        cars = collection.distinct("car_id")
        results = []
        for car in cars:
            data = collection.find_one(
                {"car_id": car},
                sort=[("_id", -1)],
                projection={"_id": 0}
            )
            if data:
                results.append(data)
        return results
    except Exception as e:
        print(f"Erro na leitura: {e}")
        return []

@app.get("/system/stats")
def get_system_stats():
    """ Retorna a contagem de mensagens processadas por cada ISCCP e SSACP """
    try:
        pipeline_isccp = [
            {"$group": {"_id": "$processed_by_isccp", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        isccp_stats = list(collection.aggregate(pipeline_isccp))

        pipeline_ssacp = [
            {"$group": {"_id": "$stored_by_ssacp", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}}
        ]
        ssacp_stats = list(collection.aggregate(pipeline_ssacp))

        return {
            "isccp": isccp_stats,
            "ssacp": ssacp_stats
        }
    except Exception as e:
        return {"error": str(e)}