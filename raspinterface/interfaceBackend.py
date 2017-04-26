from smartDevice import SmartDevice as SmartDevice # to represent bulb devices

from flask import Flask as Flask
from flask import render_template

from RPi import GPIO as GPIO # for controlling the Raspberry Pi GPIO pins

import urllib2
import threading

pcAddr="192.168.10.249"
GPIO.setwarnings(False) # show no warnings
GPIO.setmode(GPIO.BOARD) # use RPi Board numbering

class InterfaceBackend:
	
	bulb1=SmartDevice("b1","OFF",11)
	bulb2=SmartDevice("b2","OFF",13)
	bulb3=SmartDevice("b3","OFF",15)

	stateSet=("OFF","ON")

	bulbs={ bulb1.name:bulb1, bulb2.name:bulb2, bulb3.name:bulb3 }
	
	# functions
	def __init__(self):
		#TODO[Done]: start pc sync thread
		self.pcSync()
	
	def startPage(self):
		templateData={
		'b1state':self.bulb1.stateStr,
		'b2state':self.bulb2.stateStr,
		'b3state':self.bulb3.stateStr
		}
		return render_template('InterfaceFrontend.html', **templateData)
	
	def reqSwitch(self,bulbName,newState):
		if bulbName not in self.bulbs:
			# check if bulb exists
			return "Bulb "+bulbName+" does not exist."
		elif newState not in self.stateSet:
			# check if state is valid
			return newState+" is not a valid state."
		else:
			# switch <bulbName> to <newState>
			self.bulbs[bulbName].switch(newState)
			
			"""
			#TODO:
			- send this action to PC
			- ask PC if predictions are available
			- if yes, then get those predictions and apply them
			"""
			#send actions to PC
			try:
				urllib2.urlopen("http://"+pcAddr+"/"+bulbName+"/"+newState)
			except:
				print("error sending state change")
			
			try:
				#get the prediction
				b2PredStr=urllib2.urlopen("http://"+pcAddr+"/predict/"+"b2").read()
				b3PredStr=urllib2.urlopen("http://"+pcAddr+"/predict/"+"b3").read()
			
				#apply the prediction
				self.bulb2.switch(b2PredStr)
				self.bulb3.switch(b3PredStr)
			except:
				print("error getting predictions")
		return self.bulbs[bulbName].stateStr
	
	def pcSync(self):
		#TODO[Done]: sync device states to pc
		try:
			urllib2.urlopen("http://"+pcAddr+"/writenochange")
		except:
			print("error opening /writenochange")
		threading.Timer(5.0,self.pcSync).start()

if __name__=="__main__":
	#TODO[Done]: run the interfaceBackend as a server.
	piServer=Flask(__name__)
	ib=InterfaceBackend()
	
	@piServer.route("/")
	def startPage():
		return ib.startPage()
	
	@piServer.route("/<bulbName>/<newState>")
	def reqSwitch(bulbName,newState):
		return ib.reqSwitch(bulbName,newState)
	
	piServer.run(host="0.0.0.0",port=80,debug=True)
