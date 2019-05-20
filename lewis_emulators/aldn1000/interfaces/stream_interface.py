from lewis.adapters.stream import StreamInterface, Cmd

from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.constants import STX, ETX
from lewis_emulators.utils.replies import conditional_reply

if_input_error = conditional_reply('input_correct', STX + "01I?NA" + ETX)
if_connected = conditional_reply("connected")


class Aldn1000StreamInterface(StreamInterface):

    in_terminator = "\r"

    directions = 'INF|WDR|REV'
    status_modes = 'I|W|S|P|T|U|A?R|A?S|A?T|A?E|A?O'

    def __init__(self):
        super(Aldn1000StreamInterface, self).__init__()

        self.commands = {
                CmdBuilder(self.get_diameter).int().escape('DIA').eos().build(),
                CmdBuilder(self.set_diameter).int().escape('DIA').float().eos().build(),
                CmdBuilder(self.get_volume).int().escape('VOL').eos().build(),
                CmdBuilder(self.set_volume).int().escape('VOL').float().eos().build(),
                CmdBuilder(self.get_direction).int().escape('DIR').eos().build(),
                CmdBuilder(self.set_direction).int().escape('DIR').arg(self.directions).eos().build(),
                CmdBuilder(self.get_rate).int().escape('RAT').eos().build(),
                CmdBuilder(self.set_rate).int().escape('RAT').float().string().eos().build(),
                CmdBuilder(self.get_program_function).int().escape('FUN').eos().build(),
                CmdBuilder(self.get_volume_dispensed).int().escape('DIS').eos().build(),
                CmdBuilder(self.clear_volume).int().escape('CLD').arg("INF|WDR").eos().build(),
                CmdBuilder(self.set_pump).int().arg('STP|RUN').eos().build(),
                CmdBuilder(self.get_status).int().eos().build(),
        }

    @if_input_error
    def basic_get_response(self, address, data=None, units=""):
        """It is expected that data inputs will be formatted using the format_data() method"""
        return STX + '{address:02d}{status}{data}{units}'.format(address=address, status=self.device.status,
                                                                 data=data, units=units) + ETX

    @if_input_error
    def basic_set_response(self, address):
        response = STX + '{:02d}{status}'.format(address, status=self.device.status) + ETX
        return response

    @if_connected
    def format_data(self, float):
        """ Restrict a float to only the first 5 characters

        The device requires very specific formatting (0000. to .0000) for floats, so we restrict the float output to
        to the first 5 characters of the float converted to a string. Hackish, but the only way we found to
        quickly implement this without writing our own formatter.

            Arguments:
                float (float): The float to be converted
            Returns:
                return (str): The first 5 characters of the input float.

        """
        return '{formatted_value:.5s}'.format(formatted_value=str(float))

    @if_connected
    def set_pump(self, address, action):
        self.device.address = address
        self.device.pump = action
        return self.basic_set_response(address)

    @if_connected
    def get_status(self, address):
        return self.basic_get_response(address, data=self.device.status)

    @if_connected
    def set_pump_on(self, address):
        self.device.address = address
        self.device.pump = 'ON'

    @if_connected
    def set_pump_off(self, address):
        self.device.address = address
        self.device.pump = 'OFF'

    @if_connected
    def get_diameter(self, address):
        return self.basic_get_response(address, data=self.format_data(self.device.diameter))

    @if_connected
    def set_diameter(self, address, new_diameter):
        self.device.address = address
        self.device.diameter = new_diameter
        return self.basic_set_response(address)

    @if_connected
    def get_volume(self, address):
        return self.basic_get_response(address, data=self.format_data(self.device.volume),
                                       units=self.device.volume_units)

    @if_connected
    def set_volume(self, address, volume):
        self.device.address = address
        self.device.volume = volume
        return self.basic_set_response(address)

    @if_connected
    def get_volume_dispensed(self, address):
        data = 'I{infused}W{withdrawn}{units}'.format(infused=self.format_data(self.device.volume_infused),
                                                      withdrawn=self.format_data(self.device.volume_withdrawn),
                                                      units=self.device.volume_units)
        return self.basic_get_response(address, data=data)

    @if_connected
    def get_direction(self, address):
        return self.basic_get_response(address, self.device.direction)

    @if_connected
    def set_direction(self, address, new_direction):
        self.device.address = address
        self.device.direction = new_direction
        return self.basic_set_response(address)

    @if_connected
    def get_rate(self, address):
        return self.basic_get_response(address, self.format_data(self.device.rate), self.device.units)

    @if_connected
    def set_rate(self, address, rate, units):
        self.device.address = address
        self.device.rate = rate
        self.device.units = units
        return self.basic_set_response(address)

    @if_connected
    def get_program_function(self, address):
        return self.basic_get_response(address, self.device.program_function)

    @if_connected
    def clear_volume(self, address, volume_type):
        self.device.address = address
        self.device.clear_volume(volume_type)
        return self.basic_set_response(address)
