from lewis.core.statemachine import State


class DefaultState(State):
    """
    Device is in default state.
    """
    NAME = 'Default'

    def in_state(self, dt):
        #self.device.input_lines[0] = not self.device.input_lines[0]
        #print(self.device.input_lines[0])
        pass

