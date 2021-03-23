import os
from onion_juicer import OnionJuicer

config_file = '%s/config.yaml' % os.path.dirname(os.path.abspath(__file__))
oj = OnionJuicer()
oj.export_results()

