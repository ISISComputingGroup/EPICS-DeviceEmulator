from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

if_connected = conditional_reply('connected')

'''
Stream device for Aeroflex
'''

@has_log
class CommonStreamInterface(object):

    in_terminator = '\n'
    out_terminator = '\n'

    MULT_FACTOR = {
        'k': 1000,
        'M': 1000000,
        'G': 1000000000
    }
    
    commands = [
            CmdBuilder('get_carrier_freq').escape('cfrq?').eos().build(),
            CmdBuilder('get_rf_level').escape('rflv?').eos().build(),
            CmdBuilder('get_modulation').escape('mode?').eos().build(),
            CmdBuilder('reset').escape('*RST').eos().build(),
            CmdBuilder('get_error').escape('error?').eos().build(),
            
            CmdBuilder('set_carrier_freq').escape('CFRQ:VALUE ').any().eos().build(),
            CmdBuilder('set_rf_level').escape('RFLV:VALUE ').float().eos().build(),
            CmdBuilder('set_modulation').escape('MODE ').string().eos().build(), 
    ]
        
    def handle_error(self, request, error):
        '''
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        '''
        self.log.error('An error occurred at request ' + repr(request) + ': ' + repr(error))
        
        return ''
    
    def get_rf_level(self):
        return f':RFLV:UNITS {self._device.rf_lvl_unit};TYPE {self._device.rf_lvl_type};VALUE {self._device.rf_lvl_val};INC {self._device.rf_lvl_inc};{self._device.rf_lvl_status} '
	
    def get_modulation(self):
        return f':MODE {self._device.modulation_mode}'
        
    def get_error(self):
        return self._device.error
        
    def set_carrier_freq(self, new_carrier_freq):
        new_carrier_freq_val = new_carrier_freq.split('H')[0]

        if new_carrier_freq_val[-1:].isnumeric():
            self._device.carrier_freq_val = float(new_carrier_freq_val)
        else:
            self._device.carrier_freq_val = float(new_carrier_freq_val[:-1]) * self.MULT_FACTOR[new_carrier_freq_val[-1:]]
        
        return ''
	
    def set_rf_level(self, new_rf_lvl_val):
        self._device.rf_lvl_val = new_rf_lvl_val
        
        return ''
