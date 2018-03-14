"""
Stream device for danfysik 8000
"""
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.command_builder import CmdBuilder
from .dfkps_base import CommonStreamInterface

__all__ = ["Danfysik8000StreamInterface"]


@has_log
class Danfysik8000StreamInterface(CommonStreamInterface, StreamInterface):
    """
    Stream interface for a Danfysik model 8000.
    """

    protocol = 'model8000'

    commands = CommonStreamInterface.commands + [
        CmdBuilder("set_current").escape("DA 0 ").int().eos().build(),
        CmdBuilder("get_current").escape("AD 8").eos().build(),
    ]
