import unittest
import scapy.layers.inet as inet
import scapy.layers.l2 as l2
import scapy.layers.dns as dns

import TMLib.utils.TMUnitTest as lib

import TMLib.transf.PacketProcessing as pp

import TMLib.Definitions as TMdef


class TMPacketProcessing(unittest.TestCase):

#########################################
############## Ether
#########################################

    def test_mac_src_addressNotExist(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = inet.Ether(src=src_ref, dst=dst_ref)
        mac_pkt = inet.Ether(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.mac_src_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def test_mac_dst_addressNotExist(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = inet.Ether(src=src_ref, dst=dst_ref)
        mac_pkt = inet.Ether(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.mac_dst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )

    def test_mac_src_addressExists(self):
        src_ref = 'F6:DA:77:F3:E2:E0'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = inet.Ether(src='8C:37:E1:F2:C8:E5', dst=dst_ref)
        mac_pkt = inet.Ether(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.mac_src_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )

    def test_mac_dst_addressExists(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'F6:DA:77:F3:E2:E0'
        
        ref_pkt = inet.Ether(src=src_ref, dst='8C:37:E1:F2:C8:E5')
        mac_pkt = inet.Ether(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()    

        pp.mac_dst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )

###########################################
############### ARP
###########################################

    def hwsrc_adrNotExist(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)
        mac_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_hwsrc_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def hwdst_adrNotExist(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)
        mac_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_hwdst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )

    def hwsrc_adrExists(self):
        src_ref = 'F6:DA:77:F3:E2:E0'
        dst_ref = 'FB:23:C0:22:0F:85'
        
        ref_pkt = l2.ARP(hwsrc='8C:37:E1:F2:C8:E5', hwdst=dst_ref)
        mac_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_hwsrc_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def hwdst_adrExists(self):
        src_ref = 'FB:1E:DC:3A:69:00'
        dst_ref = 'F6:DA:77:F3:E2:E0'
        
        ref_pkt = l2.ARP(hwsrc=src_ref, hwdst='8C:37:E1:F2:C8:E5')
        mac_pkt = l2.ARP(hwsrc=src_ref, hwdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_hwdst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def psrc_adrNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)
        mac_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_psrc_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def pdst_adrNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)
        mac_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_pdst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def psrc_adrExists(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = l2.ARP(psrc='124.233.255.79', pdst=dst_ref)
        mac_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_psrc_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def pdst_adrExists(self):
        src_ref = '83.78.233.252'
        dst_ref = '181.149.152.176'
        
        ref_pkt = l2.ARP(psrc=src_ref, pdst='124.233.255.79')
        mac_pkt = l2.ARP(psrc=src_ref, pdst=dst_ref)

        data = lib.build_mock_dict()

        pp.arp_pdst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


###########################################
############### IP
###########################################

    def ipsrc_adrNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.ip_src_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ipdst_adrNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.ip_dst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ipsrc_adrExists(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src='124.233.255.79', dst=dst_ref)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.ip_src_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ipdst_adrExists(self):
        src_ref = '83.78.233.252'
        dst_ref = '181.149.152.176'
        
        ref_pkt = inet.IP(src=src_ref, dst='124.233.255.79')
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref)

        data = lib.build_mock_dict()

        pp.ip_dst_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ttl_default(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=100)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=1)

        data = lib.build_mock_dict()

        pp.ip_ttl_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ttl_src_replace(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=99)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=1)

        data = lib.build_mock_dict()

        pp.ip_ttl_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ttl_dst_default(self):
        src_ref = '83.78.233.252'
        dst_ref = '181.149.152.176'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=100)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=1)

        data = lib.build_mock_dict()

        pp.ip_ttl_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def ttl_exception(self):
        src_ref = '107.149.218.168'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=1)
        mac_pkt = inet.IP(src=src_ref, dst=dst_ref, ttl=1)

        data = lib.build_mock_dict()

        pp.ip_ttl_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


###############################################
################## TCP
###############################################


    def win_default(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(window=200)
        mac_pkt = inet.TCP(window=1)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_win_size_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def win_src_replace(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(window=199)
        mac_pkt = inet.TCP(window=1)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_win_size_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def win_except(self):
        src_ref = '107.149.218.168'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(window=1)
        mac_pkt = inet.TCP(window=1)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_win_size_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def mss_default(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(options=[('MSS', 300)])
        mac_pkt = inet.TCP(options=[('MSS', 1)])

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_mss_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def mss_src_replace(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(options=[('MSS', 299)])
        mac_pkt = inet.TCP(options=[('MSS', 1)])

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_mss_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def mss_except(self):
        src_ref = '107.149.218.168'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(options=[('MSS', 1)])
        mac_pkt = inet.TCP(options=[('MSS', 1)])

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_mss_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def sport_notMapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(sport=40)
        mac_pkt = inet.TCP(sport=40)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_sport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def sport_Mapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(sport=30)
        mac_pkt = inet.TCP(sport=20)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_sport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def dport_notMapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(dport=40)
        mac_pkt = inet.TCP(dport=40)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_dport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def dport_Mapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.TCP(dport=30)
        mac_pkt = inet.TCP(dport=20)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_dport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


###############################################
################## UDP
###############################################


    def udp_sport_notMapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.UDP(sport=40)
        mac_pkt = inet.UDP(sport=40)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_sport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def udp_sport_Mapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.UDP(sport=30)
        mac_pkt = inet.UDP(sport=20)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_sport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def udp_dport_notMapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.UDP(dport=40)
        mac_pkt = inet.UDP(dport=40)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_dport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def udp_dport_Mapped(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'
        
        ref_pkt = inet.UDP(dport=30)
        mac_pkt = inet.UDP(dport=20)

        data = lib.build_mock_dict()

        data[TMdef.PACKET]['ip_src_old'] = src_ref

        pp.tcp_dport_change(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


###############################################
################## DNS
###############################################


    def dns_qd_question_ipNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'

        src_rev = '252.233.78.83.in-addr.arpa'
        
        ref_pkt = dns.DNS(qdcount=1, qd=[DNSQR(qtype=12, qname=src_rev)])
        mac_pkt = dns.DNS(qdcount=1, qd=[DNSQR(qtype=12, qname=src_rev)])

        data = lib.build_mock_dict()

        pp.dns_change_ips(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def dns_qd_questions_ipNotExist(self):
        src_ref = '83.78.233.252'
        dst_ref = '125.195.213.93'

        src_rev = '252.233.78.83.in-addr.arpa'
        src_rev = '93.213.195.125.in-addr.arpa'
        
        ref_pkt = dns.DNS(qdcount=2, qd=[DNSQR(qtype=12, qname=src_rev), DNSQR(qtype=12, qname=src_rev) ])
        mac_pkt = dns.DNS(qdcount=2, qd=[DNSQR(qtype=12, qname=src_rev), DNSQR(qtype=12, qname=src_rev) ])

        data = lib.build_mock_dict()

        pp.dns_change_ips(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def dns_qd_question_ipExist(self):
        src_ref = '181.149.152.176'
        dst_ref = '125.195.213.93'

        src_rev = '176.152.149.181.in-addr.arpa'
        
        ref_pkt = dns.DNS(qdcount=1, qd=[DNSQR(qtype=12, qname='79.255.233.124.in-addr.arpa')])
        mac_pkt = dns.DNS(qdcount=1, qd=[DNSQR(qtype=12, qname=src_rev)])

        data = lib.build_mock_dict()

        pp.dns_change_ips(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )


    def dns_qd_questions_ipExist(self):
        src_ref = '181.149.152.176'
        dst_ref = '80.142.128.2'

        src_rev = '176.152.149.181.in-addr.arpa'
        dst_rev = '2.128.142.80.in-addr.arpa'
        
        ref_pkt = dns.DNS(qdcount=2, qd=[DNSQR(qtype=12, qname='79.255.233.124.in-addr.arpa'), DNSQR(qtype=12, qname='121.163.47.167.in-addr.arpa') ])
        mac_pkt = dns.DNS(qdcount=2, qd=[DNSQR(qtype=12, qname=src_rev), DNSQR(qtype=12, qname=dst_rev ) ])

        data = lib.build_mock_dict()

        pp.dns_change_ips(mac_pkt, data)

        self.assertTrue( lib.compare_mac_pkts(ref_pkt, mac_pkt), msg= (str(ref_pkt) + ' == ' + str(mac_pkt)) )