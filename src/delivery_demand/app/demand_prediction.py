import streamlit as st

import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the model from the file
model = joblib.load('xgboost_model_class_model_B_new_clusv6.pkl')


# Function to prepare new data for prediction
def prepare_new_data(city, start_year, start_month, start_day, start_hour, start_minute, festival, clusters, hourly_orders_lag1, hourly_orders_lag2, hourly_orders_lag3, hourly_orders_lag4):
    # One-hot encode city
    city_encoded = ohe.transform(pd.DataFrame([[city]], columns=['city_name']))
    city_encoded_df = pd.DataFrame(city_encoded, columns=ohe.get_feature_names_out(['city_name']))

    # Prepare cluster data based on start_hour and end_hour
    cluster_data = np.zeros(len(unique_clusters))
    start_time = datetime(start_year, start_month, start_day, start_hour, start_minute)
    end_time = start_time + timedelta(hours=2)
    for cluster in clusters:
        unique_cluster_id = cluster_mapping.get(cluster)
        if unique_cluster_id is not None:
            column_name = f'cluster_{cluster}.0'
            if column_name in df_cluster_hr_activation_modelB_v6.columns:
                column_position = unique_clusters.index(unique_cluster_id)
                if df_cluster_hr_activation_modelB_v6.loc[
                    (df_cluster_hr_activation_modelB_v6['start_hour'] == start_time.hour) &
                    (df_cluster_hr_activation_modelB_v6['end_hour'] == end_time.hour),
                    column_name].values[0] == 1:
                    cluster_data[column_position] = 1
            else:
                print(f"Warning: Column {column_name} does not exist in df_cluster_hr_activation_modelB_v2")
        else:
            print(f"Warning: Cluster {cluster} does not have a corresponding unique ID in cluster_mapping")

    # Calculate sin and cos transformations for start_hour and end_hour
    start_hour_sin = np.sin(2 * np.pi * start_hour / 24)
    start_hour_cos = np.cos(2 * np.pi * start_hour / 24)
    end_hour_sin = np.sin(2 * np.pi * end_time.hour / 24)
    end_hour_cos = np.cos(2 * np.pi * end_time.hour / 24)

    # Calculate interaction variables
    lag_1_hour_sin_interaction = hourly_orders_lag1 * start_hour_sin
    lag_1_hour_cos_interaction = hourly_orders_lag1 * start_hour_cos
    lag_2_hour_sin_interaction = hourly_orders_lag2 * start_hour_sin
    lag_2_hour_cos_interaction = hourly_orders_lag2 * start_hour_cos
    lag_3_hour_sin_interaction = hourly_orders_lag3 * start_hour_sin
    lag_3_hour_cos_interaction = hourly_orders_lag3 * start_hour_cos
    lag_4_hour_sin_interaction = hourly_orders_lag4 * start_hour_sin
    lag_4_hour_cos_interaction = hourly_orders_lag4 * start_hour_cos

    # Calculate zero_orders
    zero_orders_row = zero_orders_data[
        (zero_orders_data['city_name'] == city) &
        (zero_orders_data['start_hour'] == start_hour) &
        (zero_orders_data['end_hour'] == end_time.hour)
    ]
    zero_orders = 0 if len(zero_orders_row) > 0 and zero_orders_row['zero_orders'].values[0] > 0 else 1

    # Combine all features
    new_data = np.concatenate([
        cluster_data,
        [festival, hourly_orders_lag1, hourly_orders_lag2, hourly_orders_lag3, hourly_orders_lag4],
        city_encoded_df.values.flatten(),
        [start_year, start_month, start_day, start_hour, start_minute, end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute],
        [start_hour_sin, start_hour_cos, end_hour_sin, end_hour_cos, lag_1_hour_sin_interaction, lag_1_hour_cos_interaction, lag_2_hour_sin_interaction, lag_2_hour_cos_interaction, lag_3_hour_sin_interaction, lag_3_hour_cos_interaction, lag_4_hour_sin_interaction, lag_4_hour_cos_interaction, zero_orders]
    ])


    # Create a DataFrame with model's feature names
    new_data_df = pd.DataFrame([new_data], columns=model_feature_names)

    # Align the new data with the model's expected features
    aligned_new_data_df = new_data_df[model_feature_names]

    return aligned_new_data_df

def predict_for_periods(model, city, end_year, end_month, end_day, end_hour, end_minute, festival, clusters, initial_lag_values):
    start_time = datetime(2022, 4, 7, 0, 0)  # Start time as per the requirement
    end_time = datetime(end_year, end_month, end_day, end_hour, end_minute)  # User-input end time

    # Initial lag values (encoded as integers)
    lag_values = [category_mapping[val] for val in initial_lag_values]

    # Loop to predict from start_time to end_time
    predictions = []
    time_stamps = []
    while start_time <= end_time:
        if len(predictions) < 1:
            # Use initial lag values for the first prediction
            hourly_orders_lag1 = lag_values[0]
            hourly_orders_lag2 = lag_values[1]
            hourly_orders_lag3 = lag_values[2]
            hourly_orders_lag4 = lag_values[3]
        elif len(predictions) < 2:
            # Update lag values based on previous predictions
            hourly_orders_lag1 = predictions[-1]
            hourly_orders_lag4 = lag_values[3 - len(predictions)]
            hourly_orders_lag3 = lag_values[2 - len(predictions)]
            hourly_orders_lag2 = lag_values[1 - len(predictions)]
        elif len(predictions) < 3:
            hourly_orders_lag1 = predictions[-1]
            hourly_orders_lag2 = predictions[-2]
            hourly_orders_lag3 = lag_values[2 - len(predictions)]
            hourly_orders_lag4 = lag_values[3 - len(predictions)]
        elif len(predictions) < 4:
            hourly_orders_lag1 = predictions[-1]
            hourly_orders_lag2 = predictions[-2]
            hourly_orders_lag3 = predictions[-3]
            hourly_orders_lag4 = lag_values[3 - len(predictions)]
        else:
            hourly_orders_lag1 = predictions[-1]
            hourly_orders_lag2 = predictions[-2]
            hourly_orders_lag3 = predictions[-3]
            hourly_orders_lag4 = predictions[-4]

        # Prepare new data for prediction
        new_data = prepare_new_data(city, start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, festival, clusters, hourly_orders_lag1, hourly_orders_lag2, hourly_orders_lag3, hourly_orders_lag4)

        prediction = model.predict(new_data.values)
        predictions.append(int(prediction[0]))  # Convert to int for category mapping
        time_stamps.append(start_time)

        # Move to the next time period
        start_time += timedelta(hours=1)

    return time_stamps, predictions



def plot_predictions(time_stamps, predictions):
    # Convert predictions to their corresponding categories using inverse_category_mapping
    category_predictions = [inverse_category_mapping[pred] for pred in predictions]
    # Map category predictions to numerical values for plotting
    category_to_numeric = {v: k for k, v in inverse_category_mapping.items()}
    numeric_predictions = [category_to_numeric[category] for category in category_predictions]


    plt.figure(figsize=(12, 6))
    plt.plot(time_stamps, numeric_predictions, marker='o', linestyle='-', label='Predictions')
    plt.xlabel('Time')
    plt.ylabel('Predicted Hourly Orders Category')
    plt.title('Prediction of Hourly Orders Category over Time')
    plt.grid(True)

    # Set x-axis to 3-hour intervals
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))  # 3-hour intervals
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M'))  # Day of the month and time

    plt.xticks(rotation=45)

    # Correctly set y-ticks and their labels
    yticks_positions = list(category_to_numeric.values())
    yticks_labels = list(category_to_numeric.keys())
    plt.yticks(ticks=yticks_positions, labels=yticks_labels)

    return plt

    #plt.legend()
    #plt.tight_layout()
    #plt.show()
        
# List of cities expected by the model
expected_cities = [
    'Bangalore', 'Chennai', 'Coimbatore', 'Hyderabad', 'Indore', 'Jaipur',
    'Mumbai', 'Mysore', 'Pune', 'Ranchi', 'Surat', 'Vadodra'
]

# One-hot encode the city_name column using the expected cities
ohe = OneHotEncoder(sparse_output=False)
ohe.fit(pd.DataFrame(expected_cities, columns=['city_name']))

# Load the unique cluster mapping table
unique_cluster_mapping_modelB_v6 = pd.read_csv('unique_clusters_mapping_model_Bv6.csv')

# Use the DataFrame index as the unique_id
unique_clusters = unique_cluster_mapping_modelB_v6.index.tolist()

# Create the mapping dictionary using the index as the unique_id
cluster_mapping = unique_cluster_mapping_modelB_v6.reset_index().set_index('cluster')['index'].to_dict()

# Define your feature names based on your training data
model_feature_names = [
    'cluster_' + str(key) for key in cluster_mapping.keys()
] + [
    'festival', 'hourly_orders_lag1', 'hourly_orders_lag2', 'hourly_orders_lag3', 'hourly_orders_lag4',
    'city_name_Bangalore', 'city_name_Chennai', 'city_name_Coimbatore',
    'city_name_Hyderabad', 'city_name_Indore', 'city_name_Jaipur',
    'city_name_Mumbai', 'city_name_Mysore', 'city_name_Pune',
    'city_name_Ranchi', 'city_name_Surat', 'city_name_Vadodra', 'start_year',
    'start_month', 'start_day', 'start_hour', 'start_minute',
    'end_year', 'end_month', 'end_day', 'end_hour', 'end_minute', 'start_hour_sin',
    'start_hour_cos','end_hour_sin','end_hour_cos','lag_1_hour_sin_interaction',
    'lag_1_hour_cos_interaction','lag_2_hour_sin_interaction','lag_2_hour_cos_interaction',
    'lag_3_hour_sin_interaction', 'lag_3_hour_cos_interaction','lag_4_hour_sin_interaction',
    'lag_4_hour_cos_interaction', 'zero_orders'
]

# Category mapping
category_mapping = {
    '0': 0,
    '1-10': 1,
    '11-20': 2,
    '>20': 3
}
inverse_category_mapping = {v: k for k, v in category_mapping.items()}

# Load df_cluster_hr_activation_modelB_v2 from the CSV file (assuming it has been saved as such)
df_cluster_hr_activation_modelB_v6 = pd.read_csv('sum_clusters_by_hour_modelB_v6.csv')

# Load zero_orders data
zero_orders_data = pd.read_csv('zero_orders_datav6.csv')

st.title("Food Delivery Demand Prediction")
    
with st.form("my_form_1"):
    city_name = st.selectbox('Choose City',('Bangalore', 'Chennai', 'Coimbatore', 'Hyderabad', 'Indore', 'Jaipur',
    'Mumbai', 'Mysore', 'Pune', 'Ranchi', 'Surat', 'Vadodra'))
            
    submitted = st.form_submit_button("Submit")

    if submitted:
        print(city_name)
        
with st.form("my_form_2"):
    unique_cluster_mapping = pd.read_csv('unique_clusters_mapping_model_Bv6.csv')
    cluster_option_df = unique_cluster_mapping[unique_cluster_mapping['city_name'].isin([city_name])]
    city_cluster_list = cluster_option_df['cluster'].values.tolist()
    clusters = st.multiselect('Choose cluster from', (city_cluster_list))
    end_hour = st.selectbox('Choose Hour Window',('1','2','3','4','5','6','7','8',
        '9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'))
    festival = st.selectbox("Is it a festival", (0,1))

                
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        
        end_year = 2022
        end_month = 4
        end_day = 7
        end_minute = 0
        
        initial_lag_values = ['>20', '11-20', '>20', '>20']  # Replace with actual initial lag values (encoded categories)

        # Make predictions for the period
        time_stamps, predictions = predict_for_periods(model, city_name, end_year, end_month, end_day, int(end_hour), end_minute, int(festival), clusters, initial_lag_values)

        # Plot the predictions
        fig=plot_predictions(time_stamps, predictions)
        fig.legend()
        fig.tight_layout()
        st.pyplot(fig)
       
        

    