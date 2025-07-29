import streamlit as st

st.set_page_config(layout="wide")

dashboard_price = st.Page('./pages/dashboard_analyst_price.py', title='Price')
dashboard_demand = st.Page('./pages/dashboard_demand.py', title='Demand')

describe_raw_data = st.Page('./pages/describe_raw_data.py', title='About this project')

EDA_before_preprocessing = st.Page('./pages/EDA_before_preprocessing.py', title='EDA before preprocessing')
EDA_after_preprocessing = st.Page('./pages/EDA_after_preprocessing.py', title='EDA after preprocessing')

build_model_process = st.Page('./pages/build_model_process.py', title='Build model process')
model_results = st.Page('./pages/model_results.py', title='Model results')

pages = {
    'About': [describe_raw_data],
    'Dashboard': [dashboard_demand, dashboard_price],
    'EDA': [EDA_before_preprocessing, EDA_after_preprocessing],
    'Model results': [build_model_process, model_results]
}

pg = st.navigation(pages)

pg.run()


