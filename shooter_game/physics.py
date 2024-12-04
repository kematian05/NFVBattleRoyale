# Function to check collision with obstacles for a circular player
import math

from config import MapConfig


def can_move(player_position, player_radius, dx, dy, obstacles):
    # Calculate the new player position after the move
    x = player_position[0]
    y = player_position[1]
    new_x = x + dx
    new_y = y + dy
    can_move_x, can_move_y = True, True
    # Check for map borders
    if new_x < 0 or new_x >= MapConfig.map_width: can_move_x = False
    if new_y < 0 or new_y >= MapConfig.map_height: can_move_y = False

    # Check for collision with each obstacle
    for obstacle in obstacles:
        # Find the closest point on the obstacle to the new player position
        closest_x = max(obstacle.left, min(new_x, obstacle.right))
        closest_y = max(obstacle.top, min(y, obstacle.bottom))
        # Calculate the distance from the player's new position to the closest point
        distance_x = math.sqrt((closest_x - new_x) ** 2 + (closest_y - y) ** 2)

        # Find the closest point on the obstacle to the new player position
        closest_x = max(obstacle.left, min(x, obstacle.right))
        closest_y = max(obstacle.top, min(new_y, obstacle.bottom))
        # Calculate the distance from the player's new position to the closest point
        distance_y = math.sqrt((closest_x - x) ** 2 + (closest_y - new_y) ** 2)

        if distance_x < player_radius:
            can_move_x = False
        if distance_y < player_radius:
            can_move_y = False

    return (can_move_x, can_move_y)