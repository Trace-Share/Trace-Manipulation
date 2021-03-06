import numbers

from .. import Definitions as TMdef 
from ..utils.utils import find_or_make

def make_tcp_timestamp_shift_map(data, config):
    """
    [
        {
            'ip': '0.0.0.0',
            'shift' : 0.01
        }
    ]
    """
    atk = data[TMdef.GLOBAL][TMdef.ATTACK]
    shift = find_or_make(atk, "tcp.timestamp.shift")

    for entry in config['tcp.timestamp.shift']:
        shift[entry['ip']] = entry['shift']
    
    atk["tcp.timestamp.shift.default"] = config["tcp.timestamp.shift.default"]


def make_attack_tcp_avg_delay_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics
    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    data = data.get(TMdef.GLOBAL)
    if data:
        make_tcp_avg_delay_map(data.attack_statistics, data, TMdef.ATTACK)
    

def make_target_tcp_avg_delay_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics
    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    data = data.get(TMdef.GLOBAL)
    if data:
        make_tcp_avg_delay_map(data.statistics, data, TMdef.TARGET)


def make_tcp_delay_map_forLabel(label, statistics, data, source):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics

    :param data: TMLib.TMdict.GlobalRWdict dictionary

    :param source: TMdef.ATTACK or TMdef.Target
    """
    LABELS = {
        'avg' : 'tcp_avg_delay_map'
        , 'min' : 'tcp_min_delay_map'
        , 'max' : 'tcp_max_delay_map'
    }

    field = LABELS.get(label)
    if not field:
        return

    conversations = statistics.process_db_query('SELECT ipAddressA, ipAddressB, avgDelay FROM conv_statistics')

    delay_dict = data[source].get(field)
    if not delay_dict:
        delay_dict = {}
        data[TMdef.GLOBAL][source][field] = delay_dict

    for conversation in conversations:
        ip_dict = delay_dict.get(conversation[0])
        if not ip_dict:
            ip_dict = {}
            delay_dict[conversation[0]] = ip_dict
        ip_dict[conversation[1]] = conversation[2]
        
        ip_dict = delay_dict.get(conversation[1])
        if not ip_dict:
            ip_dict = {}
            delay_dict[conversation[1]] = ip_dict
        ip_dict[conversation[0]] = conversation[2]


def make_tcp_avg_delay_map(*args, **kwargs):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics
    :param data: TMLib.TMdict.GlobalRWdict dictionary
    :param source: TMdef.ATTACK or TMdef.Target
    """
    make_tcp_delay_map_forLabel('avg', *args, **kwargs)


def make_tcp_min_delay_map(*args, **kwargs):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics
    :param data: TMLib.TMdict.GlobalRWdict dictionary
    :param source: TMdef.ATTACK or TMdef.Target
    """
    make_tcp_delay_map_forLabel('min', *args, **kwargs)


def make_tcp_max_delay_map(*args, **kwargs):
    """
    Fills TMdef.GLOBAL dictionary map of tcp handshake average delays (tcp_avg_delay_map)
    based on provided statistics for each existing conversation in statistics.

    :param statistics: Core.Statistics.Statistics object containing pcap statistics
    :param data: TMLib.TMdict.GlobalRWdict dictionary
    :param source: TMdef.ATTACK or TMdef.Target
    """
    make_tcp_delay_map_forLabel('max', *args, **kwargs)


def make_mac_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of mac adresses using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if global_dict and isinstance(global_dict, dict):
        mac_map = config.get('mac.map')
        if mac_map and isinstance(mac_map, list):
            for entry in mac_map:
                entry = entry.get('mac')
                if entry and isinstance(entry, dict):
                    old = entry.get('old')
                    new = entry.get('new')
                    if old and new and isinstance(old, str) and isinstance(new, str):
                        global_dict.to_mac_map(old, new)


def make_ip_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of ip adresses using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if global_dict and isinstance(global_dict, dict):
        ip_map = config.get('ip.map')
        if ip_map and isinstance(ip_map, list):
            for entry in ip_map:
                entry = entry.get('ip')
                if entry and isinstance(entry, dict):
                    old = entry.get('old')
                    new = entry.get('new')
                    if old and new and isinstance(old, str) and isinstance(new, str):
                        global_dict.to_ip_map(old, new)


def make_port_ip_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of old to new ports based on ip adress using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    port_ip_map = config.get('port.ip.map')
    if not port_ip_map or not isinstance(port_ip_map, list):
        return
    for entry in port_ip_map:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type or ip_type != 'old':
            continue
        ip_address = ip.get('address')
        if not ip_address or not isinstance(ip, str):
            continue
        port = entry.get('port')
        if not port or not isinstance(port, dict):
            continue
        old = port.get('old')
        new = port.get('new')
        if old and new and isinstance(old, str) and isinstance(new, str):
            global_dict.port_map_forIP(ip_address, old, new)


def make_mss_ip_exceptions(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of maximum segment size based on ip using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    mss_ip_exceptions = config.get('mss.ip.exceptions')
    if not mss_ip_exceptions or isinstance(mss_ip_exceptions, list):
        return
    for entry in mss_ip_exceptions:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type or ip_type != 'old':
            continue
        ip_address = ip.get('address')
        if ip_address and isinstance(ip_address, str):
            global_dict.to_mss_exceptions(ip_address)


def make_win_ip_exceptions(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of win size exceptions based on ip using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    win_ip_exceptions = config.get('win.ip.exceptions')
    if not win_ip_exceptions or not isinstance(win_ip_exceptions, list):
        return
    for entry in win_ip_exceptions:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type or ip_type != 'old':
            continue
        ip_address = ip.get('address')
        if ip_address and isinstance(ip_address, str):
            global_dict.to_win_size_exceptions(ip_address)


def make_ttl_ip_exceptions(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of time to live expetions based on ip using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    ttl_exceptions = config.get('win.ip.exceptions')
    if not ttl_exceptions or not isinstance(ttl_exceptions, list):
        return
    for entry in ttl_exceptions:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type or ip_type != 'old':
            continue
        ip_address = ip.get('address')
        if ip_address and isinstance(ip_address, str):
            global_dict.to_ttl_exceptions(ip_address)


def make_userdef_tcp_delay(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of user defined tcp delays for ip adress communication using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    tcp_delay = config.get('tcp.delay')
    if not tcp_delay or not isinstance(tcp_delay, list):
        return
    for entry in tcp_delay:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type:
            continue
        ip_source = ip.get('source.address')
        ip_dest = ip.get('destination.address')
        if not ip_source or not ip_dest or isinstance(ip_source, str) or isinstance(ip_dest, str):
            continue
        delay = entry.get('delay')
        if not delay or not isinstance(delay, numbers.Real):
            continue
        if ip_type == 'new':
            global_dict.add_tcp_avg_delay_record(TMdef.TARGET, ip_source,
                 ip_dest, delay)
        if ip_type == 'old':
            global_dict.add_tcp_avg_delay_record(TMdef.ATTACK, ip_source,
                 ip_dest, delay)


def make_timestamp_random_treshold_map(data, config):
    """
    Fills TMdef.GLOBAL dictionary map of random tresholds based on ip using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    timestamp_random_tresholds = config.get('timestamp.random.thresholds')
    if not timestamp_random_tresholds or not isinstance(timestamp_random_tresholds, list):
        return
    for entry in timestamp_random_tresholds:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type:
            continue
        ip_address = ip.get('address')
        if not ip_address or isinstance(ip_address, str):
            continue
        threshold = entry.get('threshold')
        if not threshold or not isinstance(threshold, numbers.Real):
            continue
        if ip_type == 'old':
            global_dict.to_timestamp_random_delay_threshold_map(ip_address, threshold)


def make_timestamp_random_treshold_set(data, config):
    """
    Fills TMdef.GLOBAL dictionary set of mac ip adresses for random treshold using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    timestamp_random_tresholds = config.get('timestamp.random.set')
    if not timestamp_random_tresholds or not isinstance(timestamp_random_tresholds, list):
        return
    for entry in timestamp_random_tresholds:
        ip = entry.get('ip')
        if not ip or not isinstance(ip, dict):
            continue
        ip_type = ip.get('type')
        if not ip_type:
            continue
        ip_address = ip.get('address')
        if not ip_address or isinstance(ip_address, str):
            continue
        if ip_type == 'old':
            global_dict.to_timestamp_random_delay_set(ip_address)



def make_random_treshold(data, config):
    """
    Fills TMdef.GLOBAL dictionary random treshold using config.

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    dict_ref = config.get('timestamp')
    if dict_ref:
        ## required by random delay/oscilation functions
        threshold = dict_ref.get('random.threshold')
        if threshold:
            data['timestamp_threshold'] = threshold

def init_tcp_window_map(data, config):
    """

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    atk_dict = global_dict[TMdef.ATTACK]
    tcp_defaults = find_or_make(atk_dict, 'tcp.defaults')
    
    if tcp_defaults.get('tcp.window.shift') is None:
        tcp_defaults['tcp.window.shift'] = 0
    if tcp_defaults.get('tcp.window.irw') is None:
        tcp_defaults['tcp.window.irw'] = {
            'default' : 8192 # win ? TODO add more
        }

def make_tcp_window_map(data, config):
    """

    :param data: dict containing TMLib.TMdict dictionaries
    :param config: config file parsed as dict
    """
    global_dict = data.get(TMdef.GLOBAL)
    if not global_dict or not isinstance(global_dict, dict):
        return
    atk_dict = global_dict[TMdef.ATTACK]
    tcp_conversation = find_or_make(atk_dict, 'tcp.conversation')
    tcp_defaults_ip_map = find_or_make(atk_dict, 'tcp.defaults.ip_map')
    tcp_defaults = find_or_make(atk_dict, 'tcp.defaults')

    config_tcp_window = config.get('tcp.window.config')
    if config_tcp_window is None:
        return

    """
    {
        tcp.window.config : {
            defaults : {
                tcp.window.shift : + 100
                , tcp.window.irw : [
                    {
                        irw.from : default
                        , irw.to : 10000
                    }
                ]
            }
            , conversation : [
                {
                    ip.source : 0.0.0.0
                    , ip.destination : 0.0.0.0
                    , ports : [
                        {
                            port.source : 0
                            , port.destination : 0
                            , counter.handshake.first_two : []
                            , tcp.window.shift : 0
                            , tcp.window.irw : {
                                default : 0
                                , map : [
                                    from : 0
                                    , to : 0
                                ]
                            }
                        }
                    ]
                }
            ]
            , defaults.ip_map : [
                {
                    ip.src : 0.0.0.0
                    , counter.handshake_first_two : []
                    , tcp.window.shift : 0
                    , tcp.window.irw : {
                        'default' : 0
                    }
                }
            ]
        }
    }
    """
    config_defaults = config_tcp_window.get('defaults')
    if config_defaults is not None:
        defaults_shift = config_defaults.get('tcp.window.shift')
        if defaults_shift is not None:
            tcp_defaults['tcp.window.shift'] = defaults_shift
        defaults_irw = config_defaults.get('tcp.window.irw')
        if defaults_irw is not None:
            defaults_irw_map = {}
            for mapping in defaults_irw:
                defaults_irw_map[mapping['irw.from']] = mapping['irw.to']
            tcp_defaults['tcp.window.irw'].update(defaults_irw_map)
        defaults_irw_del = config_defaults.get('tcp.window.irw.del')
        if defaults_irw_del is not None:
            _tcp_defaults_irw = tcp_defaults['tcp.window.irw']
            for key in defaults_irw_del:
                try:
                    del _tcp_defaults_irw[key]
                except KeyError:
                    continue
    
    config_defaults_ip_map = config_tcp_window.get('defaults.ip_map')
    if config_defaults_ip_map is not None:
        for entry in config_defaults_ip_map:
            mapping =  {}
            tcp_defaults_ip_map[entry['ip.src']] = mapping
            entry_shift = entry.get('tcp.window.shift')
            if entry_shift is not None:
                mapping['tcp.window.shift'] = entry_shift
            entry_handshake = entry.get('counter.handshake_first_two')
            if entry_handshake is not None:
                mapping['counter.handshake.first_two'] = entry_handshake
            entry_irw_map = entry.get('tcp.window.irw')
            if entry_irw_map is None:
                continue
            irw_mapping = {}
            mapping['tcp.window.irw'] = irw_mapping
            entry_default = entry_irw_map.get('default')
            if entry_default is not None:
                irw_mapping['default'] = entry_default
            entry_irw_map = entry_irw_map.get('map')
            if entry_irw_map is None:
                continue
            for e in entry_irw_map:
                irw_mapping[e['from']] = e['to']
    
    config_conversations = config_tcp_window.get('conversation')
    if config_conversations is None:
        return

    
    for entry in config_conversations:
        ip_src = entry['ip.source']
        ip_dst = entry['ip.destination']
        _map = find_or_make(tcp_conversation, ip_src)
        _map = find_or_make(_map, ip_dst)
        for port in entry.get('port'):
            port_src = port['port.source']
            port_dst = port['port.destination']
            _map = find_or_make(_map, port_src)
            _map = find_or_make(_map, port_dst)
            counter_handshake = port.get('counter.handshake.first_two')
            if counter_handshake is not None:
                _map['counter.handshake.first_two'] = counter_handshake
            window_shift = port.get('tcp.window.shift')
            if window_shift is not None:
                _map['tcp.window.shift'] = window_shift
            window_irw = port.get('tcp.window.irw')
            if window_irw is None:
                continue
            _irw = {}
            _map['tcp.window.irw'] = _irw
            default = window_irw.get('default')
            if default is not None:
                _irw['default'] = default
            window_irw = window_irw.get('map')
            if window_irw is None:
                continue
            for entry in window_irw:
                _irw[entry['from']] = entry['to']
    

"""
TODO improve validation and filling (?)

{
    "name" : ""
    , "type" : ""
    , "data" : ""
    , "validation" : ""
    , "loader" : ""
    # -> .parent -> obj
    # -> .children -> (list, dict , val, None)
    # -> .type -> ("dict", "list", "key", "val")
    # -> .name -> (None, None, "key", "val")
    # -> .validation -> callable
    # -> .loader -> callable
}

->

{
    "key" : "val"
}

{
    "key" : [
        "val"
    ]
}

{
    "key" : [
        {
            "key" : "val"
        }
    ]
}
"""
    
