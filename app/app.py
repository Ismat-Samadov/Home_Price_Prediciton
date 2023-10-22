import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import warnings
import requests
import streamlit as st

# Suppress FutureWarning in Flask
warnings.filterwarnings("ignore", category=FutureWarning)

# Load the XGBoost model
model = joblib.load('xgb.pkl')

# Define the Flask API URL
API_URL = "http://localhost:5000/predict"

# Create a Streamlit app
st.title("Real Estate Price Prediction App")
st.sidebar.title("Input Data")

# Define a function to make predictions
def make_prediction(data):
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['predicted_price']
        else:
            return None
    except Exception as e:
        return None

# Create input fields for user data in the Streamlit sidebar
is_near_metro = st.sidebar.number_input("Is Near Metro (0 or 1):", min_value=0, max_value=1, step=1)
seller_type_encoded = st.sidebar.number_input("Seller Type Encoded (0 or 1):", min_value=0, max_value=1, step=1)
flat = st.sidebar.number_input("Flat:", value=2)
total_flat = st.sidebar.number_input("Total Flat:", value=5)
area_converted = st.sidebar.number_input("Area (converted):")
category_encoded = st.sidebar.number_input("Category Encoded (0 or 1):", min_value=0, max_value=1, step=1)
documents_encoded = st.sidebar.number_input("Documents Encoded (0 or 1):", min_value=0, max_value=1, step=1)
is_repair_encoded = st.sidebar.number_input("Is Repair Encoded (0 or 1):", min_value=0, max_value=1, step=1)

# Make a prediction when the "Predict" button is clicked
if st.sidebar.button("Predict"):
    data = {
        "is_near_metro": is_near_metro,
        "seller_type_encoded": seller_type_encoded,
        "flat": flat,
        "total_flat": total_flat,
        "area_converted": area_converted,
        "category_encoded": category_encoded,
        "documents_encoded": documents_encoded,
        "is_repair_encoded": is_repair_encoded,
    }
    
    predicted_price = make_prediction(data)
    if predicted_price is not None:
        st.sidebar.success(f"Predicted Price: {predicted_price:.2f}")
    else:
        st.sidebar.error("Prediction request failed.")

if __name__ == '__main__':
    app = Flask(__name__)

    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            data = request.get_json()
            feature_names = [
                'is_near_metro', 'seller_type_encoded', 'flat', 'total_flat', 'area_converted',
                'category_encoded', 'documents_encoded', 'is_repair_encoded'
            ]
            df = pd.DataFrame([data], columns=feature_names)
            df = df.applymap(lambda x: float(x) if isinstance(x, np.float32) else x)
            predicted_price = model.predict(df)
            response = {'predicted_price': float(predicted_price[0])}
            return jsonify(response)
        except Exception as e:
            return jsonify({'error': str(e)})
    
    app.run(debug=False)  # Disable Flask debugging when using Streamlit
