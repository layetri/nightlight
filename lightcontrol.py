import time
from gpiozero import RGBLED
from colorzero import Color

led = RGBLED(26, 6, 5, active_high=True, initial_value=Color(130, 200, 40))
blinking = False

while 1:
    command = input(" -> ")

    if command == 'on':
        led.on()
    elif command == 'off':
        led.off()
    elif command == 'blink':
        if not blinking:
            blinking = True
            led.blink(fade_in_time=0.5, fade_out_time=0.3)
        else:
            blinking = False
            led.off()
    elif command == 'quit':
        led.off()
        exit()
