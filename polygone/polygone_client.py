import socket
import time


if __name__ == "__main__":

    p_ip = "192.168.1."

    for i in range(255):
        try:
            time.sleep(5)
            ip = p_ip + str(i)
            port = 8080
            data = "Hey its ping from client!".encode("utf-8")

            print(f"Connect to {ip}")

            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((ip, port))
            print("point2")
            result = connection.recv(1024)
            result = result.decode("utf-8")

            print("point")
            if result == "koto":
                while True:

                    connection.send(data)

                    time.sleep(5)
            else:
                connection.close()
                print("close")
        except Exception:
            a = 0
