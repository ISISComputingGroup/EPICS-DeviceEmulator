"""
Stream device for danfysik 8500-like PSU on RIKEN (RB2)
"""

from lewis.core.logging import has_log

from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply
from .dfkps_base import CommonStreamInterface

from dfkps_8500 import Danfysik8500StreamInterface

__all__ = ["DanfysikRIKENStreamInterface"]


@has_log
class DanfysikRIKENStreamInterface(Danfysik8500StreamInterface):
    """
    Stream interface for a Danfysik-like PSU on RIKEN (RB2).  Inherited from Danfysik 8500.
    """

    protocol = 'RIKEN'

    commands = CommonStreamInterface.commands + [
        CmdBuilder("set_current").escape("WA 0 ").int().eos().build(),  # ** only difference from 8500 **
        CmdBuilder("get_current").escape("AD 8").eos().build(),
        CmdBuilder("set_address").escape("ADR ").int().eos().build(),
        CmdBuilder("get_address").escape("ADR").eos().build(),
        CmdBuilder("init_comms").escape("REM").eos().build(),
        CmdBuilder("init_comms").escape("UNLOCK").eos().build(),
        CmdBuilder("get_slew_rate").escape("R").arg(r"[1-3]", argument_mapping=int).eos().build(),
        CmdBuilder("set_slew_rate").escape("W").arg(r"[1-3]", argument_mapping=int).spaces().int().eos().build()
    ]

    pass
