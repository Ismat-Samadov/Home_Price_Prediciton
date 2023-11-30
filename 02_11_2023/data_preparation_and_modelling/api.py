from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import gzip
from joblib import load
import joblib
import numpy as np
import streamlit as st

app = FastAPI()

@app.on_event("startup")
async def load_model():
    try:
        with gzip.open('random_forest.joblib.gz', 'rb') as f:
            app.model = load(f)
    except Exception as e:
        st.error(f"Error loading the model: {e}")

fitted_scaler = joblib.load('fitted_scaler.pkl')

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
        prediction = app.model.predict(features_scaled)[0]
        return JSONResponse(content={"predicted_price": float(prediction)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")
