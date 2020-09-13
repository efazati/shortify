import pathlib

import yaml

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
APP_ROOT = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = APP_ROOT / 'configs' / 'base_config.yaml'
TEMPLATES_ROOT = APP_ROOT / 'templates'


def load_config(config_path="None"):
    if not config_path:
        config_path = DEFAULT_CONFIG_PATH
    with open(config_path, 'rt') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return data


def load_envs():
    return {
        "PROJECT_ROOT": PROJECT_ROOT,
        "APP_ROOT": APP_ROOT,
        "TEMPLATES_ROOT": TEMPLATES_ROOT
    }
