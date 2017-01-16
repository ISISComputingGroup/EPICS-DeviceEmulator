from collections import OrderedDict

from lewis.devices import StateMachineDevice

from lewis.core import approaches

from lewis_emulators.neocera_ltc21.states import MonitorState


class SimulatedNeocera(StateMachineDevice):


    def _initialize_data(self):
        pass

    def _get_state_handlers(self):
        return {
            MonitorState.NAME: MonitorState()
        }

    def _get_initial_state(self):
        return MonitorState.NAME

    def _get_transition_handlers(self):
        return OrderedDict([
            ((MonitorState.NAME, 'moving'), lambda: False),
        ])
