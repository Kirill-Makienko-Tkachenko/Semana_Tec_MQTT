import sys
from paho.mqtt import client as mqtt_client
import random
import time

port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

#py Main.py send -c Carlos -m hola -p 192.168.244.1


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
    


def connect_mqtt(broker):
    def on_connect(client, userdata, flags, rc):
        
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    msg_count = 0
    while True:
        time.sleep(1)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1






def connect_mqtt(broker) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message







if sys.argv[1] == "send":
    broker,topic,message = descifrar_orden(sys.argv)
    print(broker)
    client = connect_mqtt(broker)
    publish(client, topic, message)


elif sys.argv[1] == "subscribe":
    broker,topic = descifrar_orden(sys.argv)
    client = connect_mqtt(broker)
    subscribe(client, topic)
    client.loop_forever()

else:
    print("Opcion invalida\n")
    print("Terminando programa\n")