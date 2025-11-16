from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

MONGO_URI = "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0"

try:
    client = MongoClient(MONGO_URI)
    db = client["gp_db"]
    collection = db["tire_data"]
    print(f"[SSACP] Conectado ao Cluster MongoDB: {MONGO_URI}")
except Exception as e:
    print(f"[SSACP] Erro crítico ao conectar no Banco: {e}")

class TireData(BaseModel):
    car_id: str
    timestamp: float
    tires: dict

@app.post("/tires")
def receive_tire_data(data: TireData):
    try:
        tire_dict = data.dict()
        result = collection.insert_one(tire_dict)
        print(f"[SSACP] Dados salvos! ID: {result.inserted_id}")
        return {"status": "success", "db_id": str(result.inserted_id)}
    except Exception as e:
        print(f"[SSACP] Erro ao salvar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "SSACP is running"}