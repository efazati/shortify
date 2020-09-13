import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'configs' / 'base_config.yaml'


def load_config(config_path="None"):
    if not config_path:
        config_path = DEFAULT_CONFIG_PATH
    with open(config_path, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    print(data)
    return data
