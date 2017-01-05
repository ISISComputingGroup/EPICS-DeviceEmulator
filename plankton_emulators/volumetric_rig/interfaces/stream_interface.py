from lewis.adapters.stream import StreamAdapter, Cmd
from ..device import SimulatedVolumetricRig
from ..sensor_status import SensorStatus


class VolumetricRigStreamInterface(StreamAdapter):

    # The rig typically splits a command by whitespace and then uses the arguments it needs and then ignores the rest
    # so "IDN" will respond as "IDN BLAH BLAH BLAH" and "BCS 01" would be the same has "BCS 01 02 03".
    # Some commands that take input will respond with default (often invalid) parameters if not present. For example
    # "BCS" is the same as "BCS 00" and also "BCS AA".
    commands = {
        #Cmd("get_identity", "^IDN$"),
        Cmd("get_identity", "^IDN(\s.*)?$"),
        Cmd("get_identity", "^\?(\s.*)?$"),
        Cmd("get_buffer_control_and_status", "^BCS$"),
        Cmd("get_buffer_control_and_status", "^BCS\s(\S*).*$"),
        Cmd("get_ethernet_and_hmi_status", "^ETN(\s.*)?$"),
        Cmd("get_gas_control_and_status", "^GCS(\s.*)?$"),
        Cmd("get_gas_mix_matrix", "^GMM(\s.*)?$"),
        Cmd("gas_mix_check", "^GMC$"),
        Cmd("gas_mix_check", "^GMC\s(\S*)$"),
        Cmd("gas_mix_check", "^GMC\s(\S*)\s(\S*).*$"),
        Cmd("get_gas_number_available", "^GNA(\s.*)?$"),
        Cmd("get_hmi_status", "^HMI(\s.*)?$"),
        Cmd("get_hmi_count_cycles", "^HMC(\s.*)?$"),
        Cmd("get_memory_location", "^RDM"),
        Cmd("get_memory_location", "^RDM\s(\S*).*$"),
        Cmd("get_pressure_and_temperature_status", "^PTS(\s.*)?$"),
        Cmd("get_pressures", "^PMV(\s.*)?$"),
        Cmd("get_temperatures", "^TMV(\s.*)?$"),
        Cmd("get_ports_and_relays_hex", "^PTR(\s.*)?$"),
        Cmd("get_ports_output", "^POT(\s.*)?$"),
        Cmd("get_ports_input", "^PIN(\s.*)?$"),
        Cmd("get_ports_relays", "^PRY(\s.*)?$"),
        Cmd("get_system_status", "^STS(\s.*)?$"),
        Cmd("get_com_activity", "^COM(\s.*)?$"),
        Cmd("get_valve_status", "^VST(\s.*)?$"),
        Cmd("set_valve_open", "^OPV$"),
        Cmd("set_valve_open", "^OPV\s(\S*).*$"),
        Cmd("set_valve_closed", "^CLV.*$"),
        Cmd("set_valve_closed", "^CLV\s(\S*).*$"),
        Cmd("halt", "^HLT(\s.*)?$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self, device, arguments=None):
        self.rig = SimulatedVolumetricRig()
        # Lots of formatted output is based on fixed length strings
        self.gas_output_length = 20
        super(VolumetricRigStreamInterface, self).__init__(device, arguments)

    def get_identity(self, dummy):
        return "IDN,00," + self.rig.identify()

    def get_buffer_control_and_status(self, buffer_number_string="0"):
        try:
            buffer_number = int(buffer_number_string)
        except ValueError:
            # This is how the volumetric rig currently responds
            buffer_number = 0

        message_prefix = "BCS"
        num_length = 3
        error_message_prefix = " ".join([message_prefix, "Buffer", str(buffer_number)[:num_length].zfill(num_length)])
        buffer_too_low = " ".join([error_message_prefix,"Too Low"])
        buffer_too_high = " ".join([error_message_prefix + "Too High"])

        if buffer_number <= 0:
            return buffer_too_low
        elif buffer_number > len(self.rig.buffers):
            return buffer_too_high

        buff = self.rig.buffer(buffer_number)
        assert buff is not None
        return " ".join([
            message_prefix,
            buff.index_string(),
            buff.buffer_gas.index_string(),
            buff.buffer_gas.pad_name(self.gas_output_length, " "),
            "E" if buff.valve.is_enabled else "d",
            "O" if buff.valve.is_open else "c",
            buff.system_gas.index_string(),
            buff.system_gas.name
        ])

    def get_ethernet_and_hmi_status(self, dummy):
        # The syntax of the return string is odd: the separators are not consistent
        return " ".join([
            "ETN:PLC",
            self.rig.plc.ip + ",HMI",
            self.rig.hmi.status,
            "," + self.rig.hmi.ip
        ])

    def get_gas_control_and_status(self, dummy):
        lines = list()
        lines.append("No No Buffer               E O No System")
        for buff in self.rig.buffers:
            words = list()
            words.append(buff.index_string())
            words.append(buff.buffer_gas.index_string())
            words.append(buff.buffer_gas.pad_name(self.gas_output_length, ' '))
            words.append("E" if buff.valve.is_enabled else "d")
            words.append("O" if buff.valve.is_open else "c")
            words.append(buff.system_gas.index_string())
            words.append(buff.system_gas.name)
            lines.append(" ".join(words))
        lines.append("GCS")
        return '\r\n'.join(lines)

    def get_gas_mix_matrix(self, dummy):

        # Gather data
        system_gases = self.rig.system_gases.gases

        column_headers = [gas.pad_name(self.gas_output_length, '-') for gas in system_gases]
        row_titles = [" ".join([gas.index_string(), gas.pad_name(self.gas_output_length, ' ')]) for gas in system_gases]
        mixable_chars = [["<" if self.rig.mixer.can_mix(g1, g2) else "." for g1 in system_gases]
                         for g2 in system_gases]

        # Put data in output format
        lines = list()
        # Add column headers
        for i in range(len(max(column_headers, key=len))):
            words = list()
            # For the top-left block of white space
            words.append((len(max(row_titles, key=len))-1)*" ")
            # Vertically aligned gas names
            for j in range(len(column_headers)):
                words.append(column_headers[j][i])
            lines.append(' '.join(words))
        # Add rows
        assert len(row_titles) == len(mixable_chars)
        for i in range(len(row_titles)):
            words = list()
            words.append(row_titles[i])
            words.append(' '.join(mixable_chars[i]))
            lines.append(''.join(words))
        # Add footer
        lines.append("GMM allowance limit: " + str(len(system_gases)))

        return '\r\n'.join(lines)

    def gas_mix_check(self, gas1_index_raw="0", gas2_index_raw="0"):
        try:
            gas1_index = int(gas1_index_raw)
        except ValueError:
            gas1_index = 0
        try:
            gas2_index = int(gas2_index_raw)
        except ValueError:
            gas2_index = 0

        gas1 = self.rig.system_gases.gas_by_index(gas1_index)
        gas2 = self.rig.system_gases.gas_by_index(gas2_index)
        return ' '.join(["GMC",
                         gas1.index_string(), gas1.pad_name(self.gas_output_length, '.'),
                         gas2.index_string(), gas2.pad_name(self.gas_output_length, '.'),
                        "ok" if self.rig.mixer.can_mix(gas1, gas2) else "NO"])

    def get_gas_number_available(self, dummy):
        return len(self.rig.system_gases)

    def get_hmi_status(self, dummy):
        hmi = self.rig.hmi
        return " ".join(["HMI " + hmi.status + " ",
                         hmi.ip, "B", hmi.base_page_string(), "S", hmi.sub_page_string()])

    def get_hmi_count_cycles(self, dummy):
        return " ".join(["HMC"] + self.rig.hmi.count_cycles)

    def get_memory_location(self, location_raw="0"):
        try:
            location = int(location_raw)
        except ValueError:
            location = 0
        return " ".join(["RDM", location.zfill(4), self.rig.memory_location(location)])

    def get_pressure_and_temperature_status(self, dummy):

        def get_status_code(s):
            if s == SensorStatus.DISABLED:
                return "D"
            elif s == SensorStatus.NO_REPLY:
                return "X"
            elif s == SensorStatus.VALUE_IN_RANGE:
                return "O"
            elif s == SensorStatus.VALUE_TOO_LOW:
                return "L"
            elif s == SensorStatus.VALUE_TOO_HIGH:
                return "H"
            else:
                return "?"

        return "PTS " + \
               "".join([get_status_code(self.rig.temperature_sensors[i].status)
                        for i in reversed(range(len(self.rig.temperature_sensors)))]) + \
               "".join([get_status_code(self.rig.pressure_sensors[i].status)
                        for i in reversed(range(len(self.rig.pressure_sensors)))])

    def get_pressures(self, dummy):
        return " ".join(["PMV"] +
                        [self.rig.pressure_sensors[i].pressure
                         for i in reversed(range(len(self.rig.pressure_sensors)))] +
                        ["T", self.rig.target_pressure])

    def get_temperatures(self, dummy):
        return " ".join(["TMV"] +
                        [self.rig.temperature_sensors[i].temperature
                         for i in reversed(range(len(self.rig.temperature_sensors)))])

    def get_valve_status(self, dummy):
        valves = [self.rig.supply_valve, self.rig.vacuum_extract_valve,  self.rig.cell_valve] + \
                 [b.valve for b in self.rig.buffers.reverse()]

        def derive_status(valve):
            if valve.enabled() and valve.is_open():
                return "O"
            elif valve.enabled() and not valve.is_open():
                return "E"
            elif not valve.enabled() and valve.is_open():
                return "!"
            elif not valve.enabled() and not valve.is_open():
                return "D"
            else:
                assert False

        return "VST Valve Status " + "".join([derive_status(v) for v in valves])

    def _set_valve_status(self, buffer_number_raw, set_to_open):
        try:
            buffer_number = int(buffer_number_raw)
        except TypeError:
            buffer_number = 0

        message_prefix = " ".join([
            "OPV" if set_to_open else "CLV",
            "Value",
            str(buffer_number)
            ])
        if buffer_number <= 0:
            return message_prefix + " Too Low"
        elif buffer_number > len(self.rig.buffers):
            return message_prefix + " Too High"

        if self.rig.halted:
            return "CLV Rejected only allowed when running"
        else:
            valve = self.rig.buffer(buffer_number).valve
            original_status = valve.is_open
            valve.open() if set_to_open else valve.close()
            new_status = self.rig.buffer(buffer_number).valve.is_open

            def derive_status(is_open):
                return "open" if is_open else "closed"

            # e.g. CLV Valve Buffer 1 closed was open
            return " ".join([
                "OPV" if set_to_open else "CLV",
                "Valve Buffer",
                buffer_number.lstrip("0"),
                derive_status(original_status),
                "was",
                derive_status(new_status)])

    def set_valve_closed(self, buffer_number_raw):
        self._set_valve_status(buffer_number_raw, False)

    def set_valve_open(self, buffer_number_raw):
        self._set_valve_status(buffer_number_raw, True)

    def halt(self, dummy):
        if self.rig.halted:
            message = "SYSTEM ALREADY HALTED"
        else:
            self.rig.halt()
            assert self.rig.halted
            message = "SYSTEM NOW HALTED"
        return "HLT *** " + message + " ***"

    def get_system_status(self, dummy):
        return " ".join([
            "STS",
            str(self.rig.status_code).zfill(2),
            "STOP" if self.rig.errors.run else "run",
            "HMI" if self.rig.errors.hmi else "hmi",
            # Spelling error duplicated as on device
            "GUAGES" if self.rig.errors.gauges else "guages",
            "COMMS" if self.rig.errors.comms else "comms",
            "HLT" if self.rig.halted else "halted",
            "E-STOP" if self.rig.errors.estop else "estop"
        ])

    # Information about ports, relays and com traffic are currently returned statically
    def get_ports_and_relays_hex(self, dummy):
        return "PTR I:00 0000 0000 R:0000 0200 0000 O:00 0000 4400"

    def get_ports_output(self, dummy):
        return "POT qwertyus vsbbbbbbzyxwvuts aBhecSssvsbbbbbb"

    def get_ports_input(self, dummy):
        return "PIN qwertyui zyxwvutsrqponmlk abcdefghijklmneb"

    def get_ports_relays(self, dummy):
        return "PRY qwertyuiopasdfgh zyxwhmLsrqponmlk abcdefghihlbhace"

    def get_com_activity(self, dummy):
        return "COM ok  0113/0000"

    def handle_error(self, request, error):
        if str(error) == "None of the device's commands matched.":
            return "URC,04,Unrecognised Command," + str(request)
        else:
            print "An error occurred at request " + repr(request) + ": " + repr(error)