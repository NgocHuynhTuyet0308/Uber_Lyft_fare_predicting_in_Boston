import streamlit as st
from utils.load_data import load_csv
import pydeck as pdk
import pandas as pd

RAW_CAB_RIDE = 'Dataset\cab_rides.csv'
RAW_WEATHER = 'Dataset\weather.csv'

df_cabride = load_csv(RAW_CAB_RIDE)
df_weather = load_csv(RAW_WEATHER)

# Description page
st.title('Project: Uber/ Lyft fare in Boston')

st.subheader('Introduction')
st.write('Unlike traditional public transportation, ' \
'the pricing of ride-hailing services such as Uber and Lyft is highly dynamic and influenced by various contextual factors. ' \
'These services employ surge pricing algorithms that adjust fares in real-time based on fluctuations in demand and supply. ' \
'For instance, ride prices typically increase during peak commuting hours—around 9 AM and 5 PM—when more people are heading to or returning from work. ' \
'Weather conditions also play a critical role; rainy or snowy days often drive up demand, leading to higher fares.')
st.write('This project aims to analyze several factor that influence the price of each ride offered by Uber and Lyft. ' \
'Besides that i will use machine learning model, such as Linear Regression, Gradient Boosting, Random Forest to predict fare of Uber and Lyft.')
col11, col21, col31 = st.columns([1, 2, 1])
with col21:
    st.image("static/image/Uber and Lyft logo.jpg", caption="Uber and Lyft")


# Dataset
st.subheader('Dataset of this project')
st.write('The dataset used in this project was collected from [Kaggle](https://www.kaggle.com/datasets/ravi72munde/uber-lyft-cab-prices). ' \
'According to the dataset author, real-time data was collected by querying the Uber and Lyft APIs at regular intervals, alongside corresponding weather conditions. ' \
'To simulate real-world ride scenarios, the author selected several high-demand locations across Boston (based on a heatmap of popular areas) and built a custom Scala-based application to automatically request fare estimates. These queries were executed every 5 minutes for ride estimates and every hour for weather data, and all responses were stored in Amazon DynamoDB. ' \
'The data spans approximately one week in late November 2018, though due to additional testing during development, there are also entries that extend into early December. The dataset is not strictly time-series based, as the main objective was to gather as much diverse real-time data as possible while minimizing redundancy.')
st.write('This dataset contains 2 CSV files: "Cab ride" (containing ride information) with 693.071 ride records from Uber and Lyft , "Weather" (containing weather data in Boston) with 6276 records.')

# High-demand location
location_data = pd.DataFrame({
    'location': ['North Station', 'Beacon Hill', 'Boston University', 'Northeastern University',
                 'North End', 'Back Bay', 'South Station', 'West End', 'Theatre District',
                 'Fenway', 'Haymarket Square', 'Financial District'],
    'latitude': [42.36630, 42.35779, 42.34889, 42.34000, 42.36500, 42.35149, 42.35261,
                 42.3585, 42.35389, 42.34205, 42.36158, 42.357101],
    'longitude': [-71.06222, -71.0703, -71.10028, -71.08833, -71.05444, -71.08045,
                  -71.05536, -71.0635, -71.06278, -71.10025, -71.05599, -71.055702]
})
layer = pdk.Layer(
    "ScatterplotLayer",
    location_data,
    get_position='[longitude, latitude]',  
    get_radius=150,           
    get_fill_color='[255, 0, 0, 160]',  
    pickable=True  
)
view_state = pdk.ViewState(
    latitude=42.3601,
    longitude=-71.0589,
    zoom=12
)
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Location: {location}"}
))

# Feature description
st.subheader('Feature description')
col1, col2 = st.columns(2)
with col1:
    st.write('In the "Can ride" dataset: ')
    st.markdown("""
        - **ID**: The id of the record.
        - **Product ID**: Uber or Lyft indentifier for cab type.
        - **Name**: Visible type of the cab. eg: Uber Pool, UberXL.
        - **Distance**: Distance betweeb source and destination (Mile).
        - **Cab type**: Uber or Lyft. 
        - **Timestamp**: Epoch time when data was queried.
        - **Destination**: Destination of the ride.
        - **Source**: Source of the ride.
        - **Surge multiplier**: The multiplier by which price was increased, default 1.
        - **Price**: Price estimate for the ride (USD).                     
    """)
with col2:
    st.write('In the "Weather" dataset: ')
    st.markdown("""
        - **Timestamp**: Epoch time when row data was collected.
        - **Location**: The location name.
        - **Temperature**: Air temperature of the location (°F).
        - **Cloud cover**: Cloud cover of the location.
        - **Pressure**: Pressure of the location (mb).
        - **Rain**: Rain for the last hour (inches).
        - **Humidity**: Humidity of the location (%).
        - **Wind**: Wind speed (mph).                   
    """)

# The cab type
st.subheader("Types of cab in the dataset")
st.write("This dataset includes a variety of ride options from Uber and Lyft, categorized as follows:")
st.markdown("""
| **Category**              | **Uber**              | **Lyft**             | **Description**                                                                 |
|--------------------------|------------------------|-----------------------|---------------------------------------------------------------------------------|
| **Standard**             | UberX                  | Lyft                  | Standard ride option.                                                           |
| **Shared Ride**          | UberPool               | Shared                | Ride-sharing option with other passengers.                                     |
| **Large Vehicle**        | UberXL                 | Lyft XL               | Larger vehicles with more seating capacity.                                    |
| **Luxury (Black Car)**   | Black                  | Lux Black             | Luxury black car service.                                                      |
| **Luxury SUV**           | Black SUV              | Lux Black XL          | High-end black SUV with more space.                                            |
| **Premium**              | –                      | Lux                   | Premium ride with high-end vehicles (exclusive to Lyft).                       |
| **Wheelchair Access**    | WAV                    | –                     | Wheelchair Accessible Vehicle (exclusive to Uber).                             |
| **Taxi**                 | Taxi                   | –                     | Traditional taxi rides (offered via Uber platform).                            |
""")

col3, col4 = st.columns(2)
with col3:
    st.image("static/image/uber_ride_services_1.webp", caption="Uber cab type", use_container_width=True)
with col4:
    st.image("static/image/lyft_car_types_2.webp", caption="Lyft cab type", use_container_width=True)


# Date
st.subheader('Number of days of per location')
st.write('The data was collected from late November (26/11/2018) to early December 2018 (18/12/2018), covering 17 non-consecutive days across all stations. Therefore, I will not apply time series analysis for this project. The following days:')
st.markdown("""
        - **November 2018:** 26, 27, 28, 29, 30.
        - **December 2018:** 1, 2, 3, 4, 9, 10, 13, 14, 15, 16, 17, 18.
        """)

# Dataset cab ride
st.subheader('Dataset "Cab ride"')
st.dataframe(df_cabride)

# Dataset weather
st.subheader('Dataset "Weather"')
st.dataframe(df_weather)