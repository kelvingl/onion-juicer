import os
from onion_juicer import OnionJuicer

OnionJuicer('%s/config.yaml' % os.path.dirname(os.path.abspath(__file__))).extract()
