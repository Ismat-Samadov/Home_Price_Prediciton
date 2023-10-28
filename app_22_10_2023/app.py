import streamlit as st
import requests
API_URL = "https://home-price-predicition-209f2b8f62a1.herokuapp.com"

home_image_url = "https://images.pexels.com/photos/463734/pexels-photo-463734.jpeg?auto=compress&cs=tinysrgb&w=600"

image_html = f'<img src="{home_image_url}" style="max-width: 100%; height: auto;">'
st.markdown(image_html, unsafe_allow_html=True)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.sidebar.title("Input Data")
st.title("Real Estate Price Prediction App")
no_yes_mapping = {"No": 0, "Yes": 1}
is_near_metro = st.sidebar.selectbox("Is near Metro ?", ("No", "Yes"), format_func=lambda x: x)
seller_type_encoded = st.sidebar.selectbox("Seller Type Agent or not ?", ("No", "Yes"), format_func=lambda x: x)
flat = st.sidebar.selectbox("Flat of home", list(range(1, 11)))
total_flat = st.sidebar.slider("Total Flat of Building", 1, 25, 5)
area_converted = st.sidebar.slider("Area of home in square meter:", 1, 100, 1)
category_encoded = st.sidebar.selectbox("Category of building:", ("Old Building", "New Building"), format_func=lambda x: x)
documents_encoded = st.sidebar.selectbox("Has documents ?", ("No", "Yes"), format_func=lambda x: x)
is_repair_encoded = st.sidebar.selectbox("Is repaired ?", ("No", "Yes"), format_func=lambda x: x)
data = {
    "is_near_metro": no_yes_mapping[is_near_metro],
    "seller_type_encoded": no_yes_mapping[seller_type_encoded],
    "flat": flat,
    "total_flat": total_flat,
    "area_converted": area_converted,
    "category_encoded": 0 if category_encoded == "Old Building" else 1,
    "documents_encoded": no_yes_mapping[documents_encoded],
    "is_repair_encoded": no_yes_mapping[is_repair_encoded],
}
if st.sidebar.button("Predict"):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL + "/predict", json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            predicted_price = int(result['predicted_price'])
            st.sidebar.success(f"Predicted Price: {predicted_price}")
        else:
            st.sidebar.error("Prediction request failed.")
    except Exception as e:
        st.sidebar.error(f"An error occurred: {str(e)}")