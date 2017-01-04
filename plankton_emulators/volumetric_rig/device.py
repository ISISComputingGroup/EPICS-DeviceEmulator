from lewis.devices import Device
from system_gases import SystemGases

# Define string literals for all gas names to avoid typos
UNKNOWN = "UNKNOWN"
EMPTY = "EMPTY"
VACUUM_EXTRACT = "VACUUM EXTRACT"
ARGON = "ARGON"
NITROGEN = "NITROGEN"
NEON = "NEON"
CARBON_DIOXIDE = "CARBON DIOXIDE"
CARBON_MONOXIDE = "CARBON MONOXIDE"
HELIUM = "HELIUM"
GRAVY = "GRAVY"
LIVER = "LIVER"
HYDROGEN = "HYDROGEN"
OXYGEN = "OXYGEN"
CURRIED_RAT = "CURRIED RAT"
FRESH_COFFEE = "FRESH COFFEE"
BACON = "BACON"
ONION = "ONION"
CHIPS = "CHIPS"
GARLIC = "GARLIC"
BROWN_SAUCE = "BROWN SAUCE"


class SimulatedVolumetricRig(Device):
    def __init__(self):
        self.system_gases = SystemGases()

        # Populate system gases
        gas_names = [UNKNOWN, EMPTY, VACUUM_EXTRACT, ARGON, NITROGEN, NEON, CARBON_DIOXIDE, CARBON_MONOXIDE, HELIUM,
                     GRAVY, LIVER, HYDROGEN, OXYGEN, CURRIED_RAT, FRESH_COFFEE, BACON, ONION, CHIPS, GARLIC,
                     BROWN_SAUCE]
        index = 0
        for gas_name in gas_names:
            self.system_gases.add_gas(index,gas_name)
            index += 1

        # Set unmixable gases
        for g in gas_names:
            self.system_gases.set_unmixable_by_name(UNKNOWN, g)
            self.system_gases.set_unmixable_by_name(LIVER, g)
            if g not in {ARGON, NITROGEN, VACUUM_EXTRACT, EMPTY}:
                self.system_gases.set_unmixable_by_name(NITROGEN, g)
            if g not in {NEON, CARBON_DIOXIDE, CARBON_MONOXIDE}:
                self.system_gases.set_unmixable_by_name(CARBON_MONOXIDE, g)
            if g in {CURRIED_RAT, FRESH_COFFEE, BACON, CHIPS}:
                self.system_gases.set_unmixable_by_name(GRAVY, g)
            if g in {OXYGEN, ONION, BROWN_SAUCE}:
                self.system_gases.set_unmixable_by_name(HYDROGEN, g)

        self.system_gases.set_buffer_gas(1, ARGON)
        self.system_gases.set_buffer_gas(2, NITROGEN)
        self.system_gases.set_buffer_gas(3, NEON)
        self.system_gases.set_buffer_gas(4, CARBON_DIOXIDE)
        self.system_gases.set_buffer_gas(5, HELIUM)
        self.system_gases.set_buffer_gas(6, HYDROGEN)

    def get_identity(self):
        return "ISIS Volumetric Gas Handing Panel"

    def get_plc_ip(self):
        return "192.168.1.100"

    def get_hmi_ip(self):
        return "192.168.1.101"

    def get_hmi_status(self):
        return "OK"