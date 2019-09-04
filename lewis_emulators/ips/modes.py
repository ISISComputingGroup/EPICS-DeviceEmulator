from enum import Enum


class Activity(Enum):
    HOLD = "Hold"
    TO_SETPOINT = "To Setpoint"
    TO_ZERO = "To Zero"
    CLAMP = "Clamped"
