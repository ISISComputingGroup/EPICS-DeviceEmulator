from lewis.core.statemachine import State


class StoppedState(State):

    def on_entry(self, dt):
        self.log.info("Entering STOPPED state")


class JoggingState(State):

    def on_entry(self, dt):
        self.log.info("Entering JOGGING state")

    def in_state(self, dt):
        device = self._context
        device.position += device.velocity * dt

