from collections import OrderedDict

from lewis.devices import StateMachineDevice

from lewis.core import approaches

from lewis_emulators.neocera_ltc21.states import MonitorState, ControlState


class SimulatedNeocera(StateMachineDevice):

    def _initialize_data(self):

        """

        Sets the initial state of the device

        """

        self.current_state = self._get_initial_state()
        self.temperature = 0
        self.setpoint = 0
        self.unit = "C"

    def _get_state_handlers(self):

        """

        Returns: states and their names

        """
        return {
            MonitorState.NAME: MonitorState()
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
