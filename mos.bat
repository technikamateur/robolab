set /p planet_name="Please set Planetname: "
mosquitto_pub -h mothership.inf.tu-dresden.de -p 8883 -u "118" -P "LQR2AabmwY" -t "explorer/118" -m '{"from":"client","type":"testplanet","payload":{"planetName":"%planet_name%"}}' -q 1