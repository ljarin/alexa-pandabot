#!/usr/bin/env python

from shadow_pubsub import *
from setup_environment import endpoint,rootCA,cert,key
import os.path
import RPi.GPIO as GPIO

# Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key


class PandaBot:
	
	def __init__(self):
		
		#Create a deviceShadow with persistent subscription
		myAWSIoTMQTTShadowClient=make_shadow_client(endpoint,rootCA,cert,key)
		self.shadowClient=myAWSIoTMQTTShadowClient.createShadowHandlerWithName("pandaDanceMotor", True) 
			
		# Delete stored shadow upon initializing
		self.shadowClient.shadowDelete(customShadowCallback_Delete, 5)

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
#~ while True:
	#~ myPandaBot.deltaGetShadow()
