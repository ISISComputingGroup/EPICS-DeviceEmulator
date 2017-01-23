from collections import OrderedDict

from lewis.devices import StateMachineDevice

from lewis_emulators.neocera_ltc21.device_errors import NeoceraDeviceErrors
from lewis_emulators.neocera_ltc21.states import MonitorState, ControlState


class SimulatedNeocera(StateMachineDevice):
    """
    Simulated Neocera LTG21 temperature controller
    """

    def _initialize_data(self):

        """

        Sets the initial state of the device

        """

        # desired current state of the system
        self.current_state = self._get_initial_state()

        # number of sensors
        self.sensor_count = 2

        # temperature of the samples measure by sensor n
        self.temperatures = [0] * self.sensor_count

        # display units
        self.units = ["K"] * self.sensor_count

        # the set points
        self.setpoints = [2] * self.sensor_count

        # errors created within the device
        self.error = NeoceraDeviceErrors()

    def _get_state_handlers(self):

        """

        Returns: states and their names

        """
        return {
            MonitorState.NAME: MonitorState(),
            ControlState.NAME: ControlState()
        }

    def _get_initial_state(self):
        """

        Returns: the name of the initial state

        """
        return ControlState.NAME

    def _get_transition_handlers(self):

        """

        Returns: the state transitions

        """

        return OrderedDict([
            ((MonitorState.NAME, ControlState.NAME), lambda: self.current_state == ControlState.NAME),
            ((ControlState.NAME, MonitorState.NAME), lambda: self.current_state == MonitorState.NAME),
        ])

    def set_state_monitor(self):
        """

        Sets the current state to MONITOR

        """
        self.current_state = MonitorState.NAME

    def set_state_control(self):
        """

        Sets the current state to CONTROL

        """
        self.current_state = ControlState.NAME

    @property
    def state(self):
        """

        Returns: the state

        """
        return self._csm.state
