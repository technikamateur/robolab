#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import uuid
import paho.mqtt.client as mqtt
from planet import Direction, Planet
from communication import Communication
from odometry import *

client = None  # DO NOT EDIT


# test
def run():
    # DO NOT EDIT
    # the deploy script uses this variable to stop the mqtt client after your program stops or crashes.
    # your script isn't able to close the client after crashing.
    global client
    client = mqtt.Client(
        client_id=str(
            uuid.uuid4()),  # client_id has to be unique among ALL users
        clean_session=False,
        protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    bob = Robot()
    bob.drive()
    planet = Planet()
    com = Communication(client, planet)
    bob.setView(Direction.SOUTH)
    com.timer()
    bob.setPosition(com.get_startP())
    if not com.node_scanned():
        com.scan_result(bob.scanPoint(Direction.SOUTH))
    bob.turn_by_direction(com.where_to_go())
    playSound_telekom()
    bob.drive()
    while True:
        #got to point
        com.discovered_path(bob.createMessage())
        position = com.get_korre_pos()
        bob.setPosition(position[0])
        bob.setView(position[1])
        if not com.node_scanned():
            com.scan_result(bob.scanPoint())
        direction = com.where_to_go()
        if direction is None:
            playSound_weAreNumberOne()
            break
        playSound_telekom()
        bob.turn_by_direction(direction)
        bob.drive()


# DO NOT EDIT
if __name__ == '__main__':
    run()
