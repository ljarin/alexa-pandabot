#!/usr/bin/env python

import shadow_pubsub
import os.path

# Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key
home=os.path.expanduser('~')
endpoint='a2rig0317k0i1k.iot.us-east-1.amazonaws.com'
rootCA=home+'/pandabot/certificate/root-CA.crt'
cert=home+'/pandabot/certificate/pandaDanceMotor.cert.pem'
key=home+'/pandabot/certificate/pandaDanceMotor.private.key'


myPandaBot=shadow_pubsub.initialize(endpoint,rootCA,cert,key)
myPandaBot.turnOnMotor()
while True:
	myPandaBot.deltaGetShadow()



