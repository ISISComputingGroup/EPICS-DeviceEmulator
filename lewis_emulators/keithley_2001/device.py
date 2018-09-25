from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from utils import Channel, ContScanningStatus
from Buffer import Buffer


class SimulatedKeithley2001(StateMachineDevice):
    """
    Simulated Keithley2700 Multimeter
    """
    number_of_times_reset = 0

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.idn = "KEITHLEY INSTRUMENTS INC.,MODEL 2001,4301578,B17  /A02  "
        self.elements = {
            "READ": False, "CHAN": False, "RNUM": False, "UNIT": False, "TIME": False, "STAT": False
        }
        self.buffer = Buffer()
        self._continuous_scanning_status = ContScanningStatus.OFF

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
        """
        for element in self.elements:
            self.elements[element] = False
        SimulatedKeithley2001.number_of_times_reset += 1

    def get_number_of_times_buffer_has_been_cleared(self):
        return self.buffer.number_of_times_buffer_cleared

    @property
    def continuous_scanning_status(self):
        """
        Returns status of continuous initialization mode.
        """
        return self._continuous_scanning_status.name

    @continuous_scanning_status.setter
    def continuous_scanning_status(self, value):
        try:
            self._continuous_scanning_status = ContScanningStatus[value]
        except KeyError:
            raise ValueError("{} is not a valid argument.".format(value))
