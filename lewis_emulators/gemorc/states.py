from lewis.core.statemachine import State


class StoppedState(State):

    def on_entry(self, dt):
        self._context.state = StoppedState.__name__


class OscillatingState(State):

    def on_entry(self, dt):
        self._context.state = OscillatingState.__name__


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = OscillatingState.__name__


class InitialisingState(State):

    def on_entry(self, dt):
        self._context.state = InitialisingState.__name__
        self._context.initialisation_requested = False

    def on_exit(self, dt):
        self._context.stop_initialisation = False
