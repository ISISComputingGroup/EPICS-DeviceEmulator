from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from utils import Channel, StatusRegister, ScanTrigger
from buffer import Buffer


class SimulatedKeithley2001(StateMachineDevice):
    """
    Simulated Keithley2700 Multimeter
    """
    number_of_times_device_has_been_reset = 0


    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.idn = "KEITHLEY INSTRUMENTS INC.,MODEL 2001,4301578,B17  /A02  "
        self.elements = {
            "READ": False, "CHAN": False, "RNUM": False, "UNIT": False, "TIME": False, "STAT": False
        }
        self._channel_readback_format = None

        self.buffer = Buffer()
        self.status_register = StatusRegister()

        self.scan_count = 0
        self._scan_trigger_type = ScanTrigger.IMM
        self.measurement_scan_count = 0

        self.continuous_initialisation_status = False
        self._channels = {
            1: Channel(1),
            2: Channel(2),
            3: Channel(3),
            4: Channel(4),
            5: Channel(5),
            6: Channel(6),
            7: Channel(7),
            8: Channel(8),
            9: Channel(9),
            10: Channel(10)
        }
        self.closed_channel = None
        self._error = [0, "No Error"]

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def reset_device(self):
        """
        Resets device to initialized state.

        This does not reset the buffer or status register.
        """

        for element in self.elements:
            self.elements[element] = False

        self.continuous_initialisation_status = False

        self._channels = {
            1: Channel(1),
            2: Channel(2),
            3: Channel(3),
            4: Channel(4),
            5: Channel(5),
            6: Channel(6),
            7: Channel(7),
            8: Channel(8),
            9: Channel(9),
            10: Channel(10)
        }
        self.closed_channel = None
        self._scan_trigger_type = ScanTrigger.IMM
        self.clear_error()

        SimulatedKeithley2001.number_of_times_device_has_been_reset += 1

    def close_channel(self, channel):
        """
        Closes channel to read from and opens the previously closed channel.

        Args:
            channel (int): Channel number to close.
                Valid channels are 1,2,3,4,5,6,7,8,9,10.

        Raises:
            ValueError if channel is not a valid channel.
        """

        channel = int(channel)
        try:
            if self.closed_channel != channel:
                if self.closed_channel is not None:
                    self._channels[self.closed_channel].close = False
                self._channels[channel].close = True
                self.closed_channel = channel
        except KeyError:
            raise ValueError("Channel {} is not a valid channel".format(channel))

    def take_single_reading(self):
        """
        Takes a single reading from the closed channel.

        Returns:
            dict: closed channel reading data containing
                READ: channel reading
                CHAN: Channel number
                UNIT: channel reading unit
        """

        channel = self._channels[self.closed_channel]
        return {
            "READ": channel.reading,
            "CHAN": channel.channel,
            "READ_UNIT": channel.reading_units.name
            }

    @property
    def scan_trigger_type(self):
        """
        Returns name of the scan trigger type.
        """
        return self._scan_trigger_type.name

    def scan_channels(self):
        """
        Generates buffer of readings.

        Each element of the buffer is a dictinoary of values
        generated from the channel.

        """
        for channel_to_scan in self.buffer.scan_channels:
            channel = self._channels[int(channel_to_scan)]
            self.buffer.buffer.append({
                "READ": channel.reading,
                "CHAN": channel.channel,
                "READ_UNIT": channel.reading_units.name
            })

    def clear_error(self):
        """
        Clears any error
        """
        self._error = [0, "No Error"]

    # Backdoor functions
    def get_number_of_times_buffer_has_been_cleared_via_the_backdoor(self):
        """
        Gets the number of times the buffer has been cleared.
        Only called via the backdoor.

        Returns:
            int: Number of times the buffer has been cleared.
        """

        return self.buffer.number_of_times_buffer_cleared

    def get_number_of_times_status_register_has_been_reset_and_cleared_via_the_backdoor(self):
        """
       Gets the number of times the status register has been reset and cleared.

       Only called via the backdoor.

       Returns:
           int: Number of times the status register has been reset and cleared.
       """

        return self.status_register.number_of_times_reset_and_cleared

    def set_channel_value_via_the_backdoor(self, channel, value):
        """
        Sets a channel value using Lewis backdoor.

        rgs:
            channel (int): Channel number 1,2,3,4,6,7,8, or 9.
            value (float): Value to set the channel to
        """
        self._channels[channel].reading = value

    def set_error_via_the_backdoor(self, error_code, error_message):
        """
        Sets an error via the using Lewis backdoor.

        Args:
            error_code (string): error code number
            error_message (string): error message

        Returns:

        """
        self._error = [int(error_code), error_message]

    @property
    def error(self):
        """
        Returns the current error status.

        Returns:
            list [int, string]: list of integer error code and error message.
        """

        return self._error
