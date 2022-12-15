import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target",
                        help="target ip address")

    (options, arguments) = parser.parse_args()
    return options


def scan(ip):

    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # testing wlan0 in future!
    arp_request_broadcast =  broadcast/arp_request

    answeres_list = scapy.srp(arp_request_broadcast,
                                timeout=2,
                                verbose=False)[0]

    mac_w_ip = []

    for element in answeres_list:
        ans_ip = element[1].psrc
        ans_mac = element[1].hwsrc
        mac_w_ip_dict = { "ip" : ans_ip, "mac" : ans_mac }
        mac_w_ip.append(mac_w_ip_dict)
    return mac_w_ip


def output(data):
    for item in data:
        ip = item['ip']
        mac = item['mac']
        print(f"[info] {ip} -> {mac}")


if __name__ == "__main__":
    options = get_arguments()
    target = options.target
    macs_and_ip = scan(target)
    output(macs_and_ip)
