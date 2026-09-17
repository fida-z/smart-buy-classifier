import streamlit as st
from pathlib import Path
import pandas as pd
from schema import submit_car
from run_model import predict_price
from feature_eng import calc_ngt_life
from shap_self import shap_calculator
from depreciation import depreciation_calculator
from charts import render_waterfall, render_depcurve
from find_cluster import get_segment, model_popularity, segment_analysis
from gemini import get_gemini_stream, def_gemini
from listing_scraper import fetch_similar
from styles import STYLES

SEGPATH = Path(__file__).resolve().parent.parent/'data_models'
st.markdown(STYLES, unsafe_allow_html=True)
@st.cache_data
def load_dataset():
    return(pd.read_csv(SEGPATH/'data.csv'))


# SIDEBAR

with st.sidebar.form(key="car_details", clear_on_submit=False):

    st.markdown('Please Enter details about your Car')
    st.markdown('## Car Details')

    # getting data for dropdowns : 
    data = load_dataset()
    model_list = data['model'].unique()
    fuel_list = ['Petrol', 'Diesel', 'CNG', 'Electric', 'LPG', 'Hybrid']
    transmission_list = ['Automatic', 'Manual']

    model = st.selectbox(label="Model", options=model_list) 
    year = st.number_input(label='Make Year', min_value=2000, max_value=2026)
    fuel = st.selectbox(label="Fuel Type",options=fuel_list) 
    transmission = st.selectbox(label="Transmission Type", options=transmission_list) 
    km_driven = st.text_input(label="Distance Driven (in KM)", value="", placeholder="50000")
    engine_capacity = st.text_input(label="Engine Capacity (in cc)", value="", placeholder="1200")
    ownership = st.number_input(label="Ownership",min_value=1, max_value=10,placeholder=2) 
    asking_price = st.text_input(label="Asking Price (in INR)", value="", placeholder="450000")
    
    submitted = st.form_submit_button(label="Analyse Car")

if submitted:
    try:
        st.session_state['user_details'] = submit_car(model, year, fuel, transmission, km_driven, engine_capacity, ownership, asking_price)
    except Exception as e:
        st.error(str(e))


# DASHBOARD :
st.markdown('\n\n')
if 'user_details' in st.session_state:
    user_details = st.session_state['user_details']
    st.title(f'{user_details.model} {user_details.year}')

    prediction_card, smart_score, market_position, ngt_left = st.columns(4)

    with prediction_card:
        pred_price = predict_price(user_details)
        lakh_num = (pred_price)/100000
        lakh_string = f'₹{lakh_num.item():.2f} L'
        st.metric(label='Predicted Market Value', value=lakh_string, border=True)
    with smart_score:
        st.metric(label='Smart Buy Score', value='72/100', border=True)
    with market_position:
        mark_val = ((user_details.asking_price - pred_price)/pred_price)
        st.metric(label="Market Position", value=mark_val, border=True, format='percent')
    with ngt_left:
        st.metric(label="NGT Life Remaining", value = f'{calc_ngt_life(user_details.fuel, user_details.car_age)} years', delta_color='normal', border=True)


    # SHAP and Market Insights :

    st.divider()

    shap_chart, dep_curve = st.columns(2)

    with shap_chart:
        st.text('Why this Price with SHAP')
        shap_result = shap_calculator(user_details)
        fig = render_waterfall(shap_result)
        st.plotly_chart(fig, width='stretch')

    with dep_curve:
        st.text('Depreciation Curve over Years')
        dep_details = depreciation_calculator(user_details)
        fig = render_depcurve(dep_details)
        st.plotly_chart(fig, width='stretch')


    st.divider()

    # Market summary card and AI Analysis :

    mark_sum , ai_recs = st.columns(2)

    with mark_sum:
        st.text('Market Summary')

        seg, seg_pop  = st.columns(2)
        with seg:
            segment = get_segment(user_details.model)
            if(segment == 1):
                seg_label = 'Established Mid-Market Commuters' 
            elif(segment == 2):
                seg_label = 'Budget & Entry-Level Hatchbacks'
            elif(segment == 3):
                seg_label = 'Large Utility & Premium Cruisers'
            elif(segment == 4):
                seg_label = 'Modern Commuters & Premium Urban'

            st.metric(label='Segment', value=seg_label, border=True)
        with seg_pop:
            pop_val = str(model_popularity(user_details.model,segment).item())
            if pop_val.endswith('1'):
                pop_str = 'st'
            elif pop_val.endswith('2'):
                pop_str = 'nd'
            elif pop_val.endswith('3'):
                pop_str = 'rd'
            else:
                pop_str = 'th'

            st.metric(label='Model Popularity', value=f"{pop_val+pop_str} Top Model in Segment", border=True)

        
        avg_km, avg_price = st.columns(2)
        price_avg, km_avg  = segment_analysis(segment)

        with avg_km:
            st.metric(label='Average Segment Mileage', value=km_avg, border=True, format='compact')
        with avg_price:
            lakh_avg = (price_avg)/100000
            lakh_avg_str = f'₹{lakh_avg.item():.2f} L'

            st.metric(label='Average Segment Price', value=lakh_avg_str, border=True)

        market_details = {
            'segment' : seg_label,
            'segment popularity': seg_pop,
            'segment avg km': km_avg,
            'segment avg price': price_avg
        }

    with ai_recs:
        st.text('AI Market Analyst Summary')
        inp_arr = [user_details,shap_result,dep_details, market_details]
        # prompt,client = def_gemini(inp_arr)

        # with st.spinner("Processing data, please wait..."):
        #     stream = st.write_stream(get_gemini_stream(prompt,client))
    st.divider()

    st.title("Similar Active Listings")
    placeholder = st.empty()
    listings = []
    for listing in fetch_similar(user_details.model):
        listings.append(listing)

        listing_df = pd.DataFrame(listings)

        placeholder.dataframe(listing_df,hide_index=True,width="stretch", 
                              column_config= {"Link": st.column_config.LinkColumn("Listing",display_text="View Listing")})


