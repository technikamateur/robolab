#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import time
from planet import Direction



class Communication:
    """
        Class to hold the MQTT client
        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """
    def __init__(self, mqtt_client, planet):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message
        self.planet = planet
        # ADD YOUR VARIABLES HERE
        # Basic configuration of MQTT
        # Wichtig?
        self.client.on_message = self.on_message_excepthandler

        self.client.username_pw_set('118', password='LQR2AabmwY') # Your group credentials
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        self.client.subscribe('explorer/118', qos=1) # Subscribe to topic explorer/xxx

        self.send_ready()
        # Start listening to incoming messages
        self.client.loop_start()



         #Parameter:
        self.data = None
        self.topic = "explorer/118"
        self.planet_Chan = None

        self.aktX = None
        self.aktY = None
        self.direc = None



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
        print("\n")

        self.data = data

        self.timer()
        self.typ_Entsch()



    #Timer: jede 2 Sekunden warten:
    def timer(self):
        t0 = time.time()
        while (time.time()-t0) < 2:
            pass
        print("neue Message kommt!")




    def typ_Entsch(self):
        if self.data["from"] == "server" and self.data["type"] == "planet":
            self.setPlanetInfo()
        elif self.data["from"] == "server" and self.data["type"] == "path":
            self.set_korrePos()
        elif self.data["from"] == "server" and self.data["type"] == "pathUnveiled":
            self.speich_path()


        elif self.data["from"] == "server" and self.data["type"] == "pathSelect":
            self.serverPath()
        elif self.data["from"] == "server" and self.data["type"] == "target":
            self.target_server()
        elif self.data["from"] == "server" and self.data["type"] == "done":
            self.done()






    # 1.Erkundung nach der Landung.
    def send_ready(self):
        erk = '{"from": "client", "type": "ready"}'
        self.client.publish("explorer/118", erk, qos=1)

    # 2.PlanetName und StartKoordinanten übergeben
    def setPlanetInfo(self):
        playload = self.data["playload"]
        planetName = playload["planetName"]
        self.planet_Chan = 'planet/'+planetName+''+str(-118)+'
        self.client.subscribe(self.planet_Chan, qos=1)
        self.aktX = int(self.data["startX"])
        self.aktY = int(self.data["startY"])

        return (self.aktX, self.aktY)


    # 3. gefahrenden Pfad und geschätzte Posision zu MS schicken
    def pruefDaten(self, message):
        startX = message[0][0][0]
        startY = message[0][0][1]
        startDir = message[0][1]
        endX = message[1][0][0]
        endY = message[1][0][1]
        endDir = message[1][1]
        status = message[2]

        self.aktX = endX
        self.aktY = endY

        pp = '{"from":"client", "type":"path", "payload": {"startX": "'+str(startX)+'", "startY": "'+str(startY)+'", "startDirection": "'+startDir+'", "endX": "'+str(endX)+'", "endY": "'+str(endY)+'", "endDirection": "'+endDir+'", "pathStatus": "'+status+'"}}'

        self.client.publish(self.planet_Chan, pp, qos=1)   #planet/<CHANNEL>,<CHANNEL> = Planet name - 118


    # 4. Korregierte Position zu Planet schicken & Pfadaufdeckung und Pfadwahl:
    def set_korrePos(self):
        korre_pos = self.data["payload"]
        startX = int(korre_pos["startX"])
        startY = int(korre_pos["startY"])
        startDir = korre_pos["startDirection"]
        endX = int(korre_pos["endX"])
        endY = int(korre_pos["endY"])
        endDir = korre_pos["endDirection"]
        weight = int(korre_pos["pathWeight"])

        self.aktX = endX
        self.aktY = endY

        self.planet.add_path(((startX, startY), startDir), ((endX, endY), endDir), weight)

        return [(endX, endY), endDir]

    # Pfad und Position von anderen Robert gefunden haben, direkt hinzufügen:
    def speich_path(self):
        add = self.data["payload"]
        startX = int(add["startX"])
        startY = int(add["startY"])
        startDir = add["startDirection"]
        endX = int(add["endX"])
        endY = int(add["endY"])
        endDir = add["endDirection"]
        weight = int(add["pathWeight"])

        self.planet.add_path(((startX, startY), startDir), ((endX, endY), endDir), weight)



    # 5. pathSelect Publish on planet:
    def pathSelect(self, node):
        result = self.planet.unknown_paths(node)
        startX = result[0][0]
        startY = result[0][1]
        startDir = result[1].value

        self.aktX = starX
        self.aktY = starY
        self.direc = startDir

        select = '{"from":"client", "type":"pathSelect", "payload": {"startX": "'+str(startX)+'", "startY": "'+str(startY)+'", "startDirection": "'+str(startDir)+'"} }'

        self.client.publish(self.planet_Chan, select, qos=1)

        return self.direc



    # 6. pathSelect from Server:
    def serverPath(self):
        path_server = self.data["playload"]
        startDir = path_server["startDirection"]

        self.direc = startDir

        return Direction(starDir)



    # 7. Zielpossition aus Mutterschiff:
    def target_server(self):
        target = self.data["playload"]
        targetX = int(target["targetX"])
        targetY = int(target["targetY"])

        self.planet.shortest_path((self.aktX, self.aktY), (targetX, targetY))

        return (targetX, targetY)


    # 8. Abschluss der Erkundung:
    def target_Reached(self):
        targetR = '{"from":"client", "type":"targetReached", "payload": {"message": "target is reached!"} }'
        self.client.publish(self.topic, targetR, qos=1)


    # 9. ExplorationCompleted:
    def explor_compl(self):
        completed = '{"from":"client", "type":"explorationCompleted", "payload": {"message": "Exploration is completed!"} }'
        self.client.publish(self.topic, completed, qos=1)



    # 10. Done from Server:
    def done(self):
        done = self.data("playload")
        print(done("message"))
