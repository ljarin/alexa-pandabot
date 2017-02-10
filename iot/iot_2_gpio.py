#!/usr/bin/env python

from shadow_pubsub import *
from iot_endpoint_name import endpoint
import os.path
#import RPi.GPIO as GPIO

# Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key, and iot_endpoint_name.py setting endpoint name


class PandaBot:
	
	def __init__(self):
		
		home=os.path.expanduser('~')
		rootCA=home+'/pandabot/iot/certificate/root-CA.crt'
		cert=home+'/pandabot/iot/certificate/pandaDanceMotor.cert.pem'
		key=home+'/pandabot/iot/certificate/pandaDanceMotor.private.key'
		
		#Create a deviceShadow with persistent subscription
		myAWSIoTMQTTShadowClient=make_shadow_client(endpoint,rootCA,cert,key)
		self.shadowClient=myAWSIoTMQTTShadowClient.createShadowHandlerWithName("pandaDanceMotor", True) 
			
		# Delete stored shadow upon initializing
		self.shadowClient.shadowDelete(customShadowCallback_Delete, 5)
		
		#Create shadow with desired and reported state as motor off
		JSONPayload = '{"state":{"desired":{"motor":0}}}'
		self.shadowClient.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
		JSONPayload = '{"state":{"reported":{"motor":0}}}'
		self.shadowClient.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

		self.motor_GPIO=18
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.motor_GPIO, GPIO.OUT,initial=GPIO.LOW)
		
	def updateMotorStatus(self,motorStatus,state_modifier='reported'):
		if motorStatus:
			GPIO.output(self.motor_GPIO,GPIO.HIGH)
		else:
			GPIO>output(self.motor_GPIO,GPIO.LOW)
		JSONPayload = '{"state":{"desired":{"motor":' + str(motorStatus) + '}}}'
		JSONPayload = '{"state":{"'+state_modifier+'":{"motor":' + str(motorStatus) + '}}}'
		self.shadowClient.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
	def turnOnMotor(self):
		self.updateMotorStatus(1)

	def turnOffMotor(self):
		self.updateMotorStatus(0)

	def deltaGetShadow(self):
		# Listen on deltas
		self.shadowClient.shadowRegisterDeltaCallback(customShadowCallback_Delta)
		
	def getShadow(self):
		self.shadowClient.shadowGet(customShadowCallback_Get, 5)

myPandaBot = PandaBot()
time.sleep(5)
myPandaBot.turnOnMotor()
time.sleep(5)
myPandaBot.turnOffMotor()

#~ while True:
	#~ myPandaBot.deltaGetShadow()
