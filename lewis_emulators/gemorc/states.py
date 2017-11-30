from lewis.core.statemachine import State


class StoppedState(State):

    def on_entry(self, dt):
        self._context.state = StoppedState.__name__


class OscillatingState(State):

    def on_entry(self, dt):
        device = self._context
        device.state = OscillatingState.__name__
        self.time = 0.0

    def in_state(self, dt):
        self.time += dt
        dev = self._context

        def calculate_speed(time, window_width, target_speed, acceleration):
            transition_time = target_speed/acceleration
            total_cycle_time = 2*transition_time + window_width
            cycle_time = time % total_cycle_time

            spinning_up = cycle_time < transition_time
            spinning_down = cycle_time > window_width + transition_time

            if spinning_up:
                current_speed = target_speed*cycle_time/transition_time
            elif spinning_down:
                current_speed = target_speed*(total_cycle_time - cycle_time)/transition_time
            else:
                current_speed = target_speed

            return current_speed

        dev.speed = calculate_speed(self.time, dev.window_width, dev.target_speed, dev.acceleration)

        def cycle_counter(speed, acceleration, dt):
            was_in_motion = False
            while True:
                tolerance = 2*dt*acceleration/speed # 2 normalised speed steps
                in_motion = speed > tolerance
                if not in_motion and was_in_motion:
                    was_in_motion = False
                    yield 1
                else:
                    yield 0

        dev.complete_cycles += cycle_counter(dev.target_speed, dev.acceleration, dt)


class IdleState(State):

    def on_entry(self, dt):
        self._context.state = OscillatingState.__name__


class InitialisingState(State):

    def on_entry(self, dt):
        self._context.state = InitialisingState.__name__
        self._context.initialisation_requested = False

    def in_state(self, dt):
        self._context.time_spent_initialising += dt

    def on_exit(self, dt):
        self._context.stop_initialisation = False
