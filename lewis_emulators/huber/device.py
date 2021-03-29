"""
Device classes for the SM 300 motor emulator
"""

from collections import OrderedDict

from lewis.core.logging import has_log

from .states import DefaultState
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
        self._move_to_sp = 0
        self.moving = False
        self.speed = 10
        self.axis_label = axis_label

    def home(self):
        """
        Perform a homing operation.
        """
        self.sp = 0.0
        self.move_to_sp()

    def simulate(self, dt):
        """h
        Simulate movement of the axis.
        Args:
            dt: time since last simulation
        """
        if self.moving:
            self.rbv = approaches.linear(self.rbv, self._move_to_sp, self.speed, dt)
            self.moving = not self._at_position()
            self.log.debug("moving {}".format(self.moving))
        return

    def _at_position(self):
        """
        Returns: True if at position (within tolerance); False otherwise.
        """
        return abs(self.rbv - self._move_to_sp) < 0.01

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
        Start a movement of the axis to the current set point

        Returns: True if can start moving (or is already at position), False otherwise
        """
        self._move_to_sp = self.sp
        if self._at_position():
            return True
        self.moving = True
        return True


class SimulatedHuber(StateMachineDevice):
    """
    Simulated Huber SMC9300 Device
    """
    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        # Is the device initialised, if not it won't talk to me
        self.initialised = False
        self.axes = {}
        for i in range(1, 9):
            self.axes[i] = "Axis {}".format(i)
        self.is_moving = None  # let the axis report its motion
        self.is_moving_error = False
        self.reset_codes = []
        self.disconnect = ""
        self.error_code = 0
        self.is_disconnected = False

    def move_to_sp(self):
        """
        Move to the setpoint if the motor is not already moving
        Returns: True if new points set; False otherwise
        """
        if self.is_motor_moving():
            self.log.error("Called move to sp while moving")
            return False

        for axis in self.axes.values():
            axis.move_to_sp()
        return True

    def is_motor_moving(self):
        """

        Returns: whether the motor is moving

        """
        if self.is_moving is not None:
                return self.is_moving

        for axis in self.axes.values():
            if axis.moving:
                return True

        return False

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

    def set_position(self, axis, position):
        print("Move {} to dial position {}".format(axis, position))
