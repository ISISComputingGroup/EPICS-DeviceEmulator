from lewis.adapters.stream import StreamInterface
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply
from .aeroflex_base import CommonStreamInterface

__all__ = ['Aeroflex2023AStreamInterface']

if_connected = conditional_reply('connected')

@has_log
class Aeroflex2023AStreamInterface(CommonStreamInterface, StreamInterface):
    protocol = 'model2023A'
    
    commands = CommonStreamInterface.commands
    in_terminator = CommonStreamInterface.in_terminator
    out_terminator = CommonStreamInterface.out_terminator
    
    def get_carrier_freq(self):
        return f':CFRQ:VALUE {self._device.carrier_freq_val};INC {self._device.carrier_freq_inc};MODE {self._device.carrier_freq_mode}'	
        
    def reset(self):
        self._device.carrier_freq_val = 0
        self._device.rf_lvl_val = 0
        self._device.modulation_mode = 'AM'
        
        return ''
        
    def set_modulation(self, new_modulation_mode):
        cleaned_input = new_modulation_mode.replace('1','')
        split_modulation_val = cleaned_input.split('m')[0]
        self._device.modulation_mode = split_modulation_val
        
        return ''
