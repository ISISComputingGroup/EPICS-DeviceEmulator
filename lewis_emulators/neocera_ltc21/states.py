from lewis.core.statemachine import State
from lewis.core import approaches


class OffState(State):
    """
    Device is in off state.
    It does not display the temperature on the front it is not monitoring or controlling it.

    """
    NAME = 'off'


class MonitorState(State):
    """
    Temperature is being monitored but heater is switched off
    """
    NAME = 'monitor'


class ControlState(State):
    """
    Temperature is being controller and monitored. The device will try to use the heater to make
    the temperature the same as the set point.
    """
    NAME = 'control'

    def in_state(self, dt):
        device = self._context
        for setpoint_index in range(device.sensor_count):
            sensor_source = device.sensor_source[setpoint_index] - 1  # sensor source is 1 indexed
            if sensor_source != 3:
                temp = device.temperatures[sensor_source]
                setpoint = device.setpoints[setpoint_index]
                device.temperatures[sensor_source] = approaches.linear(temp, setpoint, 0.1, dt)
