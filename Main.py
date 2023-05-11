#Hecho por Kirill Makienko Tkachenko
#10/05/23
#Parte del codigo se encuentra en: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Used libraries
import sys
from paho.mqtt import client as mqtt_client
import random
import time

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Constants 
port = 1883 # Port that we will always use
client_id = f'python-mqtt-{random.randint(0, 1000)}' # Randomized ID for the client

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Function to assign values despite the order of the command line
def descifrar_orden(argv):
    for i in range(len(argv)-1):
        
        if argv[i] == "-p":
            broker = argv[i+1]
        
        if argv[i] == "-c":
            topic = argv[i+1]
        
        if argv[1] == "send":
            if argv[i] == "-m":
                message = argv[i+1]
    if argv[1] == "send":
        return[broker,topic,message]
    else:
        return[broker,topic]

 #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Function that connects the client to the IP
def connect_mqtt(broker):
    # Function that return the connection state
    def on_connect(
            client, userdata, flags, 
            rc): 
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id) # Assigns Client ID 
    client.on_connect = on_connect
    client.connect(broker, port) # Establish the connection with the server
    return client 

# Function to publish a message in a topic
def publish(client, topic, msg):
    msg_count = 0
    while True:
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
            break
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Functions that enable suscribing to a channel 

# Function that connects to the mqtt client 
def connect_mqtt(broker) -> mqtt_client:
    def on_connect(
            client, userdata, flags, 
            rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Function to suscribe the client and receive messages
def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message



#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Main program

# Verifies the client choice in order to send or receive message
if sys.argv[1] == "send":
    broker,topic,message = descifrar_orden(sys.argv)
    print(broker)
    while True: # Allows to keep sending messages 
        client = connect_mqtt(broker) # Establish the connection 
        publish(client, topic, message) # Publish the message to the topic
        message = input("Your message: ") # Receives the message to publish 


elif sys.argv[1] == "subscribe":
    broker,topic = descifrar_orden(sys.argv) 
    client = connect_mqtt(broker) # Establish the connection
    subscribe(client, topic) # Receive the message
    client.loop_forever() # Allows the client to keep receiving messages

else:
    print("Invalid option!\n")
    print("Closing program... \n")