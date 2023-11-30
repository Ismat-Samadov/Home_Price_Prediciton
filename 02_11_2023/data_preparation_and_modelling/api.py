from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gzip
from joblib import load
import joblib
import numpy as np
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class PredictionResponse(BaseModel):
    predicted_price: float

model_file_path = "random_forest.joblib.gz"  

logging.basicConfig(level=logging.INFO)

@app.on_event("startup")
async def load_model():
    try:
        with gzip.open(model_file_path, 'rb') as f:
            app.state.model = load(f)
            logging.info("Model loaded successfully.")
    except FileNotFoundError as e:
        logging.error(f"Model file not found: {e}")
        raise HTTPException(status_code=500, detail="Model file not found.")
    except Exception as e:
        logging.error(f"Error loading the model: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading the model: {e}")

fitted_scaler = joblib.load('fitted_scaler.pkl')

@app.post("/predict/", response_model=PredictionResponse)
def predict_price(item: Item):
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
        return PredictionResponse(predicted_price=float(prediction))
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
