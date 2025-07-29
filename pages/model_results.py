import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from utils.load_data import load_csv


model_results = {
    'Uber': {
        'Gradient_Boosting': {
            'R2': 0.9458,
            'MSE': 3.9725,
            'RMSE': 1.9931,
            'MAE': 1.2047,
            'Training time': 922.79,
            'Model_pkl': 'Model/model_pkl/gradient_boosting_model.pkl',
            'Model_result_csv': 'Model/model_result_csv/GB_Uber.csv'
        },
        'Random_Forest': {
            'R2': 0.9506,
            'MSE': 3.6149,
            'RMSE': 1.9013,
            'MAE': 1.16443,
            'Training time': 609.78,
            'Model_pkl': 'Model/model_pkl/random_forest_model_uber.pkl',
            'Model_result_csv': 'Model/model_result_csv/RF_Uber.csv'
        }
    },
    'Lyft': {
        'Gradient_Boosting': {
            'R2': 0.9799,
            'MSE': 2.0328,
            'RMSE': 1.42576,
            'MAE': 0.9688,
            'Training time': 923.85,
            'Model_pkl': 'Model/model_pkl/gradient_boosting_model_lyft.pkl',
            'Model_result_csv': 'Model/model_result_csv/GB_Lyft.csv'
        },
        'Random_Forest': {
            'R2': 0.9814,
            'MSE': 1.8822,
            'RMSE': 1.37193,
            'MAE': 0.9467,
            'Training time': 584.84,
            'Model_pkl': 'Model/model_pkl/random_forest_model_lyft.pkl',
            'Model_result_csv': 'Model/model_result_csv/RF_Lyft.csv'
        }
    }
}

# Description page
st.title("Model performance results")
st.write('This section performs the performance comparision between Gradient Boosting model and Random Forest model.')


color_map = {
    'Uber': '#011f4b',
    'Lyft': '#ff00bf'
}



st.subheader('Model performance results for each cab type')
st.session_state.cab_type = st.selectbox(
        "Choose cab type:",
        ['Uber', 'Lyft']
    )

# Model results dataframe
result_option_dict = model_results[st.session_state.cab_type]
df_model_result = pd.DataFrame.from_dict(result_option_dict, orient='index').reset_index()
df_model_result.rename(columns={'index': 'Model'}, inplace=True)
st.dataframe(df_model_result[['Model', 'R2', 'MSE', 'RMSE', 'MAE', 'Training time']])


col1, col2, col3 = st.columns(3)

with col1:
    fig_r2 = px.bar(
        df_model_result,
        x='Model',
        y='R2',
        color_discrete_sequence=['#1f77b4'],
        title=f"R² Score of 2 models - {st.session_state.cab_type}"
    )
    fig_r2.update_layout(yaxis_title="R² Score", xaxis_title="Model")
    fig_r2.update_traces(text=df_model_result['R2'].round(4), textposition='outside', width=0.2)
    st.plotly_chart(fig_r2, use_container_width=True)

with col2:
    df_metrics_long = df_model_result.melt(
        id_vars='Model',
        value_vars=['MAE', 'MSE', 'RMSE'],
        var_name='Metric',
        value_name='Value'
    )
    fig_all_metrics = px.bar(
    df_metrics_long,
        x='Model',
        y='Value',
        color='Metric',
        barmode='group',  # Đặt kiểu cột nhóm cạnh nhau
        title=f"Evaluation metrics of models - {st.session_state.cab_type}",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_all_metrics.update_layout(yaxis_title="Metric Value", xaxis_title="Model")
    fig_all_metrics.update_traces(text=df_metrics_long['Value'].round(3), textposition='outside', width=0.2)
    st.plotly_chart(fig_all_metrics, use_container_width=True)

with col3:
    fig_time = px.bar(
        df_model_result,
        x='Model',
        y='Training time',
        title=f"Training time of 2 models - {st.session_state.cab_type}",
        color_discrete_sequence=['#6a51a3']
    )
    fig_time.update_layout(yaxis_title="Second (s)", xaxis_title="Model")
    fig_time.update_traces(text=df_model_result['Training time'].round(4), textposition='outside', width=0.2)
    st.plotly_chart(fig_time, use_container_width=True)


st.subheader('Compare actual and predicted values')
col4, col5 = st.columns(2)
with col4:
    df_compare_GB = load_csv(f'Model/model_result_csv/GB_{st.session_state.cab_type}.csv')
    df_subset = df_compare_GB.head(150)
    fig_compare_GB = go.Figure()
    fig_compare_GB.add_trace(go.Scatter(
        y=df_subset['Actual'],
        mode='lines',
        name='Actual',
        line=dict(color='#1f77b4'),
        marker=dict(size=4)
    ))

    fig_compare_GB.add_trace(go.Scatter(
        y=df_subset['Predicted'],
        mode='lines',
        name='Predicted',
        line=dict(color='#ff7f0e'),
        marker=dict(size=4)
    ))

    fig_compare_GB.update_layout(
        title=f"Actual vs Predicted Price - Gradient Boosting - {st.session_state.cab_type}",
        xaxis_title="Sample Index (150 samples)",
        yaxis_title="Price (USD)",
        legend=dict(x=0, y=1),
        height=400,
        margin=dict(t=50, b=50),
    )

    st.plotly_chart(fig_compare_GB, use_container_width=True)


with col5:
    df_compare_RF = load_csv(f'Model/model_result_csv/RF_{st.session_state.cab_type}.csv')
    df_subset = df_compare_RF.head(150)
    fig_compare_RF = go.Figure()
    fig_compare_RF.add_trace(go.Scatter(
        y=df_subset['Actual'],
        mode='lines',
        name='Actual',
        line=dict(color='#1f77b4'),
        marker=dict(size=4)
    ))

    fig_compare_RF.add_trace(go.Scatter(
        y=df_subset['Predicted'],
        mode='lines',
        name='Predicted',
        line=dict(color='#ff7f0e'),
        marker=dict(size=4)
    ))

    fig_compare_RF.update_layout(
        title=f"Actual vs Predicted Price - Random Forest - {st.session_state.cab_type}",
        xaxis_title="Sample Index (150 samples)",
        yaxis_title="Price (USD)",
        legend=dict(x=0, y=1),
        height=400,
        margin=dict(t=50, b=50),
    )

    st.plotly_chart(fig_compare_RF, use_container_width=True)




