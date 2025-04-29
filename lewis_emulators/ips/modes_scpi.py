from enum import Enum


class Activity(Enum):
    HOLD = "HOLD"
    TO_SETPOINT = "RTOS"
    TO_ZERO = "RTOZ"
    CLAMP = "CLMP"


class Control(Enum):
    LOCAL_LOCKED = "Local & Locked"
    REMOTE_LOCKED = "Remote & Unlocked"
    LOCAL_UNLOCKED = "Local & Unlocked"
    REMOTE_UNLOCKED = "Remote & Unlocked"
    AUTO_RUNDOWN = "Auto-Run-Down"


class SweepMode(Enum):
    TESLA_FAST = "Tesla Fast"


class Mode(Enum):
    FAST = "Fast"
    SLOW = "Slow"


class MagnetSupplyStatus(Enum):
    """
    | Status                               | Bit Value | Bit Position |
    |--------------------------------------|-----------|--------------|
    | Switch Heater Mismatch               | 00000001  | 0            |
    | Over Temperature [Rundown Resistors] | 00000002  | 1            |
    | Over Temperature [Sense Resistor]    | 00000004  | 2            |
    | Over Temperature [PCB]               | 00000008  | 3            |
    | Calibration Failure                  | 00000010  | 4            |
    | MSP430 Firmware Error                | 00000020  | 5            |
    | Rundown Resistors Failed             | 00000040  | 6            |
    | MSP430 RS-485 Failure                | 00000080  | 7            |
    | Quench detected                      | 00000100  | 8            |
    | Catch detected                       | 00000200  | 9            |
    | Over Temperature [Sense Amplifier]   | 00001000  | 12           |
    | Over Temperature [Amplifier 1]       | 00002000  | 13           |
    | Over Temperature [Amplifier 2]       | 00004000  | 14           |
    | PWM Cutoff                           | 00008000  | 15           |
    | Voltage ADC error                    | 00010000  | 16           |
    | Current ADC error                    | 00020000  | 17           |

    This information is not published and was derived from
    direct questions to Oxford Instruments.
"""
    OK = 0x00000000
    SWITCH_HEATER_MISMATCH = 0x00000001
    OVER_TEMPERATURE_RUNDOWN_RESISTORS = 0x00000002
    OVER_TEMPERATURE_SENSE_RESISTOR = 0x00000004
    OVER_TEMPERATURE_PCB = 0x00000008
    CALIBRATION_FAILURE = 0x00000010
    MSP430_FIRMWARE_ERROR = 0x00000020
    RUNDOWN_RESISTORS_FAILED = 0x00000040
    MSP430_RS_485_FAILURE = 0x00000080
    QUENCH_DETECTED = 0x00000100
    CATCH_DETECTED = 0x00000200
    OVER_TEMPERATURE_SENSE_AMPLIFIER = 0x00001000
    OVER_TEMPERATURE_AMPLIFIER_1 = 0x00002000
    OVER_TEMPERATURE_AMPLIFIER_2 = 0x00004000
    PWM_CUTOFF = 0x00008000
    VOLTAGE_ADC_ERROR = 0x00010000
    CURRENT_ADC_ERROR = 0x00020000
