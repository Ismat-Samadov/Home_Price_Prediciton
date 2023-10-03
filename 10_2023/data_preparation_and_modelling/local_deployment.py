import joblib
import pandas as pd
import xgboost as xgb
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
model = joblib.load('xgb.pkl')  # Load the trained XGBoost model

data = pd.read_excel('frames.xlsx')  # Load your data for prediction

def deploy_first_row(model, data):
    first_row = data.iloc[0]
    actual_price = first_row['price']
    prediction_data = first_row.drop(['price']).to_frame().T
    predicted_price = model.predict(prediction_data)
    predicted_price = predicted_price[0]
    return actual_price, predicted_price

actual_price, predicted_price = deploy_first_row(model, data)
print('Inputs from first row:')
print(data.iloc[0])
print(f"Actual Price for the First Row: {actual_price:.2f}")
print(f"Predicted Price for the First Row: {predicted_price:.2f}")
