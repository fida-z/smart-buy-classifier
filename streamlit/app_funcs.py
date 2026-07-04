import os
import sys
import pickle
import pandas as pd
import xgboost as xgb
target_dir = os.path.abspath('../notebooks')
sys.path.insert(1,target_dir)
from feature_eng_exports import data, ngt_life

def car_preprocess(car_details):


    car_df = pd.Series(car_details).to_frame().T

    # Modifying datatype:
    car_df['model'] = car_df['model'].astype('category')
    car_df['Fuel'] = car_df['Fuel'].astype('category')
    car_df['Transmission'] = car_df['Transmission'].astype('category')

    car_df['KM driven'] = car_df['KM driven'].astype('int')
    car_df['Engine capacity'] = car_df['Engine capacity'].astype('int')
    car_df['Ownership'] = car_df['Ownership'].astype('int')
    car_df['Year'] = car_df['Year'].astype('int')

    # Feautures :
    car_df['car_age'] = 2026 - car_df['Year']
    car_df['ngt_life'] = ngt_life(car_df['Fuel'].values, int(car_df['car_age'].values))
    car_df['ngt_critical'] = car_df['ngt_life'].map(lambda x: True if x<=3 else False)
    luxury_cars = 'VOLVO|MERCEDES|AUDI|LEXUS|ROLLS-ROYCE|BENTLEY|PORSCHE|FERRARI|LAMBORGH|ASTON MARTIN|LAND ROVER|RANGE ROVER|BMW 7|BMW X7'
    car_df['is_luxury_brand'] = car_df['model'].str.contains(luxury_cars)

    return(car_df)
    

def run_predict(car_details):
    car_df = car_preprocess(car_details)
    ask_price = car_df['asking_price']
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


    bst = pickle.load(open('xgb.pkl','rb'))
    pred_price = bst.predict(X_vals)
    return pred_price




