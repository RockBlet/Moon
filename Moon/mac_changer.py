import random
import subprocess
import re
import optparse

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface",
                        help="interface to cahnge its MAC address")

    parser.add_option("-m", "--mac", dest="new_mac",
                        help="New Mac address")

    (options, arguments) = parser.parse_args()
    return options


def get_random_mac():

        rand_mac_addr = [0x00, 0x50, 0x56, random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, rand_mac_addr))


def change_mac(interface, new_mac):

    print(f"[+] Changing mac adress for [{interface}] to [{new_mac}] ")
    print(f"[+] Changing mac adress for [{interface}] to [{new_mac}] ")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

    print(f"[+] function -> {type} mac is :: {new_mac}")


def validation_result(interface, new_mac):
    print("[+] Mac address validation")

    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    ifconfig_output = ifconfig_output.decode("utf-8")
    machine_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)

    print("[+] Validation successful :: New mac address SET")
    print(f"[+] New mac address -> {new_mac}")


if __name__ == "__main__":

    print("\n")

    options = get_arguments()
    interface = options.interface
    new_mac = options.new_mac

    if not new_mac:
        new_mac = get_random_mac()

    change_mac(interface, new_mac)
    validation_result(interface, new_mac)

    print("\n")
