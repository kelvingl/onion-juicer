import os
from onion_juicer import OnionJuicer

config_path = '%s/config.yaml' % os.path.dirname(os.path.abspath(__file__))
juicer = OnionJuicer(config_path)


z = ConnectionManager()

print(z)

print('yuaodfaosdasd')
