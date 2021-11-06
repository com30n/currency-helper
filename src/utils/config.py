import os
from typing import Any, List, Optional, Type, Union

import yaml
from yaml import ScalarNode
from yaml.constructor import BaseConstructor
from yaml.loader import SafeLoader

"""
Just some reused functions that could 
load an yaml configs with some additional improvements such as 
syntax sugar !!env that could get some variables from the environment
"""


class FileNotFound(Exception):
    """no file"""


def get_config_path() -> str:
    config_default_search_paths = ["./config.yaml", "./configs/config.yaml"]
    config_path = os.environ.get("CONFIG")
    if not config_path:
        for p in config_default_search_paths:
            if os.path.exists(p):
                config_path = p
                break
        else:
            config_path = ""
    return config_path


def load_config(config_path: Optional[str] = None) -> dict[str, Any]:
    if not config_path:
        config_path = os.getenv("CONFIG")
    if not config_path:
        raise RuntimeError(
            "No config specified. "
            'Please provide config by setting "CONFIG" env var '
            "or by passing it to `init_app` explicitly"
        )

    return _load_config(config_path)


def _load_config(path: str) -> dict[str, Union[str, dict[str, str], list[str]]]:
    loader_cls = SafeLoader
    _add_env_constructor(loader_cls)
    try:
        with open(path, "r") as yaml_file:
            config = yaml.load(yaml_file.read(), Loader=loader_cls)
    except IOError:
        raise FileNotFound("File {} not found".format(path))
    return config


def _add_env_constructor(loader_cls: Type[SafeLoader]) -> None:
    def from_env(parts: List[str]) -> str:
        if len(parts) == 1:
            return os.environ[parts[0]]

        return os.environ.get(parts[0], parts[1])

    def construct_yaml_env(
        self: BaseConstructor, node: ScalarNode
    ) -> Optional[dict[str, Union[str, dict[Any, Any], List[Any]]]]:
        scalar = self.construct_scalar(node)

        if not scalar:
            raise yaml.YAMLError(
                f'Got invalid pattern "!!env {scalar}", expected '
                f'"!!env ENV_VARIABLE, DEFAULT_VAL_OPTIONAL"'
            )

        if isinstance(scalar, str):
            parts = [x.strip() for x in scalar.split(",", maxsplit=1)]
            value = from_env(parts)
        else:
            return None
        return yaml.load(value, Loader=loader_cls)

    loader_cls.add_constructor("tag:yaml.org,2002:env", construct_yaml_env)
