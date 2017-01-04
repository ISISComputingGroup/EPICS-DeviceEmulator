from lewis.adapters.stream import StreamAdapter, Cmd
from ..device import SimulatedVolumetricRig


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

    def __init__(self):
        self.simulated_rig = SimulatedVolumetricRig()
        self.gas_output_length = 20
        super(VolumetricRigStreamInterface, self).__init__()

    def get_identity(self):
        return "IDN,00," + self.simulated_rig.get_identity()

    def get_buffer_control_and_status(self,buffer_number_string):
        number_print_length = 3
        message_prefix = "BCS Buffer " + buffer_number_string.zfill(number_print_length)[:number_print_length] + " "
        buffer_too_low = message_prefix + "Too Low"
        buffer_too_high = message_prefix + "Too High"
        try:
            buffer_number = int(buffer_number_string)
        except TypeError:
            # This is how the volumetric rig currently responds
            return buffer_too_low

        if buffer_number <= 0:
            return buffer_too_low
        elif buffer_number > self.simulated_rig.number_of_buffers():
            return buffer_too_high

        buffer = self.simulated_rig.get_buffer(buffer_number)
        return " ".join([
            message_prefix[:-1],
            buffer.get_buffer_gas().get_index_string(),
            buffer.get_buffer_gas().get_name(length=self.gas_output_length, padding_character=" "),
            "E" if buffer.get_valve().enabled() else "d",
            "O" if buffer.get_valve().is_open() else "c",
            buffer.get_system_gas().get_index_string(),
            buffer.get_system_gas().get_name()
        ])


    def get_ethernet_and_hmi_status(self):
        return "ETN:PLC " + self.simulated_rig.get_plc_ip() + ",HMI " + self.simulated_rig.get_hmi_status() + " ," + \
               self.simulated_rig.get_hmi_ip()

    def get_gas_control_and_status(self):
        lines = list()
        lines.append("No No Buffer               E O No System")
        for buffer in self.simulated_rig.get_buffers():
            words = list()
            words.append(buffer.get_number())
            words.append(buffer.get_buffer_gas().get_index_string())
            words.append(buffer.get_buffer_gas().get_name(length=self.gas_output_length, padding_character=' '))
            words.append("E" if buffer.valve_available() else "d")
            words.append("O" if buffer.valve_open() else "c")
            words.append(buffer.get_system_gas().get_index_string())
            words.append(buffer.get_buffer_gas().get_name())
            lines.append(' '.join(words))
        lines.append("GCS")
        return '\n'.join(lines)

    def get_gas_mix_matrix(self):

        # Gather data
        system_gases = self.simulated_rig.get_system_gases().get_gases()
        column_headers = [gas.get_name(length=self.gas_output_length, padding_character='-')
                          for gas in system_gases]
        column_header_length = self.gas_output_length
        row_titles = [gas.get_index_string() + " " + gas.get_name(length=self.gas_output_length, padding_character=' ')
                      for gas in system_gases]
        row_title_length = max(row_titles, key=len)
        mixable_chars = [["<" if self.simulated_rig.mixable(g1,g2) else "." for g1 in system_gases]
                         for g2 in system_gases]

        # Put data in output format
        lines = list()
        # Add column headers
        for i in range(column_header_length):
            words = list()
            words.append((row_title_length-1)*" ")
            for j in range(len(column_headers)):
                words.append(column_headers[j][i])
            lines.append(' '.join(words))
        # Add rows
        assert len(row_titles)==len(mixable_chars)
        for i in range(len(row_titles)):
            words = list()
            words.append(row_titles[i])
            words.append(' '.join(mixable_chars[i]))
            lines.append(''.join(words))
        # Add footer
        lines.append("GMM allowance limit: " + str(len(system_gases)))

        return '\n'.join(lines)

    def gas_mix_check(self,gas1_index,gas2_index):
        gas1 = self.simulated_rig.get_system_gases().get_gas_by_index(gas1_index)
        gas2 = self.simulated_rig.get_system_gases().get_gas_by_index(gas2_index)
        return ' '.join(["GMC",
                        gas1.get_index_string(), gas1.get_name(length=self.gas_output_length, padding_character='.'),
                        gas2.get_index_string(), gas2.get_name(length=self.gas_output_length, padding_character='.'),
                        "ok" if self.simulated_rig.mixable(gas1, gas2) else "NO"])


    def get_gas_number_available(self):
        return str(self.simulated_rig.system_gases.count())

    def get_hmi_status(self):
        hmi = self.simulated_rig.get_hmi()
        return " ".join(["HMI " + hmi.get_status() + " ",
                         hmi.get_ip(), "B", hmi.get_base_page(), "S", hmi.get_sub_page()])

    def get_hmi_count_cycles(self):
        return " ".join(["HMC"] + self.simulated_rig.get_hmi().get_count_cycles())

    def get_memory_location(self,location):
        location_length = 4
        return " ".join(["RDM", location.zfill(location_length), self.simulated_rig.get_memory_location(location)])

    def get_pressure_and_temperature_status(self):

        def get_status_code(s):
            if s==Sensor.DISABLED:
                return "D"
            elif s==Sensor.NO_REPLY:
                return "X"
            elif s==Sensor.VALUE_IN_RANGE:
                return "O"
            elif s==Sensor.VALUE_TOO_LOW:
                return "L"
            elif s==Sensor.VALUE_TOO_HIGH:
                return "H"
            else:
                return "?"

        return "PTS " + \
               "".join([get_status_code(self.simulated_rig.get_temperature_sensor(i).get_status())
                        for i in reversed(range(self.simulated_rig.number_of_temperature_sensors()))]) + \
               "".join([get_status_code(self.simulated_rig.get_pressure_sensor(i).get_status())
                        for i in reversed(range(self.simulated_rig.number_of_pressure_sensors()))])

    def get_pressures(self):
        return " ".join(["PMV"] + [self.simulated_rig.get_pressure_sensor(i).get_pressure()
                                   for i in reversed(range(self.simulated_rig.number_of_pressure_sensors()))])

    def get_temperatures(self):
        return " ".join(["TMV"] + [self.simulated_rig.get_temperature_sensor(i).get_temperature()
                                   for i in reversed(range(self.simulated_rig.number_of_temperature_sensors()))])

    def get_valve_status(self):
        valves = [self.simulated_rig.get_supply_valve(),
                  self.get_vacuum_extract_valve(),
                  self.get_cell_valve()] + \
                 [b.get_valve() for b in self.simulated_rig.get_buffers().reverse()]

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

        return "VST Valve Status " + ''.join([derive_status(v) for v in valves])

    def set_valve_status(self,valve_number,set_to_open):
        if self.simulated_rig.halted():
            return "CLV Rejected only allowed when running"
        else:
            original_status = self.simulated_rig.is_valve_open(valve_number)
            self.simulated_rig.set_valve_open(set_to_open)
            new_status = self.simulated_rig.is_valve_open(valve_number)

            def derive_status(is_open):
                return "open" if is_open else "closed"

            return " ".join(["OPV" if set_to_open else "CLV", "Valve Buffer", valve_number.lstrip("0"),
                             derive_status(original_status), "was", derive_status(new_status)])

    def set_valve_closed(self, valve_number):
        self.set_valve_status(valve_number, False)

    def set_valve_open(self, valve_number):
        self.set_valve_status(valve_number, True)

    def halt(self):
        if self.simulated_rig.halted():
            message = "SYSTEM ALREADY HALTED"
        else:
            self.simulated_rig.halt()
            assert self.simulated_rig.halted()
            message = "SYSTEM NOW HALTED"
        return "HLT *** " + message + " ***"

    def get_system_status(self):
        return " ".join([
            "STS",
            str(self.simulated_rig.get_status_code()).zfill(2),
            "STOP" if self.simulated_rig.errors().run else "run",
            "HMI" if self.simulated_rig.errors().hmi else "hmi",
            "GUAGES" if self.simulated_rig.errors().guages else "guages",
            "COMMS" if self.simulated_rig.errors().guages else "comms",
            "HLT" if self.simulated_rig.halted() else "halted",
            "E-STOP" if self.simulated_rig.errors().estop else "estop"
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