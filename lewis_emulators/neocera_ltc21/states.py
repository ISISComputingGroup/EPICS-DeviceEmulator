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
