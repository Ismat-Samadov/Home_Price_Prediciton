import re

import pandas as pd

data_1 = pd.read_csv('bina_az_02102023.csv')
data_2 = pd.read_csv('bina_az_new.csv')
data_3 = pd.read_csv('bina_az_old.csv')
data_4 = pd.read_csv('bina_az_25102023.csv')
frames = pd.concat([data_1, data_2, data_3,data_4]).drop_duplicates().dropna()
frames['is_near_metro'] = (frames['description'].str.contains('m\.', case=False) | frames['description'].str.contains('metro',case=False)).astype(int)
frames = frames[frames['seller_type'] != 'seller_type']
frames[['flat', 'total_flat']] = frames['flat_number'].str.split(' / ', expand=True).astype(int)
remove_non_numeric_and_convert_to_float = lambda value: float(re.sub(r'[^\d.]', '', value)) if value else None
frames['area_converted'] = frames['area'].apply(remove_non_numeric_and_convert_to_float)
frames['room_count'] = frames['room_count'].astype(int)
frames['documents_encoded'] = frames['documents'].map({'var': 1, 'yoxdur': 0})
frames['is_repair_encoded'] = frames['is_repair'].map({'var': 1, 'yoxdur': 0})
frames['seller_type_encoded'] = frames['seller_type'].map({'vasitəçi (agent)': 0, 'mülkiyyətçi': 1})
frames['category_encoded'] = frames['category'].map({'Yeni tikili': 0, 'Köhnə tikili': 1})
frames['price'] = frames['price'].str.replace(' ', '').astype(int)
frames = frames[['is_near_metro', 
                 'seller_type_encoded', 
                 'flat', 
                 'total_flat', 
                 'room_count',
                 'area_converted', 
                 'category_encoded',
                 'documents_encoded',
                 'is_repair_encoded', 
                 'price']].drop_duplicates(ignore_index=True)
frames.to_excel('frames.xlsx', index=False)
