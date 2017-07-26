from lewis.devices import Device


class SimulatedAG33220A(Device):
    make = "Agilent Technologies,33220A"
    firmwareRevNum = "MY44033103,2.02"
    bootKernelRevisionNumber = "2.02"
    asicRevNum = "22"
    printedCircuitBoardRevNum = "2"
    idn = make+"-"+firmwareRevNum+"-"+bootKernelRevisionNumber+"-"+asicRevNum+"-"+printedCircuitBoardRevNum
    voltage = 1
    frequency = 1000
    offset = 0
    units = "VPP"
    function = "SIN"
    output = 0
    pass
