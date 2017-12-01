from lewis.core.statemachine import State


class StoppedState(State):

    def on_entry(self, dt):
        self._context.state = StoppedState.__name__


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = IdleState.__name__


class InitialisedState(State):

    def on_entry(self, dt):
        self._context.state = InitialisedState.__name__


class OscillatingState(State):

    def on_entry(self, dt):
        dev = self._context
        dev.state = OscillatingState.__name__
        self.time = 0.0
        self.new_cycle = False

    @staticmethod
    def transition_time(speed, acceleration):
        return speed/acceleration

    @staticmethod
    def window_time(width, speed):
        return width/speed

    @staticmethod
    def total_cycle_time(width, speed, acceleration):
        transition_time = OscillatingState.transition_time(speed, acceleration)
        window_time = OscillatingState.window_time(width, speed)
        return 2*transition_time + window_time

    @staticmethod
    def cycle_time(actual_time, width, speed, acceleration):
        return actual_time % OscillatingState.total_cycle_time(width, speed, acceleration)

    @staticmethod
    def spinning_up(actual_time, width, speed, acceleration):
        cycle_time = OscillatingState.cycle_time(actual_time, width, speed, acceleration)
        transition_time = OscillatingState.transition_time(speed, acceleration)
        return cycle_time < transition_time

    # TODO: The following methods static methods are only needed if the ORC reports its instantaneous speed/acceleration
    # At the moment we don't know if it reports only the requested speed/acceleration rather than the instantaneous
    # values.

    @staticmethod
    def spinning_down(actual_time, width, speed, acceleration):
        cycle_time = OscillatingState.cycle_time(actual_time, width, speed, acceleration)
        window_time = OscillatingState.window_time(width, speed)
        transition_time = OscillatingState.transition_time(speed, acceleration)
        return cycle_time > window_time + transition_time

    @staticmethod
    def calculate_speed(time, window_width, speed, acceleration):
        cycle_time = OscillatingState.cycle_time(time, window_width, speed, acceleration)
        transition_time = OscillatingState.transition_time(speed, acceleration)
        total_cycle_time = OscillatingState.total_cycle_time(window_width, speed, acceleration)

        if OscillatingState.spinning_up(time, window_width, speed, acceleration):
            current_speed = speed*cycle_time/transition_time
        elif OscillatingState.spinning_down(time, window_width, speed, acceleration):
            current_speed = speed*(total_cycle_time-cycle_time)/transition_time
        else:
            current_speed = speed

        return current_speed

    @staticmethod
    def calculate_acceleration(time, window_width, speed, acceleration):
        if OscillatingState.spinning_up(time, window_width, speed, acceleration):
            current_acceleration = acceleration
        elif OscillatingState.spinning_down(time, window_width, speed, acceleration):
            current_acceleration = 0
        else:
            current_acceleration = -acceleration
        return current_acceleration

    def in_state(self, dt):
        self.time += dt
        dev = self._context
        spinning_up = OscillatingState.spinning_up(self.time, dev.window_width, dev.speed, dev.acceleration)

        if spinning_up and self.new_cycle:
            dev.complete_cycles += 1  # Increment the complete cycles during spin up once per cycle
            self.new_cycle = False
        elif spinning_up and not self.new_cycle:
            pass  # We've already incremented the cycles
        elif not spinning_up and self.new_cycle:
            pass  # We've already set the new cycle flag ready for the next cycle
        elif not spinning_up and not self.new_cycle:
            self.new_cycle = True
        else:
            raise AssertionError("Should not logically be reached")


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = IdleState.__name__


class InitialisedState(State):

    def on_entry(self, dt):
        self._context.state = InitialisedState.__name__


class InitialisingState(State):

    def on_entry(self, dt):
        self._context.state = InitialisingState.__name__
        self._context.initialisation_requested = False

    def in_state(self, dt):
        self._context.time_spent_initialising += dt

    def on_exit(self, dt):
        self._context.stop_initialisation = False
        self._context.time_spent_initialising = 0.0

class ResetState(State):

    def on_entry(self, dt):
        dev = self._context
        dev.window_width = 100
        dev.acceleration = 500
        dev.speed = 20
        dev.offset = 0