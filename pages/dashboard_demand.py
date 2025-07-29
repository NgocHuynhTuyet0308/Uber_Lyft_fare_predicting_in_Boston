import streamlit as st
import pandas as pd
from utils.load_data import load_csv
import plotly.express as px
import plotly.graph_objects as go


df_cab_rides_preprocessed = load_csv('Dataset\cab_ride_preprocessed.csv')
df_weather_preprocessed = load_csv('Dataset\weather_preprocessed.csv')
df_merge_data = load_csv('Dataset\merge_data.csv')

col_metric_1, col_metric_2 = st.columns(2)

with col_metric_1:
    uber_count = len(df_cab_rides_preprocessed[df_cab_rides_preprocessed['cab_type'] == 'Uber'])
    total_count = len(df_cab_rides_preprocessed)
    delta_uber = round((uber_count / total_count) * 100.0, 2)
    st.metric(label="Total number of Uber rides", 
              value=f'{uber_count}\n ({delta_uber}% of total)', 
              border=True)
with col_metric_2:
    lyft_count = len(df_cab_rides_preprocessed[df_cab_rides_preprocessed['cab_type'] == 'Lyft'])
    total_count = len(df_cab_rides_preprocessed)
    delta_lyft = round((lyft_count / total_count) * 100.0, 2)
    st.metric(label="Total number of Lyft rides", 
              value=f'{lyft_count} \n({delta_lyft}% of total)', 
              border=True)


df_cab_rides_preprocessed['datetime'] = pd.to_datetime(df_cab_rides_preprocessed['datetime'], errors='coerce')

color_map = {
    'Uber': '#011f4b',
    'Lyft': '#ff00bf'
}

location_data = pd.DataFrame({
    'location': ['North Station', 'Beacon Hill', 'Boston University', 'Northeastern University',
                 'North End', 'Back Bay', 'South Station', 'West End', 'Theatre District',
                 'Fenway', 'Haymarket Square', 'Financial District'],
    'latitude': [42.36630, 42.35779, 42.34889, 42.34000, 42.36500, 42.35149, 42.35261,
                 42.3585, 42.35389, 42.34205, 42.36158, 42.357101],
    'longitude': [-71.06222, -71.0703, -71.10028, -71.08833, -71.05444, -71.08045,
                  -71.05536, -71.0635, -71.06278, -71.10025, -71.05599, -71.055702]
})

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

distance_bin_order = ['Very Short (0 - 0.5 mile)', 'Short (0.5 - 1.0 mile)', 'Medium (1.0 - 2.0 mile)', 'Long (2.0 - 3.5 mile)', 'Very Long (3.5 - 5.0 mile)', 'Extra Long (5.0+ mile)']
df_cab_rides_preprocessed['distance_bin'] = df_cab_rides_preprocessed['distance'].apply(assign_distance_bin)
df_cab_rides_preprocessed['distance_bin'] = pd.Categorical(
    df_cab_rides_preprocessed['distance_bin'],
    categories=distance_bin_order,
    ordered=True
)


col1, col2, col3 = st.columns(3)
with col1:
    # Using demand on hours in weekday
    df_cab_rides_preprocessed['hour'] = df_cab_rides_preprocessed['datetime'].dt.hour
    df_cab_rides_preprocessed['dayofweek'] = df_cab_rides_preprocessed['datetime'].dt.dayofweek
    df_weekdays = df_cab_rides_preprocessed[~df_cab_rides_preprocessed['dayofweek'].isin([5, 6])]

    demand_on_hour_in_weekday = df_weekdays.groupby(['cab_type', 'hour']).size().reset_index(name='ride_count')

    fig_demand_on_hour_in_weekday = px.line(
        demand_on_hour_in_weekday,
        x='hour',
        y='ride_count',
        color='cab_type',
        color_discrete_map=color_map,
        labels={'hour': 'Hour', 'ride_count': 'Number of rides', 'cab_type': 'Cab type'},
        title=('Ride demand by hour on weekdays')
    )
    fig_demand_on_hour_in_weekday.update_traces(mode='lines+markers')  
    fig_demand_on_hour_in_weekday.update_layout(xaxis=dict(dtick=4)) 
    st.plotly_chart(fig_demand_on_hour_in_weekday, use_container_width=True)



with col2:
    # Using demand on hours in weekend
    df_weekend = df_cab_rides_preprocessed[df_cab_rides_preprocessed['dayofweek'].isin([5, 6])]
    demand_on_hour_in_weekend = df_weekend.groupby(['cab_type', 'hour']).size().reset_index(name='ride_count')

    fig_demand_on_hour_in_weekend = px.line(
        demand_on_hour_in_weekend,
        x='hour',
        y='ride_count',
        color='cab_type',
        color_discrete_map=color_map,
        labels={'hour': 'Hour', 'ride_count': 'Number of rides', 'cab_type': 'Cab type'},
        title=('Ride demand by hour on weekend')
    )
    fig_demand_on_hour_in_weekend.update_traces(mode='lines+markers')  
    fig_demand_on_hour_in_weekend.update_layout(xaxis=dict(dtick=4))
    st.plotly_chart(fig_demand_on_hour_in_weekend, use_container_width=True)

with col3:
    # Using deman on day in week
    demand_on_day_in_week = df_cab_rides_preprocessed.groupby(['cab_type', 'dayofweek']).size().reset_index(name='ride_count')

    fig_demand_on_day_in_week = px.line(
        demand_on_day_in_week,
        x='dayofweek',
        y='ride_count',
        color='cab_type',
        color_discrete_map=color_map,
        labels={'dayofweek': 'Day of week', 'ride_count': 'Number of rides', 'cab_type': 'Cab type'},
        title=('Ride demand by day on week')
    )
    fig_demand_on_day_in_week.update_traces(mode='lines+markers')  
    fig_demand_on_day_in_week.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )) 
    st.plotly_chart(fig_demand_on_day_in_week, use_container_width=True)


col4, col5 = st.columns(2)
with col4:
    # Using demand on source/ destination
    demand_on_source = df_cab_rides_preprocessed.groupby(['cab_type', 'source']).size().reset_index(name='ride_count')
    source_order = demand_on_source.groupby('source')['ride_count'].sum().sort_values(ascending=True).index.tolist()
    fig_demand_on_source = go.Figure()

    for cab in demand_on_source['cab_type'].unique():
        filtered = demand_on_source[demand_on_source['cab_type'] == cab]
        fig_demand_on_source.add_trace(go.Bar(
            y=filtered['source'],  # y là tên địa điểm
            x=filtered['ride_count'],  # x là số lượt
            name=cab,
            orientation='h',  # thanh ngang
            marker=dict(color=color_map.get(cab, '#999999'))
        ))

    fig_demand_on_source.update_layout(
        barmode='group',
        yaxis=dict(
            title='Source/Destination',
            categoryorder='array',
            categoryarray=source_order
        ),
        xaxis_title='Number of rides',
        title='Ride demand by source/ destination',
        legend_title='Cab type',
    )

    st.plotly_chart(fig_demand_on_source, use_container_width=True)
    
with col5:
    # Using demand by service category
    demand_on_category = df_cab_rides_preprocessed.groupby(['cab_type', 'category']).size().reset_index(name='ride_count')
    category_order = demand_on_category.groupby('category')['ride_count'].sum().sort_values(ascending=True).index.tolist()
    fig_demand_on_category = go.Figure()
    for cab in demand_on_source['cab_type'].unique():
        filtered = demand_on_category[demand_on_category['cab_type'] == cab]
        fig_demand_on_category.add_trace(go.Bar(
            y=filtered['category'],  
            x=filtered['ride_count'],  
            name=cab,
            orientation='h',  # thanh ngang
            marker=dict(color=color_map.get(cab, '#999999'))
        ))

    fig_demand_on_category.update_layout(
        barmode='group',
        yaxis=dict(
            title='Service category',
            categoryorder='array',
            categoryarray=category_order
        ),
        xaxis_title='Number of rides',
        title='Ride demand by service category',
        legend_title='Cab type',
    )

    st.plotly_chart(fig_demand_on_category, use_container_width=True)



# Using deman on distance category
fig_demand_on_distance_category = px.histogram(
    df_cab_rides_preprocessed,
    x='distance',
    color='cab_type',
    nbins=100, 
    color_discrete_map=color_map,
    labels={
        'distance': 'Trip distance (mile)',
        'count': 'Number of rides',
        'cab_type': 'Cab type'
    },
    title='Ride demand distribution by trip distance'
)
st.plotly_chart(fig_demand_on_distance_category, use_container_width=True)


col6, col7, col8 = st.columns(3)
with col6:
    df_merge_data['temp_rounded'] = df_merge_data['temp'].round(0)
    demand_on_temp = df_merge_data.groupby(['cab_type', 'temp_rounded']).size().reset_index(name='ride_count')
    fig_temp = px.line(demand_on_temp, x='temp_rounded', y='ride_count',
                        title='Impact of temperature on ride demand',
                        color='cab_type',
                        color_discrete_map=color_map,
                        labels={'cab_type':'Cab type', 'temp_rounded': 'Temperature (℉)', 'ride_count': 'Number of rides'})
    st.plotly_chart(fig_temp, use_container_width=True)

with col7:
    df_merge_data['cloud_rounded'] = df_merge_data['clouds'].round(1)
    demand_on_cloud = df_merge_data.groupby(['cab_type', 'cloud_rounded']).size().reset_index(name='ride_count')
    fig_cloud = px.line(demand_on_cloud, x='cloud_rounded', y='ride_count',
                        title='Impact of cloud on ride demand',
                        color='cab_type',
                        color_discrete_map=color_map,
                        labels={'cab_type':'Cab type', 'cloud_rounded': 'Cloud', 'ride_count': 'Number of rides'})
    st.plotly_chart(fig_cloud, use_container_width=True)

with col8:
    df_merge_data['wind_rounded'] = df_merge_data['wind'].round(0)
    demand_on_wind = df_merge_data.groupby(['cab_type', 'wind_rounded']).size().reset_index(name='ride_count')
    fig_wind = px.line(demand_on_wind, x='wind_rounded', y='ride_count',
                        title='Impact of wind on ride demand',
                        color='cab_type',
                        color_discrete_map=color_map,
                        labels={'cab_type':'Cab type', 'wind_rounded': 'Wind', 'ride_count': 'Number of rides'})
    st.plotly_chart(fig_wind, use_container_width=True)

