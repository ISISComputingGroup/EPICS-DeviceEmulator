from lewis.core.statemachine import State


class PumpOff(State):

    def on_entry(self, dt):
        device = self._context
        device.program_runtime = 0


class PumpOn(State):
    pass


class PumpTimed(State):

    # Update time for each tick while in state
    def in_state(self, dt):
        device = self._context
        device.program_runtime += int(dt)
