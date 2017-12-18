from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core import approaches


class Axis():
    def __init__(self, axis_label):
        self.rbv_error = None
        self.rbv = 10.0
        self.sp = self.rbv
        self.moving = False
        self.speed = 0.1
        self.axis_label = axis_label

    def home(self):
        self.sp = 0.0
        self.moving = True

    def simulate(self, dt):
        self.rbv = approaches.linear(self.rbv, self.sp, self.speed, dt)
        self.moving = self.rbv == self.sp

    def get_label_and_position(self):
        if self.rbv_error is not None:
            return self.rbv_error
        else:
            return "{label}{0:.0f}".format(self.rbv, label=self.axis_label)


class SimulatedSm300(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        # Is the device initialised, if not it won't talk to me
        self.initialised = False

        self.x_axis = Axis("X")
        self.y_axis = Axis("Y")
        self.is_moving = None  # let the axis report its motion
        self.is_moving_error = False

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

    def reset(self):
        self._initialize_data()

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

    @property
    def x_axis_sp(self):
        return self.x_axis.rbv

    @x_axis_sp.setter
    def x_axis_sp(self, position):
        self.x_axis.sp = position

    @property
    def y_axis_sp(self):
        return self.y_axis.rbv

    @y_axis_sp.setter
    def y_axis_sp(self, position):
        self.y_axis.sp = position

    @property
    def x_axis_rbv_error(self):
        return self.x_axis.rbv_error

    @x_axis_rbv_error.setter
    def x_axis_rbv_error(self, error_return):
        self.x_axis.rbv_error = error_return
