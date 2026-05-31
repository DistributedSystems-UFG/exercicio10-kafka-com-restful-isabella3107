from flask import Flask, jsonify
from kafka import KafkaConsumer
import threading
import json

app = Flask(__name__)

database = []

consumer = KafkaConsumer(
    'temperature_averages',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def consume_kafka():
    for message in consumer:
        database.append(message.value)
        print("Stored:", message.value)

@app.route("/latest", methods=["GET"])
def get_latest():

    if not database:
        return jsonify({"error": "No data available"}), 404

    return jsonify(database[-1])

@app.route("/temperatures", methods=["GET"])
def list_temperatures():

    return jsonify(database)

if __name__ == "__main__":

    thread = threading.Thread(target=consume_kafka)
    thread.daemon = True
    thread.start()

    print("REST Server running...")
    app.run(host="0.0.0.0", port=5000)