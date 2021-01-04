#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import argparse
import sys
import time
import signal

def main(session):
    # Get the service ALTabletService.
    memory = session.service("ALMemory")
    subscriberweb = memory.subscriber("Web/Button1")
    subscriberweb.signal.connect(Web)
    tts = session.service("ALTextToSpeech")
    tts.setLanguage('English')
    
    tts.say("Hello, I don't know you, write your name on my tablet !")
    try:
        tabletService = session.service("ALTabletService")
        tabletService.loadApplication("Web")
        tabletService.showWebview()
        raw_input("\n press enter\n")

    except Exception, e:
        print "Error was: ", e

def Web(prenom):
    print "The name is :"
    print prenom
    tts = session.service("ALTextToSpeech")
    tts.setLanguage('English')
    tts.say("I learn your face" + prenom + "I hope to become your best friend, we will have a great time together")
    return prenom

if __name__ == "__main__":
    
    ip = "134.214.51.44"
    port = "9559"

    session = qi.Session()
    try:
        session.connect("tcp://" + ip + ":" + port)
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + port +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
