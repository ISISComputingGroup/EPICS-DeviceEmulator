from lewis.adapters.stream import StreamAdapter, Cmd

gases = ["UNKNOWN", "EMPTY", "VACUUM EXTRACT", "ARGON", "NITROGEN", "NEON", "CARBON DIOXIDE", "CARBON MONOXIDE",
         "HELIUM", "GRAVY", "LIVER", "HYDROGEN", "OXYGEN", "CURRIED RAT", "FRESH COFFEE", "BACON", "ONION", "CHIPS",
         "GARLIC", "BROWN SAUCE"]


def is_mixable(g1, g2):
    if "LIVER" in {g1, g2}:
        return False
    elif "NITROGEN" in {g1, g2} and not {g1, g2}.isdisjoint({"EMPTY", "VACUUM EXTRACT", "ARGON", "NEON"}):
        return False
    else:
        return True


class VolumetricRigStreamInterface(StreamAdapter):

    commands = {
        Cmd("get_identity", "^IDN$"),
        Cmd("get_identity", "^\?$"),
        Cmd("get_buffer_control_and_status", "^BCS\s([0-9]+)$"),
        Cmd("get_ethernet_and_hmi_status", "^ETN$"),
        Cmd("get_gas_control_and_status", "^GCS$"),
        Cmd("get_gas_mix_matrix", "^GMM$"),
        Cmd("gas_mix_check", "^GMC\s([0-9]+)\s([0-9]+)$"),
        Cmd("get_gas_number_available", "^GNA$"),
        Cmd("get_hmi_status", "^HMI$"),
        Cmd("get_hmi_count_cycles", "^HMC$"),
        Cmd("get_memory_location", "^RDM\s([0-9]+)$"),
        Cmd("get_pressure_and_temperature_status", "^PTS$"),
        Cmd("get_pressures", "^PMV$"),
        Cmd("get_temperatures", "^TMV$"),
        Cmd("get_ports_and_relays_hex", "^PTR$"),
        Cmd("get_ports_output", "^POT$"),
        Cmd("get_ports_input", "^PIN$"),
        Cmd("get_ports_relays", "^PRY$"),
        Cmd("get_system_status", "^STS$"),
        Cmd("get_com_activity", "^COM$"),
        Cmd("get_valve_status", "^VST$"),
        Cmd("set_valve_open", "^OPV\s([0-9]+)$"),
        Cmd("set_valve_closed", "^CLV\s([0-9]+)$"),
        Cmd("halt", "^HLT$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def get_identity(self):
        return "IDN,00,ISIS Volumetric Gas Handing Panel"

    def get_buffer_control_and_status(self,buffer):
        return "BCS "+buffer+" 04 NITROGEN             d c 01 EMPTY"

    def get_ethernet_and_hmi_status(self):
        return "ETN:PLC 192.168.100.156,HMI OK ,192.168.100.208"

    def get_gas_control_and_status(self):
        lines = list()
        lines.append("No No Buffer               E O No System")
        lines.append(" 1 03 ARGON                E O 03 ARGON")
        lines.append(" 2 04 NITROGEN             d c 01 EMPTY")
        lines.append(" 3 05 NEON                 E c 01 EMPTY")
        lines.append(" 4 06 CARBON DIOXIDE       E c 01 EMPTY")
        lines.append(" 5 08 HELIUM               E c 08 HELIUM")
        lines.append(" 6 11 HYDROGEN             E c 01 EMPTY")
        lines.append("GCS")
        return '\n'.join(lines)

    def get_gas_mix_matrix(self):
        length_limit = 20
        padded_gases = [(g + (length_limit-len(g))*"-") for g in gases]
        lines = list()

        # Column headers
        for i in range(length_limit):
            words = list()
            words.append(' '*(length_limit+3))
            for j in range(length_limit):
                words.append(padded_gases[j][i])
            lines.append(''.join(words))

        # Rows
        for i in range(length_limit):
            words = list()
            words.append(str(i).zfill(2))
            words.append(padded_gases[i])
            for j in range(length_limit):
                words.append("<" if is_mixable(gases[i], gases[j]) else ".")
            lines.append(' '.join(words))

        # Footer
        lines.append("GMM allowance limit: " + str(length_limit))

        return '\n'.join(lines)

    def gas_mix_check(self,gas1_index,gas2_index):
        gas1 = gases[int(gas1_index)]
        gas2 = gases[int(gas2_index)]
        gas1_padded = gas1 + "."*(20-len(gas1))
        gas2_padded = gas2 + "."*(20-len(gas2))
        return "GMC " + gas1_index.zfill(2) + " " + gas1_padded + " " + gas2_index.zfill(2) + " " + \
               gas2_padded + " " + ("ok" if is_mixable(gas1,gas2) else "NO")

    def get_gas_number_available(self):
        return "20"

    def get_hmi_status(self):
        return "HMI OK ,192.168.100.208,B,034,S,041"

    def get_hmi_count_cycles(self):
        return "HMC 999 006 002 002 002 002 002 001 001 310"

    def get_memory_location(self,location):
        return "RDM " + location.zfill(4) + " 000000"

    def get_pressure_and_temperature_status(self):
        return "PTS ODDDDDDDDDDDDD"

    def get_pressures(self):
        return "PMV 00.00 01.00 00.00 00.00 01.02 00.00"

    def get_temperatures(self):
        return "TMV 25.00 00.00 00.00 00.00 00.00 00.00 00.00 00.00 00.00"

    def get_ports_and_relays_hex(self):
        return "PTR I:00 0000 0000 R:0000 0200 0000 O:00 0000 4400"

    def get_ports_output(self):
        return "POT qwertyus vsbbbbbbzyxwvuts aBhecSssvsbbbbbb"

    def get_ports_input(self):
        return "PIN qwertyui zyxwvutsrqponmlk abcdefghijklmneb"

    def get_ports_relays(self):
        return "PRY qwertyuiopasdfgh zyxwhmLsrqponmlk abcdefghihlbhace"

    def get_system_status(self):
        return "STS 09 STOP hmi guages comms hlt E-STOP"

    def get_com_activity(self):
        return "COM ok  0113/0000"

    def get_valve_status(self):
        return "VST Valve Status DDDDDDDDD"

    def set_valve_closed(self,valve_number):
        #return "CLV Rejected only allowed when running"
        return "CLV Valve Buffer " + valve_number.lstrip("0") + " closed was open"

    def set_valve_open(self,valve_number):
        #return "OLV Rejected only allowed when running"
        return "OPV Valve Buffer " + valve_number.lstrip("0") + " opened was closed "

    def halt(self):
        return "HLT *** SYSTEM NOW HALTED ***"