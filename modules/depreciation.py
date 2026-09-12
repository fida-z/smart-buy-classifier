import pickle
import numpy as np
from run_model import load_data, load_xgb

def predict_depreciation(car_details,year):
    model = load_xgb()
    X_vals = load_data(car_details)

    X_vals['Ownership'] = X_vals['Ownership']+1
    X_vals['car_age'] = X_vals['car_age']+year
    X_vals['ngt_life'] = X_vals['ngt_life']+year
    X_vals['ngt_critical'] = True if X_vals['ngt_life']<=3 else False

    dep_pred_price = model.predict(X_vals)
    return dep_pred_price


def depreciation_calculator(car_details):
    dep_details = {}
    for yr in range(8):
        dep_details[2026+yr] = np.expm1(predict_depreciation(car_details, yr))
    
    return(dep_details)

