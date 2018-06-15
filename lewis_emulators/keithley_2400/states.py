from lewis.core.statemachine import State


class DefaultInitState(State):
    pass


class StaticRunningState(State):
    def in_state(self, dt):
        pass


class DefaultRunningState(State):
    def in_state(self, dt):
        self._context.update(dt)
