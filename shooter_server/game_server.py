import sys
# sys.path.insert(1, '../res/values')
# sys.path.insert(1, '../data')
import socket
import threading
import time
import json
from config import GameConfig

from theme import ColorPalette
from server_global_variables import all_players, bullets
from network import create_server_socket
from config import MapConfig


def run_server():

    def send_game_state(client_socket):
        last_sent_players_state = ""
        last_sent_bullets_state = ""
        while True:
            time.sleep(0.03)
            # keep sending latest game state
            players_state = json.dumps({"state_type": "players", "data": all_players})
            # print(f"LAST: {last_sent_players_state}, CURRENT: {players_state}, ARE EQUAL: {last_sent_players_state == players_state}")
            if (last_sent_players_state != players_state):
                try:
                    client_socket.sendall((players_state + "\t").encode('utf-8'))
                    last_sent_players_state = players_state
                    print(f"Sent players data: {all_players}")
                except:
                    # FIXME
                    pass

            bullets_state = json.dumps({"state_type": "bullets", "data": bullets})
            if (last_sent_bullets_state != bullets_state):
                # \t used here as a sign of termination! Client-side will handle this
                client_socket.sendall((bullets_state + "\t").encode('utf-8'))
                last_sent_bullets_state = bullets_state
                print(f"ALL BULLETS SENT: {bullets}")

    def get_game_state(client_socket):
        client_id : str = ""
        while True:
            data = client_socket.recv(4096)
            print("received data!")
            if not data:
                break
            print("received data is not empty!")
            print("data: ", data.decode('utf-8'))
            for data_part in data.decode('utf-8').split('\t')[:-1]:
                try:
                    print(f"data part: {data_part}")
                    updated_state = json.loads(data_part)
                    print(f"Received: {updated_state}")
                    if (updated_state['action'] == 'play'):
                        client_id = updated_state['id']
                        all_players[client_id] = {
                            "id": client_id,
                            "x": 20, # START AT THE CENTRE X
                            "y": 20 * MapConfig.one_height_unit, # START AT THE CENTRE Y
                            "health": 100,
                            "armor": 100,
                            "bullets_left": GameConfig.get_bullet_count(updated_state['weapon']),
                            "reloading": False,
                            "healing": False,
                            "weapon": "pistol",
                            "reload_start_time": None,
                            "healing_start_time": None,
                            "color": ColorPalette.GREEN,
                            "gun_length": 40,
                            "score": 0,
                            "alive": True  # Track if the player is alive
                        }
                        client_socket.sendall("200".encode('utf-8'))
                        print(f"Client connection complete, id: {client_id}")
                        this_player = all_players[client_id]
                        # push game state continuously once joined
                        threading.Thread(target=send_game_state, args=(client_socket,)).start()
                    elif (updated_state['action'] == 'player_position'):
                        this_player['x'] = updated_state['x']
                        this_player['y'] = updated_state['y']
                        this_player['reload_start_time'] = updated_state['reload_start_time']
                        this_player['healing_start_time'] = updated_state['healing_start_time']
                        this_player['reloading'] = updated_state['reloading']
                        this_player['healing'] = updated_state['healing']
                        this_player['bullets_left'] = updated_state['bullets_left']
                        this_player['weapon'] = updated_state['weapon']
                        this_player['health'] = updated_state['health']
                        # this_player['armor'] = updated_state['armor']
                        print(f"Received position data: {updated_state}")
                    elif (updated_state['action'] == "bullet_fired"):
                        # {"x": bullet_start_x, "y": bullet_start_y, "angle": player1_angle, "distance_traveled": 0}
                        bullets[client_id] = updated_state['data']
                        # bullets[client_id]['x'] = updated_state['x']
                        # bullets[client_id]['y'] = updated_state['y']
                        # bullets[client_id]['angle'] = updated_state['angle']
                        # bullets[client_id]['distance_traveled'] = updated_state['distance_traveled']
                        # this_player['bullets_left'] -= 1
                        print(f"Received bullet data: {updated_state}")
                    elif (updated_state['action'] == 'flag_score'):
                        # increase score
                        all_players[client_id]['score'] += 10
                        print(f"Received flag score: {updated_state}")
                    elif (updated_state['action'] == "bullet_hit"):
                        damage = updated_state['damage']
                        # increase score
                        all_players[client_id]['score'] += damage
                        # damage player
                        target = all_players[updated_state['target_id']]
                        if target["armor"] > 0:
                            target["armor"] -= damage
                            if target["armor"] < 0:
                                target["health"] += target["armor"]
                                target["armor"] = 0
                        else: target["health"] -= damage
                        # check damaged player:
                        if target["health"] <= 0:
                            target["alive"] = False
                            time.sleep(0.1)
                            # clean up everything related to the player
                            del all_players[updated_state['target_id']]
                            del bullets['target_id']
                        print(f"Received hit data: {updated_state}")
                # except JSONDecodeError:
                #     print("went wrong!")
                except Exception as e:
                    print(f"Went wrong: {e}")


    def client_handler(client_socket):
        # get game state continuously
        threading.Thread(target=get_game_state, args=(client_socket,)).start()



    server_socket = create_server_socket()

    # SERVER LOBBY LOGIC
    while True:
        # wait for the incoming requests (blocking function)
        client_socket, client_address = server_socket.accept()
        print(f"LOBBY: Connection established with {client_address}")
        # handle each client request in a separate thread
        client_handler_thread = threading.Thread(target=client_handler, args=(client_socket,))  # Create a new thread to handle the connection (parallelism)
        client_handler_thread.start()

run_server()