import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np
import warnings
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
        return jsonify({'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)

# curl -X POST -H "Content-Type: application/json" -d '{
#   "is_near_metro": 1,
#   "seller_type_encoded": 0,
#   "flat": 2,
#   "total_flat": 5,
#   "area_converted": 100,
#   "category_encoded": 1,
#   "documents_encoded": 0,
#   "is_repair_encoded": 1
# }' http://localhost:5000/predict
