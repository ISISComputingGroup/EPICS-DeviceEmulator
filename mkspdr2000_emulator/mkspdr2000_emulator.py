import sys, random
sys.path.append("../test_framework")

from telnet_engine import TelnetEngine

class TemplateEmulator:
	def __init__(self):
		self.state = 0
		
	def process(self, data):
		if data == 'p':
			return "%e %e" % (random.uniform(0,1000),random.uniform(0,1000))
			
		if data == 'f':
			return "%e %e" % (random.uniform(0,1000),random.uniform(0,1000))
			
		if data == 'v':
			return "Emulated device v1.0"
			
		if data == 'u':
			return 'mBar'
		
		return None
		
		
if __name__ == "__main__":
	port_file = __file__
	dev = TemplateEmulator()
	TelnetEngine().start(dev, port_file)



