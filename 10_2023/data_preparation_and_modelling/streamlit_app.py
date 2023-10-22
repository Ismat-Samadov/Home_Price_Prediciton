import streamlit as st
import requests

API_URL = "http://localhost:5000/predict"  

st.title("Real Estate Price Prediction App")

is_near_metro = st.number_input("Is Near Metro (0 or 1):", min_value=0, max_value=1, step=1)
seller_type_encoded = st.number_input("Seller Type Encoded (0 or 1):", min_value=0, max_value=1, step=1)
flat = st.number_input("Flat:", value=2)
total_flat = st.number_input("Total Flat:", value=5)
area_converted = st.number_input("Area (converted):")
category_encoded = st.number_input("Category Encoded (0 or 1):", min_value=0, max_value=1, step=1)
documents_encoded = st.number_input("Documents Encoded (0 or 1):", min_value=0, max_value=1, step=1)
is_repair_encoded = st.number_input("Is Repair Encoded (0 or 1):", min_value=0, max_value=1, step=1)

if st.button("Predict"):
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
            st.success(f"Predicted Price: {result['predicted_price']:.2f}")
        else:
            st.error("Prediction request failed.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# streamlit run streamlit_app.py
