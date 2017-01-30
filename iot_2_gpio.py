#!/usr/bin/env python

import sys
import os
import basicShadowDeltaListener_panda
import basicShadowUpdater_panda
import shadow_pubsub

# Requires certificate directory containing root-CA.crt, pandaDanceMotor.cert.pem, and pandaDanceMotor.private.key
endpoint='a2rig0317k0i1k.iot.us-east-1.amazonaws.com'
rootCA='/home/ljarin/pandabot/certificate/root-CA.crt'
cert='/home/ljarin/pandabot/certificate/pandaDanceMotor.cert.pem'
key='/home/ljarin/pandabot/certificate/pandaDanceMotor.private.key'


myPandaBot=shadow_pubsub.initialize(endpoint,rootCA,cert,key)
while True:
	myPandaBot.listen()



