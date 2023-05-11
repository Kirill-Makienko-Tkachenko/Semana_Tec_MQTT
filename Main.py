#Hecho por Kirill Makienko Tkachenko
#10/06/23
#Parte del codigo se encuentra en: https://www.emqx.com/en/blog/how-to-use-mqtt-in-python

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Librerias utilizadas
import sys
from paho.mqtt import client as mqtt_client
import random
import time

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#Constantes
port = 1883 #El puerto siempre es constante debido a las intrucciones del profesor
client_id = f'python-mqtt-{random.randint(0, 1000)}' #Asigna un id al cleinte que envia o subscribe de manera automatica

#py Main.py send -c Marco -m hola -p 52.23.241.126
#py Main.py subscribe -c Marco -p 52.23.241.126

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#Funcion utilizada para asignar valores sin importar el orden en el que se encuentren en la linea de comandos

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

#Funciones que habilitan el push del mensaje

#Funcion que conecta el cliente al IP
def connect_mqtt(broker):
    def on_connect(client, userdata, flags, rc): #Funcion que confirma conexion exitosa
        
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id) #Asigna Client Id a la maquina que se conecta
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#Funcion que publica un mensaje (Push en un canal, indicado en CLI) 
def publish(client, topic, msg):
    msg_count = 0
    while True:
        #time.sleep(1)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
            break
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#Funciones que habilitan suscribirse a un topico de un canal

#Funcion que apunta a connect_mqtt para conectar
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


#Funcion para suscribir el cliente y recibir mensajes

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message



#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

#Programa Main

#Revisa si el argumento pasado del CLI es send o subscribe
if sys.argv[1] == "send":
    broker,topic,message = descifrar_orden(sys.argv)
    print(broker)
    while True:#Permite enviar mensajes de manera perpetua hasta que se cancele

        client = connect_mqtt(broker)
        publish(client, topic, message)
        message = input("Cual es tu mensaje (Apaga la consola para salir): ")


elif sys.argv[1] == "subscribe":
    broker,topic = descifrar_orden(sys.argv)
    client = connect_mqtt(broker)
    subscribe(client, topic)
    client.loop_forever()#Permite que el cliente de subscibcion este constantemente refrescandose

else:
    print("Opcion invalida\n")
    print("Terminando programa\n")