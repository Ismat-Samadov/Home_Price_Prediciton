import streamlit as st
import requests

# Define the Flask API URL
API_URL = "http://localhost:5000/predict"
# Streamlit app title
st.title("Real Estate Price Prediction App")

# Create a sidebar
st.sidebar.title("Input Data")

# Create input fields for user data in the sidebar
is_near_metro = st.sidebar.number_input("Is Near Metro (0 or 1):", min_value=0, max_value=1, step=1)
seller_type_encoded = st.sidebar.number_input("Seller Type Encoded (0 or 1):", min_value=0, max_value=1, step=1)
flat = st.sidebar.number_input("Flat:", value=2)
total_flat = st.sidebar.number_input("Total Flat:", value=5)
area_converted = st.sidebar.number_input("Area (converted):")
category_encoded = st.sidebar.number_input("Category Encoded (0 or 1):", min_value=0, max_value=1, step=1)
documents_encoded = st.sidebar.number_input("Documents Encoded (0 or 1):", min_value=0, max_value=1, step=1)
is_repair_encoded = st.sidebar.number_input("Is Repair Encoded (0 or 1):", min_value=0, max_value=1, step=1)

# Make a prediction request when a button is clicked
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
    try:
        response = requests.post(API_URL, json=data)
        if response.status_code == 200:
            result = response.json()
            st.sidebar.success(f"Predicted Price: {result['predicted_price']:.2f}")
        else:
            st.sidebar.error("Prediction request failed.")
    except Exception as e:
        st.sidebar.error(f"An error occurred: {str(e)}")

# streamlit run streamlit_app.py
