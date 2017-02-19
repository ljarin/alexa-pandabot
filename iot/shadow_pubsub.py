'''
/*
 * AWSIotPythonSDK - AWSIoTMQTTShadowClient callback functions
 * Originally included as sample, but modified to allow callbacks to pass back information instead of just printing it.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient #Probably could use boto3 again instead? But I installed this already
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
class shadowCallbacks:
	def __init__(self):
		self.deltaPayload={}
		self.deltaStatus=0
		self.getPayload={}
		self.getStatus=0
	def customShadowCallback_Delta(self,payload, responseStatus, token):
		# payload is a JSON string ready to be parsed using json.loads(...)
		# in both Py2.x and Py3.x
		print("Delta request " + responseStatus)
		payloadDict = json.loads(payload)
		self.deltaPayload=payloadDict
		self.deltaStatus=1
		#print("++++++++DELTA++++++++++")
		#print("motor: " + str(payloadDict["state"]["motor"]))
		#print("version: " + str(payloadDict["version"]))
		#print("+++++++++++++++++++++++\n\n")

	def customShadowCallback_Get(self,payload, responseStatus, token):
		# payload is a JSON string ready to be parsed using json.loads(...)
		# in both Py2.x and Py3.x
		print("Get request " + responseStatus)
		payloadDict = json.loads(payload)
		self.getPayload=payloadDict
		self.getStatus=1
		#print("+++++++++ShadowGet+++++++++++")
		#print("motor: " + str(payloadDict["state"]["desired"]["motor"]))
		#print("version: " + str(payloadDict["version"]))
		#print("+++++++++++++++++++++++\n\n")
			
	def customShadowCallback_Update(self,payload, responseStatus, token):
		# payload is a JSON string ready to be parsed using json.loads(...)
		# in both Py2.x and Py3.x
		if responseStatus == "timeout":
			print("Update request " + token + " time out!")
		if responseStatus == "accepted":
			payloadDict = json.loads(payload)
			print("~~~~~~~~~~~~~~~~~~~~~~~")
			print("Update request with token: " + token + " accepted!")
			if 'reported' in payload: state_modifier='reported'
			elif 'desired' in payload: state_modifier='desired'
			else: state_modifier = 'error'
			print("motor: " + str(payloadDict["state"][state_modifier]["motor"]))
			print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
		if responseStatus == "rejected":
			print("Update request " + token + " rejected!")

	def customShadowCallback_Delete(self,payload, responseStatus, token):
		if responseStatus == "timeout":
			print("Delete request " + token + " time out!")
		if responseStatus == "accepted":
			print("~~~~~~~~~~~~~~~~~~~~~~~")
			print("Delete request with token: " + token + " accepted!")
			print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
		if responseStatus == "rejected":
			print("Delete request " + token + " rejected!")
		

def make_shadow_client(host,rootCAPath,certificatePath,privateKeyPath):

	# Configure logging
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.INFO)
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

	print("Shadow client initialization complete")
	
	return myAWSIoTMQTTShadowClient
	
