import re
import pandas as pd
import warnings
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from joblib import dump, load
import gzip
import pickle

warnings.filterwarnings("ignore", category=FutureWarning)

data_1 = pd.read_csv('bina_az_02102023.csv')
data_2 = pd.read_csv('bina_az_new.csv')
data_3 = pd.read_csv('bina_az_old.csv')
data_4 = pd.read_csv('bina_az_25102023.csv')
data_5 = pd.read_csv('bina_az_01112023.csv')
frames = pd.concat([data_1, data_2, data_3,data_4,data_5]).drop_duplicates().dropna()
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
frames = frames[frames['price']>5000]
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
# frames.to_excel('frames.xlsx', index=False)

data = frames
X = data.drop(columns=['price'])
y = data['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=50,
    min_samples_split=5,
    min_samples_leaf=4,
    random_state=42
)

model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)

print("Model performance metrics")
print("-----------------------")
print(f"R-squared: {r2:.2f}")
print(f"Root Mean Squared Error: {rmse:.2f}")
print(f"Mean Absolute Error: {mae:.2f}")
print("-----------------------")
# joblib.dump(scaler, 'fitted_scaler.pkl')
with open('fitted_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)


dump(model, 'random_forest.joblib')
loaded_model = load('random_forest.joblib')
with open('random_forest.joblib', 'rb') as f_in:
    with gzip.open('random_forest.joblib.gz', 'wb') as f_out:
        f_out.writelines(f_in)
