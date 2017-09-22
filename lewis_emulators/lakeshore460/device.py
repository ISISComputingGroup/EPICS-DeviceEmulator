from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class Channel(object):
    def __init__(self):
        self.display_filter_window = 0
        self.filter_points = 0
        self.manual_range = 0
        self.max_multiplier = "u"
        self.rel_multiplier = "u"
        self.magnetic_field_multiplier = "u"
        self.rel_mode_multiplier = "u"
        self.unit = "G"
        self.status = 0
        self.mode = 0
        self.prms = 0
        self.filter = 0
        self.max_hold = 0
        self.rel_mode = 0
        self.auto_range = 0
        self.rel_setpoint = 0


class SimulatedLakeshore460(StateMachineDevice):
    """
    Simulated Lakeshore 460
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._idn = "000000000000000000000000000000000000000"
        self._rel_mode_reading = 4906
        self._source = 1
        self._channel = "X"
        self._rel_set_point = 500
        self._max_reading = 100
        self._magnetic_field_reading = 400
        self.channels = {"X": Channel(), "Y":Channel(), "Z": Channel(), "V": Channel()}

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
    def unit(self):
        """
        :return: unit for the device
        """
        return self.channels[self._channel].unit

    @unit.setter
    def unit(self, unit):
        """
        :param unit: set unit for the device
        """
        self.channels[self._channel].unit = unit

    @property
    def status(self):
        """
        :return: status of device. If its on/off
        """
        return self.channels[self._channel].status

    @status.setter
    def status(self, status):
        """
        :param status: sets the device status, if device is on/off
        """
        self.channels[self._channel].status = status

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
    def filter(self):
        """
        :return: returns filter
        """
        return self.channels[self._channel].filter

    @filter.setter
    def filter(self, state):
        """
        :param state:  sets filter state (binary)
        """
        self.channels[self._channel].filter = state

    @property
    def max_hold(self):
        """
        :return: returns binary max hold
        """
        return self.channels[self._channel].max_hold

    @max_hold.setter
    def max_hold(self, max_hold):
        """
        :param max_hold: sets the max hold value
        """
        self.channels[self._channel].max_hold = max_hold

    @property
    def rel_mode(self):
        """
        :return: Return relative mode reading
        """
        return self.channels[self._channel].rel_mode

    @rel_mode.setter
    def rel_mode(self, rel_mode):
        """
        :param rel_mode:  Sets the relative mode reading
        """
        self.channels[self._channel].rel_mode = rel_mode

    @property
    def auto_range(self):
        """
        :return: Returns the auto range
        """
        return self.channels[self._channel].auto_range

    @auto_range.setter
    def auto_range(self, range):
        """
        :param range: sets the auto range
        """
        self.channels[self._channel].auto_range = range

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
    def display_filter(self):
        """
        :return: returns the percentage for display filter opening
        """
        return self.channels[self._channel].display_filter_window

    @display_filter.setter
    def display_filter(self, percentage):
        """
        :param percentage: sets the percentage for display filter opening
        """
        self.channels[self._channel].display_filter_window = percentage

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
    def rel_multiplier(self):
        """
        :return: Returns relative multiplier for device
        """
        return self.channels[self._channel].rel_multiplier

    @rel_multiplier.setter
    def rel_multiplier(self, multiplier):
        """
        :param multiplier: sets the relative multiplier for the device
        """
        self.channels[self._channel].rel_multiplier = multiplier

    @property
    def max_reading_multiplier(self):
        """
        :return:  return max reading multiplier
        """
        return self.channels[self._channel].max_multiplier


    @max_reading_multiplier.setter
    def max_reading_multiplier(self, multiplier):
        """
        :param multiplier:  sets the max reading multiplier for the device
        """
        self.channels[self._channel].max_multiplier = multiplier

    @property
    def rel_set_point(self):
        """
        :return: return relative mode setpoint for Lakeshore 460
        """
        return self.channels[self._channel].rel_setpoint

    @rel_set_point.setter
    def rel_set_point(self, setpoint):
        """
        :param setpoint:  sets the relative mode set point
        """
        self.channels[self._channel].rel_setpoint = setpoint

    @property
    def max_reading(self):
        """
        :return: returns max reading for Lakeshore 460
        """
        return self._max_reading

    @max_reading.setter
    def max_reading(self, reading):
        """
        :param reading:  sets max_reading for device
        """
        self._max_reading = reading

    @property
    def rel_mode_reading(self):
        """
        :return: Return relative mode reading
        """
        return self._rel_mode_reading

    @rel_mode_reading.setter
    def rel_mode_reading(self, rel_mode):
        """
        :param rel_mode: sets relative mode reading
        """
        self._rel_mode_reading = rel_mode

    @property
    def rel_mode_reading_multiplier(self):
        """
        :return: Return relative mode multiplier
        """
        return self.channels[self._channel].rel_mode_multiplier

    @rel_mode_reading_multiplier.setter
    def rel_mode_reading_multiplier(self, multiplier):
        """
        :param multiplier:  sets relative mode multiplier
        """
        self.channels[self._channel].rel_mode_multiplier = multiplier

    @property
    def magnetic_field_multiplier(self):
        """
        :return: Returns Magnetic Field Multiplier
        """
        return self.channels[self._channel].magnetic_field_multiplier

    @magnetic_field_multiplier.setter
    def magnetic_field_multiplier(self, multiplier):
        """
        :param multiplier:  Sets Magnetic field multiplier i.e micro, kilo, etc.
        """
        self.channels[self._channel].magnetic_field_multiplier = multiplier

    @property
    def magnetic_field_reading(self):
        """
        :return: Magnetic field Reading
        """
        return self._magnetic_field_reading

    @magnetic_field_reading.setter
    def magnetic_field_reading(self, field):
        """
        :param field: sets Magnetic Field Reading
        """
        self._magnetic_field_reading = field
