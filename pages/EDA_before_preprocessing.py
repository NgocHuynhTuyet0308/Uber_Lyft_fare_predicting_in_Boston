import streamlit as st
from utils.load_data import load_csv
import pandas as pd
import plotly.express as px


RAW_CAB_RIDE = 'Dataset/cab_rides.csv'
RAW_WEATHER = 'Dataset/weather.csv'

df_cabride = load_csv(RAW_CAB_RIDE)
df_weather = load_csv(RAW_WEATHER)

def check_missing_values(df):
    missing_values_series = df.isnull().sum()
    total = len(df)
    missing_df = pd.DataFrame({
        'Missing count': missing_values_series,
        'Missing %': (missing_values_series / total * 100).round(2)
    })
    return missing_df

def check_duplicated_rows(df, name):
    duplicated_rows = df.duplicated().sum()
    total = len(df)
    duplicated_df = pd.DataFrame([{
        'Dataset': name,
        'Duplicated count': duplicated_rows,
        'Duplicated %': round((duplicated_rows / total * 100), 2)
    }])
    return duplicated_df




# Description page
st.title('Exploratory Data Analysis (EDA) – Before Preprocessing')
st.write('This section performs an EDA on the raw datasets before applying any preprocessing or cleaning steps. ' \
'The main purpose of this page is to understand the initial structure of the data and define cleaning steps.')

# Check missing values
st.subheader('Check missing values')
st.write('The missing values in "Cab ride" dataset: ')
st.write(check_missing_values(df_cabride))

st.write('The missing values in "Weather" dataset: ')
st.write(check_missing_values(df_weather))

st.write('**In the "Cab Ride" dataset**, most of the missing values in the price column are associated with rides using traditional taxis (Taxi type). ' \
'Since these fares are metered and not quoted upfront in the app, their prices are unavailable. ' \
'As these records account for nearly 8% of the entire dataset, I decided to remove them completely to ensure data consistency.')
st.write('**In the "Weather" dataset**, most of the missing values in the rain column indicate that here was no rainfall. ' \
'Since the amount of missing data is relatively large and cannot be removed without significant data loss, ' \
'I chose to fill these missing values with 0.')

# Check duplicated values
st.subheader('Check duplicated rows')
cab_ride_dup = check_duplicated_rows(df_cabride, 'Cab ride')
weather_dup = check_duplicated_rows(df_weather, 'Weather')
merged_df = pd.concat([cab_ride_dup, weather_dup], ignore_index=True)
st.dataframe(merged_df)
st.write('Both datasets do not have duplicated rows.')

# Describe data
st.subheader('Statistical summary of raw data')
st.write('Dataset "Cab ride" with continous data: ')
st.dataframe(df_cabride.describe())

st.write('Dataset "Weather": ')
st.dataframe(df_weather.describe())

# Problem in Weather dataset
st.subheader('Problem in "Weather" dataset')
st.write("According to the dataset author's description, the Weather dataset was collected at each locations every 1 hour. " \
"Instead of having only one record per hour at each station, the dataset contains multiple records within the same hour for a given station.")
st.write('Example of location Back Bay on 26/11/2018 4h')
df_weather['datetime'] = pd.to_datetime(df_weather['time_stamp'], unit='s')
df_weather['date_hour'] = pd.to_datetime(df_weather['datetime']).dt.floor('H')
st.dataframe(df_weather[
    (df_weather['location'] == 'Back Bay')
    & (df_weather['date_hour'] == '2018-11-26 04:00:00')
    ])

# Distribute of numerical features
st.subheader('Distribute of numerical features')
features = ['distance', 'price', 'surge_multiplier',
            'temp', 'clouds', 'pressure', 'rain', 'humidity', 'wind']
option = st.selectbox("Choose features", features)
if option in ['distance', 'price', 'surge_multiplier']:
    data = df_cabride[option]
    fig = px.histogram(data, x=option, nbins=1000, color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig)
else:
    data = df_weather[option]
    fig = px.histogram(data, x=option, nbins=1000, color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig)
