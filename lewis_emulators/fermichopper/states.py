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

        if self._context.get_true_speed() > 10 and not self._context.magneticbearing:
            self._context.is_broken = True


class GoingState(State):
    def in_state(self, dt):
        device = self._context

        rate = 0

        if device.drive:
            rate += 50
            if not device.magneticbearing:
                rate -= 1

        device.set_true_speed(approaches.linear(device.get_true_speed(), device.get_speed_setpoint(), rate, dt))

        if device.get_true_speed() > 10 and not device.magneticbearing:
            device.is_broken = True


class StoppedState(State):
    def in_state(self, dt):
        if self._context.get_true_speed() > 10 and not self._context.magneticbearing:
            self._context.is_broken = True

    def on_entry(self, dt):
        self._context.drive = False
