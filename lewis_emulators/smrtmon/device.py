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
        self.temp1 = 0
        self.temp2 = SmrtmonValue("TEMP2")
        self.temp3 = SmrtmonValue("TEMP3")
        self.temp4 = SmrtmonValue("TEMP4")
        self.temp5 = SmrtmonValue("TEMP5")
        self.temp6 = SmrtmonValue("TEMP6")
        self.volt1 = SmrtmonValue("VOLT1")
        self.volt2 = SmrtmonValue("VOLT2")
        self.volt3 = SmrtmonValue("VOLT3")
        self.mi = 0
        self.status = 0

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

