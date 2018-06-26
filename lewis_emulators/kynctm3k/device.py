from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core.logging import has_log


class SimulatedKynctm3K(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
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
        Formats a data output string given the current measurement values and program.

        Returns:
            formatted_data: String containing the measurement values for the current program

        """

        if self.OUT_values is None:
            return None
        else:
            channel_strings = []
            self.log.info(self.OUT_values)
            for channel, output_value in enumerate(self.OUT_values):
                if output_value is not False:
                    channel_strings.append("TG,{:02d},{:+08.3f}\r".format(channel+1, self.OUT_values[channel]))
                else:
                    continue

        self.log.info('channel strings ' + ''.join(channel_strings))
        return ''.join(channel_strings)
