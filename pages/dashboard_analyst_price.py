import streamlit as st
from utils.load_data import load_csv
import pandas as pd
import plotly.express as px

df_cab_rides_preprocessed = load_csv('Dataset/cab_ride_preprocessed.csv')
df_weather_preprocessed = load_csv('Dataset/weather_preprocessed.csv')
df_merge_data = load_csv('Dataset/merge_data.csv')

color_map_uber = {
    'Shared Ride': '#b3cde3',   
    'Standard': '#6497b1',     
    'Large Vehicle': '#005b96',
    'Luxury': '#084594',       
    'Luxury Suv': '#011f4b'    
}

color_map_lyft = {
    'Shared Ride': '#fce4ec',   
    'Standard':    '#f8bbd0',   
    'Large Vehicle': '#f48fb1', 
    'Luxury':      '#ec407a',   
    'Luxury Suv':  '#880e4f'    
}

type = 'Uber'
color_map = color_map_uber
color = '#011f4b'

def assign_distance_bin(distance):
    if 0 <= distance <= 0.5:
        return 'Very Short (0 - 0.5 mile)'
    elif 0.5 < distance <= 1.0:
        return 'Short (0.5 - 1.0 mile)'
    elif 1.0 < distance <= 2.0:
        return 'Medium (1.0 - 2.0 mile)'
    elif 2.0 < distance <= 3.5:
        return 'Long (2.0 - 3.5 mile)'
    elif 3.5 < distance <= 5.0:
        return 'Very Long (3.5 - 5.0 mile)'
    elif distance > 5.0:
        return 'Extra Long (5.0+ mile)'
    else:
        return 'Unknown'


# Uber and Lyft buttons
uber_button, lyft_button = st.columns(2)
if uber_button.button('Uber', use_container_width=True):
    type = 'Uber'
    color_map = color_map_uber
    color = '#011f4b'
if lyft_button.button('Lyft', use_container_width=True):
    type = 'Lyft'
    color_map = color_map_lyft
    color = '#ff00bf'

df_cab_rides_option = df_cab_rides_preprocessed[df_cab_rides_preprocessed['cab_type'] == type]
df_merge_data_option = df_merge_data[df_merge_data['cab_type'] == type]

df_cab_rides_option['datetime'] = pd.to_datetime(df_cab_rides_option['datetime'], errors='coerce')

df_cab_rides_option['category'] = df_cab_rides_option['category'].str.title()

category_order = ['Shared Ride', 'Standard', 'Large Vehicle', 'Luxury', 'Luxury Suv']
df_cab_rides_option = df_cab_rides_option[
    df_cab_rides_option['category'].isin(category_order)
]
df_cab_rides_option['category'] = pd.Categorical(
    df_cab_rides_option['category'],
    categories=category_order,
    ordered=True
)

distance_bin_order = ['Very Short (0 - 0.5 mile)', 'Short (0.5 - 1.0 mile)', 'Medium (1.0 - 2.0 mile)', 'Long (2.0 - 3.5 mile)', 'Very Long (3.5 - 5.0 mile)', 'Extra Long (5.0+ mile)']
df_cab_rides_option['distance_bin'] = df_cab_rides_option['distance'].apply(assign_distance_bin)
df_cab_rides_option['distance_bin'] = pd.Categorical(
    df_cab_rides_option['distance_bin'],
    categories=distance_bin_order,
    ordered=True
)
    
    
col1, col2 = st.columns(2)
with col1:
    mean_price_distance = df_cab_rides_option.groupby(['distance_bin', 'category'])['price'].mean().reset_index()
    fig_scatter = px.line(
        data_frame=mean_price_distance,
        x='distance_bin',
        y='price',
        color='category',
        color_discrete_map=color_map,
        labels={'category': 'Category', 'price': 'Mean fare (USD)', 'distance_bin': 'Distance category'},
        title=f'Impact of distance on fare - {type}'
    )
    fig_scatter.update_traces(mode='lines+markers')  
    fig_scatter.update_layout(xaxis=dict(dtick=1)) 
    st.plotly_chart(fig_scatter, use_container_width=True) 

    df_merge_data_option['temp_rounded'] = df_merge_data_option['temp'].round(0)
    demand_on_temp = df_merge_data_option.groupby(['temp_rounded'])['price'].mean().reset_index()
    fig_temp = px.line(demand_on_temp, x='temp_rounded', y='price',
                        title=f'Impact of temperature on fare - {type}',
                        labels={'cab_type':'Cab type', 'temp_rounded': 'Temperature (℉)', 'price': 'Mean fare (USD)'})
    fig_temp.update_traces(line=dict(color=color))
    st.plotly_chart(fig_temp, use_container_width=True)



with col2:
    # Standard deviation of ride fares
    df_cab_rides_option['hour'] = df_cab_rides_option['datetime'].dt.hour
    df_cab_rides_option['dayofweek'] = df_cab_rides_option['datetime'].dt.dayofweek
    df_weekdays = df_cab_rides_option[~df_cab_rides_option['dayofweek'].isin([5, 6])]
    mean_fare_groupby_hour_category = df_weekdays.groupby(['category', 'hour'])['price'].std().reset_index()
    fig_std_price_hour = px.line(mean_fare_groupby_hour_category,
                x='hour',
                y='price',
                color='category',
                labels={'hour': 'Hour', 'price': 'Standard deviation of ride fares', 'category': 'Category'},
                title=f'Impact of hour on fare - {type}',
                color_discrete_map=color_map)

    fig_std_price_hour.update_traces(mode='lines+markers')  
    fig_std_price_hour.update_layout(xaxis=dict(dtick=1))  
    st.plotly_chart(fig_std_price_hour, use_container_width=True) 

    # Mean of ride fares by category
    mean_fare_groupby_category = df_cab_rides_option.groupby(['category'])['price'].mean().reset_index()
    mean_fare_groupby_category = mean_fare_groupby_category.sort_values(by='price', ascending=False)
    fig_mean_price_category = px.bar(
        mean_fare_groupby_category,
        x='category',
        y='price',
        color='category',
        color_discrete_map=color_map,
        labels={'category': 'Category', 'price': 'Mean fare (USD)'},
        title=f'Impact of service category on fare - {type}'
    )
    st.plotly_chart(fig_mean_price_category, use_container_width=True) 



        


