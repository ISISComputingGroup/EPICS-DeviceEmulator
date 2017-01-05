from lewis.adapters.stream import StreamAdapter, Cmd
from ..device import SimulatedVolumetricRig
from ..sensor_status import SensorStatus
from ..utilities import optional_int_string_format, convert_raw_to_int


class VolumetricRigStreamInterface(StreamAdapter):

    # The rig typically splits a command by whitespace and then uses the arguments it needs and then ignores the rest
    # so "IDN" will respond as "IDN BLAH BLAH BLAH" and "BCS 01" would be the same has "BCS 01 02 03".
    # Some commands that take input will respond with default (often invalid) parameters if not present. For example
    # "BCS" is the same as "BCS 00" and also "BCS AA".
    commands = {
        Cmd("get_identity", "^IDN(?: .*)?$"),
        Cmd("get_identity", "^\?(?: .*)?$"),
        Cmd("get_buffer_control_and_status", "^BCS(?:\s(\S*))?.*$"),
        Cmd("get_ethernet_and_hmi_status", "^ETN(?: .*)?$"),
        Cmd("get_gas_control_and_status", "^GCS(?: .*)?$"),
        Cmd("get_gas_mix_matrix", "^GMM(?: .*)?$"),
        Cmd("gas_mix_check", "^GMC(?:\s(\S*))?(?:\s(\S*))?.*$"),
        Cmd("get_gas_number_available", "^GNA(?: .*)?$"),
        Cmd("get_hmi_status", "^HMI(?: .*)?$"),
        Cmd("get_hmi_count_cycles", "^HMC(?: .*)?$"),
        Cmd("get_memory_location", "^RDM(?:\s(\S*))?.*"),
        Cmd("get_pressure_and_temperature_status", "^PTS(?: .*)?$"),
        Cmd("get_pressures", "^PMV(?: .*)?$"),
        Cmd("get_temperatures", "^TMV(?: .*)?$"),
        Cmd("get_ports_and_relays_hex", "^PTR(?: .*)?$"),
        Cmd("get_ports_output", "^POT(?: .*)?$"),
        Cmd("get_ports_input", "^PIN(?: .*)?$"),
        Cmd("get_ports_relays", "^PRY(?: .*)?$"),
        Cmd("get_system_status", "^STS(?: .*)?$"),
        Cmd("get_com_activity", "^COM(?: .*)?$"),
        Cmd("get_valve_status", "^VST(?: .*)?$"),
        Cmd("set_valve_open", "^OPV(?:\s(\S*))?.*$"),
        Cmd("set_valve_closed", "^CLV(?:\s(\S*))?.*$"),
        Cmd("halt", "^HLT(?: .*)?$"),
    }

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self, device, arguments=None):
        self.rig = SimulatedVolumetricRig()
        # Lots of formatted output is based on fixed length strings
        self.gas_output_length = 20
        super(VolumetricRigStreamInterface, self).__init__(device, arguments)

    def get_identity(self):
        return "IDN,00," + self.rig.identify()

    def _build_buffer_control_and_status_string(self, buffer_number):
        buff = self.rig.buffer(buffer_number)
        assert buff is not None
        return " ".join([
            "",
            buff.index(as_string=True),
            buff.buffer_gas().index(as_string=True),
            buff.buffer_gas().name(self.gas_output_length, " "),
            "E" if buff.valve_is_enabled() else "d",
            "O" if buff.valve_is_open() else "c",
            buff.system_gas().index(as_string=True),
            buff.system_gas().name()
        ])

    def get_buffer_control_and_status(self, buffer_number_raw):
        buffer_number = convert_raw_to_int(buffer_number_raw)
        message_prefix = "BCS"
        num_length = 3
        error_message_prefix = " ".join([message_prefix, "Buffer", str(buffer_number)[:num_length].zfill(num_length)])
        buffer_too_low = " ".join([error_message_prefix, "Too Low"])
        buffer_too_high = " ".join([error_message_prefix, "Too High"])

        if buffer_number <= 0:
            return buffer_too_low
        elif buffer_number > len(self.rig.buffers()):
            return buffer_too_high
        else:
            return "BCS " + self._build_buffer_control_and_status_string(buffer_number)

    def get_ethernet_and_hmi_status(self):
        # The syntax of the return string is odd: the separators are not consistent
        return " ".join([
            "ETN:PLC",
            self.rig.plc.ip() + ",HMI",
            self.rig.hmi_status(),
            "," + self.rig.hmi_ip()
        ])

    def get_gas_control_and_status(self):
        return "\r\n".join(
            ["No No Buffer               E O No System"] +
            [self._build_buffer_control_and_status_string(b.index()) for b in self.rig.buffers()] +
            ["GCS"]
        )

    def get_gas_mix_matrix(self):
        # Gather data
        system_gases = self.rig.system_gases.gases()

        column_headers = [gas.name(self.gas_output_length, '|') for gas in system_gases]
        row_titles = [" ".join([gas.index(as_string=True), gas.name(self.gas_output_length, ' ')])
                      for gas in system_gases]
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

    def gas_mix_check(self, gas1_index_raw, gas2_index_raw):
        gas1 = self.rig.system_gases.gas_by_index(convert_raw_to_int(gas1_index_raw))
        gas2 = self.rig.system_gases.gas_by_index(convert_raw_to_int(gas2_index_raw))
        if gas1 is None:
            gas1 = self.rig.system_gases.gas_by_index(0)
        if gas2 is None:
            gas2 = self.rig.system_gases.gas_by_index(0)

        return ' '.join(["GMC",
                         gas1.index(as_string=True), gas1.name(self.gas_output_length, '.'),
                         gas2.index(as_string=True), gas2.name(self.gas_output_length, '.'),
                        "ok" if self.rig.mixer.can_mix(gas1, gas2) else "NO"])

    def get_gas_number_available(self):
        return self.rig.system_gases.gas_count()

    def get_hmi_status(self):
        hmi = self.rig.hmi()
        return ",".join(["HMI " + hmi.status() + " ", hmi.ip(),
                         "B",hmi.base_page(as_string=True, length=3),
                         "S",hmi.sub_page(as_string=True, length=3),
                         "C",hmi.count(as_string=True, length=4),
                         "L",hmi.limit(as_string=True, length=4),
                         "M",hmi.max_grabbed(as_string=True, length=4)
                         ])

    def get_hmi_count_cycles(self):
        return " ".join(["HMC"] + self.rig.hmi_count_cycles())

    def get_memory_location(self, location_raw):
        location = convert_raw_to_int(location_raw)
        return " ".join(["RDM", optional_int_string_format(location, as_string=True, length=4),
                         self.rig.memory_location(location, as_string=True, length=6)])

    def get_pressure_and_temperature_status(self):

        def get_status_code(status):
            if status == SensorStatus.DISABLED:
                return "D"
            elif status == SensorStatus.NO_REPLY:
                return "X"
            elif status == SensorStatus.VALUE_IN_RANGE:
                return "O"
            elif status == SensorStatus.VALUE_TOO_LOW:
                return "L"
            elif status == SensorStatus.VALUE_TOO_HIGH:
                return "H"
            else:
                return "?"

        return "PTS " + \
               "".join([get_status_code(s.status()) for s in
                        self.rig.pressure_sensors(reverse=True)+self.rig.temperature_sensors(reverse=True)])

    def get_pressures(self):
        return " ".join(["PMV"] +
                        [p.pressure for p in self.rig.pressure_sensors(reverse=True)] +
                        ["T", self.rig.target_pressure()])

    def get_temperatures(self):
        return " ".join(["TMV"] +
                        [t.temperature for t in self.rig.temperature_sensors(reverse=True)])

    def get_valve_status(self):

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

        return "VST Valve Status " + "".join([derive_status(v) for v in self.rig.valves()])

    def _set_valve_status(self, valve_number_raw, set_to_open):
        valve_number = convert_raw_to_int(valve_number_raw)
        command = "OPV" if set_to_open else "CLV"
        message_prefix = " ".join([
            command,
            "Value",
            str(valve_number)
            ])
        if self.rig.halted():
            return "CLV Rejected only allowed when running"
        elif valve_number <= 0:
            return message_prefix + " Too Low"
        elif valve_number <= self.rig.buffer_count():
            valve_status = self.rig.buffer_valve_is_open(valve_number)
            open_valve = self.rig.open_buffer_valve(valve_number)
            close_valve = self.rig.close_buffer_valve(valve_number)
        elif valve_number == self.rig.buffer_count() + 1:
            valve_status = self.rig.cell_valve_is_open()
            open_valve = self.rig.open_cell_valve()
            close_valve = self.rig.close_cell_valve()
        elif valve_number == self.rig.buffer_count() + 2:
            valve_status = self.rig.vacuum_valve_is_open()
            open_valve = self.rig.open_vacuum_valve()
            close_valve = self.rig.close_vacuum_valve()
        else:
            return message_prefix + " Too High"

        original_status = valve_status()
        open_valve() if set_to_open else close_valve()
        new_status = valve_status()

        def derive_status(is_open):
            return "open" if is_open else "closed"

        # e.g. CLV Valve Buffer 1 closed was open
        return " ".join([
            command,
            "Valve Buffer",
            str(valve_number),
            derive_status(original_status),
            "was",
            derive_status(new_status)])

    def set_valve_closed(self, buffer_number_raw):
        self._set_valve_status(buffer_number_raw, False)

    def set_valve_open(self, buffer_number_raw):
        self._set_valve_status(buffer_number_raw, True)

    def halt(self):
        if self.rig.halted():
            message = "SYSTEM ALREADY HALTED"
        else:
            self.rig.halt()
            assert self.rig.halted()
            message = "SYSTEM NOW HALTED"
        return "HLT *** " + message + " ***"

    def get_system_status(self):
        return " ".join([
            "STS",
            self.rig.status_code(as_string=True, length=2),
            "STOP" if self.rig.errors().run else "run",
            "HMI" if self.rig.errors().hmi else "hmi",
            # Spelling error duplicated as on device
            "GUAGES" if self.rig.errors().gauges else "guages",
            "COMMS" if self.rig.errors().comms else "comms",
            "HLT" if self.rig.halted() else "halted",
            "E-STOP" if self.rig.errors().estop else "estop"
        ])

    # Information about ports, relays and com traffic are currently returned statically
    def get_ports_and_relays_hex(self):
        return "PTR I:00 0000 0000 R:0000 0200 0000 O:00 0000 4400"

    def get_ports_output(self):
        return "POT qwertyus vsbbbbbbzyxwvuts aBhecSssvsbbbbbb"

    def get_ports_input(self):
        return "PIN qwertyui zyxwvutsrqponmlk abcdefghijklmneb"

    def get_ports_relays(self):
        return "PRY qwertyuiopasdfgh zyxwhmLsrqponmlk abcdefghihlbhace"

    def get_com_activity(self):
        return "COM ok  0113/0000"

    def handle_error(self, request, error):
        if str(error) == "None of the device's commands matched.":
            return "URC,04,Unrecognised Command," + str(request)
        else:
            print "An error occurred at request " + repr(request) + ": " + repr(error)