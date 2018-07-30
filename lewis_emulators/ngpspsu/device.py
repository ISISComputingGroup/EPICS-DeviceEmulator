from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice

# List of length 8 of lists of length 4 containing 1's and '0's.
# Each sublist represent 8 hexadecimal characters in terms of bits.
STATUS_SETUP = [["0" for _ in range(4)] for _ in range(8)]


class SimulatedNgpspsu(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self._model_no_and_firmware = "NGPS 100-50:0.9.01"
        self._status = STATUS_SETUP
        self._voltage = 0.0
        self._voltage_setpoint = 0.0
        self._current = 0.0
        self._current_setpoint = 0.0
        self._connected = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @property
    def model_number_and_firmware(self):
        """
        Returns the model number and firmware version.
        """

        return self._model_no_and_firmware

    @property
    def status(self):
        """
        Returns the status of the device as a 8 digit hexadecimal string.
        """

        status_as_eight_hex_digits = [hex(int("".join(word), 2))[2]
                                      for word in self._status]
        return "".join(status_as_eight_hex_digits)

    @property
    def voltage(self):
        """
        Returns device's current voltage to 6 decimal places.
        """

        return "{0:.6f}".format(self._voltage)

    @property
    def voltage_setpoint(self):
        """
        Returns device's last voltage setpoint to 6 decimal places.
        """

        return "{0:.6f}".format(self._voltage_setpoint)

    def try_setting_voltage_setpoint(self, value):
        """
        Sets the  device's setpoint voltage to 6 decimal places.
        """

        if self._status[0][3] == "0":
            return "#NAK:13"
        else:
            value = float(value)
            self._voltage_setpoint = value
            return "#AK"

    @property
    def current(self):
        """
        Returns device's current voltage to 6 decimal places.
        """

        return "{0:.6f}".format(self._current)

    @property
    def current_setpoint(self):
        """
        Returns device's last voltage setpoint to 6 decimal places.
        """

        return "{0:.6f}".format(self._current_setpoint)

    def try_setting_current_setpoint(self, value):
        """
        Sets the  device's setpoint voltage to 6 decimal places.
        """

        if self._status[0][3] == "0":
            return "#NAK:13"
        else:
            value = float(value)
            self._current_setpoint = value
            return "#AK"

    def start_device(self):
        """
        Turns on the device.

        Returns:
            string: "#AK" if successful. #NK:%i if not where %i is an error
                code.
        """
        if self._status[0][3] == '1':
            return "#NAK:09"
        elif self._status[0][3] == '0':
            self._status[0][3] = '1'
            return "#AK"
        else:
            return "#NAK99"

    def stop_device(self):
        """
        Turns off the device.

        Returns:
            string: "#AK" if successful. #NK:%i otherwise where %i is an error
                code.
        """
        if self._status[0][3] == '0':
            return "#NAK:13"
        elif self._status[0][3] == '1':
            self._status[0][3] = '0'
            return "#AK"
        else:
            return "#NAK99"

    def reset_device(self):
        """
        Resets the device.

        Returns:
            string: "#AK" if successful. #NK:%i otherwise where %i is an error
                code.
        """
        self._status = STATUS_SETUP
        self._voltage = 0
        self._voltage_setpoint = 0
        self._current = 0
        self._current_setpoint = 0
        return "#AK"

    @property
    def connected(self):
        """
        Returns True if the device is connected. False otherwise.
        """
        return self._connected

    def connect(self):
        """
        Connects the device.
        Returns:
            None
        """

        self._connected = True

    def disconnect(self):
        """
        Disconnects the device.

        Returns:
            None
        """

        self._connected = False


