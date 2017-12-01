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
        self.target_reached = False

    @staticmethod
    def calculate_speed(time, window_width, target_speed, acceleration):
        transition_time = target_speed/acceleration
        window_time = window_width/target_speed
        total_cycle_time = 2*transition_time + window_time
        cycle_time = time % total_cycle_time

        spinning_up = cycle_time < transition_time
        spinning_down = cycle_time > window_time + transition_time

        if spinning_up:
            current_speed = target_speed * cycle_time / transition_time
        elif spinning_down:
            current_speed = target_speed * (total_cycle_time - cycle_time) / transition_time
        else:
            current_speed = target_speed
        return current_speed

    def in_state(self, dt):
        self.time += dt
        dev = self._context

        dev.speed = OscillatingState.calculate_speed(self.time, dev.window_width, dev.target_speed, dev.acceleration)

        # Increment the cycle counter if needed. Important to only do this once per cycle
        # Has the cycle hit its target speed this cycle
        self.target_reached = self.target_reached or dev.speed == dev.target_speed
        in_motion = dev.speed/(dev.acceleration*dt) > 2  # 2 dimensionless speed increments
        if not in_motion and self.target_reached:
            dev.complete_cycles += 1
            self.target_reached = False


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
