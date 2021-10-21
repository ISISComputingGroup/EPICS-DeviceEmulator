from collections import OrderedDict
from .states import StoppedState, JoggingState
from lewis.devices import StateMachineDevice


states = OrderedDict([("Stopped", StoppedState()),
                      ("Jogging", JoggingState())])


class SimulatedMclennan(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.is_jogging = False
        self.velocity = 0
        self.position = 0
        self.is_pm304 = False
        self.creep_speed = 700

    def jog(self, velocity):
        self.velocity = velocity
        self.is_jogging = True

    def stop(self):
        self.is_jogging = False

    def _get_state_handlers(self):
        return states

    def _get_initial_state(self):
        return "Stopped"

    def _get_transition_handlers(self):
        return OrderedDict([
            (("Stopped", "Jogging"), lambda: self.is_jogging),
            (("Jogging", "Stopped"), lambda: not self.is_jogging),
        ])
