#!/usr/bin/env python3


# supress RST
# sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP

import os
from scapy.all import *

#note:
# supress RST using 'sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP'
# we have to 'ping mail.yahoo.com' in background termial to sniff packets


def ARP():
    packets = sniff(timeout=10, filter="arp")
    print(packets.summary())
    wrpcap("./output/ARP_2001CS35.pcap", packets)


def DNS_request_response():
    dns_req = IP(dst="8.8.8.8")/UDP(dport=53) / \
        DNS(rd=1, qd=DNSQR(qname="mail.yahoo.com"))
    dns_res = sr1(dns_req, verbose=1)
    print(dns_res.summary())
    ans = PcapWriter("./output/DNS_request_response_2001CS35.pcap",
                     append=True, sync=True)
    ans.write(dns_req)
    ans.write(dns_res)


def PING_request_response():
    packet = IP(dst="172.16.180.95")/ICMP()
    answer = sr1(packet)
    ans = PcapWriter("./output/PING_request_response_2001CS35.pcap",
                     sync=True, append=True)
    ans.write(packet)
    ans.write(answer)


def TCP_3_way_handshake_start():
    ip = IP(dst="172.16.180.95")
    tcp = TCP(sport=1234, dport=80, flags="S", seq=1000)
    synack = sr1(ip/tcp)
    ack = TCP(sport=synack[TCP].dport, dport=synack[TCP].sport,
          flags="A", seq=synack[TCP].ack, ack=synack[TCP].seq + 1)
    send(ip/ack)
    wrpcap("./output/TCP_3_way_handshake_start_2001CS35.pcap", [ip/tcp, synack, ip/ack])

#change dst ip to any localhost to capture packets
def ARP_request_response():
    packet = IP(dst="172.16.180.95")/ICMP()
    answer = sr1(packet)
    ans = PcapWriter("./output/ARP_request_response_2001CS35.pcap",
                     sync=True, append=True)
    ans.write(packet)
    ans.write(answer)


def TCP_handshake_close():
    ip = IP(dst="172.16.180.95")
    tcp = TCP(sport=1234, dport=80, flags="F", seq=2000)
    finack = sr1(ip/tcp)
    ack = TCP(sport=finack[TCP].dport, dport=finack[TCP].sport, flags="A", seq=finack[TCP].ack, ack=finack[TCP].seq + 1)
    send(ip/ack)
    tcp = TCP(sport=1234, dport=80, flags="A", seq=ack.ack, ack=finack[TCP].seq + 1)
    fin = sr1(ip/tcp)
    ack = TCP(sport=fin[TCP].dport, dport=fin[TCP].sport, flags="A", seq=fin[TCP].ack, ack=fin[TCP].seq + 1)
    send(ip/ack)
    wrpcap("./output/TCP_handshake_close_2001CS35.pcap", [ip/tcp, finack, ack, fin, ip/ack])


#calling functions

# os.system("gnome-terminal -e 'ping mail.yahoo.com'")
ARP()
DNS_request_response()
PING_request_response()
TCP_3_way_handshake_start()
ARP_request_response()
TCP_handshake_close()

