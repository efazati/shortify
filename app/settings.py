import os
import pathlib

import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
APP_ROOT = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = APP_ROOT / 'configs' / 'base_config.yml'
TEMPLATES_ROOT = APP_ROOT / 'templates'


def load_config(config_path=None):
    """
    Load configs from yaml file.
    # @TODO: later we should make a proccess to overwrite all the configs with environment variables
    :param config_path:
    :return:
    """
    if not config_path:
        config_path = DEFAULT_CONFIG_PATH
    with open(config_path, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def load_envs():
    """
    Add some envs details for components that needs these environments variables
    :return:
    """
    POD_NAME = os.environ.get('POD_NAME', 'pod')
    return {
        "PROJECT_ROOT": PROJECT_ROOT,
        "APP_ROOT": APP_ROOT,
        "TEMPLATES_ROOT": TEMPLATES_ROOT,
        "POD_NAME": POD_NAME
    }
