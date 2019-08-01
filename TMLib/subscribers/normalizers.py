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
from ..utils import tmdict_fillers as Filler
from .. import Definitions as TMdef

def timestamp_static_shift(packet, data, prev_timestamp_old, prev_timestamp_new, curr_timestamp_old, curr_timestamp_new):
    """
    Shift current packet timestamp by specified value. Ignored timestamp changes by postprocessing.
    Data must be a dictionary with field 'timestamp_shift' containing signed float
    Data[TMdef.GLOBAL][TMdef.ATTACK] must contain key timestamp_shift.

    :param packet: Ether scapy packet
    :param data: dict containing TMLib.TMdict dictionaries
    :param prev_timestamp_old: old (unchanged) timestamp of previous packet, float
    :param prev_timestamp_new: new (generated) timestamp of previous packet, float
    :param curr_timestamp_old: old (unchanged) timestamp of current packet, float
    :param curr_timestamp_new: new timestamp value to be changed
    :return: new timestamp of the packet, float 
    """
    return curr_timestamp_old + data[TMdef.GLOBAL][TMdef.ATTACK]['timestamp_shift']
def to_hex(i):
    a = hex(i).replace('0x', '')
    if len(a) == 1:
        a = '0'+a
    return a

class MacSpace(object):
    def __init__(self, _from, _to, preserve_prefix=True):
        self.prefix=preserve_prefix
        self.to = _to
        self._from = _from

        if self.prefix:
            self.rng = [_from, 0 ,0]
        else:
            self.rng = [_from, 0, 0, 0, 0, 0]

    def get_next(self, addr):
        if self.prefix:
            r = [int(i,16) for i in addr.split(':')[0:3]] + self.rng
        else:
            r = self.rng
        r = ':'.join([to_hex(i).replace('0x', '') for i in r])
        c = 1
        adr_len = 6
        if self.prefix:
            adr_len = 3
        for i in range(adr_len-1, 0,-1):
            self.rng[i], c = _carry(self.rng[i], c, 256)
        if self.rng[0] > self.to or self._from > self.rng[0]:
            raise ValueError('MAC range exceeded')
        return r 

def _carry(a, b, m):
    a += b
    return a%m, a==m

_blocks = [(255*i)//3 for i in range(1, 4, 1) ]
macs = {
    'source' : MacSpace(0, _blocks[0])
    , 'intermediate' : MacSpace(_blocks[0], _blocks[1])
    , 'destination' : MacSpace(_blocks[1], _blocks[2])
}

def is_ignored(addr):
    return addr.lower() == 'ff'+5*':ff'

def mac_dict_atruntime_withprefix(fields):
    def f(packet, data):
        for field in fields:
            v = packet.getfieldval(field)
            mac_new = TMpp.globalRWdict_findMatch(data, 'mac_address_map', v)
            if mac_new is None and not is_ignored(v):
                rm = data[TMdef.PACKET].get('mac_remmap')
                if rm is None:
                    rm = {}
                    data[TMdef.PACKET]['mac_remmap'] = rm
                rm[field] = v
    return f

def ipv4_mac_remmap(field_map):
    """
    map of getter lambdas
    {
        field : lambda d: d.get('')
    }
    """
    def f(packet, data):
        TMpp.get_new_ips(packet, data)
        mac_remmap = data[TMdef.PACKET].get('mac_remmap')
        ip_remmap = data[TMdef.GLOBAL].get('ip_norm_map')
        if mac_remmap is not None and ip_remmap is not None:
            for key, val in mac_remmap.items():
                ref = field_map.get(key)
                if ref is not None:
                    tp = ref(data)
                    tp = ip_remmap.get(tp)
                    if tp is not None:
                        new_mac = macs[tp].get_next(val)
                        data[TMdef.GLOBAL].to_mac_map(val, new_mac)
                    else:
                        data[TMdef.GLOBAL].to_mac_map(val, macs['intermediate'].get_next(val)) 
            data[TMdef.PACKET]['mac_remmap'] = {}
    return f

def ip_norm_map_cpy(data, cfg):
    r = cfg.get('ip.norm')
    if r is not None:
        data[TMdef.GLOBAL]['ip_norm_map'] = r

def arp_norm():
    fields = [
        ('hwsrc', 'psrc')
        , ('hwdst', 'pdst')
    ]
    def f(packet, data):
        ip_remmap = data[TMdef.GLOBAL].get('ip_norm_map')
        mac_map = data[TMdef.GLOBAL][TMdef.TARGET]['mac_address_map']
        if ip_remmap is None:
            return
        for hw, p in fields:
            old_mac = packet.getfieldval(hw)
            if old_mac is not None and mac_map.get(old_mac) is None:
                ip = packet.getfieldval(p)
                tp = ip_remmap.get(ip)
                if tp is not None:
                    mac_map[old_mac] = macs[tp].get_next(old_mac)
                else:
                    data[TMdef.GLOBAL].to_mac_map(old_mac, macs['intermediate'].get_next(old_mac))
    return f

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

'mac_change_default' : {
    PREPROCESSING : [
        {
        PROTOCOL : inet.Ether
        , FUNCTION : mac_dict_atruntime_withprefix(['src', 'dst'])
        }
    ]
    , PROCESSING : [
        {
        PROTOCOL : inet.Ether
        , FUNCTION : TMpp.mac_change_default
        }
    ]
    , FILL : [
        Filler.make_mac_map
        , lambda _data, _config : _data[TMdef.GLOBAL].update({'mac_remmap' : {}} )
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
    PREPROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : ipv4_mac_remmap({
            'src' : lambda x : x[TMdef.PACKET].get('ip_src_old')
            , 'dst' : lambda x : x[TMdef.PACKET].get('ip_dst_old')
        })
        }
    ]
    , PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_src_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
        ,ip_norm_map_cpy
    ]
}

, 'ip_dst_change' : {
    PREPROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : ipv4_mac_remmap({
            'src' : lambda x : x[TMdef.PACKET].get('ip_src_old')
            , 'dst' : lambda x : x[TMdef.PACKET].get('ip_dst_old')
        })
        }
    ]
    , PROCESSING : [
        {
        PROTOCOL : inet.IP
        , FUNCTION : TMpp.ip_dst_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
        , ip_norm_map_cpy
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


#################
#### ICMPv4
#################
, 'icmp_ip_src_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IPerror
        , FUNCTION : TMpp.ip_src_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

, 'icmp_ip_dst_change' : {
    PROCESSING : [
        {
        PROTOCOL : inet.IPerror
        , FUNCTION : TMpp.ip_dst_change
        }
    ]
    , FILL : [
        Filler.make_ip_map
    ]
}

#################
#### TCP
#################

, 'tcp_auto_checksum' : {
    PROCESSING : [
        {
        PROTOCOL : inet.TCP
        , FUNCTION : TMpp.tcp_auto_checksum
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
'timestamp_shift' : {
    FUNCTION : timestamp_static_shift
}
}

subscribe_protocol_transformation(subsribed_functions)
subscribe_timestamp_process(timestamp_function_dict)
