import streamlit as st
from utils.load_data import load_csv
import pandas as pd

df_merge_data = load_csv('Dataset\merge_data.csv')

# Description page
st.title("Model development process")
st.write('This section presents the model development process. ' \
'It uses the "merge_data" dataset, which combines two datasets: "Cab rides" and "Weather". ' \
'My aim is to predict the fare for each cab type (Uber or Lyft), so I develop separate models for each service. ' \
'The data exhibits nonlinear relationships, so I chose **Gradient Boosting** and **Random Forest**, which are well-suited for modeling complex patterns. ' \
'This process consists of 2 stages: ') 

st.markdown("""
1. **Data preparation** 
2. **Develop models and compare their performance**
 """)



# Stage: Data preparation
st.subheader('Data preparation')
st.write('To predict the fare of each cab type, I decided to use features such as datetime, destination/source, distance, surge multiplier, service category, and weather conditions.' \
'But since some of these features are in datetime or categorical format, I first performed feature engineering steps like parsing datetime into separate components (e.g., hour, day, month) and encoding categorical variables. ')
st.markdown("""
- **Date parsing**: To better capture temporal patterns, I decomposed the date and time columns. The date column was split into day, month, and year, while the time column was parsed into hour and minute components.
""")
st.image('static\image\date_parsing.jpg', caption='Date parsing', use_container_width=False)
df_merge_data['date'] = pd.to_datetime(df_merge_data['date'], errors='coerce')
df_merge_data['time'] = pd.to_datetime(df_merge_data['time'], errors='coerce')

df_merge_data = df_merge_data.sort_values(['date', 'time'])

df_merge_data['day'] = df_merge_data['date'].dt.day
df_merge_data['month'] = df_merge_data['date'].dt.month
df_merge_data['year'] = df_merge_data['date'].dt.year

df_merge_data['hour'] = df_merge_data['time'].dt.hour
df_merge_data['minute'] = df_merge_data['time'].dt.minute


# Encoding categorical features
st.markdown("""
- **Encoding categorical features**: Categorical features like destination, source, and category are encoded using **Target Mean Encoding**, where each category is replaced with the average ride price (price) corresponding to that category.
This preserves the relationship between categorical features and the target variable while converting them into numerical form.    
""")
df_merge_data['destination_encoded'] = df_merge_data.groupby('destination')['price'].transform("mean")
df_merge_data['source_encoded'] = df_merge_data.groupby('source')['price'].transform("mean")
df_merge_data['category_encoded'] = df_merge_data.groupby('category')['price'].transform("mean")

col1, col2, col3 = st.columns(3)
with col1:
    st.dataframe(df_merge_data[['destination', 'destination_encoded']].drop_duplicates())

with col2:
    st.dataframe(df_merge_data[['source', 'source_encoded']].drop_duplicates())

with col3:
    st.dataframe(df_merge_data[['category', 'category_encoded']].drop_duplicates())


# Define X and y feature
st.markdown("""
- **Feature selection**: The input features `X` include time components (day, month, year, hour, minute), ride characteristics (distance, surge multiplier), encoded categorical variables, and weather conditions. The target variable `y` is the ride price.
""")
col4, col5 = st.columns([4, 1])
with col4:
    st.dataframe(df_merge_data[['day', 'month', 'year', 
                                'surge_multiplier', 'distance', 
                                'destination_encoded', 'source_encoded', 'category_encoded',
                                'temp', 'clouds', 'pressure', 'rain', 'humidity', 'wind']])

with col5:
    st.dataframe(df_merge_data['price'])


# Train/ test split
st.markdown("""
- **Train/ test split**: This is the process of dividing the dataset into two parts:
    - **Training set:** 80% of the data (approximately 263.312 records) is used to allow the model to learn the relationships between variables.
    - **Testing set**: 20% of the data (approximatelt 65.828 records) is used to evaluate the model’s predictive performance on unseen data.
    The split is performed randomly and made reproducible using random_state = 42.
""")




# Stage: Develop models and compare their performance
st.subheader('Develop models and compare their performance')
st.markdown("""
- **Model development and performance evaluation**:
    In this stage, I applied ensemble tree-based models including **Random Forest** and **Gradient Boosting**.
    Key hyperparameters such as the number of trees (`n_estimators`), maximum tree depth (`max_depth`),... were configured to optimize model performance.
    The effectiveness of each model was then evaluated using various regression metrics:  
    - **R-squared (R²)**: Measures how well the model explains the variance in the data.  
    - **Mean Squared Error (MSE)**: Captures the average squared difference between predicted and actual values.  
    - **Root Mean Squared Error (RMSE)**: Provides error in the same units as the target variable.  
    - **Mean Absolute Error (MAE)**: Indicates the average absolute difference between predicted and actual values.  
    This comparison helps determine which model performs best in predicting ride fares.
""")

st.markdown("""
- **Gradient Boosting and Random Forest model**
""")
col6, col7 = st.columns(2)
with col6: 
    st.image('static\image\Gradient_Boosting.png', caption='Gradient Boosting', use_container_width=True)
with col7:
    st.image('static\image\Random_forest.png', caption='Random Forest', use_container_width=True)




st.markdown("""
- **Parameters in each model**
""")
st.markdown("""
| Parameter           | Random Forest                                  | Gradient Boosting                                         |
|--------------------|-------------------------------------------------|-----------------------------------------------------------|
| `n_estimators`      | 500 (Number of trees in the forest)            | 500 (Number of sequential boosting trees)                 |
| `max_depth`         | 15 (Maximum depth of each tree)                | 15 (Maximum depth of each tree)                           |
| `min_samples_split` | 5 (Minimum samples required to split a node)   | 5 (Minimum samples required to split a node)              |
| `learning_rate`     | *(Not used)*                                   | 0.01 (Learning rate – smaller values require more trees)  |
| `loss`              | *(Not used)*                                   | `'squared_error'` (Loss function – standard regression)   |

            """)
