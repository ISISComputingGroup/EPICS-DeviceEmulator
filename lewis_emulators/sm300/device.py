from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core import approaches


class Axis():
    def __init__(self):
        self.rbv = 0
        self.sp = 0
        self.moving = False
        self.speed = 0.1

    def home(self):
        self.sp = 0
        self.moving = True

    def simulate(self, dt):
        self.rbv = approaches.linear(self.rbv, self.sp, self.speed, dt)
        self.moving = self.rbv == self.sp


class SimulatedSm300(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        # Is the device initialised, if not it won't talk to me
        self.initialised = False

        self.x_axis = Axis()
        self.y_axis = Axis()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    @property
    def x_axis_rbv(self):
        return self.x_axis.rbv

    @x_axis_rbv.setter
    def x_axis_rbv(self, position):
        self.x_axis.rbv = position

    @property
    def y_axis_rbv(self):
        return self.y_axis.rbv

    @y_axis_rbv.setter
    def y_axis_rbv(self, position):
        self.y_axis.rbv = position
