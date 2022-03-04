#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path, RPi.GPIO, random, subprocess, time

RPi.GPIO.setmode(RPi.GPIO.BCM)

# Match GPIO channel numbers with actually wired hardware
audio_files_by_channel_number = {
	14: ['4_robotic.mp3'],
	15: ['4_angry.mp3'],
	18: ['4_flirty.mp3'],
	23: ['4_gossip.mp3']}

def play(channel_number):
	directory_of_script = os.path.dirname(os.path.realpath(__file__))  # Get the directory name of this script
	audio_file = random.choice(audio_files_by_channel_number[channel_number])  # Pick a random audio file
	path_to_file = os.path.join(directory_of_script, 'audio', audio_file)  # Compose the full path
	print('Playing {}'.format(path_to_file))
	subprocess.Popen(['/home/pi/dbuscontrol.sh', 'stop'])  # Stop any playing audio file
	subprocess.Popen(['omxplayer', '--adev', 'both', path_to_file], stdout=subprocess.DEVNULL)  # Play the audio file, minimize verbosity

def push_button_down(channel_number):
	if RPi.GPIO.input(channel_number) == False:
		print('Push button {} pressed.'.format(channel_number))
		play(channel_number)
	
for push_button, audio_files in audio_files_by_channel_number.items():  # Iterate over keys and values in dictionary
	RPi.GPIO.setup(push_button, RPi.GPIO.IN, RPi.GPIO.PUD_UP)  # Set GPIO as input and enable internal pull up resistor
	RPi.GPIO.add_event_detect(push_button, RPi.GPIO.FALLING, callback = push_button_down, bouncetime = 200)  # Call the funtction push_button_down when a button was pressed

def main():
	play(list(audio_files_by_channel_number.keys())[0])
	try:
		while True:
			time.sleep(10)

	except KeyboardInterrupt:  # Control-C was pressed
		pass

	RPi.GPIO.cleanup()
	print('\nBye, bye.')

if __name__ == '__main__':
	main()

"""
Requirements
============

    - omxplayer for playing audio files
    - RPi.GPIO for interacting with buttons and 
    - dbuscontrol.sh to control omxplayer


Installation instructions
=========================

# Update packages (only updates the info about the installed software)

    sudo apt-get update

# Upgrade all packages (actually updates the installed software)

    sudo apt-get upgrade

# Install omxplayer

    sudo apt-get install omxplayer

# Install RPi.GPIO
    sudo apt-get install rpi.gpio

# Copy dbuscontrol.sh to current directory (should be /home/pi)
	
	wget https://raw.githubusercontent.com/popcornmix/omxplayer/master/dbuscontrol.sh


Enabeling autoplay on start up
==============================

Edit rc.local

	sudo nano /etc/rc.local

and add the line

	su pi -c 'python3 /home/pi/audio_player.py &'

just before the (existing) line

	exit 0
"""
