#!/usr/bin/env python2
import subprocess
import os
import signal

from Reader import Reader

reader = Reader()
continue_reading = True

# get absolute path of this script
dir_path = os.path.dirname(os.path.realpath(__file__))


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    reader.reader.cleanup()


# Welcome message
print "Press Ctrl-C to stop."

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

maxtries = 3
tries = 0
prevcardid = "-1"

while continue_reading:
    # reading the card id
    cardid = reader.reader.read_card()
    if cardid is None:
       if tries <= maxtries:
          tries += 1
       else:
          cardid="NoCardId"
          tries = 0
    else:
       tries = 0
    
    # ToDo Handle second Swipe.. 
    if cardid != prevcardid and cardid is not None:
       prevcardid = cardid
       try:
          # start the player script and pass on the card id
          subprocess.call([dir_path + '/rfid_trigger_play.sh --cardid=' + cardid], shell=True)
       except OSError as e:
          print "Execution failed:" + str(e)
