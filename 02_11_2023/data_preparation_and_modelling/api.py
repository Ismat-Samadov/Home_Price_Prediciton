from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gzip
from joblib import load
import joblib
import numpy as np
import os

app = FastAPI()

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

# Explicitly define the model file path
model_file_path = os.path.join(os.path.dirname(__file__), 'random_forest.joblib.gz')

@app.on_event("startup")
async def load_model():
    try:
        with gzip.open(model_file_path, 'rb') as f:
            app.state.model = load(f)
            print("Model loaded successfully.")
    except FileNotFoundError as e:
        print(f"Model file not found: {e}")
        raise HTTPException(status_code=500, detail="Model file not found.")
    except Exception as e:
        print(f"Error loading the model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading the model: {e}")

fitted_scaler = joblib.load('fitted_scaler.pkl')

@app.post("/predict/")
def predict_price(item: Item):
    if app.state.model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Check the startup logs.")
    
    try:
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
        features_scaled = fitted_scaler.transform(features)
        prediction = app.state.model.predict(features_scaled)[0]
        return JSONResponse(content={"predicted_price": float(prediction)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
