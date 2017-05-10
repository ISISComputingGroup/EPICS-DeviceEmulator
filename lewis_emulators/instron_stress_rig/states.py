from lewis.core.statemachine import State
from lewis.core import approaches


class DefaultInitState(State):
    pass


class DefaultStoppedState(State):
    def in_state(self, dt):
        device = self._context
        device.stop()


class DefaultStartedState(State):
    def in_state(self, dt):
        device = self._context
        device.start()
