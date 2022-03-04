import os
from markovbot import MarkovBot
import twitter
import time
import serial  # Used to communicate with the printer
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initilalise printer
# Create a connection to the printer
printer = serial.Serial('/dev/serial0', baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS, timeout=1)

RESET = b'\x1b\x40'

SELECT_PRINT_MODE = b'\x1b\x21'


FONT_A = 0
FONT_B = 1
BOLD = 8
DOUBLE_HEIGHT = 16
DOUBLE_WIDTH  = 32

SELECT_CHARACTER_SIZE = b'\x1d\x21'
NORMAL = b'\x00'
DOUBLE = b'\x11'
TRIPLE = b'\x22'

printer.write(RESET)
printer.write(SELECT_PRINT_MODE + bytes([FONT_A + BOLD]))  # Enabled emphasis (bold) mode


# Initialise a MarkovBot instance
tweetbot = MarkovBot()

# Get the current directory's path
dirname = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the book
book = os.path.join(dirname, 'porno.txt')

# Make your bot read the book!
tweetbot.read(book)

while True:
	input_state = GPIO.input(18)
	if input_state == False:
		my_first_text = tweetbot.generate_text(30, seedword=['I', 'want'])
		# print("")
		# print(my_first_text)
		# print("")
		printer.write('\n\n\n{}\n\n\n\n\n\n\n\n'.format(my_first_text).encode())
		time.sleep(0.2)

