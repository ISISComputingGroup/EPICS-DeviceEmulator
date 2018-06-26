from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


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

    def format_output_data(self):
        """
        Recalls and formats the measurement values

        Returns:
            A string containing the measurement values for the current program, formatted as per the user manual

        """

        if self.OUT_values is None:
            return None
        else:
            channel_strings = []
            for channel, output_value in enumerate(self.OUT_values):
                # Only return output if the OUT value is in the program
                if output_value is not False:
                    channel_strings.append("TG,{:02d},{:+08.3f}\r".format(channel+1, self.OUT_values[channel]))
                else:
                    continue

        return ''.join(channel_strings)
