import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import time

# Create a dataframe to store the data
df = pd.DataFrame(columns=['timestamp', 'Speed'])

# Define the API URL
url = 'https://flaskapi-c746027-streamlittutorial-streamlittutorial-a46e73b8.deployments.quix.io'

# Create a placeholder for the chart
chart_placeholder = st.empty()

# Define a function to poll data from the API
def poll_data():
    while True:
        response = requests.get(url)
        data = response.json()
        if 'Speed' in data:
            df.loc[len(df)] = [data['timestamp'], data['Speed']]
            plot_chart()
        time.sleep(1)  # Wait for a second before polling again

# Define a function to plot the chart
def plot_chart():
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['Speed'])
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Speed over Time')
    chart_placeholder.pyplot(plt)

# Poll data from the API
poll_data()