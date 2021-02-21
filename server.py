import socket
import threading
import time
import itertools
import json

HEADER = 1024
HOST = 'localhost'
PORT = 22692
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

connections = dict()

def broadcast(msg):
  temp_dict = dict(**connections)
  for conn in temp_dict.values():
    try:
      send_message(conn, msg)
    except:
      pass

def send_message(conn, msg):
  send_msg = (msg).encode(FORMAT)
  send_length = str(len(send_msg)).encode(FORMAT)
  send_length += b' ' * (HEADER - len(send_length))
  conn.send(send_length)
  conn.send(send_msg)

def receive_message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT).strip() # receive msg length from client
    if msg_length:
      msg_length = int(msg_length)
      msg = conn.recv(msg_length).decode(FORMAT)
      message = json.loads(msg)['message'].strip()
    return message

def handle_client(clientname, conn, addr):
  print(f"new connection: {addr} connected.")
  connected = True
  try:
    while connected:
      message = receive_message(conn)
      if message == DISCONNECT_MESSAGE:
        connected = False
        
      if connected:
        # send to other client 
        broadcast(f"[{clientname}]: {message}")
  except KeyboardInterrupt:
    print("Thread interrupted")
  except:
    print("Connection closed by client...")
  finally:
    conn.close()
    broadcast(f"[{clientname}] ---Disconnected---")

def start():
  server.listen()
  print(f"server is listening on {HOST}.{PORT}")
  try:
    while True:
      conn, addr = server.accept()
      username = conn.recv(1024).decode(FORMAT).strip()
      print(f"[{username}] has been connected...")
      if username:
        client = threading.Thread(target=handle_client, args=(username, conn, addr))
        client.start()

        # add connections
        connections[username] = conn
        print(f"active connections: {threading.activeCount() - 1}")
  except:
    print("Server closing...")
  finally:
    server.close()
    
print(f"server is starting...")
start()
