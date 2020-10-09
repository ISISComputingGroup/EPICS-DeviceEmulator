from .kepco_base import KepcoStreamInterface

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis_emulators.utils.replies import conditional_reply

if_connected = conditional_reply("connected")

__all__ = ["KepcoNoRemStreamInterface"]


@has_log
class KepcoNoRemStreamInterface(KepcoStreamInterface, StreamInterface):
    """
    A stream interface for the kepco with no remote command available
    """

    protocol = "no_rem"

    def __init__(self):
        super(KepcoNoRemStreamInterface, self).__init__()
        self._idn_no_firmware = "KEPCO, BIT 4886 100-2 123456 1.8-"
        self._firmware = 1.8

    @if_connected
    def set_control_mode(self, mode):
        raise ValueError("No SYST:REM command available")

    @if_connected
    def reset(self):
        self._device.reset(self._idn_no_firmware, self._firmware)

