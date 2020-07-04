from pyhap.accessory import Accessory
from pyhap.const import Category
import pyhap.loader as loader


class Light(Accessory):
    """Implementation of a mock light accessory."""

    category = Category.CATEGORY_LIGHTBULB  # This is for the icon in the iOS Home app.

    def __init__(self, *args, **kwargs):
        """Here, we just store a reference to the on and brightness characteristics and
        add a method that will be executed every time their value changes.
        """
        # If overriding this method, be sure to call the super's implementation first.
        super().__init__(*args, **kwargs)

        # Add the services that this Accessory will support with add_preload_service here
        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char('On', value=self._state)
        self.char_brightness = serv_light.configure_char('Brightness', value=100)

        serv_light.setter_callback = self._set_chars

    def _set_chars(self, char_values):
        """This will be called every time the value of the on of the
        characteristics on the service changes.
        """
        if "On" in char_values:
            print('On changed to: ', char_values["On"])
        if "Brightness" in char_values:
            print('Brightness changed to: ', char_values["Brightness"])

    @Acessory.run_at_interval(3)  # Run this method every 3 seconds
    # The `run` method can be `async` as well
    def run(self):
        """We override this method to implement what the accessory will do when it is
        started.

        We set the current temperature to a random number. The decorator runs this method
        every 3 seconds.
        """
        self.char_on.set_value(random.randint(0, 1))
        self.char_brightness.set_value(random.randint(1, 100))

    # The `stop` method can be `async` as well
    def stop(self):
        """We override this method to clean up any resources or perform final actions, as
        this is called by the AccessoryDriver when the Accessory is being stopped.
        """
        print('Stopping accessory.')