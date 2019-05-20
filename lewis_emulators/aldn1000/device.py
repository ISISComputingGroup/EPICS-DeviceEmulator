from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedAldn1000(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.connected = True
        self.input_correct = True

        self.status = 'S'
        self._pump = 'STP'
        self.program_function = 'RAT'

        self.address = 0
        self._diameter = 0.0
        self.volume = 0.0
        self.volume_infused = 0.0
        self.volume_withdrawn = 0.0
        self._direction = 'INF'
        self.rate = 0.0
        self.units = 'UM'
        self.volume_units = 'UL'

    def clear_volume(self, volume_type):
        if volume_type == 'INF':
            self.volume_infused = 0.0
        elif volume_type == 'WDR':
            self.volume_withdrawn = 0.0
        return

    @property
    def pump(self):
        return self._pump

    @pump.setter
    def pump(self, action):
        if action == 'STP':
            self._pump = 'STP'
            if self.status == 'P':  # Currently paused
                self.status = 'S'  # Stop
            elif self.status == 'S':
                pass
            else:
                self.status = 'P'  # Pause
        elif action == 'RUN':
            self._pump = 'RUN'
            if self.direction == 'Infusing':
                self.status = 'I'
            else:
                self.status = 'W'
        else:
            print('An error occurred while trying to start/stop the pump')

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, new_value):
        if new_value > 14.0:  # Device changes the volume units automatically based on the diameter set
            self.volume_units = 'ML'
        else:
            self.volume_units = 'UL'
        self._diameter = new_value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction):
        if new_direction == 'REV':  # Reverse
            if self._direction == 'INF':  # Infuse
                self._direction = 'WDR'  # Withdraw
            else:
                self._direction = 'INF'
        else:
            self._direction = new_direction

    def reset(self):
        self._initialize_data()

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([
        ])

