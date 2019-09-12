# Controllable-LED-Strip
A Gemma M0 controls a 30 pixel LED strip with custom animations mapped to the analog input from a potentiometer

Supplies:
  - [Gemma M0 Microcontroller](https://www.adafruit.com/product/3501)
  - [10k Potentiometer](https://www.adafruit.com/product/562?gclid=Cj0KCQjw2efrBRD3ARIsAEnt0eiVpuXrk4T1edEbNSqT1RYbQBknHH4lBoS_mDyq1fyyc574SFwEtukaAsoFEALw_wcB)
  - [1m NeoPixel LED strip 30 pixels/meter](https://www.adafruit.com/product/2954?length=1)
  - [10K Resistor]


## Light Modes

When the voltage reads between ~0.5-1.6 V, the user will be able to control the position of a pulsing light blob
```python
# create center point
pi = int(num_pixels*volts)

for j in range(num_pixels):
    if (j > pi-3) and (j < pi+3):
        pass
    else:
        y = sin( 6.28*abs(pi-j)/num_pixels - phase )
        if abs(y) > 0.2:
            pixels[j] = (0,0,0)
```

![](user_animation.gif)

When the voltage reads between 1.6-3.2 V square waves of different frequencies block pixels out and propagate
```python
for j in range(num_pixels):
    y = sin( 6.28*j/(num_pixels*volts) - phase )
    if abs(y) > 0.5:
        pixels[j] = (0,0,0)
```
![](led_animation.gif)

At high frequencies you get some cool aliasing effects that make the light strip look random
