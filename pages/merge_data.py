import pandas as pd

if __name__ == "__main__":
    df_cabride = pd.read_csv('Dataset\cab_ride_preprocessed.csv')
    df_cabride['time'] = pd.to_datetime(df_cabride['time'], errors='coerce')
    df_cabride['date_hour'] =df_cabride['date'].astype(str) + ' ' + df_cabride['time'].dt.hour.astype(str)
    print(df_cabride)

    df_weather = pd.read_csv('Dataset\weather_preprocessed.csv')
    # df_weather['time'] = pd.to_datetime(df_weather['time'], errors='coerce')

    # df_weather['date_hour'] = df_weather['date'].astype(str) + ' ' + df_weather['time'].dt.hour.astype(str)
    # df_weather_hourly = df_weather.groupby(['date_hour', 'location']).agg({
    #     'temp': 'mean',
    #     'clouds': 'mean',
    #     'pressure': 'mean',
    #     'rain': 'mean',
    #     'humidity': 'mean',
    #     'wind': 'mean',
    # }).reset_index()

    df_merge = pd.merge(df_cabride, df_weather, left_on=['source', 'date_hour'], right_on=['location', 'date_hour'])
    
    df_merge.to_csv('merge_data.csv', index=False)
    

    




    

   
