import pygame
import random
class DisplayConfig:
    # Display settings
    width, height = 800, 600

class MapConfig:
    ## MAP CONFIGURATION VARIABLES
    # Map settings
    map_width, map_height = DisplayConfig.width * 2, DisplayConfig.height


obstacle_size = 50
class GameConfig:
    @staticmethod
    def get_bullet_count(weapon):
        if (weapon == "pistol"):
            return 14
        if (weapon == "sniper"):
            return 5
        if (weapon == "shotgun"):
            return 5

    # Player settings
    player_radius = 25
    rect_speed = 5
    recoil_force = 3
    # Bullet settings
    bullet_radius = 5
    bullet_speed = 10
    bullet_max_distance = 300
    # Obstacle settings
    num_obstacles = 20

    obstacles = [
        pygame.Rect(
            random.randint(0, MapConfig.map_width - obstacle_size),
            random.randint(0, MapConfig.map_height - obstacle_size),
            obstacle_size, obstacle_size
        ) for _ in range(num_obstacles)
    ]