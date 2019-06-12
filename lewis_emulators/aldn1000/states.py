from lewis.core.statemachine import State
from lewis.core import approaches


class InfusingState(State):
    def on_entry(self, dt):
        self._context.volume_dispensed = 0.0
        self.originally_infused = self._context.volume_infused

    def in_state(self, dt):
        device = self._context
        device.volume_dispensed = approaches.linear(device.volume_dispensed, device.volume_target,
                                                    device.normalised_rate(), dt)
        device.volume_infused = self.originally_infused + device.volume_dispensed

    def on_exit(self, dt):
        self._context.pump_on = "STP"


class WithdrawingState(State):
    def on_entry(self, dt):
        self._context.volume_dispensed = 0.0
        self.originally_withdrawn = self._context.volume_withdrawn

    def in_state(self, dt):
        device = self._context
        device.volume_dispensed = approaches.linear(device.volume_dispensed, device.volume_target,
                                                    device.normalised_rate(), dt)
        device.volume_withdrawn = self.originally_withdrawn + device.volume_dispensed

    def on_exit(self, dt):
        self._context.pump_on = "STP"


class PumpingProgramStoppedState(State):
    pass


class PumpingProgramPausedState(State):
    def on_entry(self, dt):
        self._context.new_action = False


class PausePhaseState(State):
    pass


class UserWaitState(State):
    pass
