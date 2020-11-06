from lewis.devices import StateMachineDevice
from .states import DefaultState
from collections import OrderedDict


class SmrtmonValue:
    def __init__(self, name):
        self.name = name
        self._stat = 0.0
        self.lims = 0.0
        self.oplm = 0.0

    @property
    def stat(self):
        """
        Returns: the Setpoint Voltage
        """
        return self._stat

    @stat.setter
    def stat(self, stat):
        """
        :param setpoint_voltage: set the Setpoint Voltage
        :return:
        """
        self._stat = stat


class SimulatedSmrtmon(StateMachineDevice):
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.stat = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.oplm = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.lims = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

    def set_stat(self, num_stat, stat_value):
        self.stat[num_stat] = stat_value

    def set_oplm(self, num_oplm, oplm_value):
        self.oplm[num_oplm] = oplm_value

    def set_lims(self,num_lims, lims_value):
        self.lims[num_lims] = lims_value

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

