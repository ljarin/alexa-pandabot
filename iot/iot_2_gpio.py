#!/usr/bin/env python

'''
Runs on the local machine (Raspberry Pi). Subscribes to the AWS IOT device shadow 'pandaDanceMotor'
Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key, and iot_endpoint_name.py setting endpoint name
'''


from shadow_pubsub import *
from iot_endpoint_name import endpoint
import os.path
import time
#import RPi.GPIO as GPIO

class PandaBot:
	
	def __init__(self,test_mode=False):
		
		home=os.path.expanduser('~')
		rootCA=home+'/pandabot/iot/certificate/root-CA.crt'
		cert=home+'/pandabot/iot/certificate/pandaDanceMotor.cert.pem'
		key=home+'/pandabot/iot/certificate/pandaDanceMotor.private.key'
		
		#Create a deviceShadow with persistent subscription
		myAWSIoTMQTTShadowClient=make_shadow_client(endpoint,rootCA,cert,key)
		self.shadowClient=myAWSIoTMQTTShadowClient.createShadowHandlerWithName("pandaDanceMotor", True) 
		self.callbacks=shadowCallbacks()
		# Delete stored shadow upon initializing
		self.shadowClient.shadowDelete(self.callbacks.customShadowCallback_Delete, 5)
		#Create shadow with desired and reported state as motor off
		JSONPayload = '{"state":{"desired":{"motor":0},"reported":{"motor":0}}}'
		self.shadowClient.shadowUpdate(JSONPayload, self.callbacks.customShadowCallback_Update, 5)
		self.test_mode=test_mode
		if test_mode is False:
			self.motor_GPIO=18
			GPIO.setmode(GPIO.BOARD)
			GPIO.setup(self.motor_GPIO, GPIO.OUT,initial=GPIO.LOW)
		
	def updateMotorStatus(self,motorStatus,state_modifier='reported'):
		if not self.test_mode:
			if motorStatus:
				GPIO.output(self.motor_GPIO,GPIO.HIGH)
			else:
				GPIO.output(self.motor_GPIO,GPIO.LOW)
		JSONPayload = '{"state":{"desired":{"motor":' + str(motorStatus) + '}}}'
		JSONPayload = '{"state":{"'+state_modifier+'":{"motor":' + str(motorStatus) + '}}}'
		self.shadowClient.shadowUpdate(JSONPayload, self.callbacks.customShadowCallback_Update, 5)
	def turnOnMotor(self):
		self.updateMotorStatus(1)

	def turnOffMotor(self):
		self.updateMotorStatus(0)

	def deltaGetShadow(self):
		# Listen on deltas
		self.shadowClient.shadowRegisterDeltaCallback(self.callbacks.customShadowCallback_Delta)
		while self.callbacks.deltaStatus is 0:
			pass
		self.callbacks.deltaStatus=0
		return myPandaBot.callbacks.deltaPayload
		
	def getShadow(self):
		self.shadowClient.shadowGet(self.callbacks.customShadowCallback_Get, 5)
		while self.callbacks.getStatus is 0: #kinda dangerous. wait for callback to finish
			pass
		self.callbacks.getStatus=0
		return myPandaBot.callbacks.getPayload



myPandaBot = PandaBot(test_mode=True)
print(myPandaBot.getShadow())
myPandaBot.turnOnMotor()
print(myPandaBot.getShadow())
	
