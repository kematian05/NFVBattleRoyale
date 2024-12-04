import pygame

import random

pygame.init()


class DisplayConfig:
    # Display settings

    width, height = 1000, 800


class MapConfig:
    ## MAP CONFIGURATION VARIABLES

    # Map settings

    map_width, map_height = DisplayConfig.width * 1.25, DisplayConfig.height * 1.4

    one_height_unit = map_height / 140

    one_width_unit = map_width / 125


def add_rectangle(from_width_percent, to_width_percent, from_height_percent, to_height_percent):
    return pygame.Rect(

        MapConfig.one_width_unit * from_width_percent, MapConfig.one_height_unit * from_height_percent,

        MapConfig.one_width_unit * (to_width_percent - from_width_percent),

        MapConfig.one_height_unit * (to_height_percent - from_height_percent)

    )


obstacle_size = 50


class GameConfig:
    # Obstacle settings

    num_obstacles = 20

    @staticmethod
    def get_recoil_force(weapon):

        if (weapon == "pistol"):
            return 5

        if (weapon == "sniper"):
            return 30

        if (weapon == "shotgun"):
            return 15

    @staticmethod
    def get_bullet_speed(weapon):

        if (weapon == "pistol"):
            return 10

        if (weapon == "sniper"):
            return 30

        if (weapon == "shotgun"):
            return 20

    @staticmethod
    def get_bullet_max_distance(weapon):

        if (weapon == "pistol"):
            return 300

        if (weapon == "sniper"):
            return 600

        if (weapon == "shotgun"):
            return 80

    @staticmethod
    def get_player_speed(weapon):

        if (weapon == "pistol"):
            return 5

        if (weapon == "sniper"):
            return 2.5

        if (weapon == "shotgun"):
            return 7

    @staticmethod
    def get_bullet_count(weapon):

        if (weapon == "pistol"):
            return 14

        if (weapon == "sniper"):
            return 5

        if (weapon == "shotgun"):
            return 5

    @staticmethod
    def get_heal_amount():

        return 10

    @staticmethod
    def get_reload_duration(weapon):

        if (weapon == "pistol"):
            return 3

        if (weapon == "sniper"):
            return 10

        if (weapon == "shotgun"):
            return 5

    @staticmethod
    def get_heal_duration():

        return 3

    @staticmethod
    def get_bullet_damage(weapon):

        if (weapon == "pistol"):
            return 25

        if (weapon == "sniper"):
            return 100

        if (weapon == "shotgun"):
            return 100

    @staticmethod
    def get_bullet_radius(weapon):

        if (weapon == "pistol"):
            return 5

        if (weapon == "sniper"):
            return 10

        if (weapon == "shotgun"):
            return 7

    @staticmethod
    def get_player_radius(weapon):

        if (weapon == "pistol"):
            return 25

        if (weapon == "sniper"):
            return 40

        if (weapon == "shotgun"):
            return 30

    obstacles = [

        # TEAM 1

        add_rectangle(

            5, 8,
            5, 10

        ),

        add_rectangle(

            10, 17,

            20, 30

        ),

        add_rectangle(

            12, 15,

            50, 70

        ),

        add_rectangle(

            20, 27,

            30, 52

        ),

        add_rectangle(

            20, 27,
            70, 92

        ),

        add_rectangle(

            30, 33,

            15, 35

        ),

        # FLAG

        # add_rectangle(

        #     40, 60,

        #     20,80

        # ),

        # TEAM 2

        add_rectangle(

            92, 95,
            5, 10

        ),

        add_rectangle(

            83, 90,

            20, 30

        ),

        add_rectangle(

            85, 88,

            50, 70

        ),

        add_rectangle(

            73, 80,

            30, 52

        ),

        add_rectangle(

            73, 80,

            70, 92
        ),

        add_rectangle(

            67, 70,

            15, 35

        ),

        add_rectangle(200 - 95 - 50, 200 - 92 - 50, 200 - 10 - 50, 200 - 5 - 50),  # Transformed obstacle 1
        add_rectangle(200 - 92 - 50, 200 - 95 - 50, 200 - 20 - 50, 200 - 30 - 50),  # Transformed obstacle 2
        add_rectangle(200 - 88 - 50, 200 - 85 - 50, 200 - 70 - 50, 200 - 50 - 50),  # Transformed obstacle 3
        add_rectangle(200 - 80 - 50, 200 - 73 - 50, 200 - 52 - 50, 200 - 30 - 50),  # Transformed obstacle 4
        add_rectangle(200 - 80 - 50, 200 - 73 - 50, 200 - 92 - 50, 200 - 70 - 50),  # Transformed obstacle 5
        add_rectangle(200 - 70 - 50, 200 - 67 - 50, 200 - 35 - 50, 200 - 15 - 50),  # Transformed obstacle 6
        add_rectangle(200 - 48 - 50, 200 - 45 - 50, 200 - 10 - 50, 200 - 5 - 50),  # Transformed obstacle 7
        add_rectangle(200 - 123 - 50, 200 - 111 - 50, 200 - 93 - 50, 200 - 91 - 50),  # Transformed obstacle 8
        add_rectangle(200 - 37 - 50, 200 - 30 - 50, 200 - 30 - 50, 200 - 20 - 50),  # Transformed obstacle 9
        add_rectangle(200 - 35 - 50, 200 - 32 - 50, 200 - 70 - 50, 200 - 50 - 50),  # Transformed obstacle 10
        add_rectangle(200 - 47 - 50, 200 - 50 - 50, 200 - 52 - 50, 200 - 30 - 50),  # Transformed obstacle 11
        add_rectangle(200 - 47 - 50, 200 - 50 - 50, 200 - 92 - 50, 200 - 70 - 50),  # Transformed obstacle 12
        add_rectangle(200 - 43 - 50, 200 - 40 - 50, 200 - 35 - 50, 200 - 15 - 50)  # Transformed obstacle 13

    ]

    visuals = [

        add_rectangle(

            40, 60,

            20, 80

        ),

    ]
