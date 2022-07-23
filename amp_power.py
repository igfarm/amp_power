from enum import Enum
import time
import subprocess
import re
import logging
import sys

STEAM_PROC = '/proc/asound/card2/stream0'
KASA_DEVICE = 'Amplifier'

KASA_AMP_CMD = ['kasa', '--type', 'plug', '--alias', KASA_DEVICE]

class State(Enum):
	UNKNOWN = 'unkown'
	OFF = 'off'
	ON = 'on'

#
# Here we look for the playback status
#	$ cat /proc/asound/card2/stream0
#	MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio
#	Playback:
#	  Status: Running
#	    ...
#
def getSoundState() :
    state = State.ON;
    
    file = open(STEAM_PROC)
    data = file.read()
    file.close()
    
    result = re.search("Playback:\s+Status:\s+(Running|Stop)", data)
    if result is not None:
	    match result.group(1):
	    	case 'Running':
	    		state = State.ON
	    	case 'Stop':
	    		state = State.OFF
        
    #log.info("Sound is " + str(state))
    return state;

#
# Here we look for the AMP state
#
#	$ kasa --type plug --alias "Amplifier" state
#	Alias is given, using discovery to find host Amplifier
#	Found hostname is 192.168.86.29
#	== Amplifier - HS103(US) ==
#		Host: 192.168.86.29
#		Device state: ON
#		...
#
def getAmpState() :
    state = State.UNKNOWN
    
    cmd = KASA_AMP_CMD.copy()
    cmd.append('state')
    data = subprocess.check_output(cmd)

    result = re.search("Device state: (ON|OFF)", str(data))
    if result is not None:
	    match result.group(1):
	    	case 'ON':
	    		state = State.ON
	    	case 'OFF':
	    		state = State.OFF
    
    log.info("Amp is " + str(state))
    return state;

#
# Set the AMP state
#
#	$ kasa --type plug --alias "Amplifier" on
#	Alias is given, using discovery to find host Amplifier
#	Found hostname is 192.168.86.29
#	...
#
def setAmpState(state) :
	if (state == State.UNKNOWN):
		return
	log.info("Setting Amp to " + str(state))

	cmd = KASA_AMP_CMD.copy()
	cmd.append(str(state.value))
	
	subprocess.check_output(cmd)

#
#	Main loop
#
if __name__ == '__main__':
	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
	log = logging.getLogger("amp_power")
	log.info("Starting")

	sound_prev_state = State.UNKNOWN;
	while (True) :
		sound_new_state = getSoundState();
		if sound_new_state == State.UNKNOWN:
			log.error("Unable to get sound state")
			sys.exit()
		elif sound_prev_state != sound_new_state:
			log.info("Sound changed from " + str(sound_prev_state) + " to " + str(sound_new_state));
			amp_state = getAmpState()
			if amp_state == State.UNKNOWN:
				log.error("Unable to get amp state")
				sys.exit()
			elif amp_state != sound_new_state:
				setAmpState(sound_new_state)
			else:
				log.info("Amp is already " + str(sound_new_state))

		sound_prev_state = sound_new_state
		time.sleep(1)
