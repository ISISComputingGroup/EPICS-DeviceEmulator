from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFinsPLC(StateMachineDevice):

    HELIUM_RECOVERY_NODE = 58

    HE_RECOVERY_DOUBLE_WORD_MEMORY_LOCATIONS = {}

    PV_NAME_TO_MEMORY_MAPPING = {
        "HEARTBEAT": 19500,
        "MCP:BANK1:TS2": 19501,
        "MCP:BANK1:TS1": 19502,
        "MCP1:BANK2:IMPURE_HE": 19503,
        "MCP2:BANK2:IMPURE_HE": 19504,
        "MCP1:BANK3:MAIN_HE_STORAGE": 19505,
        "MCP2:BANK3:MAIN_HE_STORAGE": 19506,
        "MCP1:BANK4:DLS_HE_STORAGE": 19507,
        "MCP2:BANK4:DLS_HE_STORAGE": 19508,
        "MCP1:BANK5:SPARE_STORAGE": 19509,
        "MCP2:BANK5:SPARE_STORAGE": 19510,
        "MCP1:BANK6:SPARE_STORAGE": 19511,
        "MCP2:BANK6:SPARE_STORAGE": 19512,
        "MCP1:BANK7:SPARE_STORAGE": 19513,
        "MCP2:BANK7:SPARE_STORAGE": 19514,
        "MCP1:BANK8:SPARE_STORAGE": 19515,
        "MCP2:BANK8:SPARE_STORAGE": 19516,
        "MCP:INLET:PRESSURE": 19517,
        "MCP:EXTERNAL_TEMP": 19518,
        "MASS_FLOW:GAS_LIQUEFACTION": 19521,
        "MASS_FLOW:HE_FILLS": 19522,
        "KAISER_COMPR:INTERNAL_TEMP": 19523,
        "COLDBOX:HE_TEMP": 19524,
        "COLDBOX:HE_TEMP:LIMIT": 19525,
        "TRANSPORT_DEWAR:PRESSURE": 19526,
        "HE_PURITY": 19533,
        "DEW_POINT": 19534
    }

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.network_address = 0x00
        self.unit_address = 0x00

        self.connected = True

        self.memory = {
            19500: 0,  # heartbeat
            19501: 0,  # mcp bank 1 TS2 helium gas resupply
            19502: 0,  # mcp bank 1 TS1 helium gas resupply
            19503: 0,  # mcp 1 bank 2 impure helium
            19504: 0,  # mcp 2 bank 2 impure helium
            19505: 0,  # mcp 1 bank 3 main helium storage
            19506: 0,  # mcp 2 bank 3 main helium storage
            19507: 0,  # mcp 1 bank 4 dls helium storage
            19508: 0,  # mcp 2 bank 4 dls helium storage
            19509: 0,  # mcp 1 bank 5 spare storage
            19510: 0,  # mcp 2 bank 5 spare storage
            19511: 0,  # mcp 1 bank 6 spare storage
            19512: 0,  # mcp 2 bank 6 spare storage
            19513: 0,  # mcp 1 bank 7 spare storage
            19514: 0,  # mcp 2 bank 7 spare storage
            19515: 0,  # mcp 1 bank 8 spare storage
            19516: 0,  # mcp 2 bank 8 spare storage
            19517: 0,  # mcp manifold inlet pressure from compressors
            19518: 0,  # mcp external temperature
            19521: 0,  # mass flow meter for gas flow liquefaction
            19522: 0,  # mass flow meter for helium fills,
            19523: 0,  # Kaiser compressor container internal temperature
            19524: 0,  # Coldbox Helium temperature
            19525: 0,  # Coldbox Helium temperature limit
            19526: 0,  # Transport dewar flash pressure
            19533: 0,  # helium purity
            19534: 0,  # dew point
        }

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
        Public method that re-initializes the device's fields.
        :return: Nothing.
        """
        self._initialize_data()

    def set_memory(self, pv_name, data):
        memory_location = SimulatedFinsPLC.PV_NAME_TO_MEMORY_MAPPING[pv_name]
        self.memory[memory_location] = data
