import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import warnings
import os  # Import the 'os' module to access environment variables

warnings.filterwarnings("ignore", category=FutureWarning)
app = Flask(__name__)
model = joblib.load('xgb.pkl')

def convert_float32_to_float(x):
    if isinstance(x, np.float32):
        return float(x)
    return x

@app.route('/')
def home():
    return "Welcome to the Price Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        feature_names = [
            'is_near_metro', 'seller_type_encoded', 'flat', 'total_flat', 'area_converted',
            'category_encoded', 'documents_encoded', 'is_repair_encoded'
        ]
        df = pd.DataFrame([data], columns=feature_names)
        df = df.applymap(convert_float32_to_float)
        predicted_price = model.predict(df)
        response = {'predicted_price': float(predicted_price[0])}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})  # Fixed the missing closing parenthesis

if __name__ == '__main__':
    # Use the PORT environment variable for Heroku, or 5000 if running locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
