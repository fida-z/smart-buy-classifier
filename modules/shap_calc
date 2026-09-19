import numpy as np
import shap
from run_model import load_data, load_xgb

def shap_calculator(car_details):
    model = load_xgb()
    car_df = load_data(car_details)

    shap_explain = shap.TreeExplainer(model)
    explanation = shap_explain(car_df)

    shap_vals = explanation.values[0]
    base_vals = explanation.base_values[0]
    features = car_df.columns.to_list()

    order = sorted(range(len(shap_vals)), key=lambda i: -abs(shap_vals[i]))[:6]

    base_price = np.expm1(base_vals)
    running_log = base_vals
    running_rs = base_price

    contri = []

    for i in order:
         running_log += shap_vals[i]
         new_rs = np.expm1(running_log)
         delta = new_rs - running_rs
         contri.append((features[i], delta))
         running_rs = new_rs

    return {
         'base_price': base_price,
         'contributions': contri,
         'final_price' : running_rs
    }
