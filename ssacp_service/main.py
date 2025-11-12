from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client["gp_db"]
collection = db["tire_data"]

class TireData(BaseModel):
    car_id: str
    timestamp: float
    tires: dict

@app.post("/tires")
def receive_tire_data(data: TireData):
    try:
        tire_dict = data.dict()
        
        result = collection.insert_one(tire_dict)
        
        print(f"[SSACP] Dados recebidos e salvos! ID: {result.inserted_id}")
        return {"status": "success", "db_id": str(result.inserted_id)}
    except Exception as e:
        print(f"[SSACP] Erro ao salvar: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "SSACP is running"}