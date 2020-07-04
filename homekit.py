import logging
import signal
import random

from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB
import pyhap.loader as loader
from pyhap.accessory_driver import AccessoryDriver
from gpiozero import RGBLED
from colorzero import Color

led = RGBLED(26, 6, 5, active_high=True, initial_value=Color(130, 200, 40))
logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")


class Nightlight(Accessory):
    """Implementation of a mock light accessory."""

    category = CATEGORY_LIGHTBULB  # This is for the icon in the iOS Home app.

    def __init__(self, *args, **kwargs):
        """Here, we just store a reference to the on and brightness characteristics and
        add a method that will be executed every time their value changes.
        """
        # If overriding this method, be sure to call the super's implementation first.
        super().__init__(*args, **kwargs)

        # Setup the Bulb
        serv_light = self.add_preload_service(
            'Lightbulb', chars=['On', 'Hue', 'Saturation', 'Brightness'])

        # Configure our callbacks
        self.char_hue = serv_light.configure_char(
            'Hue', setter_callback=self.set_hue)
        self.char_saturation = serv_light.configure_char(
            'Saturation', setter_callback=self.set_saturation)
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_state)
        self.char_on = serv_light.configure_char(
            'Brightness', setter_callback=self.set_brightness)

        # Set our instance variables
        self.accessory_state = 0  # State of the nightlight - On/Off
        self.hue = 0  # Hue Value 0 - 360 Homekit API
        self.saturation = 100  # Saturation Values 0 - 100 Homekit API
        self.brightness = 100  # Brightness value 0 - 100 Homekit API

    def set_state(self, value):
        self.accessory_state = value
        if value == 1:  # On
            self.set_hue(self.hue)
        else:
            self.update_color(0, 0, 0)  # Off

    def set_hue(self, value):
        # Lets only write the new RGB values if the power is on
        # otherwise update the hue value only
        if self.accessory_state == 1:
            self.hue = value
            rgb_tuple = self.hsv_to_rgb(
                self.hue, self.saturation, self.brightness)
            if len(rgb_tuple) == 3:
                self.update_color(
                    rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])
        else:
            self.hue = value

    def set_brightness(self, value):
        self.brightness = value
        self.set_hue(self.hue)

    def set_saturation(self, value):
        self.saturation = value
        self.set_hue(self.hue)

    def update_color(self, red, green, blue):
        led.color = Color(red, green, blue)

    def hsv_to_rgb(self, h, s, v):
        """
        This function takes
         h - 0 - 360 Deg
         s - 0 - 100 %
         v - 0 - 100 %
        """

        hPri = h / 60
        s = s / 100
        v = v / 100

        if s <= 0.0:
            return int(0), int(0), int(0)

        C = v * s  # Chroma
        X = C * (1 - abs(hPri % 2 - 1))

        rgb_pri = [0.0, 0.0, 0.0]

        if 0 <= hPri <= 1:
            rgb_pri = [C, X, 0]
        elif 1 <= hPri <= 2:
            rgb_pri = [X, C, 0]
        elif 2 <= hPri <= 3:
            rgb_pri = [0, C, X]
        elif 3 <= hPri <= 4:
            rgb_pri = [0, X, C]
        elif 4 <= hPri <= 5:
            rgb_pri = [X, 0, C]
        elif 5 <= hPri <= 6:
            rgb_pri = [C, 0, X]
        else:
            rgb_pri = [0, 0, 0]

        m = v - C

        return int((rgb_pri[0] + m) * 255), int((rgb_pri[1] + m) * 255), int((rgb_pri[2] + m) * 255)

    # The `stop` method can be `async` as well
    def stop(self):
        """We override this method to clean up any resources or perform final actions, as
        this is called by the AccessoryDriver when the Accessory is being stopped.
        """
        led.off()
        print('Stopping accessory.')


def get_accessory(driver):
    """Call this method to get a standalone Accessory."""
    return Nightlight(driver, 'nightlight')


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)

# Change `get_accessory` to `get_bridge` if you want to run a Bridge.
driver.add_accessory(accessory=get_accessory(driver))

# We want SIGTERM (terminate) to be handled by the driver itself,
# so that it can gracefully stop the accessory, server and advertising.
signal.signal(signal.SIGTERM, driver.signal_handler)

# Start it!
driver.start()
