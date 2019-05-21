from lewis.core.statemachine import State


class InfusingState(State):

    def on_entry(self, dt):
        device = self._context
        device.volume_dispensed = 0.0

    def in_state(self, dt):
        device = self._context
        device.volume_infused += dt * device.rate
        device.volume_dispensed += dt * device.rate

        if device.volume_dispensed >= device.volume:
            device.pump_on = "STP"


class WithdrawingState(State):

    def on_entry(self, dt):
        self._context.volume_dispensed = 0.0

    def in_state(self, dt):
        device = self._context
        device.volume_withdrawn += dt * device.rate
        device.volume_dispensed += dt * device.rate

        if device.volume_dispensed >= device.volume:
            device.pump_on = "STP"


class PumpingProgramStoppedState(State):
    pass


class PumpingProgramPausedState(State):
    def on_entry(self, dt):
        self._context.new_action = False


class PausePhaseState(State):
    pass


class UserWaitState(State):
    pass
