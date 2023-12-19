import quixstreams as qx
import os
import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS
import time
from waitress import serve
import threading


speed = 0
timestamp = int(time.time() * 1e9)

client = qx.QuixStreamingClient()

topic_consumer = client.get_topic_consumer(os.environ["input"], consumer_group = "empty-transformation")

def on_dataframe_received_handler(stream_consumer: qx.StreamConsumer, df: pd.DataFrame):
    global speed
    global timestamp

    # every time data is received, update the global variables
    if "Speed" in df and df["Speed"][0]:
        speed = df["Speed"][0]
    if "timestamp" in df and df["timestamp"][0]:
        timestamp = df["timestamp"][0]

# connect to the stream and connect the data handler
def on_stream_received_handler(stream_consumer: qx.StreamConsumer):
    stream_consumer.timeseries.on_dataframe_received = on_dataframe_received_handler

# subscribe to new streams being received
topic_consumer.on_stream_received = on_stream_received_handler

# create the flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/')
def get_data():
    # return the latest data
    data = {
        'timestamp': int(time.time() * 1e9),
        'Speed': speed
    }
    return jsonify(data)

def run_server():
    #app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
    # use waitress instead for production
    serve(app, host='0.0.0.0', port = 80)

if __name__ == '__main__':
    # Run the server in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    qx.App.run()
