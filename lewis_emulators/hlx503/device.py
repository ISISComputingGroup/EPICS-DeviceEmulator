from collections import OrderedDict
from lewis.core.logging import has_log
from .states import DefaultState
from lewis.devices import StateMachineDevice


class Channel:

    def __init__(self):
        self.temperature = 0
        self.temperature_sp = 0
        self.mode = 0
        self.heater_percent = 0.0
        self.heater_voltage = 0


class MagicBox:

    def __init__(self):
        self.sorb_channel = Channel()
        self.onekpot_channel = Channel()
        self.he3pothigh_channel = Channel()
        self.he3potlow_channel = Channel()
        self.port_channel_map = {
            1: self.sorb_channel,
            2: self.he3potlow_channel,
            3: self.he3pothigh_channel
        }
        self.channels = [self.sorb_channel, self.onekpot_channel, self.he3potlow_channel, self.he3pothigh_channel]

    def plug_in_onekpot(self):
        self.port_channel_map[1] = self.onekpot_channel

    def plug_in_he3potlow(self):
        self.port_channel_map[1] = self.he3potlow_channel

    def get_temperature(self, control_channel):
        return self.port_channel_map[control_channel].temperature

    def get_temperature_sp(self, control_channel):
        return self.port_channel_map[control_channel].temperature_sp

    def set_temperature_sp(self, control_channel, temp_sp):
        self.port_channel_map[control_channel].temperature_sp = temp_sp

    def get_mode(self, control_channel):
        return self.port_channel_map[control_channel].mode

    def set_mode(self, control_channel, new_mode):
        self.port_channel_map[control_channel].mode = new_mode

    def get_heater_voltage(self, control_channel):
        return self.port_channel_map[control_channel].heater_voltage

    def set_heater_voltage(self, control_channel, new_heater_voltage):
        self.port_channel_map[control_channel].heater_voltage = new_heater_voltage
        self.port_channel_map[control_channel].heater_percent = new_heater_voltage

    def get_heater_percent(self, control_channel):
        return self.port_channel_map[control_channel].heater_percent


@has_log
class SimulatedItc503(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.magic_box = MagicBox()
        self.p, self.i, self.d = 0, 0, 0
        self.control = 0
        self.control_channel = 1
        self.autopid = False
        self.sweeping = False

        # Set by tests, affects the response format of the device. Slightly different models of ITC will respond
        # differently
        self.report_sweep_state_with_leading_zero = False

    def _get_state_handlers(self):
        return {'default': DefaultState()}

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    @property
    def temperature_1(self):
        return self.magic_box.get_temperature(1)

    @property
    def temperature_2(self):
        return self.magic_box.get_temperature(2)

    @property
    def temperature_3(self):
        return self.magic_box.get_temperature(3)

    @property
    def temperature(self):
        return self.magic_box.get_temperature(self.control_channel)

    @property
    def temperature_sp(self):
        return self.magic_box.port_channel_map[self.control_channel].temperature_sp

    @temperature_sp.setter
    def temperature_sp(self, new_temperature):
        self.magic_box.set_temperature_sp(self.control_channel, new_temperature)

    @property
    def mode(self):
        return self.magic_box.get_mode(self.control_channel)

    @mode.setter
    def mode(self, new_mode):
        self.magic_box.set_mode(self.control_channel, new_mode)

    @property
    def heater_voltage(self):
        return self.magic_box.get_heater_voltage(self.control_channel)

    @heater_voltage.setter
    def heater_voltage(self, new_heater_voltage):
        self.magic_box.set_heater_voltage(self.control_channel, new_heater_voltage)

    @property
    def heater_percent(self):
        return self.magic_box.get_heater_percent(self.control_channel)

    def backdoor_plug_in_onekpot(self):
        self.magic_box.plug_in_onekpot()

    def backdoor_plug_in_he3potlow(self):
        self.magic_box.plug_in_he3potlow()

    def backdoor_set_port_temp(self, port, temp):
        self.magic_box.set_temperature_sp(port, temp)
