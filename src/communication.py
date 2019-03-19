#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import time



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

        self.startX = None
        self.startY = None

        self.startDir = None
        self.endDir = None

        self.pathStat = None
        self.pathWeight = None     #int

        self.geschaePx = None
        self.geschaePy = None

        self.korrPx = None
        self.korrPy = None

        self.targetX = None
        self.targetY = None


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

        self.data = json.dumps(data, indent=2)

        self.timer()
        self.typ_Entsch()



    #Timer: jede 2 Sekunden warten:
    def timer(self):
        t0 = time.time()
        alt_message = self.data
        while (time.time()-t0) < 2:
            if alt_message == self.data:   #Prüf neue Message. Warte auf neue Message.
                print("warte auf neue Message.")
        print("neue Message kommt!")
        self.typ_Entsch()




    def typ_Entsch(self):
        if "planetName" in self.data:
            self.setPlanetInfo()
        elif '{"from": "server", "type": "path"}' in self.data:
            self.set_korrePos()
        elif '{"from": "server", "type": "pathUnveiled"}' in self.data:
            self.set_korrePos()
        elif '{"from": "client", "type": "pathSelect"}' in self.data:
            self.pathSelect()
        elif '{"from": "server", "type": "pathSelect"}' in self.data:
            self.serverPath()
        elif '{"from": "server", "type": "target"}' in self.data:
            self.target_server()
        elif '{"from": "client", "type": "targetReached"}' in self.data:
            self.target_Reached()
        elif '{"from": "server", "type": "done"}' in self.data:
            self.done()






    # 1.Erkundung nach der Landung.
    def send_ready(self):
        erk = '{"from": "client", "type": "ready"}'
        self.client.publish("explorer/118", erk, qos=1)

    # 2.PlanetName und StartKoordinanten übergeben
    def setPlanetInfo(self):
        if "planetName" in self.data:
            playload = self.data("playload")
            planetName = playload("planetName")
            self.planet_Chan = 'planet/'+str(planetName)+''+str(-118)+'
            self.startX = int(self.data("startX"))
            self.startY = int(self.data("startY"))
            self.planet.setPlanetInfo(self.data("planetName"), self.startX, self.startY)


    # 3. gefahrenden Pfad und geschätzte Posision zu MS schicken
    def pruefDaten(self):
        self.pathStat = "free"
        pruef = '{"from":"client", "type":"path", "payload": {"startX": '+str(self.startX)+', "startY": '+str(self.startY)+', "startDirection": '+self.startDir+', "endX": '+str(self.geschaePx)+', "endY": '+str(self.geschaePy)+', "endDirection": '+self.endDir+', "pathStatus": '+self.pathStat+'}}'

        self.client.subscribe(self.planet_Chan, qos=1)
        self.client.publish(self.planet_Chan, pruef, qos=1)   #planet/<CHANNEL>,<CHANNEL> = Planet name - 118


    # 4. Korregierte Position zu Planet schicken & Pfadaufdeckung und Pfadwahl:
    def set_korrePos(self):
        korre_pos = self.data("payload")
        self.startX = int(korre_pos("startX"))
        self.startY = int(korre_pos("startY"))
        self.startDir = korre_pos("startDirection")
        self.korrPx = int(korre_pos("endX"))
        self.korrPy = int(korre_pos("endY"))
        self.endDir = korre_pos("endDirection")
        self.pathStat = korre_pos("pathStatus")
        self.pathWeight = int(korre_pos("pathWeight"))

        self.planet.add_path(((self.aktPx, self.aktPy), self.startDir), ((self.korrPx, self.korrPy, self.endDir)), self.pathWeight)



    # 5. pathSelect Publish on planet:
    def pathSelect(self):
        path = self.data("playload")
        self.startX = int(path("startX"))
        self.startY = int(path("startY"))
        self.startDir = path("startDirection")
        select = '{"from":"client", "type":"pathSelect", "payload": {"startX": '+str(self.startX)+', "startY": '+str(self.startY)+', "startDirection": '+self.startDir+'}}'

        self.client.publish(self.planet_Chan, select, qos=1)


    # 6. pathSelect from Server:
    def serverPath(self):
        path_server = self.data("playload")
        self.startDir = path_server("startDirection")


    # 7. Zielpossition aus Mutterschiff:
    def target_server(self):
        target = self.data("playload")
        self.targetX = int(target("targetX"))
        self.targetY = int(target("targetY"))


    # 8. Abschluss der Erkundung:
    def target_Reached(self):
        targetR = '{"from":"client", "type":"targetReached", "payload": {"message": "target is reached!"}}'
        self.client.publish(self.topic, targetR, qos=1)


    # 9. ExplorationCompleted:
    def explor_compl(self):
        completed = '{"from":"client", "type":"explorationCompleted", "payload": {"message": "Exploration is completed!"}}'
        self.client.publish(self.topic, completed, qos=1)



    # 10. Done from Server:
    def done(self):
        done = self.data("playload")
        print(done("message"))
