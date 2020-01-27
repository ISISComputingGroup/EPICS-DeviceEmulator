from lewis.devices import StateMachineDevice
from collections import OrderedDict
from .states import DefaultState


class SimulatedKepco(StateMachineDevice):
    """
    Simulated Kepco
    """

    def _initialize_data(self):
        """
        Sets the initial state of the device.
        """
        self._voltage = 10.0
        self._current = 10.0
        self._setpoint_voltage = 10.0
        self._setpoint_current = 10.0
        self._output_mode = 0
        self._output_status = 0
        self._idn = "000000000000000000000000000000000000000"
        self.connected = True

        self.remote_comms_enabled = True

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
        :return: IDN- Identificaiton String
        """
        return self._idn

    @idn.setter
    def idn(self, idn):
        """
        :param idn:
        :return: sets IDN- Identificaiton String
        """
        self._idn = idn

    @property
    def voltage(self):
        """
        Returns: the Voltage
        """
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        """
        :param voltage: Write the Voltage
        """
        self._voltage = voltage

    @property
    def current(self):
        """
        :return: get the Current
        """
        return self._current

    @current.setter
    def current(self, current):
        """
        :param write the current:
        """
        self._current = current

    @property
    def setpoint_voltage(self):
        """
        Returns: the Setpoint Voltage
        """
        return self._setpoint_voltage

    @setpoint_voltage.setter
    def setpoint_voltage(self, setpoint_voltage):
        """
        :param setpoint_voltage: set the Setpoint Voltage
        :return:
        """
        self._setpoint_voltage = setpoint_voltage

    @property
    def setpoint_current(self):
        """
        Returns: the Setpoint Current
        """
        return self._setpoint_current

    @setpoint_current.setter
    def setpoint_current(self, setpoint_current):
        """
        :param setpoint_current: set the setpoint current
        :return:
        """
        self._setpoint_current = setpoint_current

    @property
    def output_mode(self):
        """
        :return:  Returns the output mode
        """
        return self._output_mode

    @output_mode.setter
    def output_mode(self, mode):
        """
        :param mode: Set output mode
        """
        self._output_mode = mode

    @property
    def output_status(self):
        """
        :return: Output status
        """
        return self._output_status

    @output_status.setter
    def output_status(self, status):
        """
        :param status: set Output status
        """
        self._output_status = status

    def reset(self):
        self._initialize_data()
