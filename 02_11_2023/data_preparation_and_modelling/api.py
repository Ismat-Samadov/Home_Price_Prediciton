from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# Load the trained XGBoost model
model = joblib.load('xgb.pkl')

class Item(BaseModel):
    is_near_metro: int
    seller_type_encoded: int
    flat: int
    total_flat: int
    room_count: int
    area_converted: float
    category_encoded: int
    documents_encoded: int
    is_repair_encoded: int

@app.post("/predict/")
def predict_price(item: Item):
    features = np.array([[
        item.is_near_metro,
        item.seller_type_encoded,
        item.flat,
        item.total_flat,
        item.room_count,
        item.area_converted,
        item.category_encoded,
        item.documents_encoded,
        item.is_repair_encoded
    ]])
    prediction = model.predict(features)[0]  
    return {"predicted_price": float(prediction)} 


# uvicorn api:app --host 0.0.0.0 --port 8000 --reload


# curl -X POST "http://localhost:8000/predict/" -H "Content-Type: application/json" -d '{
#     "is_near_metro": 1,
#     "seller_type_encoded": 2,
#     "flat": 3,
#     "total_flat": 4,
#     "room_count": 2,
#     "area_converted": 80.0,
#     "category_encoded": 1,
#     "documents_encoded": 0,
#     "is_repair_encoded": 1
# }'
