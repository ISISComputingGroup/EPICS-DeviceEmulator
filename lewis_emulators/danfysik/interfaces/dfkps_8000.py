"""
Stream device for danfysik 8000
"""
from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log

from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply
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
        CmdBuilder("init_comms").escape("UNLOCK").build(),
    ]

    @conditional_reply("comms_initialized")
    def get_status(self):
        """
        Respond to the get_status command (S1)
        """
        def bit(condition):
            return "!" if condition else "."

        def ilk(name):
            return bit(name in self.device.active_interlocks)

        response = "{power_off}{pol_normal}{pol_reversed}{reg_transformer}{dac16}{dac17}{is_percent}{spare}"\
                   "{transistor_fault}{sum_interlock}{dc_overcurrent}{dc_overload}{reg_mod_fail}{prereg_fail}" \
                   "{phase_fail}{mps_waterflow_fail}{earth_leak_fail}{thermal_fail}{mps_overtemperature}" \
                   "{door_switch}{mag_waterflow_fail}{mag_overtemp}{mps_not_ready}{spare}".format(
                        spare=bit(False),
                        power_off=bit(not self.device.power),
                        pol_normal=bit(not self.device.negative_polarity),
                        pol_reversed=bit(self.device.negative_polarity),
                        reg_transformer=bit(False),
                        dac16=bit(False),
                        dac17=bit(False),
                        is_percent=bit(False),
                        transistor_fault=ilk("transistor_fault"),
                        sum_interlock=bit(len(self.device.active_interlocks) > 0),
                        dc_overcurrent=ilk("dc_overcurrent"),
                        dc_overload=ilk("dc_overload"),
                        reg_mod_fail=ilk("reg_mod_fail"),
                        prereg_fail=ilk("prereg_fail"),
                        phase_fail=ilk("phase_fail"),
                        mps_waterflow_fail=ilk("mps_waterflow_fail"),
                        earth_leak_fail=ilk("earth_leak_fail"),
                        thermal_fail=ilk("thermal_fail"),
                        mps_overtemperature=ilk("mps_overtemperature"),
                        door_switch=ilk("door_switch"),
                        mag_waterflow_fail=ilk("mag_waterflow_fail"),
                        mag_overtemp=ilk("mag_overtemp"),
                        mps_not_ready=bit(not self.device.power),
                    )

        assert len(response) == 24, "length should have been 24 but was {}".format(len(response))
        return response
