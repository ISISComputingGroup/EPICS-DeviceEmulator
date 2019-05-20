from lewis.core.statemachine import State


class InfusingState(State):
    def in_state(self, dt):
        device = self._context
        device.volume_infused += device.rate

        if device.volume_infused >= device.volume:
            device.pump_on = "STP"


class WithdrawingState(State):
    def in_state(self, dt):
        device = self._context
        device.volume_withdrawn += device.rate

        if device.volume_withdrawn >= device.volume:
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
