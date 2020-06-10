from collections import OrderedDict
from states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedFinsPLC(StateMachineDevice):

    HELIUM_RECOVERY_NODE = 58

    #  a dictionary representing the mapping between pv names, and the memory addresses in the helium recovery FINS PLC
    #  that store the data corresponding to each PV.
    PV_NAME_MEMORY_MAPPING = {
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
        "COMPRESSOR:INTERNAL_TEMP": 19523,
        "COLDBOX:HE_TEMP": 19524,
        "COLDBOX:HE_TEMP:LIMIT": 19525,
        "TRANSPORT_DEWAR:PRESSURE": 19526,
        "HE_PURITY": 19533,
        "DEW_POINT": 19534,
        "TS2:EAST:FLOW_METER": 19652,
        "TS2:EAST:O2": 19653,
        "TS2:WEST:FLOW_METER": 19662,
        "TS2:WEST:O2": 19663,
        "TS1:NORTH:O2": 19668,
        "TS1:SOUTH:O2": 19669,
        "TS1:WINDOW:FLOW_METER": 19697,
        "TS1:SHUTTER:FLOW_METER": 19698,
        "TS1:VOID:FLOW_METER": 19699,
        "GC:R108:U40": 19700,
        "GC:R108:DEWAR_FARM": 19702,
        "GC:R55:TOTAL": 19704,
        "GC:R55:NORTH": 19706,
        "GC:R55:SOUTH": 19708,
        "GC:MICE_HALL": 19710,
        "GC:MUON": 19712,
        "GC:PEARL_HRPD_MARI_ENGINX": 19714,
        "GC:SXD_AND_MERLIN": 19720,
        "GC:CRYO_LAB": 19724,
        "GC:MAPS_AND_VESUVIO": 19726,
        "GC:SANDALS": 19728,
        "GC:CRISP_AND_LOQ": 19730,
        "GC:IRIS_AND_OSIRIS": 19734,
        "GC:INES": 19736,
        "GC:RIKEN": 19738,
        "GC:R80:TOTAL": 19746,
        "GC:R53": 19748,
        "GC:R80:EAST": 19750,
        "GC:WISH": 19752,
        "GC:WISH:DEWAR_FARM": 19754,
        "GC:LARMOR_AND_OFFSPEC": 19756,
        "GC:ZOOM_SANS2D_AND_POLREF": 19758,
        "GC:MAGNET_LAB": 19762,
        "GC:IMAT": 19766,
        "GC:LET_AND_NIMROD": 19768,
        "GC:R80:WEST": 19772,
        "LIQUEFIER:COLDBOX:CV112": 19871,
        "LIQUEFIER:COMPRESSOR:CV2150": 19872,
        "LIQUEFIER:COMPRESSOR:CV2160": 19873,
        "LIQUEFIER:COMPRESSOR:CV2250": 19874,
        "LIQUEFIER:COLDBOX:MV108": 19875,
        "BANK1:TS2:RESPPLY:AVG_PURITY": 19929,
        "BANK1:TS1:RESPPLY:AVG_PURITY": 19930,
        "BANK2:IMPURE_HE:AVG_PURITY": 19931,
        "BANK3:MAIN_STRAGE:AVG_PURITY": 19933,
        "BANK4:DLS_STORAGE:AVG_PURITY": 19935,
        "BANK5:SPARE_STORA:AVG_PURITY": 19937,
        "BANK6:SPARE_STORA:AVG_PURITY": 19939,
        "BANK7:SPARE_STORA:AVG_PURITY": 19941,
        "BANK8:SPARE_STORA:AVG_PURITY": 19943
    }

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """

        self.network_address = 0x00
        self.unit_address = 0x00

        self.connected = True

        #  represents the part of the plc memory that stores 16 bit ints.
        self.int16_memory = {
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
            19652: 0,  # TS2 east flow meter
            19653: 0,  # O2 level TS2 east
            19662: 0,  # TS2 west flow meter
            19663: 0,  # TS2 west O2 level
            19668: 0,  # TS1 north O2 level
            19669: 0,  # TS1 south OS level
            19697: 0,  # TS1 window flow meter
            19698: 0,  # TS1 shutter flow meter
            19699: 0,  # TS1 void flow meter,
            19871: 0,  # liquefier coldbox cv112 %
            19872: 0,  # liquefier compressor CV2150 %
            19873: 0,  # liquefier compressor CV2160 %
            19874: 0,  # liquefier compressor CV2250 %
            19875: 0,  # liquefier coldbox MV108 Open/Close status
            19929: 0,  # bank 1 TS2 helium gas resupply average purity
            19930: 0,  # bank 1 TS1 helium gas resupply average purity
            19931: 0,  # bank 2 impure helium average purity
            19933: 0,  # bank 3 ISIS main helium purity average
            19935: 0,  # bank 4 DLS main helium storage purity average
            19937: 0,  # bank 5 ISIS helium spare storage purity average
            19939: 0,  # bank 6 ISIS helium spare storage purity average
            19941: 0,  # bank 7 ISIS helium spare storage purity average
            19943: 0,  # bank 8 ISIS helium spare storage purity average
        }

        #  represents the part of the plc memory that stores 32 bit ints.
        self.int32_memory = {
            19700: 0,  # R108 U40 gas counter
            19702: 0,  # R108 dewar farm gas counter
            19704: 0,  # gas counter R55 total
            19706: 0,  # gas counter R55 north
            19708: 0,  # gas counter R55 south
            19710: 0,  # gas counter mice hall
            19712: 0,  # gas counter muon
            19714: 0,  # gas counter PEARL, HRPD, ENGIN-X, GEM and MARI
            19720: 0,  # gas counter SXD and MERLIN
            19724: 0,  # gas counter Cryo Lab
            19726: 0,  # gas counter MAPS and VESUVIO
            19728: 0,  # gas counter SANDALS
            19730: 0,  # gas counter CRISP and LOQ
            19734: 0,  # gas counter IRIS and OSIRIS
            19736: 0,  # gas counter INES
            19738: 0,  # gas counter RIKEN
            19746: 0,  # gas counter R80 total
            19748: 0,  # gas counter R53
            19750: 0,  # gas counter R80 east
            19752: 0,  # gas counter WISH
            19754: 0,  # gas counter WISH dewar farm
            19756: 0,  # gas counter LARMOR and OFFSPEC
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
        """
        Sets a location in the plc emulator's memory to the given data.
        :param pv_name: The pv name that the test wants to set. Each PV name corresponds to only one memory location in
        the emulator.
        :param data: The data to be put in the plc memory.
        :return: None.
        """
        memory_location = SimulatedFinsPLC.PV_NAME_MEMORY_MAPPING[pv_name]

        if memory_location in self.int16_memory.keys():
            self.int16_memory[memory_location] = data
        else:
            self.int32_memory[memory_location] = data
