import streamlit as st
import pandas as pd
import json
import asyncio
import websockets
import matplotlib.pyplot as plt

# Create a dataframe to store the data
df = pd.DataFrame(columns=['timestamp', 'Speed'])

# Define the WebSocket URL
url = 'wss://   /timeseries'

# Create a placeholder for the chart
chart_placeholder = st.empty()

# Define an async function to receive data from the WebSocket
async def receive_data():
    async with websockets.connect(url) as ws:
        while True:
            data = await ws.recv()
            data = json.loads(data)
            if 'Speed' in data:
                df.loc[len(df)] = [data['timestamp'], data['Speed']]
            plot_chart()

# Define a function to plot the chart
def plot_chart():
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['Speed'])
    plt.xlabel('Timestamp')
    plt.ylabel('Speed')
    plt.title('Speed over Time')
    chart_placeholder.pyplot(plt)

# Run the async function
asyncio.run(receive_data())