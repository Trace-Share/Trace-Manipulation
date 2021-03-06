import json
import yaml


###############################################
################## Parsing
###############################################


def parse_yaml_args_withReference(config_filepath, arg_filepath):
    """
    Parses input arg(ument) yml file and default config file. Creates resulting
    dictionary of arguments and their values. 
    Arguments in arg file that are not in config file are ignored.
    Arguments in config file and not in arg file are assigned default value from config file.

    Arguments must by listed in dictionary form.

    :param config_filepath: yml file containing default values for all accepted arguments
    :param arg_filepath: yml file containing input arguments and their values
    :return: dictionary of argument (based on config) and their values (based on arg file and config)
    """
    with config_filepath.open('r') as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc) # add logger

    with arg_filepath.open('r') as stream:
        try:
            args = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc) # add logger

    for key in config.keys():
        if  key in args:
            config[key] = args[key]

    return config


def parse_yaml_args(config_filepath):
    """
    Parses input config into a dictionary. 

    :param config_filepath: YAML file path
    :return: dinctionary of arguments and values
    """
    with config_filepath.open('r') as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc) # add logger

    return config


def parse_json_args(config_filepath):
    """
    Parses input config into a dictionary. 

    :param config_filepath: json file path
    :return: dinctionary of arguments and values
    """
    with config_filepath.open('r') as stream:
        try:
            config = json.load(stream)
        except json.JSONDecodeError as exc:
            print(exc)
    return config


###############################################
################## Generic functions
###############################################


def donothing(*args):
    """
    Just like a student until week before deadline, it does nothing regardless of what you throw at it
    """
    pass

def find_or_make(_dict, key, _type=dict):
    """
    Finds entry in dictionary, or creates it and adds it to dictionary.

    :param _dict: dictionary
    :param key: key in dictionary
    :param _type: values type (will be used to construct new value)
    :return: Value for key
    """
    r = _dict.get(key)
    if r is None:
        r = _type()
        _dict[key] = r
    return r

def to_hex(i,l=4):
    a = hex(i).replace('0x', '')
    return '0'*(l-len(a))+a
