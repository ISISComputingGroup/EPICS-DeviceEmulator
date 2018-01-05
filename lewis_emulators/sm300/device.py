"""
Device classes for the SM 300 motor emulator
"""

from collections import OrderedDict

from lewis.core.logging import has_log

from states import DefaultState
from lewis.devices import StateMachineDevice
from lewis.core import approaches


@has_log
class Axis(object):
    """
    An axis within the SM300 device
    """

    def __init__(self, axis_label):
        """
        Constructor.
        Args:
            axis_label: the label for the axis
        """
        self.rbv_error = None
        self.rbv = 10.0
        self.sp = self.rbv
        self.moving = False
        self.speed = 100
        self.axis_label = axis_label

    def home(self):
        """
        Perform a homing operation.
        """
        self.sp = 0.0
        self.moving = True

    def simulate(self, dt):
        """
        Simulate movement of the axis.
        Args:
            dt: time since last simulation
        """
        if self.moving:
            self.rbv = approaches.linear(self.rbv, self.sp, self.speed, dt)
            self.moving = self.rbv != self.sp
        return

    def get_label_and_position(self):
        """
        Returns: axis label and current position in steps
        """
        if self.rbv_error is not None:
            return self.rbv_error
        else:
            return "{label}{0:.0f}".format(self.rbv, label=self.axis_label)

    def stop(self):
        """
        Stop the motor moving.

        """
        self.moving = False

    def move_to_sp(self):
        """
        Start a movement of the axis to its set point
        """
        self.moving = True


class SimulatedSm300(StateMachineDevice):
    """
    Simulated SM300 Device
    """
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        # Is the device initialised, if not it won't talk to me
        self.initialised = False
        self.axes = {
            "X": Axis("X"),
            "Y": Axis("Y")
        }
        self.x_axis = self.axes["X"]
        self.y_axis = self.axes["Y"]
        self.is_moving = None  # let the axis report its motion
        self.is_moving_error = False
        self.reset_codes = []
        self.has_bcc_at_end_of_message = True

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
        """
        Reset device to start up state
        """
        self._initialize_data()

    @property
    def x_axis_rbv(self):
        """
        Returns: Read back value for the x axis (useful usage through the back door
        """
        return self.x_axis.rbv

    @x_axis_rbv.setter
    def x_axis_rbv(self, position):
        self.x_axis.rbv = position

    @property
    def y_axis_rbv(self):
        """
        Returns: Read back value for the y axis (useful usage through the back door
        """
        return self.y_axis.rbv

    @y_axis_rbv.setter
    def y_axis_rbv(self, position):
        self.y_axis.rbv = position

    @property
    def x_axis_sp(self):
        """
        Returns: Set point value for the x axis (useful usage through the back door
        """
        return self.x_axis.rbv

    @x_axis_sp.setter
    def x_axis_sp(self, position):
        self.x_axis.sp = position

    @property
    def y_axis_sp(self):
        """
        Returns: Set point value for the y axis (useful usage through the back door
        """
        return self.y_axis.rbv

    @y_axis_sp.setter
    def y_axis_sp(self, position):
        self.y_axis.sp = position

    @property
    def x_axis_rbv_error(self):
        """
        Returns: The error to give instead of the read back value
        """
        return self.x_axis.rbv_error

    @x_axis_rbv_error.setter
    def x_axis_rbv_error(self, error_return):
        self.x_axis.rbv_error = error_return
