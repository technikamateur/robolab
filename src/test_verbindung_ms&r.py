#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 11:15:09 2019

@author: panyongyi
"""

#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import uuid
import time



class Communication:
    """
        Class to hold the MQTT client
        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """
    def __init__(self, mqtt_client):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message
        # ADD YOUR VARIABLES HERE
        # Basic configuration of MQTT
        # Wichtig?
        self.client.on_message = self.on_message_excepthandler

        self.client.username_pw_set('118', password='LQR2AabmwY') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/118', qos=1) # Subscribe to topic explorer/xxx

        # self.send_ready()
        # Start listening to incoming messages
        self.client.loop_start()

        #self.timer()



    #Parameter:
        self.data = None
        self.topic = "explorer/118"
        self.planet_Chan = None



    # this is a helper method that catches errors and prints them
    # it is necessary because on_message is called by paho-mqtt in a different thread and exceptions
    # are not handled in that thread
    #
    # you don't need to change this method at all
    def on_message_excepthandler(self, client, data, message):
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            raise


    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        """ Handles the callback if any message arrived """

        print('Got message with topic "{}":'.format(message.topic))
        data = json.loads(message.payload.decode('utf-8'))
        print(json.dumps(data, indent=2))
        print('\n')

        self.data = data

        self.typ_Entsch()
        #self.timer()

    #Timer: jede 2 Sekunden warten:
    def timer(self):
        t0 = time.time()
        while (time.time()-t0) < 2:
            pass
        print("neue Message kommt!")


    def typ_Entsch(self): #Test
        #print("schon in typ_Epntsch")
        if self.data["from"] == "server" and self.data["type"] == "planet":
            payload = self.data["payload"]
            planetName = payload["planetName"]
            self.planet_Chan = 'planet/'+planetName+'-118'
            self.pruefDaten()

    def send_ready(self):
        erk = '{"from": "client", "type": "ready"}'
        self.client.publish("explorer/118", erk, qos=1)

    def send_test(self):
        mess = '{"from": "client", "type": "testplanet", "payload": {"planetName":"Hawkeye"}}'
        self.client.publish("explorer/118", mess, qos=1)

    def pruefDaten(self):
        self.pathStat = "free"
        print(self.planet_Chan)
        pruef = '{"from":"client", "type":"path", "payload": {"startX": '+str(13)+', "startY": '+str(37)+', "startDirection": "N", "endX": '+str(14)+', "endY": '+str(36)+', "endDirection": "W", "pathStatus": "'+str(self.pathStat)+'"} }'
        print(pruef)
        self.client.subscribe(self.planet_Chan, qos=1)
        self.client.publish(self.planet_Chan, pruef, qos=1)


client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

com = Communication(client)
com.send_ready()
com.timer()
#com.send_test()
#com.timer()
com.pruefDaten()
com.timer()


'''
t0 = time.time()
while (time.time()-t0) < 2:
    pass
print("neue Message kommt!")
com.pruefDaten()
while (time.time()-t0) < 2:
    pass
print("neue Message kommt!")
'''
