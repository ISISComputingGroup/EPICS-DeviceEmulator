from lewis.core.statemachine import State


class OffState(State):
    pass


class MonitorState(State):
    NAME = __name__

class ControlState(State):
    pass