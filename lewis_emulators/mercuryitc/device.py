from __future__ import absolute_import, division, unicode_literals, print_function

from collections import OrderedDict
from lewis.core.logging import has_log
from .states import DefaultState
from lewis.devices import StateMachineDevice


class Channel(object):
    def __init__(self, nickname):
        super(Channel, self).__init__()
        self.nickname = nickname


class TemperatureChannel(Channel):
    def __init__(self, nickname):
        super(TemperatureChannel, self).__init__(nickname)
        self.channel_type = "TEMP"

        self.temperature = 0
        self.temperature_sp = 0
        self.resistance = 0
        self.calibration_file = "sim_calib_file"

        self.autopid = False
        self.autopid_file = "sim_autopid_file"
        self.p = 0
        self.i = 0
        self.d = 0

        self.gas_flow_auto = True
        self.gas_flow = 0
        self.heater_auto = True
        self.heater_percent = 0

        self.associated_heater_channel = None
        self.associated_aux_channel = None


class HeaterChannel(Channel):
    def __init__(self, nickname):
        super(HeaterChannel, self).__init__(nickname)
        self.channel_type = "HTR"

        self.power = 0
        self.voltage = 0
        self.current = 0
        self.voltage_limit = 0


class AuxChannel(Channel):
    def __init__(self, nickname):
        super(AuxChannel, self).__init__(nickname)
        self.channel_type = "AUX"

        self.percent_open = 0


@has_log
class SimulatedMercuryitc(StateMachineDevice):

    def _initialize_data(self):
        self.connected = True

        self.channels = {
            "MB0": TemperatureChannel("MB0.T0"),
            "DB0": HeaterChannel("DB0.H0"),
            "DB1": AuxChannel("DB0.A1"),
            "MB1": TemperatureChannel("MB1.T1"),
            "DB2": HeaterChannel("DB0.H1"),
            "DB3": AuxChannel("DB0.A0"),
        }

        # Associate each temperature channel with a heater and an auxilary channel:
        self.channels["MB0"].associated_heater_channel = "DB0"
        self.channels["MB0"].associated_aux_channel = "DB1"

        self.channels["MB1"].associated_heater_channel = "DB2"
        self.channels["MB1"].associated_aux_channel = "DB3"

    def reset(self):
        self._initialize_data()

    def _get_state_handlers(self):
        return {'default': DefaultState()}

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def backdoor_set_channel_property(self, chan_id, property_name, value):
        setattr(self.channels[chan_id], property_name, value)
