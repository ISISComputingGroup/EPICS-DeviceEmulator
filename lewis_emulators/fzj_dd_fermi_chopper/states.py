from lewis.core.statemachine import State

# FZJ Digital Drive Fermi Chopper Controller


class DefaultState(State):
    """
    Device is in default state.
    """
    NAME = 'Default'
