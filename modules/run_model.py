import pickle
import numpy as np
from pathlib import Path
from feature_eng import car_builder


MODEL_PATH = Path(__file__).resolve().parent.parent/'data_models'/'xgb.pkl'

def load_data(car_details):
    car_df = car_builder(car_details)
    X_vals = car_df[[
        'model',
        'Fuel',
        'Transmission',
        'KM driven',
        'Engine capacity',
        'Ownership',
        'car_age',
        'ngt_life',
        'ngt_critical',
        'is_luxury_brand',
    ]].copy()

    return(X_vals)

def load_xgb():
    bst = pickle.load(open(MODEL_PATH, 'rb'))
    return(bst)

def predict_price(X,model):

    predval = model.predict(X)
    pred_price = np.expm1(predval)
    return pred_price
