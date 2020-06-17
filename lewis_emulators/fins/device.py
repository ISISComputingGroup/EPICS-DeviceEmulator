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
        "GAS_LIQUEFACTION:MASS_FLOW": 19521,
        "HE_FILLS:MASS_FLOW": 19522,
        "CMPRSSR:INTERNAL_TEMP": 19523,
        "COLDBOX:HE_TEMP": 19524,
        "COLDBOX:HE_TEMP:LIMIT": 19525,
        "TRANSPORT_DEWAR:PRESSURE": 19526,
        "HE_PURITY": 19533,
        "DEW_POINT": 19534,
        "FLOW_METER:TS2:EAST": 19652,
        "TS2:EAST:O2": 19653,
        "FLOW_METER:TS2:WEST": 19662,
        "TS2:WEST:O2": 19663,
        "TS1:NORTH:O2": 19668,
        "TS1:SOUTH:O2": 19669,
        "FLOW_METER:TS1:WINDOW": 19697,
        "FLOW_METER:TS1:SHUTTER": 19698,
        "FLOW_METER:TS1:VOID": 19699,
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
        "LIQUEFIER:CMPRSSR:CV2150": 19872,
        "LIQUEFIER:CMPRSSR:CV2160": 19873,
        "LIQUEFIER:CMPRSSR:CV2250": 19874,
        "LIQUEFIER:COLDBOX:MV108": 19875,
        "BANK1:TS2:RSPPL:AVG_PURITY": 19929,
        "BANK1:TS1:RSPPL:AVG_PURITY": 19930,
        "BANK2:IMPURE_HE:AVG_PURITY": 19931,
        "BANK3:MAIN_STRG:AVG_PURITY": 19933,
        "BANK4:DLS_STRG:AVG_PURITY": 19935,
        "BANK5:SPR_STRG:AVG_PURITY": 19937,
        "BANK6:SPR_STRG:AVG_PURITY": 19939,
        "BANK7:SPR_STRG:AVG_PURITY": 19941,
        "BANK8:SPR_STRG:AVG_PURITY": 19943,
        "COLDBOX:TURBINE_100:SPEED": 19945,
        "COLDBOX:TURBINE_101:SPEED": 19946,
        "COLDBOX:T106:TEMP": 19947,
        "COLDBOX:TT111:TEMP": 19948,
        "COLDBOX:PT102:PRESSURE": 19949,
        "PT203:BUFFER_PRESSURE": 19950,
        "TT104:PURIFIER_TEMP": 19951,
        "TT102:PURIFIER_TEMP": 19952,
        "COLDBOX:TT108:TEMP": 19953,
        "COLDBOX:PT112:PRESSURE": 19954,
        "LIQUEFIER:COLDBOX:CV103": 19955,
        "LIQUEFIER:COLDBOX:CV111": 19956,
        "MOTHER_DEWAR:HE_LEVEL": 19958,
        "PURIFIER:LEVEL": 19961,
        "IMPURE_HE_SUPPLY:PRESSURE": 19962,
        "CMPRSSR:LOW_CNTRL_PRESSURE": 19963,
        "CMPRSSR:HIGH_CNTRL_PRESSURE": 19964,
        "CV2250": 19972,
        "CV2150": 19974,
        "CV2160": 19975,
        "LIQUID_NITROGEN:STATUS": 19979,
        "LIQUEFIER:ALARM1": 19982,
        "LIQUEFIER:ALARM2": 19983,
        "MCP:LIQUID_HE_INVENTORY": 19996,
        "CV120:MODE": 19967,
        "CV121:MODE": 19969,
        "LOW_PRESSURE:MODE": 19971,
        "HIGH_PRESSURE:MODE": 19973,
        "TIC106:MODE": 19976,
        "PIC112:MODE": 19977,
        "CV120:POSITION": 19968,
        "CV121:POSITION": 19970,
        "PURIFIER:STATUS": 19978,
        "CMPRSSR:STATUS": 19980,
        "COLDBOX:STATUS": 19981
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
            19945: 0,  # coldbox turbine 100 speed
            19946: 0,  # coldbox turbine 101 speed
            19947: 0,  # coldbox tempereture T106
            19948: 0,  # coldbox temperature TT111
            19949: 0,  # coldbox pressure PT102
            19950: 0,  # buffer pressure PT203
            19951: 0,  # purifier temperature TT104
            19952: 0,  # purifier temperature TT102
            19953: 0,  # coldbox temperature TT108
            19954: 0,  # coldbox pressure PT112
            19955: 0,  # liquefier coldbox CV103 %
            19956: 0,  # liquefier coldbox CV111 %
            19957: 0,  # liquefier coldbox CV112 %
            19958: 0,  # helium mother dewar level
            19961: 0,  # purifier level %
            19962: 0,  # impure helium supply pressure
            19963: 0,  # compressor low pressure control pressure
            19964: 0,  # compressor high pressure control pressure
            19966: 0,  # liquefier coldbox cv103 %
            19972: 0,  # CV2250 %
            19974: 0,  # CV2150 %
            19975: 0,  # CV2160 %
            19979: 0,  # liquid nitrogen status
            19982: 0,  # liquefier alarm 1
            19983: 0,  # liquefier alarm 2
            19996: 0,  # mcp liquid helium inventory
            19967: 0,  # CV120 automatic/manual
            19969: 0,  # CV121 automatic/manual
            19971: 0,  # low pressure automatic/manual
            19973: 0,  # high pressure automatic/manual
            19976: 0,  # TIC106 automatic/manual
            19977: 0,  # PIC112 automatic/manual
            19968: 0,  # CV120 position
            19970: 0,  # CV121 position
            19978: 0,  # purifier status
            19980: 0,  # compressor status
            19981: 0  # coldbox status
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
            19758: 0,  # gas counter ZOOM, SANS2D and POLREF
            19762: 0,  # gas counter magnet lab
            19766: 0,  # gas counter IMAT
            19768: 0,  # gas counter LET and NIMROD
            19772: 0  # gas counter R80 west
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
