from flask import Flask, request, jsonify
import joblib
app = Flask(__name__)
model = joblib.load('random_forest_regressor.pkl')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        predictions = model.predict(input_data)
        return jsonify({'predictions': predictions.tolist()})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main':
    app.run(debug=True)
