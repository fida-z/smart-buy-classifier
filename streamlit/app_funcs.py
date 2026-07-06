import os
import sys
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import google.generativeai as genai
from dotenv import load_dotenv

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

def predict_dep(car_details,yr):
    car_df = car_preprocess(car_details)
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

    X_vals['Ownership'] = X_vals['Ownership']+1
    X_vals['car_age'] = X_vals['car_age']+yr    

    bst = pickle.load(open('xgb.pkl','rb'))
    pred_price = bst.predict(X_vals)
    return pred_price



def dep_calc(car_details):
    year = car_details['Year']
    dep_details = {}
    for yr in range(8):
        dep_details[2026+yr] = np.expm1(predict_dep(car_details, yr))
    
    return(dep_details)


def shap_calc(car_details):
    model = pickle.load(open('xgb.pkl','rb')) 
    car_pp = car_preprocess(car_details)
    car_df = car_pp[[
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

    shap_explain = shap.TreeExplainer(model)
    shap_vals = sorted(shap_explain(car_df).values[0])[:6]
    
    shap_dict = {}
    for val, col in zip(shap_vals, car_df.columns):
        if val < 0:
            shap_dict[col] = 'Negative'
        else:
            shap_dict[col] = 'Positive'

    return(shap_dict)


def ai_insights(content):
    load_dotenv()
    GEMINI = os.getenv("GEMINI")
    genai.configure(api_key=GEMINI)

    ai_bot = genai.GenerativeModel(model_name='gemini-3.5-flash')
    prompt = f'''
    You are an automotive market analyst.
    You are given structured information about a used car, its predicted market value, market position, and the main factors affecting its valuation.
    Write exactly 3–5 concise bullet points.
    Requirements:
    - Focus only on useful buying insights.
    - Base every statement only on the provided information.
    - Do not invent facts.
    - Do not speculate about maintenance, accidents, insurance, reliability, resale, service history, or ownership history unless explicitly provided.
    - Do not mention machine learning, AI, SHAP, prediction models, or confidence scores.
    - Do not greet the user.
    - Do not use emojis.
    - Do not repeat the numerical values unless they help explain the insight.
    - Keep each bullet under 20 words.
    - Use professional, neutral language.
    - Avoid generic advice such as "inspect the vehicle" or "verify documents."

    Generate insights that explain:
    - whether the asking price appears favorable,
    - how the car compares with similar listings,
    - any noteworthy strengths or weaknesses evident from the supplied data.

    Return the output in markdown format.
    Input:
    {content}
    '''

    response = ai_bot.generate_content(prompt)
    return(response.text)


def get_segment(model_name):
    seg0 = pd.read_csv('seg0.csv')
    seg1 = pd.read_csv('seg1.csv')
    seg2 = pd.read_csv('seg2.csv')
    seg3 = pd.read_csv('seg3.csv')

    seg_count = {}
    for seg, i in zip([seg0,seg1,seg2,seg3],range(4)):
        seg_count[i] = seg.loc[seg['model'] == model_name, 'count'].sum()
        
    return(max(seg_count,key=seg_count.get))


def model_popularity(model_name,seg):
    if(seg == 0):
        df = pd.read_csv('seg0.csv')
    elif(seg == 1):
        df = pd.read_csv('seg1.csv')
    elif(seg == 2):
        df = pd.read_csv('seg2.csv')
    elif(seg == 3):
        df = pd.read_csv('seg3.csv')

    return(df[df['model'] == model_name].index + 1)

def listing_no(model_name, seg):
    if(seg == 0):
        df = pd.read_csv('seg0.csv')
    elif(seg == 1):
        df = pd.read_csv('seg1.csv')
    elif(seg == 2):
        df = pd.read_csv('seg2.csv')
    elif(seg == 3):
        df = pd.read_csv('seg3.csv')

    return(df.loc[df['model'] == model_name, 'count'].sum())

def seg_analysis(model_name, segment):
    

