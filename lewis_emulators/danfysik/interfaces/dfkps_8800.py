"""
Stream device for danfysik 8800
"""
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from .dfkps_base import CommonStreamInterface

__all__ = ["Danfysik8800StreamInterface"]


@has_log
class Danfysik8800StreamInterface(CommonStreamInterface, StreamInterface):
    """
    Stream interface for a Danfysik model 8800.
    """

    protocol = 'model8800'

    commands = CommonStreamInterface.commands + [
        CmdBuilder("set_current").escape("WA ").int().eos().build(),
        CmdBuilder("get_current").escape("ADCV").eos().build(),
    ]
