from lewis.adapters.modbus import ModbusInterface, ModbusBasicDataBank
from lewis.core.logging import has_log


@has_log
class Moxa1210ModbusInterface(ModbusInterface):
    """
    Creates modbus data registers and makes them available to the lewis device.
    """

    di = ModbusBasicDataBank(False, last_addr=0x10)
    co = di
    ir = ModbusBasicDataBank(0)
    hr = ir

    @ModbusInterface.device.setter
    def device(self, new_device):
        """
        Overrides base implementation to give attached device a reference to self
        Required to allow communications between the interface and device
        """
        ModbusInterface.device.fset(self, new_device)
        self.device.interface = self
