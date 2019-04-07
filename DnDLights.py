#!/usr/bin/python
#
# -Port of the Arduino NeoPixel library strandtest example (Adafruit).
# -Uses the WS2811 to animate RGB light strings (I am using a 5V, 50x RGB LED strand)


# Import libs used
import time
import random
import getopt
import sys
from neopixel import *

#Start up random seed
random.seed()

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#Predefined Colors and Masks
OFF = Color(0,0,0)
WHITE = Color(255,255,255)
RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
PURPLE = Color(128,0,128)
YELLOW = Color(255,255,0)
ORANGE = Color(255,50,0)
TURQUOISE = Color(64,224,208)
RANDOM = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

FIRE_COLORS = [RED, ORANGE]

#bitmasks used in scaling RGB values
REDMASK = 0b111111110000000000000000
GREENMASK = 0b000000001111111100000000
BLUEMASK = 0b000000000000000011111111

# Other vars
LIGHT_ARRAY_LENGTH = 50
LIGHTSHIFT = 0  #shift the lights down the strand to the other end 
FLICKERLOOP = 3  #number of loops to flicker

def fireWall(strip):
  for i in range(0,LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(i, RED)

  strip.show()

  endTime = time.time() + 10.0

  while (endTime > time.time()):
    randomLedIndex = random.randint(0,LIGHT_ARRAY_LENGTH)

    #turn off for a random short period of time
    strip.setPixelColor(randomLedIndex, OFF)
    strip.show()
    time.sleep(random.randint(10,50)/1000.0)
    random_fire_color = random.randint(0,1)
    strip.setPixelColor(randomLedIndex, FIRE_COLORS[random_fire_color])
    strip.show()

  #kill all lights
  for led in range(0, LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(led+LIGHTSHIFT, OFF)
  strip.show()

def showPlayerColor(strip, color, duration):

  for i in range(0,LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(i, color)
  
  strip.show()

  time.sleep(duration)

  #kill all lights
  for led in range(0,LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(led+LIGHTSHIFT, OFF)
  strip.show()

def levelUp(strip, color):

  for i in range(0,LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(i, color)

  strip.show()

  endTime = time.time() + 10.0

  pixelIndex = 0
  forward = True
  while (endTime > time.time()):

    if (pixelIndex >= LIGHT_ARRAY_LENGTH-1):
      forward = False
    elif (pixelIndex <= 0):
      forward = True

    #turn off for a random short period of time
    strip.setPixelColor(pixelIndex, OFF)
    strip.setPixelColor(pixelIndex+1, OFF)
    strip.show()
    time.sleep(0.02)
    strip.setPixelColor(pixelIndex, color)
    strip.setPixelColor(pixelIndex+1, color)
    strip.show()

    if (forward):
      pixelIndex += 2
    else:
      pixelIndex -= 2


  #kill all lights
  for led in range(0, LIGHT_ARRAY_LENGTH):
    strip.setPixelColor(led+LIGHTSHIFT, OFF)
  strip.show()

def usage():
  print("DndLights.py -e <fire/bla/foo/yadalevelup>")
  print("DndLights.py --event fire")
  print("DndLights.py --event levelup -p <red/green/blue/purple/yellow/orange/turquoise>")
  print("DndLights.py -p <red/green/blue/purple/yellow/orange/turquoise> -t <seconds>")

def playerColorLookup(color):
    return {
        'red': RED,
        'green': GREEN,
        'blue': BLUE,
        'purple': PURPLE,
        'yellow': YELLOW,
        'orange': ORANGE,
        'turquoise': TURQUOISE
    }.get(color, WHITE) 

# Main program logic follows:
if __name__ == '__main__':
  eventName = ''
  playerColor = ''
  duration = 0.0
  try:
    opts, args = getopt.getopt(sys.argv[1:],"h:e:p:t",['help=', 'event=', 'playercolor=', 'time='])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      usage()
      sys.exit(2)
    elif opt in ('-e', '--event'):
      eventName = arg
    elif opt in ('-p', '--playercolor'):
      playerColor = arg
    elif opt in ('-t', '--time'):
      duration = float(arg)

	# Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
  strip.begin()

  print ('Press Ctrl-C to quit.')

  if (eventName == 'fire'):
    fireWall(strip)
  elif (eventName == 'levelup'):
    levelUp(strip, playerColorLookup(playerColor))
  elif (playerColor != ''):
    showPlayerColor(strip, playerColorLookup(playerColor), duration)
  else:
    print ("You didn't select a valid event!")
