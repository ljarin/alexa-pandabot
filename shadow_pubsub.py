'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json

# Shadow JSON schema:
#
# Name: pandaDanceMotor
 #{
	#"state": {
		#"desired":{
			#"motor":<1 or 0>
		#}
	#}
#}

# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	print("Delta request " + responseStatus)
	payloadDict = json.loads(payload)
	print("++++++++DELTA++++++++++")
	print("motor: " + str(payloadDict["state"]["motor"]))
	print("version: " + str(payloadDict["version"]))
	print("+++++++++++++++++++++++\n\n")

def customShadowCallback_Get(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	print("Get request " + responseStatus)
	payloadDict = json.loads(payload)
	print("+++++++++ShadowGet+++++++++++")
	print("motor: " + str(payloadDict["state"]["desired"]["motor"]))
	print("version: " + str(payloadDict["version"]))
	print("+++++++++++++++++++++++\n\n")
		
def customShadowCallback_Update(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("motor: " + str(payloadDict["state"]["desired"]["motor"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")

def customShadowCallback_Delete(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Delete request " + token + " time out!")
	if responseStatus == "accepted":
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Delete request " + token + " rejected!")
		
class PandaBot:
	
	def __init__(self, myAWSIoTMQTTShadowClient):
		#Create a deviceShadow with persistent subscription
		self.shadowClient=myAWSIoTMQTTShadowClient.createShadowHandlerWithName("pandaDanceMotor", True) 
		self.motorStatus=0
		
	def updateMotorDesiredStatus(self,motorStatus):
		self.motorStatus=motorStatus
		JSONPayload = '{"state":{"desired":{"motor":' + str(self.motorStatus) + '}}}'
		self.shadowClient.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)

	def turnOnMotor(self):
		self.updateMotorDesiredStatus(1)

	def turnOffMotor(self):
		self.updateMotorDesiredStatus(0)

	def deltaGetShadow(self):
		# Listen on deltas
		self.shadowClient.shadowRegisterDeltaCallback(customShadowCallback_Delta)
		
	def getShadow(self):
		self.shadowClient.shadowGet(customShadowCallback_Get, 5)


def initialize(host,rootCAPath,certificatePath,privateKeyPath):

	# Configure logging
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)

	# Init AWSIoTMQTTShadowClient
    #see aws-iot-device-sdk-python/AWSIoTPythonSDK/core/shadow
	myAWSIoTMQTTShadowClient = None
	myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowDeltaListener")
	myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	# AWSIoTMQTTShadowClient configuration
	myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

	# Connect to AWS IoT
	myAWSIoTMQTTShadowClient.connect()

	# initialize PandaBot object
	myPandaBot = PandaBot(myAWSIoTMQTTShadowClient)
	
	# Delete shadow
	myPandaBot.shadowClient.shadowDelete(customShadowCallback_Delete, 5)
		
	# Set motor off in shadow
	myPandaBot.updateMotorDesiredStatus(0)
	
	# Get as a sanity check
	myPandaBot.getShadow()
	
	print("Initialization complete")
	
	return myPandaBot
	
	


#if __name__ == "__main__":
	#main()
