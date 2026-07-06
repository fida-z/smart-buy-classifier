import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os
from app_funcs import run_predict, dep_calc, shap_calc, ai_insights, get_segment, model_popularity, listing_no

# import app_funcs
target_dir = os.path.abspath('../notebooks')
sys.path.insert(1,target_dir)
from feature_eng_exports import data, ngt_life


# submit function definition:

def submit_car(model, year, fuel, transmission, km_driven, engine_capacity, ownership, asking_price):
    user_input = {
        'model': model if model else np.nan,
        'Fuel': fuel if fuel else np.nan,
        'Year': year if year else np.nan,
        'Transmission': transmission if transmission else np.nan,
        'KM driven': int(km_driven) if km_driven else np.nan ,
        'Engine capacity': int(engine_capacity) if engine_capacity else np.nan,
        'Ownership': ownership if ownership else np.nan,
        'asking_price': float(asking_price) if asking_price else np.nan
    }
    if np.nan in user_input.values():
        st.sidebar.error('Incomplete Input!')
    
    return(user_input)




# Sidebar

with st.sidebar.form(key="car_details", clear_on_submit=False):

    st.markdown('## Car Details')

    # getting data for dropdowns : 
    model_list = data['model'].unique()
    fuel_list = data['Fuel'].unique()
    transmission_list = data['Transmission'].unique()

    model = st.selectbox(label="Model", options=model_list) 
    year = st.number_input(label='Make Year', min_value=1950, max_value=2026)
    fuel = st.selectbox(label="Fuel Type",options=fuel_list) 
    transmission = st.selectbox(label="Transmission Type", options=transmission_list) 
    km_driven = st.text_input(label="Distance Driven (in KM)", value="", placeholder="50000")
    engine_capacity = st.text_input(label="Engine Capacity (in cc)", value="", placeholder="1200")
    ownership = st.number_input(label="Ownership",min_value=1, max_value=10,placeholder=2) 
    asking_price = st.text_input(label="Asking Price (in INR)", value="", placeholder="450000")
    
    submitted = st.form_submit_button(label="Analyse Car", type='primary')

if submitted:
    st.session_state['user_details'] = submit_car(model, year, fuel, transmission, km_driven, engine_capacity, ownership, asking_price)



# Main section :
if 'user_details' in st.session_state:
    user_details = st.session_state['user_details']
    st.title(f'{user_details['model']} {user_details['Year']}')

    pred_val, score, market_pos, ngt_left = st.columns(4)

    with pred_val:
        pred = run_predict(user_details)
        pred_price = np.expm1(pred)
        lakh_num = (pred_price)/100000
        lakh_string = f'₹{lakh_num.item():.2f} L'
        st.metric(label='Predicted Market Value', value=lakh_string, border=True)
    with score:
        st.metric(label='Smart Buy Score', value='72/100', border=True)
    with market_pos:
        mark_val = ((user_details['asking_price'] - pred_price)/pred_price)
        st.metric(label="Market Position", value=mark_val, border=True, format='percent')
    with ngt_left:
        st.metric(label="NGT Life Remaining", value = ngt_life(user_details['Fuel'], 2026 - user_details['Year']), delta_color='normal', border=True)


    # SHAP and Market Insights :

    st.divider()

    shap_chart, dep_curve = st.columns(2)
    with shap_chart:
        st.text('Why this Price with SHAP')
        shap_vals = shap_calc(user_details)
        st.write(shap_vals)

    with dep_curve:
        st.text('Depreciation Curve over Years')
        dep_details = dep_calc(user_details)
        fig, ax = plt.subplots()
        ax.plot(dep_details.keys(), dep_details.values())
        st.pyplot(fig)

    st.divider()

    # Recommendation card and Depreciation Curve :

    mark_sum , rec_card = st.columns(2)

    with mark_sum:
        st.text('Market Summary')

        seg, seg_pop, avg_km,  = st.columns(3)
        with seg:
            segment = get_segment(user_details['model'])
            if(segment == 0):
                seg_label = 'Established Mid-Market Commuters' 
            elif(segment == 1):
                seg_label = 'Budget & Entry-Level Hatchbacks'
            elif(segment == 2):
                seg_label = 'Large Utility & Premium Cruisers'
            elif(segment == 3):
                seg_label = 'Modern Commuters & Premium Urban'

            st.metric(label='Segment', value=seg_label, border=True)

        with seg_pop:
            pop_val = model_popularity(user_details['model'],segment)
            st.metric(label='Model Popularity', value=pop_val, border=True)

        with avg_km:
            st.metric(label='Segment-wise KM Driven', value='70,000 avg. per year', border=True)
        
        active_listings, avg_price, peer_grp_pct = st.columns(3)

        with active_listings:
            list_no = listing_no(user_details['model'],segment)
            st.metric(label='No. of Active Listings', value=list_no, border=True)
        with avg_price:
            st.metric(label='50', value='#1 in segment', border=True)
        with peer_grp_pct:
            st.metric(label='Peer group percentile', value='#1 in segment', border=True)

    with rec_card:
        st.text('AI Market Analyst Summary')
        inp_arr = [user_details,shap_vals,dep_details]
        # st.markdown(ai_insights(inp_arr))

    st.divider()

    st.title("Similar Active Listings")

    listing_table = pd.DataFrame({
        "Model": [1,2,3,4,5],
        "Year": [1,24,5,6,5],
        'Ownership': [1,2,3,5,5]
    })
    st.table(listing_table)