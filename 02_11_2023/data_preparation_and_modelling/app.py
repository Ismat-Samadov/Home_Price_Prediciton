import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import locale  
locale.setlocale(locale.LC_ALL, '')

import gzip
from joblib import load

with gzip.open('02_11_2023/data_preparation_and_modelling/random_forest.joblib.gz', 'rb') as f_in:
    with open('random_forest.joblib', 'wb') as f_out:
        f_out.writelines(f_in)

model = load('random_forest.joblib')

fitted_scaler = joblib.load('02_11_2023/data_preparation_and_modelling/fitted_scaler.pkl')
home_image_url = "https://images.pexels.com/photos/463734/pexels-photo-463734.jpeg?auto=compress&cs=tinysrgb&w=600"
image_html = f'<img src="{home_image_url}" style="max-width: 100%; height: auto;">'
st.markdown(image_html, unsafe_allow_html=True)
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
st.sidebar.title("Input Data")
st.title("Real Estate Price Prediction App")
no_yes_mapping = {"No": 0, "Yes": 1}
is_near_metro = st.sidebar.selectbox("Is near Metro?", ("No", "Yes"))
seller_type_encoded = st.sidebar.selectbox("Seller Type Agent or not?", ("No", "Yes"))
flat = st.sidebar.selectbox("Flat of home", list(range(1, 35)))
total_flat = st.sidebar.slider("Total Flat of Building", 1, 35, 5)
room_count = st.sidebar.selectbox("Room Count", list(range(1, 6)))
area_converted = st.sidebar.slider("Area of home in square meter:", 1, 500, 1)
category_encoded = st.sidebar.selectbox("Category of building:", ("Old Building", "New Building"))
documents_encoded = st.sidebar.selectbox("Has documents?", ("No", "Yes"))
is_repair_encoded = st.sidebar.selectbox("Is repaired?", ("No", "Yes"))

data = {
    "is_near_metro": no_yes_mapping[is_near_metro],
    "seller_type_encoded": no_yes_mapping[seller_type_encoded],
    "flat": flat,
    "total_flat": total_flat,
    "room_count": room_count,
    "area_converted": area_converted,
    "category_encoded": 1 if category_encoded == "New Building" else 0,
    "documents_encoded": no_yes_mapping[documents_encoded],
    "is_repair_encoded": no_yes_mapping[is_repair_encoded],
}

if st.sidebar.button('Predict Price'):
    scaled_data = fitted_scaler.transform([list(data.values())])
    prediction = model.predict(scaled_data)
    formatted_prediction = locale.format("%d", prediction[0], grouping=True)
    st.success(f'Predicted Price: {formatted_prediction}')
