from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice
from enum import Enum, unique


@unique
class Units(Enum):
    mbar = 0
    Torr = 1
    Pascal = 2
    Micron = 3


class SimulatedOercone(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.pressure = 0
        self._measurement_unit = Units.mbar

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
    def measurement_unit(self):
        return self._measurement_unit

    @measurement_unit.setter
    def measurement_unit(self, units):
        self._measurement_unit = units

    def backdoor_set_units(self, unit):
        """
        Sets unit on device. Called only via the backdoor using lewis.

        Args:
            unit: integer 0, 1, 2, or 3

        Returns:
            None
        """
        self.measurement_unit = Units(int(unit))


