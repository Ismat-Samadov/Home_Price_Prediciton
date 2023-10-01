import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib

features = pd.read_excel('features.xlsx')
target = pd.read_excel('target.xlsx')

y = target.values.ravel()

X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(
    n_estimators=88,
    random_state=47,
    max_depth=16,
    min_samples_split=2,
    min_samples_leaf=2,
    min_weight_fraction_leaf=0.1,
    max_features=0.8,
    max_leaf_nodes=None,
    min_impurity_decrease=0.8,
    bootstrap=True,
    oob_score=True,
    n_jobs=8,
    verbose=0,
    warm_start=True,
    ccp_alpha=0.0,
    max_samples=None
)

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

print(pd.DataFrame({
    'r2_score': np.ravel([r2_score(y_test, y_pred)]),
    'mean_squared_error': np.sqrt(mean_squared_error(y_test, y_pred)),
    'mean_absolute_error': mean_absolute_error(y_test, y_pred)
}))

model_filename = 'random_forest_regressor.pkl'
joblib.dump(rf_model, model_filename)
