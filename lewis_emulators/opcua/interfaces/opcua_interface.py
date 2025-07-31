from lewis.adapters import opcua

"""
This is a fake OPC UA server interface which creates three values:
a temperature float, a name string, and a status boolean.
"""

class OPCUAInterface:
    """Interface for my device."""
    
    def __init__(self):
        self._temperature = 25.0
        self._vacuum_status = False
    
    @property
    def temperature(self):
        """Current temperature (read/write)"""
        return self._temperature

    @temperature.setter
    def set_temperature(self, value):
        """Set the temperature."""
        self.temperature = float(value)
    
    @property
    def vacuum_status(self):
        """Vacuum status (read-only)"""
        return self._vacuum_status
    
    def set_vacuum(self, status: bool):
        """Simulate a change in vacuum status"""
        self._vacuum_status = bool(status)

    @property
    def name(self):
        """Device name (read-only)"""
        return "TestOPCUADevice"
    
    
    
    def reset(self):
        """Reset the device."""
        self.temperature = 25.0
        self._vacuum_status = False
        return True

# Configuration for the adapter
opcua_adapter = {
    'options': {
        'port': 4840,
        'server_name': 'OPC UA Server',
        'read_only_properties': ['status']
    }
}
