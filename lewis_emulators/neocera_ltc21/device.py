from collections import OrderedDict

from lewis.devices import StateMachineDevice

from lewis_emulators.neocera_ltc21.device_errors import NeoceraDeviceErrors
from lewis_emulators.neocera_ltc21.states import MonitorState, ControlState


class SimulatedNeocera(StateMachineDevice):
    """
    Simulated Neocera LTG21 temperature controller
    """

    # Index in the arrays of the heater output
    HEATER_INDEX = 0
    # Index in the arrays of the analog output
    ANALOG_INDEX = 1
    # Minimum allowed output control type for the output index (see self.control)
    CONTROL_TYPE_MIN = [0, 3]
    # Maximum allowed output control type for the output index (see self.control)
    CONTROL_TYPE_MAX = [5, 6]

    def _initialize_data(self):

        """

        Sets the initial state of the device

        """

        # desired current state of the system
        self.current_state = self._get_initial_state()

        # number of sensors or outputs
        self.sensor_count = 2

        # temperature of the samples measure by sensor n (this index is different to the setpoints)
        self.temperatures = [0] * self.sensor_count

        # display units (this is for sensor n and reading setpoint n)
        self.units = ["K"] * self.sensor_count

        # the set points (the setpoint in the units of the sensor connected to it)
        self.setpoints = [2] * self.sensor_count

        # sensor source for the heater/analogue (initially sensor 1 is on heater output 1 and sensor 2 is on analogue)
        # 3 is no connected
        self.sensor_source = range(1, self.sensor_count + 1)

        # output control method {0 = AUTO P, 1 = AUTO PI, 2 = AUTO PID, 3 = PID, 4 = TABLE, 5 = DEFAULT, 6 = MONITOR (only analogue)}
        self.control = [4] * self.sensor_count

        # heater range {0 = Off, 1 = 0.05W, 2=0.5W, 3=5W, 4=50W}
        self.heater_range = 4

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
