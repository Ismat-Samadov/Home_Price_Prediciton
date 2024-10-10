from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import locale

# Set locale to format currency output
locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)

# Load the trained model and columns
model = joblib.load('best_random_forest_model.pkl')
training_columns = joblib.load('training_columns.pkl')

@app.route('/')
def index():
    # Predefined values for easy testing
    predefined_values = {
        "is_near_metro": 1,
        "seller_type_encoded": 0,
        "flat": 5,
        "total_flat": 19,
        "room_count": 3,
        "area_converted": 95.0,
        "category_encoded": 0,
        "documents_encoded": 1,
        "is_repair_encoded": 1
    }
    return render_template('index.html', predefined=predefined_values)

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input data from the form
    data = request.form

    # Map binary inputs to Yes/No for display purposes
    user_inputs = {
        'Is Near Metro': 'Yes' if int(data['is_near_metro']) == 1 else 'No',
        'Seller Type': 'Owner' if int(data['seller_type_encoded']) == 1 else 'Agent',
        'Flat Number': data['flat'],
        'Total Floors': data['total_flat'],
        'Room Count': data['room_count'],
        'Area (m²)': data['area_converted'],
        'Category': 'New' if int(data['category_encoded']) == 0 else 'Old',
        'Has Documents': 'Yes' if int(data['documents_encoded']) == 1 else 'No',
        'Is Repaired': 'Yes' if int(data['is_repair_encoded']) == 1 else 'No'
    }

    # Prepare the input data for the model
    input_data = [float(data.get(col, 0)) for col in training_columns]
    input_array = np.array(input_data).reshape(1, -1)

    # Make prediction
    prediction = model.predict(input_array)

    # Format the predicted price as a currency
    formatted_prediction = locale.currency(prediction[0], grouping=True)

    # Render the page with the prediction result
    return render_template('index.html', prediction=formatted_prediction, predefined=data, user_inputs=user_inputs)

if __name__ == '__main__':
    app.run(debug=True)
