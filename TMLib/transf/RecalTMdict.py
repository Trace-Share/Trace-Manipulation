import lea

import ID2TLib.Utility as Util

from .. import Definitions as TMdef

def recalculate_ttl(global_rwdict):
    """
    Recalculates time to live for ip packets based on IP addresses (new) from ip adress map.
    IP address in statistics recieve ttl value based on distribution of ttl values for that address.
    IP addresses not in statistics recieve most used ttl value.
    """
    global_rwdict[TMdef.TARGET]['ip_ttl_default'] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_ttl_value())
    ip_dict = global_rwdict[TMdef.TARGET]['ip_address_map']
    ttl_dict = global_rwdict[TMdef.TARGET]['ip_ttl_map']
    for ip_old, ip_new in ip_dict.items():
        if ip_old not in global_rwdict[TMdef.TARGET]['ttl_exceptions']:
            ttl_dist = global_rwdict.statistics.get_ttl_distribution(ip_new)
            if len(ttl_dist) > 0:
                ttl_prob_dict = lea.Lea.fromValFreqsDict(ttl_dist)
                ttl_dict[ip_old] = ttl_prob_dict.random()
            else:
                ttl_dict[ip_old] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_ttl_value())


def recalculate_win_size(global_rwdict):
    """
    Recalculates windows size for ip packets based on IP addresses (new) from ip adress map.
    IP address in statistics recieve win size value based on distribution of win size values for that address.
    IP addresses not in statistics recieve most used win size value.
    """
    global_rwdict[TMdef.TARGET]['win_size_default'] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_win_size())
    ip_dict = global_rwdict[TMdef.TARGET]['ip_address_map']
    win_dict = global_rwdict[TMdef.TARGET]['win_size_map']
    for ip_old, ip_new in ip_dict.items():
        if ip_old not in global_rwdict[TMdef.TARGET]['ttl_exceptions']:
            win_dist = global_rwdict.statistics.get_win_distribution(ip_new)
            if len(win_dist) > 0:
                win_prob_dict = lea.Lea.fromValFreqsDict(win_dist)
                win_dict[ip_old] = win_prob_dict.random()
            else:
                win_dict[ip_old] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_win_size())

def recalculate_mss(global_rwdict):
    """
    Recalculates maximum segment size for ip packets based on IP addresses (new) from ip adress map.
    IP address in statistics recieve mss value based on distribution of mss values for that address.
    IP addresses not in statistics recieve most used mss value.
    """
    global_rwdict[TMdef.TARGET]['mss_default'] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_mss_value())    
    ip_dict = global_rwdict[TMdef.TARGET]['ip_address_map']
    mss_dict = global_rwdict[TMdef.TARGET]['mss_map']
    for ip_old, ip_new in ip_dict.items():
        if ip_old not in global_rwdict[TMdef.TARGET]['ttl_exceptions']:
            mss_dist = global_rwdict.statistics.get_mss_distribution(ip_new)
            if len(mss_dist) > 0:
                mss_prob_dict = lea.Lea.fromValFreqsDict(mss_dist)
                mss_dict[ip_old] = mss_prob_dict.random()
            else:
                mss_dict[ip_old] = Util.handle_most_used_outputs(global_rwdict.statistics.get_most_used_mss_value())
