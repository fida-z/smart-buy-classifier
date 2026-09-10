import os
import sys
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import google.generativeai as genai
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
from dotenv import load_dotenv

target_dir = os.path.abspath('../notebooks')
sys.path.insert(1,target_dir)

# Get the path of the directory where app_funcs.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'xgb.pkl')

# Load the model using the correct relative path
bst = pickle.load(open(model_path, 'rb'))

def ngt_life(fuel, car_age):
    if(fuel == 'Diesel'):
        return(10-car_age)
    elif(fuel == 'Electric'):
        return(15)
    else:
        return(15-car_age)


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


    bst = pickle.load(open(model_path, 'rb'))
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

    bst = pickle.load(open(model_path, 'rb')) 
    pred_price = bst.predict(X_vals)
    return pred_price



def dep_calc(car_details):
    year = car_details['Year']
    dep_details = {}
    for yr in range(8):
        dep_details[2026+yr] = np.expm1(predict_dep(car_details, yr))
    
    return(dep_details)


def shap_calc(car_details):
    model = pickle.load(open(model_path, 'rb'))  
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


import plotly.graph_objects as go

def render_waterfall(shap_result):
     
    contributions = shap_result['contributions']
    labels = [name for name, _ in contributions]
    deltas = [delta for _, delta in contributions]

    fig = go.Figure(go.Waterfall(
        orientation='v',
        measure=['relative'] * len(deltas),
        x=labels,
        y=deltas,
        base=shap_result['base_price'],
        increasing=dict(marker=dict(color='#2E8B57')),   # green
        decreasing=dict(marker=dict(color='#C0392B')),   # red
        connector=dict(line=dict(color='#C9DCF2', width=1)),
        text=[f'₹{d:,.0f}' for d in deltas],
        textposition='outside'
    ))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Roboto, sans-serif', color='#14203A'),
        yaxis=dict(title='Price (₹)', showgrid=True, gridcolor='#C9DCF2'),
        margin=dict(l=40, r=20, t=20, b=60),
        height=400
    )

    return fig
    

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
    - some information about the make/model and other characters of the car itself,
    - how the car compares with similar listings,
    - any noteworthy strengths or weaknesses evident from the supplied data.
    - In the end, give an overall opinion based on what you described about whether the car is worth buying or not.

    Return the output in markdown format.
    Input:
    {content}
    '''

    response = ai_bot.generate_content(prompt)
    return(response.text)


def get_segment(model_name):

    path_seg0 = os.path.join(BASE_DIR, 'seg0.csv')
    path_seg1 = os.path.join(BASE_DIR, 'seg1.csv')
    path_seg2 = os.path.join(BASE_DIR, 'seg2.csv')
    path_seg3 = os.path.join(BASE_DIR, 'seg3.csv')

    seg0 = pd.read_csv(path_seg0)                                      
    seg1 = pd.read_csv(path_seg1)                                      
    seg2 = pd.read_csv(path_seg2)                                      
    seg3 = pd.read_csv(path_seg3)                                      
    seg_count = {}
    for seg, i in zip([seg0,seg1,seg2,seg3],range(4)):
        seg_count[i] = seg.loc[seg['model'] == model_name, 'count'].sum()
        
    return(max(seg_count,key=seg_count.get))


def model_popularity(model_name,seg):
    if(seg == 0):
        path_seg0 = os.path.join(BASE_DIR, 'seg0.csv')
        df = pd.read_csv(path_seg0)
    elif(seg == 1):
        path_seg1 = os.path.join(BASE_DIR, 'seg1.csv')
        df = pd.read_csv(path_seg1)
    elif(seg == 2):
        path_seg2 = os.path.join(BASE_DIR, 'seg2.csv')
        df = pd.read_csv(path_seg2)
    elif(seg == 3):
        path_seg3 = os.path.join(BASE_DIR, 'seg3.csv')
        df = pd.read_csv(path_seg3)

    return(df[df['model'] == model_name].index + 1)

def seg_analysis(segment):
        df = pd.read_csv('kmodes.csv')
        seg_grp = df.groupby(['Segment'])
        avg_price = seg_grp['price'].mean().loc[segment]
        avg_km = seg_grp['KM driven'].mean().loc[segment]

        return(round(avg_price,2), round(avg_km,2))



def fetch_similar(model_name):
    # Setup headless Firefox options required for Streamlit Cloud servers
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Firefox(options=options)

    def listing_url(model):
        slug = model.lower().replace(" ", "-")
        return f"https://cardekho.com{slug}+cars+in+delhi-ncr"

    def get_car_data(url_list):
        cardata = []
        for url in url_list:
            try:
                driver.get(url)
                wait = WebDriverWait(driver, 20)
                
                # Extract details safely using explicit waits
                model_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
                price_element = wait.until(EC.presence_of_element_located((By.CLASS_BAR, "price") or (By.XPATH, "//*[contains(@class, 'price')]")))
                
                data = {
                    "url": url,
                    "model": model_element.text,
                    "price": price_element.text
                }
                cardata.append(data)
            except Exception as e:
                # Keep looping even if one specific page fails to scrape
                print(f"Error scraping {url}: {e}")
                continue
        return cardata

    # Execute the scraping sequence
    target_url = listing_url(model_name)
    results = get_car_data([target_url])
    
    # Clean up the browser instance from memory
    driver.quit()
    return results
  
