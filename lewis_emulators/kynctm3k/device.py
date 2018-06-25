from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedKynctm3K(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.OUT_values = None
        self.program = None

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
        Formats a data output string given the current measurement values and program.

        Returns:
            formatted_data: String containing the measurement values for the current program

        """

        if self.program is None or self.OUT_values is None:
            return None
        else:
            channel_strings = []
            for channel, program_switch in enumerate(self.program):
                if program_switch == "1":
                    channel_strings.append("TG,{:02d},{:+06.3f}\r".format(channel, self.OUT_values[channel]))
                else:
                    continue

        return ''.join(channel_strings)
