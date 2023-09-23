import joblib
import pandas as pd

def load_model(model_file):
    try:
        model = joblib.load(model_file)
        return model
    except Exception as e:
        raise Exception(f"Failed to load the model: {str(e)}")

def predict_price(user_input, model):
    try:
        # Define the desired column order
        desired_columns = ['view_count', 'seller_type_encoded', 'building_type_unified', 'is_near_metro']

        # Reorder the user_input dictionary
        user_input = {col: user_input[col] for col in desired_columns}

        user_data = pd.DataFrame([user_input])
        predicted_price = model.predict(user_data)

        return predicted_price[0]
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")

def main():
    model_file = 'model.pkl'
    model = load_model(model_file)

    user_input = {
        'view_count': 1000,
        'seller_type_encoded': 0,
        'building_type_unified': 'New building',
        'is_near_metro': 1,
    }

    try:
        predicted_price = predict_price(user_input, model)
        print(f"Predicted Price: {predicted_price:.2f}")
    except Exception as e:
        print(f"Prediction error: {str(e)}")

if __name__ == "__main__":
    main()
