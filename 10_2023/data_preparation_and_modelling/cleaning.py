import pandas as pd

data_1 = pd.read_csv('bina_az_02102023.csv')
data_2 = pd.read_csv('bina_az_new.csv')
data_3 = pd.read_csv('bina_az_old.csv')
frames = pd.concat([data_1, data_2, data_3]).drop_duplicates().dropna()
frames = frames[frames['seller_type'] != 'seller_type']
seller_type_mapping = {'vasitəçi (agent)': 0, 'mülkiyyətçi': 1}
category_mapping = {'Yeni tikili': 0, 'Köhnə tikili': 1}
documents_mapping = {'var': 1, 'yoxdur': 0}
is_repair_mapping = {'var': 1, 'yoxdur': 0}
frames[['flat', 'total_flat']] = frames['flat_number'].str.split(' / ', expand=True)
frames['area_converted'] = frames['area'].str.extract(r'([\d.]+)').astype(float)
frames['room_count'] = frames['room_count'].astype(int)
frames['documents_encoded'] = frames['documents'].map(documents_mapping)
frames['is_repair_encoded'] = frames['is_repair'].map(is_repair_mapping)
frames['seller_type_encoded'] = frames['seller_type'].map(seller_type_mapping)
frames['category_encoded'] = frames['category'].map(category_mapping)
frames['price'] = frames['price'].str.replace(' ', '').astype(int)
features = ['seller_type_encoded', 'flat', 'total_flat', 'area_converted', 'category_encoded', 'documents_encoded',
            'is_repair_encoded']
target = ['price']
features = frames[features].reset_index(drop=True)
target = frames[target]
