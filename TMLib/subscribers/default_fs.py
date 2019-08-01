from ..SubMng import PREPROCESSING, PROCESSING, POSTPROCESSING,\
    VALIDATION, CONFIG_CHECK, ENQUEUE, PROTOCOL, FUNCTION, DICTIONARY,\
    ALT, KEY, FILL, RECALCULATION, subscribe_protocol_transformation,\
    subscribe_timestamp_postprocess, subscribe_timestamp_process,\
    subscribe_timestamp_alt, subscribe_timestamp_mode

import scapy.layers.inet as inet
import scapy.layers.inet6 as inet6
import scapy.layers.dns as dns
import scapy.layers.l2 as l2
import scapy.utils

import scapy_extend.http as http

from ..transf import PacketProcessing as TMpp
from ..transf import TimestampGeneration as TMtg
from ..transf import RecalTMdict as TMrc
from ..utils import tmdict_fillers as Filler


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
"""
subsribed_functions = { # dictionary of known transformation functions

#################
#### Ether
#################
'mac_src_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.Ether
        , FUNCTION : TMpp.mac_src_change
        }
    ]
    , FILL : [
        Filler.make_mac_map
    ]
}

, 'mac_dst_change' : {
    PROCESSING : [ 
        {
        PROTOCOL : inet.Ether
        , FUNCTION : TMpp.mac_dst_change
        }
    ]
    , FILL : [
        Filler.make_mac_map
    ]
}

, 'mac_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.Ether
        , FUNCTION : TMpp.mac_change_default
        }
    ]
    , FILL : [
        Filler.make_mac_map
    ]
}

#################
#### ARP
#################

, 'arp_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : l2.ARP
        , FUNCTION : TMpp.arp_change_default
        }
    ]
    , FILL : [
        Filler.make_mac_map
        , Filler.make_ip_map
    ]
}

#################
#### IPv4
#################
, 'ip_src_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_src_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

, 'ip_dst_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_dst_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

, 'ip_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_change_default
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,  Filler.make_ttl_ip_exceptions
    ]
    , RECALCULATION : [
        TMrc.recalculate_ttl
    ]
}

, 'ip_ttl_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_ttl_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,  Filler.make_ttl_ip_exceptions
    ]
    , RECALCULATION : [
        TMrc.recalculate_ttl
    ]
}

, 'ip_auto_checksum' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_auto_checksum
        }
    ]
}

#################
#### IPv6
#################
, 'ipv6_src_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.ipv6_src_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

, 'ipv6_dst_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.ipv6_dst_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

, 'ipv6_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.ipv6_change_default
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,  Filler.make_ttl_ip_exceptions
    ]
    , RECALCULATION : [
        TMrc.recalculate_ttl
    ]
}

, 'ipv6_hlim_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.ipv6_hlim_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,  Filler.make_ttl_ip_exceptions
    ]
    , RECALCULATION : [
        TMrc.recalculate_ttl
    ]
}

#################
#### ICMPv4
#################
, 'icmp_ip_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IPerror
        , FUNCTION : TMpp.ip_change_default
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,  Filler.make_ttl_ip_exceptions
    ]
    , RECALCULATION : [
        TMrc.recalculate_ttl
    ]
}

, 'icmp_tcp_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCPerror
        , FUNCTION : TMpp.tcp_change_default
        }
    ]
    , PREPROCESSING : [
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
    , RECALCULATION : [
        TMrc.recalculate_mss
        , TMrc.recalculate_win_size
    ]
}

, 'icmp_udp_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.UDPerror
        , FUNCTION : TMpp.udp_change_default
        }
    ]
    , PREPROCESSING : [
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

#################
#### TCP
#################
, 'tcp_win_size_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.tcp_win_size_change
        }
    ]
    , PREPROCESSING : [ 
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
        , Filler.make_win_ip_exceptions
        , Filler.make_port_ip_map
    ]
    , RECALCULATION : [
        TMrc.recalculate_win_size
    ]
}
, 'tcp_mss_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.tcp_mss_change
        }
    ]
    , PREPROCESSING : [ 
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
        , Filler.make_mss_ip_exceptions
        , Filler.make_port_ip_map
    ]
    , RECALCULATION : [
        TMrc.recalculate_win_size
    ]
}
, 'tcp_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.tcp_change_default
        }
    ]
    , PREPROCESSING : [ 
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
        , Filler.make_mss_ip_exceptions
        , Filler.make_win_ip_exceptions
        , Filler.make_port_ip_map
    ]
    , RECALCULATION : [
        TMrc.recalculate_mss
        , TMrc.recalculate_win_size
    ]
}

, 'tcp_auto_checksum' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.tcp_auto_checksum
        }
    ]
}

#################
#### UDP
#################
, 'udp_change_default' : {
    PROCESSING : [
        {
        PROTOCOL : inet.UDP
        , FUNCTION : TMpp.udp_change_default
        }
    ]
    , PREPROCESSING : [
        { 
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.get_new_ips
        }
        , {
        PROTOCOL : inet6.IPv6
        , FUNCTION : TMpp.get_new_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
        , Filler.make_port_ip_map
    ]
}

, 'udp_auto_checksum' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.udp_auto_checksum
        }
    ]
}

#################
#### DNS
#################
, 'dns_change_ips' : {
    PROCESSING : [
        {
        PROTOCOL : dns.DNS
        , FUNCTION : TMpp.dns_change_ips
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

#################
#### HTTPv1
#################
, 'httpv1_regex_ip_swap' : {
    PROCESSING : [
        {
        PROTOCOL : http.HTTPv1 
        , FUNCTION : TMpp.httpv1_regex_ip_swap
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}
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
"""
timestamp_function_dict = { # dictionary of known timestamp generation functions
'default' : {
    FUNCTION : TMtg.timestamp_dynamic_shift
}
, 'timestamp_shift' : {
    FUNCTION : TMtg.timestamp_static_shift
}
, 'tcp_avg_shift' : {
    FUNCTION : TMtg.timestamp_tcp_avg_shift
    , ALT : TMtg.timestamp_dynamic_shift
    , FILL : [
        Filler.make_attack_tcp_avg_delay_map
        , Filler.make_target_tcp_avg_delay_map
    ]
}
, 'timestamp_dynamic_shift' : {
    FUNCTION : TMtg.timestamp_dynamic_shift
}
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
"""
timestamp_postprocess_dict = {
'timestamp_delay' : {
    FUNCTION : TMtg.timestamp_delay
}
, 'timestamp_delay_forIPlist' : {
    FUNCTION : TMtg.timestamp_delay_forIPlist
}
, 'timestamp_delay_forIPconst' : {
    FUNCTION : TMtg.timestamp_delay_forIPconst
}
, 'timestamp_random_oscillation' : {
    FUNCTION : TMtg.timestamp_random_oscillation
}
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
    FILL - list of functions that statistics, TMdicts and parsed config as dict on input and fill them with data
"""
timestamp_alt_function_dict = { # dictionary of known timestamp generation functions
'default' : {
    FUNCTION : TMtg.timestamp_dynamic_shift
}
, 'timestamp_shift' :{
    FUNCTION :  TMtg.timestamp_static_shift
}
, 'timestamp_dynamic_shift' : {
    FUNCTION : TMtg.timestamp_dynamic_shift
}
}

subscribe_protocol_transformation(subsribed_functions)
subscribe_timestamp_postprocess(timestamp_postprocess_dict)
subscribe_timestamp_process(timestamp_function_dict)
subscribe_timestamp_alt(timestamp_alt_function_dict)
