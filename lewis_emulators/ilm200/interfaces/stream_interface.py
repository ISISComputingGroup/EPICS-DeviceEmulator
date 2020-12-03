from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder
from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")


@has_log
class Ilm200StreamInterface(StreamInterface):

    in_terminator = "\r"
    out_terminator = "\r"

    def __init__(self):

        super(Ilm200StreamInterface, self).__init__()
        # All commands preceded by "@i" where i is the ISOBUS address. Has no impact on emulator so is ignored.
        self.commands = {
            CmdBuilder(self.get_version).escape("@").int(ignore=True).escape("V").build(),
            CmdBuilder(self.get_status).escape("@").int(ignore=True).escape("X").build(),
            CmdBuilder(self.get_level).escape("@").int(ignore=True).escape("R").int().build(),
            CmdBuilder(self.set_rate_slow).escape("@").int(ignore=True).escape("S").int().build(),
            CmdBuilder(self.set_rate_fast).escape("@").int(ignore=True).escape("T").int().build(),
            CmdBuilder(self.set_remote_unlocked).escape("@").int(ignore=True).escape("C3").build(),
        }

        self.get_level_counter = 0

    def handle_error(self, request, error):
        print("An error occurred at request " + repr(request) + ": " + repr(error))
        return str(error)

    @if_connected
    def get_version(self):
        return "VILM200_EMULATED"

    @if_connected
    def set_remote_unlocked(self):
        return "C"  # Does nothing in emulator land

    @if_connected
    def set_rate_slow(self, channel):
        self._device.set_fill_rate(channel=int(channel), fast=False)
        return "S"

    @if_connected
    def set_rate_fast(self, channel):
        self._device.set_fill_rate(channel=int(channel), fast=True)
        return "T"

    @if_connected
    def get_level(self, channel):
        self.get_level_counter += 1

        self.log.info("bad replies = {} ({}), counter = {}".format(self.device.giving_intermittent_bad_replies, self.device.giving_intermittent_bad_replies.__class__.__name__, self.get_level_counter))

        # Error every 5 messages, i.e. when get_level_counter % 5 == 0
        # Don't want to error every other message as this might "beat" with the ioc's scan and cause e.g. channel 1 to
        # always fail and channel 2 to never fail.
        if self.device.giving_intermittent_bad_replies and self.get_level_counter % 5 == 0:
            # When device is giving intermittent comms errors, we get the reply to the get_status command when we have
            # actually asked for get_level
            self.log.info("Responding with incorrect response to get_level (giving bad replies)")
            return self.get_status()

        return "R{}".format(int(self._device.get_level(channel=int(channel))*10))

    def _get_channel_status(self, channel_number):
        channel = self._device.channels[channel_number]

        #  A full description of these bits can be found in the IOC or the manual
        bits = (
            channel.has_helium_current(),
            channel.is_fill_rate_fast(),
            not channel.is_fill_rate_fast(),
            not channel.is_filling() or channel.start_filling(),
            channel.is_filling() or channel.start_filling(),
            channel.is_level_low(),
            False,  # Alarm requested is always
            False,  # Pre-Pulse flowing current
        )

        # Construct bitwise return code from the various status bits
        return sum([int(set_it)*2**bit for bit, set_it in enumerate(bits)])

    @staticmethod
    def _get_logic_status():
        return 0  # Describes the state of the ILM relay. Not currently used in IOC

    @if_connected
    def get_status(self):
        d = self._device
        # "XabcSuuvvwwRxyz" : Described fully in ILM 200 manual section 8.2
        status_string = "X{ch1_type:01d}{ch2_type:01d}{ch3_type:01d}S{ch1_status:02x}{ch2_status:02x}"\
                        "{ch3_status:02x}R{logic_status:02d}".format(
                            ch1_type=d.get_cryo_type(1), ch2_type=d.get_cryo_type(2), ch3_type=d.get_cryo_type(3),
                            ch1_status=self._get_channel_status(1), ch2_status=self._get_channel_status(2),
                            ch3_status=self._get_channel_status(3),
                            logic_status=Ilm200StreamInterface._get_logic_status()
                        )
        self.log.info("STATUS: " + status_string)
        return status_string
