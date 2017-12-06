import socket
import sys
import os


HOST = "127.0.0.1"
# HOST = socket.gethostname()
PORT = 3334

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print("[+] Connected with Server")

# get file name to send
f_send = os.getcwd() + '/sample/image/aaaa.PNG'
# f_send = "file_to_send.mp3"
# open file
file_name = open(f_send,'rb')
print("[+] Sending file...")
while True:
    strng = file_name.readline()
    if not strng:
        break

    print("[+] Sent")
    client.send(strng)
file_name.close()
client.close()

print("[+] Data sent successfully")