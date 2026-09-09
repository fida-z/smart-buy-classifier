import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
import os
from app_funcs import ngt_life, run_predict, dep_calc, shap_calc,render_waterfall ,ai_insights, get_segment, model_popularity, seg_analysis, fetch_similar
from styles import STYLES

# import app_funcs
target_dir = os.path.abspath('../notebooks')
sys.path.insert(1,target_dir)
data = pd.read_csv('data.csv')

st.markdown(STYLES, unsafe_allow_html=True)
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

    st.markdown('Please Enter details about your Car')
    st.markdown('## Car Details')

    # getting data for dropdowns : 
    model_list = data['model'].unique()
    fuel_list = data['Fuel'].unique()
    transmission_list = data['Transmission'].unique()

    model = st.selectbox(label="Model", options=model_list) 
    year = st.number_input(label='Make Year', max_value=2026)
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
st.markdown('\n\n')
st.markdown('Expand the Sidebar to Begin.')
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
        st.metric(label="NGT Life Remaining", value = f'{ngt_life(user_details['Fuel'], 2026 - user_details['Year'])} years', delta_color='normal', border=True)


    # SHAP and Market Insights :

    st.divider()

    shap_chart, dep_curve = st.columns(2)
    with shap_chart:
        st.text('Why this Price with SHAP')
        shap_result = shap_calc(user_details)
        fig = render_waterfall(shap_result)
        st.plotly_chart(fig, width='stretch')
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

        seg, seg_pop  = st.columns(2)
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

        
        avg_km, avg_price = st.columns(2)
        price_avg, km_avg  = seg_analysis(segment)

        with avg_km:
            st.metric(label='Average Segment Mileage', value=km_avg, border=True, format='compact')

        with avg_price:
            lakh_avg = (price_avg)/100000
            lakh_avg_str = f'₹{lakh_avg.item():.2f} L'

            st.metric(label='Average Segment Price', value=lakh_avg_str, border=True)

        market_details = {
            'segment' : segment,
            'segment popularity': seg_pop,
            'segment avg km': km_avg,
            'segment avg price': price_avg
        }

    with rec_card:
        st.text('AI Market Analyst Summary')
        inp_arr = [user_details,shap_result,dep_details, market_details]
        with st.spinner("Processing data, please wait..."):
            ai_answer = ai_insights(inp_arr)
        st.markdown(ai_answer)

    st.divider()

    st.title("Similar Active Listings")
    with st.spinner("Loading, please wait..."):
        cardata = fetch_similar(user_details['model'])
    listing_table = pd.DataFrame(cardata)
    # st.dataframe(listing_table, column_config={ "Link": st.column_config.LinkColumn(display_text="View Listing")
    # })