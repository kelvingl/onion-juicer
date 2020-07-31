import os
import yaml


class OnionJuicer:

    _config = None

    def __init__(self,
                 config_path='%s/config.yaml' % os.getcwd()):
        self._config = yaml.safe_load(config_path)
