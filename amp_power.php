<?php

define('STEAM_PROC', '/proc/asound/card2/stream0');
define('KASA_AMP_CMD', 'kasa --type plug --alias "Amplifier" ');

enum State
{
	case UNKNOWN;
	case OFF;
	case ON;

	public function label(): string {
        return match($this) 
        {
            State::UNKNOWN => 'unkown',   
            State::OFF => 'off',   
            State::ON => 'on',   
        };
		
	}
}

/*
	Main loop
*/
$sound_prev_state = State::UNKNOWN;
while(true) {
	 $sound_new_state = getSoundState();
	
	if ($sound_new_state != State::UNKNOWN  &&
	   $sound_prev_state != $sound_new_state) {
	
		$amp_state = getAmpState();
		
		if ($amp_state != State::UNKNOWN  && 
			$amp_state != $sound_new_state) {
			setAmpState($sound_new_state);
			sleep(1);
		}
	}
	$sound_prev_state = $sound_new_state;
	sleep(1);
}

/*
Here we look for the playback status

	ubuntu@camilla:~$ head /proc/asound/card2/stream0
	MOTU M4 at usb-0000:01:00.0-1.3, high speed : USB Audio

	Playback:
	  Status: Running
	    ...

*/
function getSoundState() {
	$state = State::UNKNOWN;
	$data = shell_exec('head ' . STEAM_PROC);
	if (preg_match("/Status: (.+)/", $data, $match)) {
		$state = match($match[1]) {
			"Running" => State::ON,
			"Stop" => State::OFF,
			default => State::UNKNOWN
		};
	}
		
	print("Sound state is  " . $state->label() ."\n");
	return $state;
}


/*
Here we look for the AMP state

	ubuntu@camilla:~$ kasa --type plug --alias "Amplifier" state
	Alias is given, using discovery to find host Amplifier
	Found hostname is 192.168.86.29
	== Amplifier - HS103(US) ==
		Host: 192.168.86.29
		Device state: ON
		...
*/

function getAmpState() {
	$state = State::UNKNOWN;
	$data = shell_exec(KASA_AMP_CMD . 'state');
	if (preg_match("/Device state: (.+)/", $data, $match)) {

		$state = match($match[1]) {
			"ON" => State::ON,
			"OFF" => State::OFF,
			default => State::UNKNOWN
		};
	}

	print("Amp state is  " . $state->label() ."\n");
	return $state;
}

function setAmpState($state) {
	print("Setting Amp state to  " . $state->label() ."\n");
	shell_exec(KASA_AMP_CMD . $state->label());
}




