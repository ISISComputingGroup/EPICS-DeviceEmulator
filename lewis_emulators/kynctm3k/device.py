from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log

import random


def truncate_if_set(function):
    """
    Truncates the decorated function's string output if truncated_output is True

    """

    def wrapper(self, *args, **kwargs):
        output = function(self, *args, **kwargs)

        if self.truncated_output:
            output = output[:int(round(len(output) / 2.))]

        return output

    return wrapper


@has_log
class SimulatedKynctm3K(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.

        OUT_values contains the measurement values to be returned. A False value is considered to not
        be in the program, and will not be returned.
        """
        self.OUT_values = None
        self.truncated_output = False

        pass

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def parse_status(self, output_setting):
        """
        Converts the status for one OUT channel to a formatted string
        Args:
            output_setting: String or float. If float, then output is on. If off or out_of_bounds, then a formatted string will be returned

        Returns:
            OUT_string: String. Contains the measurement value if on, or XXXXXXXX/FFFFFFF as appropriate if off or out of range

        """
        out_of_range_return = "FFFFFFF"
        off_return = "XXXXXXXX"

        if output_setting == "off":
            return off_return

        elif output_setting == "out_of_range":
            # Add a random sign to the out of range string
            sign = random.sample(('+', '-'), 1)[0]
            return sign + out_of_range_return

        elif type(output_setting) is float:
            return "{:+08.3f}".format(output_setting)

        else:
            return off_return

    @truncate_if_set
    def format_output_data(self):
        """
        Recalls and formats the measurement values

        Returns:
            A string containing the measurement values for the current program, formatted as per the user manual

        """

        if self.OUT_values is None:
            return None
        else:
            channel_strings = ["MM,1111111111111111", ]
            for channel, output_value in enumerate(self.OUT_values):
                # Only return output if the OUT value is in the program
                channel_strings.append(self.parse_status(output_value))

        self.log.info(','.join(channel_strings))

        return ','.join(channel_strings)
