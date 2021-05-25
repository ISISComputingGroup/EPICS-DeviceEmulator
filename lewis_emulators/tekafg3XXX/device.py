from collections import OrderedDict
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SourceChannel:
    def __init__(self):
        self.on = True
        self.function = ""  # TODO
        self.normal_polarity = True
        self.burst_on = True
        self.burst_triggered = True
        self.impedance = 0
        self.voltage = 0
        self.voltage_units = ""  # TODO
        self.voltage_low_limit = 0
        self.voltage_low_level = 0
        self.voltage_high_limit = 0
        self.voltage_high_level = 0
        self.voltage_offset = 0
        self.frequency = 0
        self.phase = 0
        self.burst_num_cycles = 0
        self.burst_time_delay = 0
        self.frequency_mode = ""  # TODO
        self.sweep_span = 0
        self.sweep_start = 0
        self.sweep_stop = 0
        self.sweep_hold_time = 0
        self.sweep_mode = True  # TODO
        self.sweep_return_time = 0
        self.sweep_spacing = True  # TODO
        self.sweep_time = 0


class SimulatedTekafg3XXX(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.output_1 = SourceChannel()
        self.output_2 = SourceChannel()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

