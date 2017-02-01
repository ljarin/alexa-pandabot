#!/usr/bin/env python

from shadow_pubsub import *
import os.path
#import RPi.GPIO as GPIO

# Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key
home=os.path.expanduser('~')
endpoint='a2rig0317k0i1k.iot.us-east-1.amazonaws.com'
rootCA=home+'/pandabot/certificate/root-CA.crt'
cert=home+'/pandabot/certificate/pandaDanceMotor.cert.pem'
key=home+'/pandabot/certificate/pandaDanceMotor.private.key'

class PandaBot:
	
	def __init__(self):
		
		#Create a deviceShadow with persistent subscription
		myAWSIoTMQTTShadowClient=make_shadow_client(endpoint,rootCA,cert,key)
		self.shadowClient=myAWSIoTMQTTShadowClient.createShadowHandlerWithName("pandaDanceMotor", True) 
			
		# Delete stored shadow upon initializing
		self.shadowClient.shadowDelete(customShadowCallback_Delete, 5)
		
		self.motorStatus=0
		
	def updateMotorStatus(self,motorStatus,state_modifier='reported'):
		self.motorStatus=motorStatus
		JSONPayload = '{"state":{"desired":{"motor":' + str(self.motorStatus) + '}}}'
		JSONPayload = '{"state":{"'+state_modifier+'":{"motor":' + str(self.motorStatus) + '}}}'
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
myPandaBot.turnOnMotor()
while True:
	myPandaBot.deltaGetShadow()
