import os

_prefix = 'OFP_'


def _get_value_str(name, default_value):
    env_value = os.environ.get(name)
    return default_value if env_value is None else env_value


def _get_value_int(name, default_value):
    try:
        return int(os.environ[name])
    except:
        return default_value


def _get_value_bool(name, default_value):
    env_value = os.environ.get(name)
    if env_value in ['FALSE', 'False', 'false', '0']:
        return False
    if env_value in ['TRUE', 'True', 'true', '1']:
        return True
    return default_value


def _get_value(name, default_value, value_type):
    env_name = _prefix + name
    if value_type == 'str':
        return _get_value_str(env_name, default_value)
    if value_type == 'int':
        return _get_value_int(env_name, default_value)
    if value_type == 'bool':
        return _get_value_bool(env_name, default_value)
    return default_value


_default_options_objects = [
    {
        'name': 'HOST',
        'default_value': '127.0.0.1',
        'value_type': 'str'
    },
    {
        'name': 'PORT',
        'default_value': 5000,
        'value_type': 'int'
    },
    {
        'name': 'DEBUG',
        'default_value': False,
        'value_type': 'bool'
    },
    {
        'name': 'USE_LOCAL_STORAGE',
        'default_value': False,
        'value_type': 'bool'
    }
]


DEFAULT_ARGUMENTS = {obj['name']: _get_value(**obj) for obj in _default_options_objects}
