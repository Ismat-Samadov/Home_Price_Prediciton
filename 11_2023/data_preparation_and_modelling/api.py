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
    prediction = model.predict(features)[0]  # Ensure it's a standard Python float
    return {"predicted_price": float(prediction)}  # Convert the prediction to float
