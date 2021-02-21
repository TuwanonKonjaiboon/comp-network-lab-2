import socket
import threading
import os
import json

HEADER = 1024
HOST = 'localhost'
PORT = 22692
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

username = input("Client username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_message(msg):
  data = {
    'message': msg
  }
  data = json.dumps(data)
  message = (data).encode(FORMAT)
  send_length = str(len(message)).encode(FORMAT) # length of msg
  send_length += b' ' * (HEADER - len(send_length)) # padaing header w/ space
  client.send(send_length) # send len of (byte) message
  client.send(message) # send actual message (byte)

def thread_send():
  send_message(f"{username} join chat room!")
  try:
    while True:
      msg = input(f">>\n")
      send_message(msg)
      if msg == DISCONNECT_MESSAGE:
        break
  finally:
    print("Closing connection send")
    client.close()
    os._exit(1)

def receive_message():
  msg_length = client.recv(HEADER).decode(FORMAT).strip()
  if msg_length:
    msg_length = int(msg_length)
    msg = client.recv(msg_length).decode(FORMAT)
    return msg

def thread_recv():
  try:
    while True:
        msg = receive_message()
        
        # display message
        print(msg)
        
        if not msg:
          break
  finally:
    print("Closing connection receive")
    client.close()
    os._exit(1)

def start():
  # noti user connect to chat room
  client.sendall(username.encode(FORMAT))
  threading.Thread(target=thread_send).start()
  threading.Thread(target=thread_recv).start()

start()