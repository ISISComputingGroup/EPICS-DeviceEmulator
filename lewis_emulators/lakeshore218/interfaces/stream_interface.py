from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis_emulators.utils.command_builder import CmdBuilder

@has_log
class Lakeshore218StreamInterface(StreamInterface):
    """
    Stream interface for the serial port
    """

    in_terminator = "\r\n"
    out_terminator = "\r\n"

    commands = {}
