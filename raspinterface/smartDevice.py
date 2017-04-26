from RPi import GPIO as GPIO # for controlling the Raspberry Pi GPIO pins

class SmartDevice:

	name="" # some unique name for the device
	stateStr="" # "ON" or "OFF"
	pin=int() # GPIO pin number the device is connected to, in board mode
	
	"""__init__() [class object initializer]
	
	Purpose: initialize the object being created
	Arguments: a name for the device, an initial state for the device, and the pin number the device is on
	Returns: nothing
	"""
	def __init__(self,name,stateStr,pin):
		self.name=name
		self.stateStr=stateStr
		self.pin=pin
		GPIO.setup(self.pin,GPIO.OUT) # setup 
		self.switch(self.stateStr)
		"""
		#old code, broken
		if stateStr is "ON" or stateStr is "OFF":
			self.name=name
			self.pin=pin
		GPIO.setup(self.pin,GPIO.OUT,GPIO)
		if stateStr is "ON":
			self.state=GPIO.HIGH
		if stateStr is "OFF":
			self.state=GPIO.LOW
		"""
	
	"""switch()
	
	Purpose: turn the device on or off.
	Arguments: a string representing state change - "ON" or "OFF"
	Returns: nothing
	"""
	def switch(self,stateStr):
		print(stateStr)
		self.stateStr=stateStr
		if stateStr=="ON":	
			GPIO.output(self.pin,GPIO.HIGH) # give high (1) output on pin
		elif stateStr=="OFF":
			GPIO.output(self.pin,GPIO.LOW) # give low (0) output on pin