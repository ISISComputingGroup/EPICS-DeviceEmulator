from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log

import random


class SimulatedKynctm3K(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.

        OUT_values contains the measurement values to be returned. A False value is considered to not
        be in the program, and will not be returned.
        """
        self.OUT_values = None

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

    @has_log
    def format_output_data(self):
        """
        Recalls and formats the measurement values

        Returns:
            A string containing the measurement values for the current program, formatted as per the user manual

        """

        out_of_range_return = "FFFFFFF"
        off_return = "XXXXXXXX"

        if self.OUT_values is None:
            return None
        else:
            channel_strings = ["MM,1111111111111111", ]
            for channel, output_value in enumerate(self.OUT_values):
                self.log.info(output_value)
                # Only return output if the OUT value is in the program

                if output_value == "off":
                    channel_strings.append(off_return)

                elif output_value == "out_of_range":
                    # Add a random sign to the out of range string
                    sign = random.sample(('+', '-'), 1)[0]
                    channel_strings.append(sign + out_of_range_return)

                elif type(output_value) is float:
                    channel_strings.append("{:+08.3f}".format(self.OUT_values[channel]))

                else:
                    channel_strings.append(off_return)

        self.log.info(self.OUT_values)
        self.log.info(','.join(channel_strings))

        return ','.join(channel_strings)
