import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import category_encoders as ce


def load_and_combine_data(file_paths):
    data_frames = [pd.read_csv(file) for file in file_paths]
    combined_data = pd.concat(data_frames, ignore_index=True)
    return combined_data
    
def clean_data(data):
    cleaned_data = data.dropna().reset_index(drop=True)
    return cleaned_data

def filter_by_keywords(data, keywords):
    mask = data['description'].str.contains('|'.join(keywords), case=False, na=False)
    filtered_data = data[mask].reset_index(drop=True)
    return filtered_data

def preprocess_data(data):
    data['view_count'] = data['view'].str.extract(r'(?i)(?:Baxışların sayı|Просмотров): (\d+)')
    data.drop('view', axis=1, inplace=True)

    seller_type_mapping = {
        'vasitəçi (agent)': 0,
        'посредник (агент)': 0,
        'собственник': 1,
        'mülkiyyətçi': 1
    }
    data['seller_type_encoded'] = data['seller_type'].replace(seller_type_mapping)
    data.drop('seller_type', axis=1, inplace=True)

    data['price'] = data['price'].str.replace(' ', '').astype(float)
    building_type_mapping = {
        'Köhnə tikili': 'Old building',
        'Yeni tikili': 'New building',
        'Ofis': 'Office',
        'Офис': 'Office',
        'Объект': 'Object',
        'Дом / Дача': 'House / Cottage',
        'Вторичка': 'Secondary',
        'Həyət evi / Bağ evi': 'House / Garden house',
        'Новостройка': 'New building',
        'Obyekt': 'Object',
        'Mənzil': 'Apartment',
        'Участок': 'Plot',
        'Torpaq': 'Land',
        'Qaraj': 'Garage',
        'Гараж': 'Garage'
    }
    data['building_type_unified'] = data['building_type'].replace(building_type_mapping)
    data['is_near_metro'] = (data['location'].str.contains('m\.', case=False) |
                             data['address_all'].str.contains('m\.', case=False) |
                             data['description'].str.contains('m\.', case=False) |
                             data['location'].str.contains('metro', case=False) |
                             data['address_all'].str.contains('metro', case=False) |
                             data['description'].str.contains('metro', case=False)).astype(int)

    features = ['view_count', 'seller_type_encoded', 'building_type_unified', 'is_near_metro']
    target = ['price']
    encoder = ce.BinaryEncoder(cols=['building_type_unified'])
    data_encoded = encoder.fit_transform(data)
    # data_encoded.to_excel('main_data.xlsx',index=False)
    #data_encoded.drop(['building_type', 'building_type_unified_0'], axis=1, inplace=True)

    for col in data_encoded.columns:
        if data_encoded[col].dtype == bool:
            data_encoded[col] = data_encoded[col].astype(int)

    return data_encoded[features], data_encoded[target]

def train_and_evaluate_model(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return model, mse, r2

def main():
    file_paths = ['bina_az_19092023.csv', 'bina_az_21092023.csv']
    combined_data = load_and_combine_data(file_paths)
    cleaned_data = clean_data(combined_data)
    keywords = ['icare', 'kiraye', 'ицаре', 'кирае', 'Сдается']
    filtered_data = filter_by_keywords(cleaned_data, keywords)
    preprocessed_features, target = preprocess_data(filtered_data)
    model, mse, r2 = train_and_evaluate_model(preprocessed_features, target)
    model = model
    model_file = 'model.pkl'
    joblib.dump(model, model_file)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R-squared (R2) Score: {r2:.2f}")

if __name__ == "__main__":
    main()
