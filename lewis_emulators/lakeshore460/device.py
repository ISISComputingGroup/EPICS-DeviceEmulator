from collections import OrderedDict

from lewis.devices import StateMachineDevice
from .states import DefaultState


class SimulatedLakeshore460(StateMachineDevice):
    """
    Simulated AM Int2-L pressure transducer.
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._idn = "000000000000000000000000000000000000000"
        self._unit= "G"
        self._status = 0
        self._mode = 0
        self._prms = 0
        self._filter = 0
        self._auto_range = 0
        self._manual_range = 2
        self._max_hold = 0
        self._rel_mode = 0
        self.rel_mode_reading = 4906
        self._rel_mode_reading_multiplier = "ON"
        self._total_fields = 7.5
        self._source = 1
        self._channel = "Channel X"
        self._display_filter = 5
        self._filter_points = 9
        self._reading_multiplier = "ON"
        self._rel_set_point = 500
        self._max_reading = 100
        self._rel_multiplier = "ON"
        self._magnetic_field_multiplier = "m"
        self._magnetic_field_reading = 400

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
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        :param unit: set unit for the device
        :return:
        """
        self._unit = unit

    @property
    def status(self):
        """
        :return: status of device. If its on/off
        """
        return self._status

    @status.setter
    def status(self,status):
        """
        :param status: sets the device status, if device is on/off
        :return:
        """
        self._status = status

    @property
    def mode(self):
        """
        :return: AC or DC unit of measurement
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def prms(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._prms

    @prms.setter
    def prms(self, prms):
        self._prms = prms

    @property
    def filter(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._filter

    @filter.setter
    def filter(self, state):
        self._filter = state

    @property
    def max_hold(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._max_hold

    @max_hold.setter
    def max_hold(self, max_hold):
        self._max_hold = max_hold

    @property
    def rel_mode(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._rel_mode

    @rel_mode.setter
    def rel_mode(self, rel_mode):
        self._rel_mode = rel_mode

    @property
    def auto_range(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._auto_range

    @auto_range.setter
    def auto_range(self, range):
        self._auto_range = range

    @property
    def manual_range(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._manual_range

    @manual_range.setter
    def manual_range(self, range):
        self._manual_range = range

    @property
    def total_fields(self):
        return self._total_fields

    @total_fields.setter
    def total_fields(self, total):
        self._total_fields = total

    @property
    def source(self):
       return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def display_filter(self):
        return self._display_filter

    @display_filter.setter
    def display_filter(self, percentage):
        self._display_filter = percentage

    @property
    def filter_points(self):
        return self._filter_points

    @filter_points.setter
    def filter_points(self, points):
        self._filter_points = points

    @property
    def rel_multiplier(self):
        return self._rel_multiplier

    @rel_multiplier.setter
    def rel_multiplier(self, multiplier):
        self._rel_multiplier = multiplier

    @property
    def reading_multiplier(self):
        return self._reading_multiplier

    @reading_multiplier.setter
    def reading_multiplier(self, multiplier):
        self._reading_multiplier = multiplier

    @property
    def rel_set_point(self):
        return self._rel_set_point

    @rel_set_point.setter
    def rel_set_point(self, setpoint):
        self._rel_set_point = setpoint

    @property
    def max_reading(self):
        return self._max_reading

    @max_reading.setter
    def max_reading(self, reading):
        self._max_reading = reading

    @property
    def rel_mode_reading(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._rel_mode_reading

    @rel_mode_reading.setter
    def rel_mode_reading(self, rel_mode):
        self._rel_mode_reading = rel_mode

    @property
    def rel_mode_reading_multiplier(self):
        """
        :return: Peajk /RMS Field reading
        """
        return self._rel_mode_reading_multiplier

    @rel_mode_reading_multiplier.setter
    def rel_mode_reading_multiplier(self, multiplier):
        self._rel_mode_reading_multiplier = multiplier

    @property
    def magnetic_field_multiplier(self):
        return self._magnetic_field_multiplier

    @magnetic_field_multiplier.setter
    def magnetic_field_multiplier(self, multiplier):
        self._magnetic_field_multiplier = multiplier

    @property
    def magnetic_field_reading(self):
        return self._magnetic_field_reading

    @magnetic_field_reading.setter
    def magnetic_field_reading(self, field):
        self._magnetic_field_reading = field



