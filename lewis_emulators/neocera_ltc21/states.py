from lewis.core.statemachine import State


class OffState(State):
    pass


class MonitorState(State):
    NAME = 'monitor'

class ControlState(State):
    NAME = 'control'