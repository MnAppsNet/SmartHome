# SmartThermostat
This is a server application written in python and controlled from a wep app created with ReactJS.
The purpose of this project is to control the house thermostat remotely from any device.
In order for the whole setup to work, your boiler must have two cables that when you connect them it opens the heat and when you disconnect them it stops.

# Schematic
![SmartThermostatDiagram](SmartThermostatDiagram.png)

# Installation
* Prepare the hardware are shown in the schematics
* Clone the repo in a raspberry py
* cd into the client folder and execute npm install and npm run build
* copy the content of the produced build folder in a client folder inside the server folder
* cd into the server folder
* execute python install -r requirements.txt
* and finlay execute the python script: python smartThermostat.py


### /!\ Warning /!\
This is an experimental project, make sure you know what you do before you do anything