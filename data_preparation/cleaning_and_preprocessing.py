import pandas as pd


def load_and_concat_data(file1, file2):
    data_1 = pd.read_csv(file1)
    data_2 = pd.read_csv(file2)
    return pd.concat([data_1, data_2], ignore_index=True).drop_duplicates(keep='last').dropna().reset_index(drop=True)


def encode_seller_type(df):
    seller_type_mapping = {
        'vasitəçi (agent)': 0,
        'посредник (агент)': 0,
        'собственник': 1,
        'mülkiyyətçi': 1
    }
    df['seller_type_encoded'] = df['seller_type'].replace(seller_type_mapping)
    df.drop('seller_type', axis=1, inplace=True)
    return df


def clean_and_sort_data(df):
    df['price'] = df['price'].str.replace(' ', '').astype(float)
    return df.sort_values(by='price', ascending=True)


def map_building_type(df):
    building_type_mapping = {
        'Köhnə tikili': 'Old_building',
        'Yeni tikili': 'New_building',
        'Ofis': 'Office',
        'Офис': 'Office',
        'Объект': 'Object',
        'Дом / Дача': 'Cottage',
        'Вторичка': 'Secondary',
        'Həyət evi / Bağ evi': 'Garden_house',
        'Новостройка': 'New_building',
        'Obyekt': 'Object',
        'Mənzil': 'Apartment',
        'Участок': 'Plot',
        'Torpaq': 'Land',
        'Qaraj': 'Garage',
        'Гараж': 'Garage'
    }
    df['building_type_unified'] = df['building_type'].replace(building_type_mapping)
    return df


def check_near_metro(df):
    df['is_near_metro'] = (df['location'].str.contains('m\.', case=False) |
                           df['address_all'].str.contains('m\.', case=False) |
                           df['description'].str.contains('m\.', case=False) |
                           df['location'].str.contains('metro', case=False) |
                           df['address_all'].str.contains('metro', case=False) |
                           df['description'].str.contains('metro', case=False)).astype(int)
    return df


def process_data(df):
    df = encode_seller_type(df)
    df = clean_and_sort_data(df)
    df = map_building_type(df)
    df = check_near_metro(df)
    return df


if __name__ == '__main__':
    file1 = 'bina_az_19092023.csv'
    file2 = 'bina_az_21092023.csv'

    frames = load_and_concat_data(file1, file2)
    frames = process_data(frames)

    features = ['seller_type_encoded', 'building_type_unified', 'is_near_metro']
    target = ['price']

    features = frames[features].reset_index(drop=True)
    target = frames[target]

    dummy_building_type = pd.get_dummies(features['building_type_unified'], prefix='building_type')
    features = pd.concat([features, dummy_building_type], axis=1)

    features.drop('building_type_unified', axis=1, inplace=True)
    features.to_excel('features.xlsx', index=False)
    target.to_excel('target.xlsx', index=False)
