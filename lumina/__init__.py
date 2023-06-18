from . import extensions


def get_config(category: str, parameter: str):
    from toml import load

    return load("config.toml").get(category).get(parameter)
