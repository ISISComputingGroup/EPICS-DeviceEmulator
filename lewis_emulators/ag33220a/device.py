from lewis.devices import Device


class SimulatedAG33220A(Device):
    voltage = 1
    frequency = 1000
    offset = 0
    units = "VPP"
    function = "SIN"
    output = 0
    pass
