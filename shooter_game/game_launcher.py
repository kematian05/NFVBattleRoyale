import os
import sys
# sys.path.insert(1, '../res/values')
# sys.path.insert(1, '../data')
import socket
import threading
import pygame
import random
import math
import time
import json
from config import MapConfig, DisplayConfig, GameConfig
from theme import ColorPalette
from network import connect_to_game_server
from physics import can_move


pygame.mixer.init()
script_dir = os.path.dirname(__file__)
# pistol_reload
pistol_reload_sound_path = os.path.join(script_dir, "sound_effects/pistol_reload.mp3")
pistol_reload_sound = pygame.mixer.Sound(pistol_reload_sound_path)
# pistol_shot
pistol_shot_sound_path = os.path.join(script_dir, "sound_effects/pistol_shot.mp3")
pistol_shot_sound = pygame.mixer.Sound(pistol_shot_sound_path)
# empty_shot
empty_shot_sound_path = os.path.join(script_dir, "sound_effects/empty_shot.mp3")
empty_shot_sound = pygame.mixer.Sound(empty_shot_sound_path)
# sniper_shot
sniper_shot_sound_path = os.path.join(script_dir, "sound_effects/sniper_shot.mp3")
sniper_shot_sound = pygame.mixer.Sound(sniper_shot_sound_path)
# sniper_reload
sniper_reload_sound_path = os.path.join(script_dir, "sound_effects/sniper_reload.mp3")
sniper_reload_sound = pygame.mixer.Sound(sniper_reload_sound_path)
# shotgun_reload
shotgun_reload_sound_path = os.path.join(script_dir, "sound_effects/shotgun_reload.mp3")
shotgun_reload_sound = pygame.mixer.Sound(shotgun_reload_sound_path)
# shotgun_shot
shotgun_shot_sound_path = os.path.join(script_dir, "sound_effects/shotgun_shot.mp3")
shotgun_shot_sound = pygame.mixer.Sound(shotgun_shot_sound_path)
# game_over
game_over_sound_path = os.path.join(script_dir, "sound_effects/game_over.mp3")
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

def launch_game(this_player_id, selected_weapon):
    is_active = True
    # Connect to the game
    client_socket = connect_to_game_server(this_player_id, selected_weapon)
    if not client_socket: return

    # Initialize Pygame
    pygame.init()
    # Font
    font = pygame.font.Font(None, 36)
    # State variables
    all_players: dict = {}
    all_bullets = {}
    # Initialize current player
    current_player = {
        "id": this_player_id,
        "x": 60,  # START AT THE CENTRE X
        "y": 50 * MapConfig.one_height_unit,  # START AT THE CENTRE Y
        "health": 100,
        "armor": 100,
        "weapon": selected_weapon,
        "bullets_left": GameConfig.get_bullet_count(selected_weapon),
        "reloading": False,
        "healing": False,
        "reload_start_time": None,
        "healing_start_time": None,
        "color": ColorPalette.RED,
        "gun_length": 40,
        "alive": True  # Track if the player is alive
    }

    def move_player(dx, dy):
        nonlocal current_player
        # Check if the player can actually move (collision check)
        can_move_x, can_move_y = can_move(player_pos, GameConfig.get_player_radius(selected_weapon), dx, dy, GameConfig.obstacles)
        if can_move_x:
            current_player['x'] += dx
        if can_move_y:
            current_player['y'] += dy


    last_sent_player_position_state: str = ""
    last_sent_bullet_state: str = ""

    def start_listening_server():
        nonlocal is_active
        nonlocal all_players
        nonlocal client_socket
        nonlocal all_bullets
        nonlocal current_player
        nonlocal this_player_id

        while is_active:
            # receive request
            data = client_socket.recv(4096)
            # print(f"Received full data: {data}")
            # populate all players
            if not data: break

            try:
                for data_part in data.decode('utf-8').split('\t')[:-1]:
                    # print(f"Received data part: {data_part}")
                    state = json.loads(data_part)
                    if (state['state_type'] == "players"):
                        all_players = state['data']
                        # get current player
                        try:
                            current_player = all_players[this_player_id]
                            current_player['color'] = ColorPalette.BLUE
                            # print(f"current player: {current_player}")
                        except KeyError:
                            print("player dead")
                    elif (state['state_type'] == 'bullets'):
                        # print(f"ALL BULLETS RECEIVED: {all_bullets}")
                        all_bullets = state['data']
            except json.decoder.JSONDecodeError:
                print(f"could not decode")
            # # Populate opponents dict
            # all_players_copy = all_players.copy()
            # del all_players_copy[this_player_id]
            # opponents = all_players_copy

    # Start listening for server messages
    threading.Thread(target=start_listening_server).start()
    # SET DISPLAY
    window = pygame.display.set_mode((DisplayConfig.width, DisplayConfig.height))
    pygame.display.set_caption("NFV Battle Royale")

    own_bullets = []  # Store all bullets with info about the shooter

    # Camera offset
    camera_x, camera_y = 0, 0
    last_flag_capture_date = 0
    # Game loop
    while is_active:
        if (current_player['alive'] == False):
            game_over_sound.play()
            time.sleep(2)
            print("Player is dead...")
            is_active = False
            pygame.quit()
            client_socket.close()
            return


        # Handle player camera movement
        player_offset_x = current_player["x"] - DisplayConfig.width // 2
        player_offset_y = current_player["y"] - DisplayConfig.height // 2
        if (player_offset_x > 0 and player_offset_x < MapConfig.map_width - DisplayConfig.width): camera_x = player_offset_x
        if (player_offset_y > 0 and player_offset_y < MapConfig.map_height - DisplayConfig.height): camera_y = player_offset_y

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting...")
                is_active = False
                pygame.quit()
                client_socket.close()
                return
                # sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                # Player fires
                if current_player["alive"] and event.key == pygame.K_SPACE and not current_player["reloading"] and not current_player["healing"]:
                    if current_player["bullets_left"] <= 0:
                        empty_shot_sound.play()
                    else:
                        # Bullet is added to the game
                        if current_player['weapon'] == "sniper":
                            sniper_shot_sound.play()
                        elif current_player['weapon'] == "pistol":
                            pistol_shot_sound.play()
                        elif current_player['weapon'] == "shotgun":
                            shotgun_shot_sound.play()
                        bullet_start_x = current_player["x"] + math.cos(player1_angle) * current_player["gun_length"]
                        bullet_start_y = current_player["y"] + math.sin(player1_angle) * current_player["gun_length"]
                        own_bullets.append(
                            {"x": bullet_start_x, "y": bullet_start_y, "angle": player1_angle, "distance_traveled": 0})
                        # RECOIL
                        move_player(-math.cos(player1_angle) * GameConfig.get_recoil_force(selected_weapon), -math.sin(player1_angle) * GameConfig.get_recoil_force(selected_weapon))
                        # Bullet decreases
                        current_player["bullets_left"] -= 1
                # Reload
                elif event.key == pygame.K_r and current_player["alive"] and not current_player["reloading"] and not current_player["healing"]:
                    current_player["reloading"] = True
                    if current_player['weapon'] == "pistol":
                        pistol_reload_sound.play()
                    elif current_player['weapon'] == "shotgun":
                        shotgun_reload_sound.play()
                    elif current_player['weapon'] == "sniper":
                        sniper_reload_sound.play()
                    current_player["reload_start_time"] = time.time()

                # Heal
                elif event.key == pygame.K_e and current_player["alive"] and not current_player["reloading"] and not current_player["healing"]:
                    current_player["healing"] = True
                    current_player["healing_start_time"] = time.time()

        # Player movement and angle calculations
        keys = pygame.key.get_pressed()

        # Player movement (WASD)
        has_moved = False
        if current_player["alive"]:
            player_pos = (current_player['x'], current_player['y'])
            dx = 0
            dy = 0
            if keys[pygame.K_w]:
                dy = -GameConfig.get_player_speed(selected_weapon)
            if keys[pygame.K_s]:
                dy = GameConfig.get_player_speed(selected_weapon)
            if keys[pygame.K_a]:
                dx = - GameConfig.get_player_speed(selected_weapon)
            if keys[pygame.K_d]:
                dx = GameConfig.get_player_speed(selected_weapon)
            has_moved = dx != 0 or dy != 0

            move_player(dx, dy)


        # Get mouse position and calculate angles only if alive
        if current_player["alive"]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player1_angle = math.atan2((mouse_y + camera_y) - current_player["y"],
                                       (mouse_x + camera_x) - current_player["x"])

        # Handle reloading
        if current_player["reloading"]:
            if has_moved:
                current_player["reloading"] = False
            elif time.time() - current_player["reload_start_time"] >= GameConfig.get_reload_duration(selected_weapon):
                current_player["bullets_left"] = GameConfig.get_bullet_count(selected_weapon)
                current_player["reloading"] = False
        # Handle healing
        if current_player["healing"]:
            if has_moved:
                current_player["healing"] = False
            elif time.time() - current_player["healing_start_time"] >= GameConfig.get_heal_duration():
                current_player["health"] += GameConfig.get_heal_amount()
                current_player["health"] = min(100, current_player['health'])
                current_player["healing"] = False

        # Update own bullet's position
        for bullet in own_bullets:
            # print(f"BULLET: {bullet}")
            # Move bullet
            dx = math.cos(bullet["angle"]) * GameConfig.get_bullet_speed(selected_weapon)
            dy = math.sin(bullet["angle"]) * GameConfig.get_bullet_speed(selected_weapon)
            can_move_x, can_move_y = can_move([bullet["x"], bullet["y"]], GameConfig.get_bullet_radius(selected_weapon), dx, dy, GameConfig.obstacles)
            if (can_move_x): bullet["x"] += dx
            if (can_move_y): bullet["y"] += dy

            bullet["distance_traveled"] += GameConfig.get_bullet_speed(selected_weapon)

            for p_id in all_players.keys():
                target = all_players[p_id]
                if target == current_player:
                    # Check if it expired or still going
                    if bullet["distance_traveled"] > GameConfig.get_bullet_max_distance(selected_weapon):
                        own_bullets.remove(bullet)
                        break
                    continue
                # Collision check
                if target["alive"]:
                    player_center = (target["x"], target["y"])
                    bullet_pos = (int(bullet["x"]), int(bullet["y"]))
                    distance_to_player = math.hypot(bullet_pos[0] - player_center[0], bullet_pos[1] - player_center[1])
                    # If hit the player
                    if distance_to_player < GameConfig.get_player_radius(selected_weapon):
                        # damage player
                        if target["armor"] > 0:
                            target["armor"] -= 10
                        else:
                            target["health"] -= 10
                        own_bullets.remove(bullet)
                        # check damaged player:
                        if target["health"] <= 0:
                            target["alive"] = False
                        # bullet can only hit one player, so break checking if it hits anyone else
                        client_socket.sendall(
                            json.dumps({"action": "bullet_hit", "target_id": target['id'], 'damage': GameConfig.get_bullet_damage(selected_weapon)}).encode(
                                'utf-8'))
                        break
                    # If bullet did not hit any player yet
                    else:
                        # Check if it expired or still going
                        if bullet["distance_traveled"] > GameConfig.get_bullet_max_distance(selected_weapon):
                            own_bullets.remove(bullet)
                            break

        # Drawing phase
        # Background
        window.fill(ColorPalette.WHITE)
        # Borders
        pygame.draw.rect(window, ColorPalette.RED, (-camera_x, -camera_y, MapConfig.map_width, MapConfig.map_height), 10)

        # Obstacles
        for obstacle in GameConfig.obstacles:
            pygame.draw.rect(window, ColorPalette.GREEN,
                             pygame.Rect(obstacle.x - camera_x, obstacle.y - camera_y, obstacle.width, obstacle.height))
        # Visuals, namely Flag area
        for visual in GameConfig.visuals:
            color = ColorPalette.BLACK
            can_move_x, can_move_y = can_move((current_player['x'], current_player['y']), GameConfig.get_player_radius(selected_weapon), 0, 0, [visual])
            if not can_move_x or not can_move_y:
                # Inside flag area
                color = ColorPalette.GREEN
                # This should be sent only once every second
                print(last_flag_capture_date,time.time())
                if time.time() - last_flag_capture_date > 2:
                    print("FLAG SCORE SENT!!!")
                    client_socket.sendall(json.dumps({"action": "flag_score"}).encode('utf-8'))
                    last_flag_capture_date = time.time()
            else:
                last_flag_capture_date = time.time()

            pygame.draw.rect(window,
                             color, pygame.Rect(visual.x - camera_x, visual.y - camera_y, visual.width, visual.height),width=5)
        # Draw player - current
        if current_player['alive']:
            armor_thickness = max(1, int((current_player['armor'] / 100) * 10))
            color = current_player['color']
            # draw armor
            pygame.draw.circle(window, ColorPalette.BLACK,
                               (int(current_player['x'] - camera_x), int(current_player["y"] - camera_y)),
                               GameConfig.get_player_radius(selected_weapon) + armor_thickness)
            # draw base circle
            pygame.draw.circle(window, color,
                               (int(current_player['x'] - camera_x), int(current_player["y"] - camera_y)),
                               GameConfig.get_player_radius(selected_weapon) - ((100 - current_player['health']) / 100) * GameConfig.get_player_radius(selected_weapon))
            # Draw player name above the player circle
            name_surface = font.render(current_player["id"], True, color)
            window.blit(name_surface, (int(current_player["x"] - camera_x) - name_surface.get_width() // 2,
                                       int(current_player["y"] - camera_y) - GameConfig.get_player_radius(selected_weapon) - 35))
            if(current_player['reloading']):
                # Draw reloading text below the player circle
                name_surface = pygame.font.Font(None, 18).render("Reloading...", True, color)
                window.blit(name_surface, (int(current_player["x"] - camera_x) - name_surface.get_width() // 2,
                                           int(current_player["y"] - camera_y) + GameConfig.get_player_radius(selected_weapon) + 12))

            if(current_player['healing']):
                # Draw healing text below the player circle
                name_surface = pygame.font.Font(None, 18).render("Healing...", True, color)
                window.blit(name_surface, (int(current_player["x"] - camera_x) - name_surface.get_width() // 2,
                                           int(current_player["y"] - camera_y) + GameConfig.get_player_radius(selected_weapon) + 12))

        # Draw opponents (exclude our player)
        for player in all_players.values():
            if (player['id'] == this_player_id): continue

            if player["alive"]:
                armor_thickness = max(1, int((player["armor"] / 100) * 10))
                color = player["color"]
                # draw armor
                pygame.draw.circle(window, ColorPalette.BLACK, (int(player["x"] - camera_x), int(player["y"] - camera_y)),
                                   GameConfig.get_player_radius(player['weapon']) + armor_thickness)
                # draw base circle
                pygame.draw.circle(window, color,
                                   (int(player['x'] - camera_x), int(player["y"] - camera_y)),
                                   GameConfig.get_player_radius(player['weapon']) - ((100 - player['health']) / 100) * GameConfig.get_player_radius(player['weapon']))
                # Draw player name above the player circle
                name_surface = font.render(player["id"], True, color)
                window.blit(name_surface, (int(player["x"] - camera_x) - name_surface.get_width() // 2,
                                           int(player["y"] - camera_y) - GameConfig.get_player_radius(player['weapon']) - 35))
                if(player['reloading']):
                    # Draw reloading text below the player circle
                    name_surface = pygame.font.Font(None, 18).render("Reloading...", True, color)
                    window.blit(name_surface, (int(player["x"] - camera_x) - name_surface.get_width() // 2,
                                           int(player["y"] - camera_y) + GameConfig.get_player_radius(player['weapon']) + 12))

                if(player['healing']):
                    # Draw reloading text below the player circle
                    name_surface = pygame.font.Font(None, 18).render("Healing...", True, color)
                    window.blit(name_surface, (int(current_player["x"] - camera_x) - name_surface.get_width() // 2,
                                           int(current_player["y"] - camera_y) + GameConfig.get_player_radius(selected_weapon) + 12))

        # Draw own bullets
        for bullet in own_bullets:
            pygame.draw.circle(window, ColorPalette.RED, (int(bullet["x"] - camera_x), int(bullet["y"] - camera_y)), GameConfig.get_bullet_radius(selected_weapon))

        # Draw other bullets
        for bullet_owner in all_bullets.keys():
            # exclude own bullets
            if (bullet_owner == this_player_id): continue
            # print(f"INSIDE BULLET IS: {bullet}")
            for bullet in all_bullets[bullet_owner]:
                # FIXME
                try:
                    pygame.draw.circle(window, ColorPalette.RED, (int(bullet["x"] - camera_x), int(bullet["y"] - camera_y)),
                                   GameConfig.get_bullet_radius(all_players[bullet_owner]['weapon']))
                except:
                    pass

        # Display stats
        if current_player["alive"]:
            window.blit(font.render(f"Health: {current_player['health']}", True, ColorPalette.BLUE), (10, DisplayConfig.height - 40))
            window.blit(font.render(f"Armor: {current_player['armor']}", True, ColorPalette.BLUE), (10, DisplayConfig.height - 70))
            window.blit(font.render(f"Bullets: {current_player['bullets_left']}", True, ColorPalette.BLUE), (10, DisplayConfig.height - 100))

        # Display leaderboard in the top-right corner
        x = DisplayConfig.width - 20  # Set x offset near the right edge
        y = 20  # Start y offset from the top
        leaderboard_font = pygame.font.Font(None, 24)
        for player in all_players.values():
            text_surface = leaderboard_font.render(f"{player['id']} - {player['score']} points", True, (0, 0, 0))  # Black text
            text_rect = text_surface.get_rect(topright=(x, y))
            window.blit(text_surface, text_rect)
            y += text_surface.get_height() + 5  # Move down for the next line with spacing

        player_position_state = json.dumps({"action": "player_position",
                                            'x': current_player['x'],
                                            'y': current_player['y'],
                                            'reloading': current_player['reloading'],
                                            'healing': current_player['healing'],
                                            'reload_start_time': current_player['reload_start_time'],
                                            'healing_start_time': current_player['healing_start_time'],
                                            'bullets_left': current_player['bullets_left'],
                                            'health': current_player['health'],
                                            'weapon': selected_weapon,
                                            'armor': current_player['armor']
                                            })
        # print(f"LAST: {last_sent_player_position_state}, CURRENT: {player_position_state}, ARE EQUAL: {last_sent_player_position_state == player_position_state}")
        if last_sent_player_position_state != player_position_state:
            # SEND POSITION DATA TO SERVER
            client_socket.sendall(player_position_state.encode('utf-8'))
            last_sent_player_position_state = player_position_state
            # print(f"player position updated: {last_sent_player_position_state}")
        # else:
        #     print("Redundant player position state send eliminated")

        bullet_state = json.dumps({"action": "bullet_fired", "data": own_bullets})
        # print("FRAME")
        if last_sent_bullet_state != bullet_state:
            # SEND BULLET DATA TO SERVER
            # print("BULLET DATA SENT TO SERVER!")
            client_socket.sendall(bullet_state.encode('utf-8'))
            last_sent_bullet_state = bullet_state

        # Update display
        pygame.display.flip()
        pygame.time.Clock().tick(30)