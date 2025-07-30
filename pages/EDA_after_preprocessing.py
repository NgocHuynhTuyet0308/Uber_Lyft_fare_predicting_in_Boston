import streamlit as st
from utils.load_data import load_csv
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


df_cab_rides_preprocessed = load_csv('Dataset/cab_ride_preprocessed.csv')
df_weather_preprocessed = load_csv('Dataset/weather_preprocessed.csv')
df_cabride = load_csv('Dataset/cab_rides.csv')
df_weather = load_csv('Dataset/weather.csv')

def check_missing_values(df):
    missing_values_series = df.isnull().sum()
    total = len(df)
    missing_df = pd.DataFrame({
        'Missing count': missing_values_series,
        'Missing %': (missing_values_series / total * 100).round(2)
    })
    return missing_df

def check_outlier_IQR(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_lower_bound, outliers_upper_bound = 0, 0
    for value in data:
        if value < lower_bound:
            outliers_lower_bound += 1 
        elif value > upper_bound:
            outliers_upper_bound += 1

    return outliers_lower_bound, outliers_upper_bound


# Description page
st.title('Exploratory Data Analysis (EDA) – After Preprocessing')
st.write('This section performs the data preprocessing steps before conducting any analysis or modeling:')
st.markdown("""
1. **Remove missing or invalid values:**  Ensure data integrity by eliminating records with missing or incorrect entries to avoid bias in subsequent analyses.

2. **Fill missing values in the 'rain' column with 0:**
    Due to a large number of missing values in the 'rain' column, I decided to fill them with 0, representing no rain during that hour.
      
3. **Convert timestamp to datetime format:**
    To analyze data easily, i will convert timestamp to datetime format. 
    Note: The "timestamp" column in "Cab rides" dataset is in milliseconds, while in the "Weather" dataset it is in seconds.
            
4. **Segment the cab types:**
    I will categorize these cab types into 6 distinct segments:  Standard, Shared Ride, Large Vehicle, Luxury (Black Car), Luxury SUV and Other.
            
5. **Calculate mean values in the "Weather" dataset at each location per hour**
    
6. **Create "Merge_data" dataset**: Each record in the "Cab ride" dataset will be merged with the corresponding record from the weather dataset based on location and time (date and hour).
              
**Note:** The code for these processing steps is available on [GitHub](https://github.com/NgocHuynhTuyet0308/Uber_Lyft_fare_predicting_in_Boston/blob/main/notebooks/Data_preprocessing.ipynb).
""")

# Check missing values
st.subheader('Check missing values after preprocessing')
st.write('The missing values in "Cab ride" dataset after preprocessing:')
st.dataframe(check_missing_values(df_cab_rides_preprocessed))
st.write('The missing values in "Weather" dataset after preprocessing:')
st.dataframe(check_missing_values(df_weather_preprocessed))


# Remain data (Trình bày số lượng dòng, cột, thêm cột nào thì ghi rõ)
st.subheader('Remaining data after preprocessing')
st.write('The columns of these datasets added to are "datetime", "date" and "time", while the "Cab rides" dataset additionally includes "category".')
remain_data = dict()

# Cab rides
raw_cab = len(df_cabride)
preprocessed_cab = len(df_cab_rides_preprocessed)
removed_cab = raw_cab - preprocessed_cab
removed_cab_pct = round(removed_cab / raw_cab * 100, 1)
cols_cab = len(df_cab_rides_preprocessed.columns)

remain_data['Cab rides'] = {
    'Raw': raw_cab,
    'Preprocessed': preprocessed_cab,
    'Removed': removed_cab,
    'Removed (%)': removed_cab_pct,
    'Columns': cols_cab
}

# Weather
raw_weather = len(df_weather)
preprocessed_weather = len(df_weather_preprocessed)
removed_weather = raw_weather - preprocessed_weather
removed_weather_pct = round(removed_weather / raw_weather * 100, 1)
cols_weather = len(df_weather_preprocessed.columns)

remain_data['Weather'] = {
    'Raw': raw_weather,
    'Preprocessed': preprocessed_weather,
    'Removed': removed_weather,
    'Removed (%)': removed_weather_pct,
    'Columns': cols_weather
}

st.dataframe(remain_data)


# Number of days 
st.subheader('Number of days after preprocessing')
st.write('These datasets after processing starts from 26/11/2018 to 18/12/2018, including 17 days.')
st.markdown("""
        - **November 2018:** 26, 27, 28, 29, 30.
        - **December 2018:** 1, 2, 3, 4, 9, 10, 13, 14, 15, 16, 17, 18.
        """)


# Describe data
st.subheader('Statistical summary of preprocessed data')
st.write('Dataset "Cab rides" with continous data: ')
st.dataframe(df_cab_rides_preprocessed.describe())
st.write('Dataset "Weather" with continous data: ')
st.dataframe(df_weather_preprocessed.describe())

# Outlier data
st.subheader('Outliers in preprocessed data')
features = ['distance', 'price', 'surge_multiplier',
            'temp', 'clouds', 'pressure', 'rain', 'humidity', 'wind']
option = st.selectbox("Choose features", features)

if option in ['distance', 'price', 'surge_multiplier']:
    data = df_cab_rides_preprocessed[option]
else:
    data = df_weather_preprocessed[option]
    
outliers_lower_bound, outliers_upper_bound = check_outlier_IQR(data)
st.write(f'Number of upper outliers of column {option}: {outliers_upper_bound}')
st.write(f'Number of lower outliers of column {option}: {outliers_lower_bound}')
fig = px.box(data, x=option, points='outliers', title=f'Boxplot of {option}')
st.plotly_chart(fig)
fig.update_traces(marker_color='#1f77b4')