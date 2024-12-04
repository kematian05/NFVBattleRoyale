import json
import socket

SERVER_PORT = 3169

def create_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'  # Server's IP
    port = SERVER_PORT  # Server's port
    client_socket.connect((host, port))
    print("Connected to the server")
    return client_socket

def create_server_socket():
    # create a tcp server socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = '0.0.0.0'  # all interfaces
    s.bind((host, SERVER_PORT))  # Tell OS to forward these packets to our socket
    s.listen(5)  # Backlog of 5 connections, after 5 are in queue, the rest will be refused
    print(f"Started listening on {host}:{SERVER_PORT}")
    return s

def connect_to_game_server(player_id, weapon):
    # connect to server
    client_socket = create_client_socket()
    # PLAY REQUEST
    client_socket.sendall(json.dumps({"action": "play", "id": player_id, "weapon": weapon}).encode('utf-8'))
    # PLAY RESPONSE
    response = client_socket.recv(1024).decode('utf-8')
    if (response != "200"):
        print(f"Couldn't join the room: {response}")
        return None

    return client_socket