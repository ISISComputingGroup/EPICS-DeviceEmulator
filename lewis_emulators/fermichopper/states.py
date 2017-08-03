from lewis.core.statemachine import State
from lewis.core import approaches


class DefaultState(State):
    pass


class StoppingState(State):
    def in_state(self, dt):
        device = self._context

        rate = 0

        if not device.magneticbearing:
            rate += 1
        if device.drive:
            rate += 50

        device.set_true_speed(approaches.linear(device.get_true_speed(), 0, rate, dt))


class GoingState(State):
    def in_state(self, dt):
        device = self._context

        rate = 0

        if device.drive:
            rate += 50
            if not device.magneticbearing:
                rate -= 1

        device.set_true_speed(approaches.linear(device.get_true_speed(), device.get_speed_setpoint(), rate, dt))


class StoppedState(State):
    def in_state(self, dt):
        pass

    def on_entry(self, dt):
        self._context.drive = False


class BrokenState(State):
    def in_state(self, dt):
        # Fail hard - This crashes the emulator (which is the realistic behaviour in this situation...)
        assert False, "The device is broken. Game over."
