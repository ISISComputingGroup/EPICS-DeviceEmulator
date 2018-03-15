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

    def get_status(self):

        def bit(condition):
            return "!" if condition else "."

        def ilk(name):
            return bit(name in self.device.active_interlocks)

        response = "{spare}{user1}{user2}{user3}{user4}{user5}{user6}{fw_diode_overtemp}{low_water_flow}{door_open}" \
                   "{pol_normal}{pol_reversed}{spare}{spare}{spare}{spare}{diode_heatsink}{chassis_overtemp}" \
                   "{igbt_heatsink_overtemp}{hf_diode_overtemp}{switch_reg_ddct_fail}{switch_reg_supply_fail}" \
                   "{igbt_driver_fail}{spare}{spare}{ac_undervolt}{spare}{ground_ripple}{ground_leak}"\
                   "{overcurrent}{power_on}{ready}".format(
                        spare=bit(False),
                        user1=ilk("user1"),
                        user2=ilk("user2"),
                        user3=ilk("user3"),
                        user4=ilk("user4"),
                        user5=ilk("user5"),
                        user6=ilk("user6"),
                        pol_normal=bit(not self.device.negative_polarity),
                        pol_reversed=bit(self.device.negative_polarity),
                        fw_diode_overtemp=ilk("fw_diode_overtemp"),
                        low_water_flow=ilk("low_water_flow"),
                        door_open=ilk("door_open"),
                        diode_heatsink=ilk("diode_heatsink"),
                        chassis_overtemp=ilk("chassis_overtemp"),
                        igbt_heatsink_overtemp=ilk("igbt_heatsink_overtemp"),
                        hf_diode_overtemp=ilk("hf_diode_overtemp"),
                        switch_reg_ddct_fail=ilk("switch_reg_ddct_fail"),
                        switch_reg_supply_fail=ilk("switch_reg_supply_fail"),
                        igbt_driver_fail=ilk("igbt_driver_fail"),
                        ac_undervolt=ilk("ac_undervolt"),
                        ground_ripple=ilk("ground_ripple"),
                        ground_leak=ilk("ground_leak"),
                        overcurrent=ilk("overcurrent"),
                        power_on=bit(not self.device.power),
                        ready=bit(self.device.power),
                    )

        assert len(response) == 32
        return response
