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
		if 'reported' in payload: state_modifier='reported'
		elif 'desired' in payload: state_modifiter='desired'
		else: state_modifier = 'error'
		print("motor: " + str(payloadDict["state"][state_modifier]["motor"]))
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
		

def make_shadow_client(host,rootCAPath,certificatePath,privateKeyPath):

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

	print("Shadow client initialization complete")
	
	return myAWSIoTMQTTShadowClient
	
	


#if __name__ == "__main__":
	#main()
