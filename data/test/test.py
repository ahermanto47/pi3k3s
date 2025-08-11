import paho.mqtt.client as mqtt
import time

# MQTT broker details
broker_address = "10.0.0.120"  # Using a public broker for demonstration
port = 1883
keepalive = 60  # Maximum period in seconds between communication with the broker

# Topic to publish to
topic = "default/topic" 

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid, reason_code, properties=None):
    print(f"Message Published (mid: {mid})")

# Create an MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # For Paho v2.x and above, use CallbackAPIVersion.VERSION1 for on_connect signature
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker_address, port, keepalive)

# Start the client loop to handle connections, publishing, and callbacks
client.loop_start() # Use loop_start() for non-blocking publishing

# Message payload
with open("sp500_tickers.txt", "r") as f:
    sp500_tickers = [line.strip() for line in f.readlines()]
    for i, ticker in enumerate(sp500_tickers):
        # Publish the message
        try:
            result = client.publish(topic, ticker)
            # You can check result.rc for the return code (0 for success)

            print(f"Attempting to publish '{ticker}' to topic '{topic}'")

            # Give some time for the message to be published and acknowledged
            time.sleep(10)

            if i > 5 and i % 10 == 0:
                print(f"Published {i} tickers, waiting for 3 minutes before next batch...")
                time.sleep(180)

        except Exception as e:
            print(f"Failed to publish message '{ticker}' to topic '{topic}': {e}")

# Disconnect from the broker
client.loop_stop()
client.disconnect()
