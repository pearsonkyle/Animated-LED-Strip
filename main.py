# Gemma IO demo
# Welcome to CircuitPython 2.2.4 :)

from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar as dotstar
from analogio import AnalogIn
from math import sin
import neopixel
import board

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Analog input on A2, linear potentiometer
ain = AnalogIn(board.A2)

num_pixels = 30
pixels = neopixel.NeoPixel(board.A1, num_pixels, brightness=0.3, auto_write=False)

# variables for animations
speed = 0.25 # time averaging and phase change speed
phase = 0    # animations depend on sin, analogous to a time
volts = 0    # normalized voltage level for different input modes
i = 0        # color index (0-255)


def getVoltage(pin):
    return (pin.value * 3.3) / 65536

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    if (pos < 0):
        return [0, 0, 0]
    if (pos > 255):
        return [0, 0, 0]
    if (pos < 85):
        return [int(pos * 3), int(255 - (pos*3)), 0]
    elif (pos < 170):
        pos -= 85
        return [int(255 - pos*3), 0, int(pos*3)]
    else:
        pos -= 170
        return [0, int(pos*3), int(255 - pos*3)]

def rainbow_cycle(offset):
    for i in range(num_pixels):
        rc_index = (i * 256 // num_pixels) + offset
        pixels[i] = wheel(rc_index % 255)
    #pixels.show()

def clamp(x,lo,up):
    if x > up: return up
    elif x< lo: return lo
    return x

while True:
    # spin internal LED around!
    dot[0] = wheel(i)
    dot.show()

    # linear potentiometer to LED strip
    voltIn = getVoltage(ain)

    # set base color of all pixels
    rainbow_cycle(i)

    # user control mode
    if voltIn > 1.6:

        # normalized voltage between 0-1, time averaged (smoothed)
        volts = ((1-speed)*volts + speed*(voltIn-1.6)/1.6)
        volts = clamp(volts,0,1)

        # create center point
        pi = int(num_pixels*volts)

        # send pulse
        for j in range(num_pixels):
            if (j > pi-3) and (j < pi+3):
                pass
            else:
                y = sin( 6.28*abs(pi-j)/num_pixels - phase )
                if abs(y) < 0.2:
                    pass
                else:
                    pixels[j] = (0,0,0)
    # wavy mode
    else:
        # scale between ~0-1
        volts = ((1-speed)*volts + speed*(voltIn-0.5))

        # propagate waves
        for j in range(num_pixels):
            #y = sin( 6.28*(0.5*num_pixels-abs(j-0.5*num_pixels))/(num_pixels*volts) - phase ) # converge toward center
            #y = sin( 6.28*(abs(j-0.5*num_pixels))/num_pixels - phase ) # diverge from center
            y = sin( 6.28*j/(num_pixels*volts) - phase )
            if abs(y) < 0.5:
                pass
            else:
                pixels[j] = (0,0,0)

    pixels.show()
    phase += speed
    phase = phase % 6.28
    i = (i+5) % 256


