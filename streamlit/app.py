import streamlit as st

# Sidebar
st.sidebar.header('Car Details')
user_input = {}
user_input['brand'] = st.sidebar.text_input(label="Brand", value="", placeholder="Honda") # dropdown
user_input['model'] = st.sidebar.text_input(label="Brand", value="", placeholder="City") # dropdown
user_input['Fuel'] = st.sidebar.text_input(label="Fuel Type",value="",placeholder="Petrol") # dropdown
user_input['Transmission'] = st.sidebar.text_input(label="Transmission Type", value="", placeholder="Automatic") # dropdown
user_input['KM driven'] = st.sidebar.text_input(label="Distance Driven (in KM)", value="", placeholder="50000")
user_input['Engine Capacity'] = st.sidebar.text_input(label="Engine Capacity (in cc)", value="", placeholder="1200")
user_input['Ownership'] = st.sidebar.number_input(label="Ownership",min_value=1, max_value=10,placeholder="2") 
user_input['asking_price'] = st.sidebar.text_input(label="Asking Price (in INR)", value="", placeholder="450000")

st.sidebar.text("\n")
if st.sidebar.button("Analyse Car", type='primary'):
    st.text("Hullo")


# Main section :

st.title('Honda City 2018')

pred_val, score, market_pos, ngt_left = st.columns(4)

with pred_val:
    st.metric(label='Predicted Market Value', value='72,000')

with score:
    st.metric(label='Smart Buy Score', value='72/100')

with market_pos:
    st.metric(label="Market Position", value=-8.5, delta_color='inverse', delta='Below Market Value')