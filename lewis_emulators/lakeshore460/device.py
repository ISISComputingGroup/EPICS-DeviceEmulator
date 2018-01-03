from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class Channel(object):

    def __init__(self):
        self.field_reading = 0.8884
        self.field_multiplier = "u"
        self.max_hold_reading = 0.1234
        self.max_hold_multiplier = "m"
        self.rel_mode_reading = 0.5645
        self.rel_mode_multiplier = "m"
        self.mode = 0
        self.prms = 0
        self.filter_status = 0
        self.rel_mode_status = 0
        self.auto_mode_status = 0
        self.max_hold_status = 0
        self.channel_status = 0
        self.filter_windows = 5
        self.filter_points = 32
        self.manual_range = 1
        self.relative_setpoint = 1.123
        self.relative_setpoint_multiplier = "u"


class SimulatedLakeshore460(StateMachineDevice):
    """
    Simulated Lakeshore 460
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self.idn = "LSCI,MODEL460,0,22323"
        self.source = 1
        self.channels = {"X": Channel(), "Y":Channel(), "Z": Channel(), "V": Channel()}
        self.channel = "X"
        self.unit = "T"

    def _get_state_handlers(self):
        """
        Returns: states and their names
        """
        return {DefaultState.NAME: DefaultState()}

    def _get_initial_state(self):
        """
        Returns: the name of the initial state
        """
        return DefaultState.NAME

    def _get_transition_handlers(self):
        """
        Returns: the state transitions
        """
        return OrderedDict()

    @property
    def idn(self):
        """
        Returns: the IDN of device
        """
        return self._idn

    @idn.setter
    def idn(self, idn):
        """
        :param: idn:sets the IDN of device
        """
        self._idn = idn

    @property
    def source(self):
        """
        :return:  Returns magnetic field source XYZ, XYZ
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        :param source: Sets magnetic field source XYZ, XYZ
        """
        self._source = source

    @property
    def channel(self):
        """
        :return: returns the channel value i.e Channel X, Channel Y
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        """
        :param channel:  sets channel i.e Channel X, Channel Y
        """
        self._channel = channel

    @property
    def field_reading(self):
        """
        :return: Magnetic field Reading
        """
        return self.channels[self._channel].field_reading

    @field_reading.setter
    def field_reading(self, field):
        """
        :param field: sets Magnetic Field Reading
        """
        self.channels[self._channel].field_reading = field

    @property
    def field_multiplier(self):
        """
        :return: Returns Magnetic Field Multiplier
        """
        return self.channels[self._channel].field_multiplier

    @field_multiplier.setter
    def field_multiplier(self, multiplier):
        """
        :param multiplier:  Sets Magnetic field multiplier i.e micro, kilo, etc.
        """
        self.channels[self._channel].field_multiplier = multiplier

    @property
    def relative_setpoint_multiplier(self):
        """
        :return: Returns relative setpoint multiplier
        """
        return self.channels[self._channel].relative_setpoint_multiplier

    @relative_setpoint_multiplier.setter
    def relative_setpoint_multiplier(self, multiplier):
        """
        :param multiplier:  Sets relative setpoint multiplier i.e micro, kilo, etc.
        """
        self.channels[self._channel].relative_setpoint_multiplier = multiplier

    @property
    def max_hold_reading(self):
        """
        :return: returns max reading for Lakeshore 460
        """
        return self.channels[self._channel].max_hold_reading

    @max_hold_reading.setter
    def max_hold_reading(self, reading):
        """
        :param reading:  sets relative mode reading for device
        """
        self.channels[self._channel].max_hold_reading = reading

    @property
    def max_hold_multiplier(self):
        """
        :return: returns max hold reading multiplier
        """
        return self.channels[self._channel].max_hold_multiplier

    @max_hold_multiplier.setter
    def max_hold_multiplier(self, reading):
        """
        :param reading:  sets max hold reading multiplier
        """
        self.channels[self._channel].max_hold_multiplier = reading

    @property
    def rel_mode_reading(self):
        """
        :return: returns relative mode reading for Lakeshore 460
        """
        return self.channels[self._channel].rel_mode_reading

    @rel_mode_reading.setter
    def rel_mode_reading(self, rel_mode):
        """
        :param rel_mode: sets relative mode reading
        """
        self.channels[self._channel].rel_mode_reading = rel_mode

    @property
    def rel_mode_multiplier(self):
        """
        :return:  return relative mode multiplier
        """
        return self.channels[self._channel].rel_mode_multiplier

    @rel_mode_multiplier.setter
    def rel_mode_multiplier(self, multiplier):
        """
        :param multiplier:  sets the relative mode multiplier for the device
        """
        self.channels[self._channel].rel_mode_multiplier = multiplier

    @property
    def unit(self):
        """
        :return: unit for the device
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        :param unit: set unit for the device
        """
        self._unit = unit

    @property
    def mode(self):
        """
        :return: AC or DC unit of measurement
        """
        return self.channels[self._channel].mode

    @mode.setter
    def mode(self, mode):
        """
        :param mode: sets the device mode, if device is set to AC or DC measurement
        """
        self.channels[self._channel].mode = mode

    @property
    def prms(self):
        """
        :return: Peak /RMS Field reading
        """
        return self.channels[self._channel].prms

    @prms.setter
    def prms(self, prms):
        """
        :param prms: Sets the value to Peak or RMS
        """
        self.channels[self._channel].prms = prms

    @property
    def filter_status(self):
        """
        :return: returns filter status
        """
        return self.channels[self._channel].filter_status

    @filter_status.setter
    def filter_status(self, state):
        """
        :param filter_status:  sets filter state (binary)
        """
        self.channels[self._channel].filter_status = state

    @property
    def rel_mode_status(self):
        """
        :return: Return relative mode reading
        """
        return self.channels[self._channel].rel_mode_status

    @rel_mode_status.setter
    def rel_mode_status(self, rel_mode):
        """
        :param rel_mode_status:  Sets the relative mode status
        """
        self.channels[self._channel].rel_mode_status = rel_mode

    @property
    def auto_mode_status(self):
        """
        :return: Return auto mode status
        """
        return self.channels[self._channel].auto_mode_status

    @auto_mode_status.setter
    def auto_mode_status(self, auto_mode):
        """
        :param auto_mode_status:  Sets the auto mode status
        """
        self.channels[self._channel].auto_mode_status = auto_mode

    @property
    def max_hold_status(self):
        """
        :return: Return max hold status
        """
        return self.channels[self._channel].max_hold_status

    @max_hold_status.setter
    def max_hold_status(self, max_hold):
        """
        :param max_hold_status:  Sets max hold status
        """
        self.channels[self._channel].max_hold_status = max_hold

    @property
    def channel_status(self):
        """
        :return: status of device. If its on/off
        """
        return self.channels[self._channel].channel_

    @channel_status.setter
    def channel_status(self, status):
        """
        :param status: sets the device status, if device is on/off
        """
        self.channels[self._channel].channel_status = status

    @property
    def filter_windows(self):
        """
        :return: returns the percentage for display filter opening
        """
        return self.channels[self._channel].filter_windows

    @filter_windows.setter
    def filter_windows(self, percentage):
        """
        :param percentage: sets the percentage for display filter opening
        """
        self.channels[self._channel].filter_windows = percentage

    @property
    def filter_points(self):
        """
        :return: returns filter points value should be between 1 to 10
        """
        return self.channels[self._channel].filter_points

    @filter_points.setter
    def filter_points(self, points):
        """
        :param points: sets filter points value should be between 1 to 10
        """
        self.channels[self._channel].filter_points = points

    @property
    def manual_range(self):
        """
        :return: the value that has been set for the manual range
        """
        return self.channels[self._channel].manual_range

    @manual_range.setter
    def manual_range(self, range):
        """
        :param range: sets the manual range
        """
        self.channels[self._channel].manual_range = range

    @property
    def relative_setpoint(self):
        """
        :return: the relative setpoint value
        """
        return self.channels[self._channel].relative_setpoint

    @relative_setpoint.setter
    def relative_setpoint(self, rel_setpoint):
        """
        :param rel_setpoint: sets the relative mode setpoint
        """
        self.channels[self._channel].relative_setpoint = rel_setpoint