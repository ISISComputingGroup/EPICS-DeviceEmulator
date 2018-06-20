from . util_classes import Mode, Direction, ErrorType

MODES = {
    "i": Mode("i", "I", "Infusion"),
    "w": Mode("w", "W", "Withdrawal"),
    "i/w": Mode("i/w", "IW", "Infusion/Withdrawal"),
    "w/i": Mode("w/i", "WI", "Withdrawal/Infusion"),
    "con": Mode("con", "CON", "Continuous")
}

NO_ERROR = ErrorType("No error", 0, "NO_ALARM")

DIRECTIONS = {
    "I": Direction("I", "Infusion"),
    "W": Direction("W", "Withdrawal"),
}
