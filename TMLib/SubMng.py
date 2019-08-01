from . import Definitions as TMdef

PROCESSING = 'processing'
PREPROCESSING = 'preprocessing'
POSTPROCESSING = 'postprocessing'
VALIDATION = 'validation'
CONFIG_CHECK = 'configcheck'
ENQUEUE = 'enqueue'
PROTOCOL = 'protocol'
FUNCTION = 'function'
DICTIONARY = 'dictionary'
ALT = 'alt'
KEY = 'key'
FILL = 'load'
RECALCULATION = 'recalculation'


"""
Single entry in subsribed_functions represents single tranformation.
Multiple processing, preprocessing & validation functions may be referenced
in single entry (including other entries).

An entry in subsribed_functions must have:
key - unique string name
value - these possible keys
    PROCESSING - contains list of dicionaries with keys PROTOCOL and FUNCTION
                representing protocol and function for rewrapper processing function
    PREPROCESSING - contains list of dictionaries with keys PROTOCOL and FUNCTION
                representing protocol and function for rewrapper preprocessing function
    VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                representing TMdict dictionaries validation function and name of the dictionary
                in rewrapper
    ENQUEUE - contains list of entries from subsribed_functions
    FILL - list of functions that takes statistics, TMdicts and parsed config as dict on input and fill them with data
    RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
"""
subsribed_functions = { # dictionary of known transformation functions
}


"""
Single entry in timestamp_function_dict represents single timestamp generation function

An entry in timestamp_function_dict must have:
key - unique string name
value - these possible keys
    FUNCTION - contains timestamp generator function 
    ALT - contains backup/alternative timestamp generation function. 
        If value is string, timestamp_alt_function_dict will be searched.
    VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                representing TMdict dictionaries validation function and name of the dictionary
                in rewrapper
    FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
    RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
"""
timestamp_function_dict = { # dictionary of known timestamp generation functions
}


"""
Single entry in timestamp_postprocess_dict represents single timestamp postprocess function

An entry in timestamp_postprocess_dict must have:
key - unique string name
value - these possible keys
    FUNCTION - contains timestamp generator function
    VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                representing TMdict dictionaries validation function and name of the dictionary
                in rewrapper 
    FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
    RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
"""
timestamp_postprocess_dict = {
}


"""
Single entry in timestamp_alt_function_dict represents single timestamp backup/alt function

An entry in timestamp_alt_function_dict must have:
key - unique string name
value - these possible keys
    FUNCTION - contains timestamp generator function 
    VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                representing TMdict dictionaries validation function and name of the dictionary
                in rewrapper
    FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with 
    RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
"""
timestamp_alt_function_dict = { # dictionary of known timestamp generation functions
}

"""
Single entry in timestamp_generation_mode represents single timestamp tranformation

An entry in timestamp_generation_mode must have:
key - unique string name
value - these possible keys
    PROCESSING - constains single timestamp generation function
    ALT - contains backup/alternative timestamp generation function
    POSTPROCESSING - contains list of postprocessing functions
    VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                representing TMdict dictionaries validation function and name of the dictionary
                in rewrapper
    FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
    RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
If any of the values, except for key VALIDATION, is string, a coresponding dictionary will be searched.
"""
timestamp_generation_mode = {
}

def subscribe_protocol_transformation(entry):
    """
    Single entry in subsribed_functions represents single tranformation.
    Multiple processing, preprocessing & validation functions may be referenced
    in single entry (including other entries).

    An entry in subsribed_functions must have:
    key - unique string name
    value - these possible keys
        PROCESSING - contains list of dicionaries with keys PROTOCOL and FUNCTION
                    representing protocol and function for rewrapper processing function
        PREPROCESSING - contains list of dictionaries with keys PROTOCOL and FUNCTION
                    representing protocol and function for rewrapper preprocessing function
        VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                    representing TMdict dictionaries validation function and name of the dictionary
                    in rewrapper
        ENQUEUE - contains list of entries from subsribed_functions
        FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
        RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
    """
    subsribed_functions.update(entry)

def subscribe_timestamp_postprocess(entry):
    """
    Single entry in timestamp_postprocess_dict represents single timestamp postprocess function

    An entry in timestamp_postprocess_dict must have:
    key - unique string name
    value - these possible keys
        FUNCTION - contains timestamp generator function
        VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                    representing TMdict dictionaries validation function and name of the dictionary
                    in rewrapper 
        FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
        RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
    """
    timestamp_postprocess_dict.update(entry)

def subscribe_timestamp_process(entry):
    """
    Single entry in timestamp_function_dict represents single timestamp generation function

    An entry in timestamp_function_dict must have:
    key - unique string name
    value - these possible keys
        FUNCTION - contains timestamp generator function 
        ALT - contains backup/alternative timestamp generation function. 
            If value is string, timestamp_alt_function_dict will be searched.
        VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                    representing TMdict dictionaries validation function and name of the dictionary
                    in rewrapper
        FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with 
        RECALCULATION - list of functions recalculates GlobalRWdict data based on current values

    """
    timestamp_function_dict.update(entry)

def subscribe_timestamp_alt(entry):
    """
    Single entry in timestamp_alt_function_dict represents single timestamp backup/alt function

    An entry in timestamp_alt_function_dict must have:
    key - unique string name
    value - these possible keys
        FUNCTION - contains timestamp generator function 
        VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                    representing TMdict dictionaries validation function and name of the dictionary
                    in rewrapper
        FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
        RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
    """
    timestamp_alt_function_dict.update(entry)

def subscribe_timestamp_mode(entry):
    """
    Single entry in timestamp_generation_mode represents single timestamp tranformation

    An entry in timestamp_generation_mode must have:
    key - unique string name
    value - these possible keys
        PROCESSING - constains single timestamp generation function
        ALT - contains backup/alternative timestamp generation function
        POSTPROCESSING - contains list of postprocessing functions
        VALIDATION - contains list of dictionaries witn keys DICTIONARY and FUNCTION
                    representing TMdict dictionaries validation function and name of the dictionary
                    in rewrapper
        FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
        RECALCULATION - list of functions recalculates GlobalRWdict data based on current values
    If any of the values, except for key VALIDATION, is string, a coresponding dictionary will be searched.
    """
    timestamp_generation_mode.update(entry)


def enqueue_function(rewrapper, name):
    """
    Enqueue transformation (for specific protocol, based on function). 
    Searches for known functions based on name match.
    During rewrapping, functions are executed in enqueue order.

    :param rewrapper: ReWrapper object
    :param name: name of the tranformation, string

    :return: set of functions that fill dictionaries based on parsed config
    """
    fill = set()
    config_validation = set()

    record = subsribed_functions.get(name)
    if record:
        processing = record.get(PROCESSING)
        if processing:
            for entry in processing:
                rewrapper.enqueue_processing_function(entry[PROTOCOL], entry[FUNCTION])
        
        preprocessing = record.get(PREPROCESSING)
        if preprocessing:
            for entry in preprocessing:
                rewrapper.enqueue_preprocessing_function(entry[PROTOCOL], entry[FUNCTION])

        postprocessing = record.get(POSTPROCESSING)
        if postprocessing:
            for entry in postprocessing:
                rewrapper.enqueue_postprocessing_function(entry[PROTOCOL], entry[FUNCTION])

        validation = record.get(VALIDATION)
        if validation:
            data_dict = rewrapper.data_dict
            for entry in validation:
                tmdict = data_dict.get(entry[DICTIONARY])
                if tmdict:
                    tmdict.add_validation_function(entry[FUNCTION])

        enqueue = record.get(ENQUEUE)
        if enqueue:
            for entry in enqueue:
                res = enqueue_function(rewrapper, entry)
                if res:
                    fill.update(res[0])
                    config_validation.update(res[1])

        cfg_validators = record.get(CONFIG_CHECK)
        if cfg_validators:
            config_validation.update(cfg_validators)

        fillers = record.get(FILL)
        if fillers:
            fill.update(fillers)
        
        recals = record.get(RECALCULATION)
        if recals:
            global_dict = rewrapper.data_dict.get(TMdef.GLOBAL)
            for entry in recals:
                global_dict.add_recalculation_function(entry)

    return fill, config_validation


def change_timestamp_function(rewrapper, name):
    """
    If name is in timestamp_function_dict, sets the timestamp generator.
    Sets alt generator if it is defined. 

    Adds validation functions if they are defined. 

    :param rewrapper: ReWrapper object
    :param name: name of the function, string

    :return: set of functions that fill dictionaries based on parsed config
    """
    fill = set()
    config_validation = set()

    record = timestamp_function_dict.get(name)
    if record :
        rewrapper.set_timestamp_generator(record[FUNCTION])

        alt = record.get(ALT)
        if alt:
            if isinstance(alt, str):
                fill.update(enlist_alt_timestamp_generation_function(rewrapper, alt))
            else:
                rewrapper.set_backup_timestamp_generator(alt)

        validation = record.get(VALIDATION)
        if validation:
            data_dict = rewrapper.data_dict
            for entry in validation:
                tmdict = data_dict.get(entry[DICTIONARY])
                if tmdict:
                    tmdict.add_validation_function(entry[FUNCTION])

        cfg_validators = record.get(CONFIG_CHECK)
        if cfg_validators:
            config_validation.update(cfg_validators)

        fillers = record.get(FILL)
        if fillers:
            fill.update(fillers)
        
        recals = record.get(RECALCULATION)
        if recals:
            global_dict = rewrapper.data_dict.get(TMdef.GLOBAL)
            for entry in recals:
                global_dict.add_recalculation_function(entry)

    return fill, config_validation


def enqueue_timestamp_postprocess(rewrapper, name):
    """
    If name is in timestamp_postprocess_dict, enqueues the timestamp postprocessing function.

    Adds validation functions if they are defined. 

    :param rewrapper: ReWrapper object
    :param name: name of the function, string

    :return: set of functions that fill dictionaries based on parsed config
    """
    fill = set()
    config_validation = set()

    record = timestamp_postprocess_dict.get(name)
    if record :
        rewrapper.enqueue_timestamp_postprocess(record[FUNCTION])

        validation = record.get(VALIDATION)
        if validation:
            data_dict = rewrapper.data_dict
            for entry in validation:
                tmdict = data_dict.get(entry[DICTIONARY])
                if tmdict:
                    tmdict.add_validation_function(entry[FUNCTION])

        cfg_validators = record.get(CONFIG_CHECK)
        if cfg_validators:
            config_validation.update(cfg_validators)

        fillers = record.get(FILL)
        if fillers:
            fill.update(fillers)
        
        recals = record.get(RECALCULATION)
        if recals:
            global_dict = rewrapper.data_dict.get(TMdef.GLOBAL)
            for entry in recals:
                global_dict.add_recalculation_function(entry)


    return fill, config_validation


def enlist_alt_timestamp_generation_function(rewrapper, name):
    """
    If name is in timestamp_alt_function_dict, sets the alternative timestamp generator.

    Adds validation functions if they are defined. 

    :param rewrapper: ReWrapper object
    :param name: name of the function, string

    :return: set of functions that fill dictionaries based on parsed config
    """
    fill = set()
    config_validation = set()

    record = timestamp_alt_function_dict.get(name)
    if record :
        rewrapper.set_backup_timestamp_generator(record[FUNCTION])

        validation = record.get(VALIDATION)
        if validation:
            data_dict = rewrapper.data_dict
            for entry in validation:
                tmdict = data_dict.get(entry[DICTIONARY])
                if tmdict:
                    tmdict.add_validation_function(entry[FUNCTION])

        cfg_validators = record.get(CONFIG_CHECK)
        if cfg_validators:
            config_validation.update(cfg_validators)

        fillers = record.get(FILL)
        if fillers:
            fill.update(fillers)
        
        recals = record.get(RECALCULATION)
        if recals:
            global_dict = rewrapper.data_dict.get(TMdef.GLOBAL)
            for entry in recals:
                global_dict.add_recalculation_function(entry)

    return fill, config_validation


def apply_timestamp_generation_mode(rewrapper, name):
    """
    If name is in timestamp_generation_mode, sets all timestamp generation, alterantive and postprocess functions.
    Multiple calls of this function on same object will cause some of the entries to be overwritten, while
    others may enqueued. 

    Adds validation functions if they are defined. 

    :param rewrapper: ReWrapper object
    :param name: name of the mode, string

    :return: set of functions that fill dictionaries based on parsed config
    """
    fill = set()
    config_validation = set()

    record = timestamp_generation_mode.get(name)
    if record :
        process = record[FUNCTION]
        if isinstance(process, str):
            fill.update(change_timestamp_function(rewrapper, process))
        else:
            rewrapper.set_timestamp_generator(process)

        alt = record.get(ALT)
        if alt:
            if isinstance(alt, str):
                fill.update(enlist_alt_timestamp_generation_function(rewrapper, alt))
            else:
                rewrapper.set_backup_timestamp_generator(alt)

        postprocess = record.get(FUNCTION)
        for entry in postprocess:
            if isinstance(entry, str):
                fill.update(enqueue_timestamp_postprocess(rewrapper, entry))
            else:
                rewrapper.enqueue_timestamp_postprocess(entry)

        validation = record.get(VALIDATION)
        if validation:
            data_dict = rewrapper.data_dict
            for entry in validation:
                tmdict = data_dict.get(entry[DICTIONARY])
                if tmdict:
                    tmdict.add_validation_function(entry[FUNCTION])

        fillers = record.get(FILL)
        if fillers:
            fill.update(fillers)
        
        recals = record.get(RECALCULATION)
        if recals:
            global_dict = rewrapper.data_dict.get(TMdef.GLOBAL)
            for entry in recals:
                global_dict.add_recalculation_function(entry)

        cfg_validators = record.get(CONFIG_CHECK)
        if cfg_validators:
            config_validation.update(cfg_validators)
    return fill, config_validation

#################
#### LOADER
#################

# def load_all():
#     """
#     Imports & executes subscribers. Never to be used during initialization of the manager. 
#     """
#     from subscribers import *

