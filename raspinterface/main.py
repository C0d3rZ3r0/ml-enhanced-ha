from smartDevice import SmartDevice as SmartDevice # to represent bulb devices

from flask import Flask as Flask
from flask import render_template

from RPi import GPIO as GPIO # for controlling the Raspberry Pi GPIO pins 

#GPIO.cleanup()
GPIO.setwarnings(False) # show no warnings
GPIO.setmode(GPIO.BOARD) # use RPi Board numbering

bulb1=SmartDevice("b1","OFF",11)
bulb2=SmartDevice("b2","OFF",13)
bulb3=SmartDevice("b3","OFF",15)

stateSet=("OFF","ON")

bulbs={ bulb1.name:bulb1, bulb2.name:bulb2, bulb3.name:bulb3 }

piServer=Flask(__name__)

#the default route returning the frontend for the interface
@piServer.route("/")
def startPage():
	#return "Pi side server is up and running!"
	
	templateData={
		'b1state':bulb1.stateStr,
		'b2state':bulb2.stateStr,
		'b3state':bulb3.stateStr
	}
	return render_template('InterfaceFrontend.html', **templateData)

#the interface will use this route to switch bulb states
@piServer.route("/<bulbName>/<newState>")
def reqSwitch(bulbName,newState):
	if bulbName not in bulbs:
		# check if bulb exists
		return "Bulb "+bulbName+" does not exist."
	elif newState not in stateSet:
		# check if state is valid
		return newState+" is not a valid state."
	else:
		# switch <bulbName> to <newState>
		bulbs[bulbName].switch(newState)
		
		return bulbs[bulbName].stateStr

#@piServer.route("/some/route")
#def someFunc():
#	#TODO:Code

"""
The following part makes sure the server is started only when this script is started as the main (standalone) module and not when imported by other modules.
"""
if __name__=="__main__":
	piServer.run(host="0.0.0.0",port=80,debug=True)