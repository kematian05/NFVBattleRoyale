import os
import sys

# sys.path.insert(1, '../res/values')
# sys.path.insert(1, '../data')
import pygame
from game_launcher import launch_game
from config import DisplayConfig
from theme import ColorPalette

def main_menu():
    # Initialize Pygame
    pygame.init()
    # Display settings
    window = pygame.display.set_mode((DisplayConfig.width, DisplayConfig.height))
    pygame.display.set_caption("Enter Name to Play")

    # Font settings
    font = pygame.font.Font(None, 50)
    input_box_font = pygame.font.Font(None, 36)

    # Input box settings
    input_box = pygame.Rect(DisplayConfig.width // 2 - 100, DisplayConfig.height // 2 - 25, 200, 50)
    player_id = ""
    start_button = pygame.Rect(DisplayConfig.width // 2 - 75, DisplayConfig.height // 2 + 50, 150, 50)

    # Load weapon images
    script_dir = os.path.dirname(__file__)
    pistol_image_path = "weapon_images/pistol.png"
    sniper_image_path = "weapon_images/sniper.png"
    shotgun_image_path = "weapon_images/shotgun.png"
    pistol_image_path = os.path.join(script_dir, pistol_image_path)
    sniper_image_path = os.path.join(script_dir, sniper_image_path)
    shotgun_image_path = os.path.join(script_dir, shotgun_image_path)
    pistol_image = pygame.image.load(pistol_image_path)
    sniper_image = pygame.image.load(sniper_image_path)
    shotgun_image = pygame.image.load(shotgun_image_path)

    # Resize images to fit in the menu
    weapon_size = (80, 80)
    pistol_image = pygame.transform.scale(pistol_image, weapon_size)
    sniper_image = pygame.transform.scale(sniper_image, weapon_size)
    shotgun_image = pygame.transform.scale(shotgun_image, weapon_size)

    # Weapon image positions
    pistol_rect = pygame.Rect(DisplayConfig.width // 2 - 235, DisplayConfig.height // 2 + 150, 80, 80)
    sniper_rect = pygame.Rect(DisplayConfig.width // 2 - 30, DisplayConfig.height // 2 + 150, 80, 80)
    shotgun_rect = pygame.Rect(DisplayConfig.width // 2 + 175, DisplayConfig.height // 2 + 150, 80, 80)

    # Selection tracking
    selected_weapon = "pistol"

    # Main menu loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return player_id, selected_weapon

                elif event.key == pygame.K_BACKSPACE:
                    player_id = player_id[:-1]

                else:
                    player_id += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return player_id, selected_weapon
                elif pistol_rect.collidepoint(event.pos):
                    selected_weapon = "pistol"
                elif sniper_rect.collidepoint(event.pos):
                    selected_weapon = "sniper"
                elif shotgun_rect.collidepoint(event.pos):
                    selected_weapon = "shotgun"

        # Draw the menu screen
        window.fill(ColorPalette.WHITE)

        # Draw instructions
        instruction_text = font.render("Enter Your Name", True, ColorPalette.BLACK)
        window.blit(instruction_text, (DisplayConfig.width // 2 - instruction_text.get_width() // 2, DisplayConfig.height // 2 - 100))

        # Draw input box
        pygame.draw.rect(window, ColorPalette.BLACK, input_box, 2)
        name_surface = input_box_font.render(player_id, True, ColorPalette.BLACK)
        window.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Draw start button
        pygame.draw.rect(window, ColorPalette.BLACK, start_button)
        start_text = font.render("Start", True, ColorPalette.WHITE)
        window.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + 5))

        # Draw weapon images and highlight the selected one
        if selected_weapon == "pistol":
            pygame.draw.rect(window, ColorPalette.YELLOW, pistol_rect.inflate(10, 10), 4)
        elif selected_weapon == "sniper":
            pygame.draw.rect(window, ColorPalette.YELLOW, sniper_rect.inflate(10, 10), 4)
        elif selected_weapon == "shotgun":
            pygame.draw.rect(window, ColorPalette.YELLOW, shotgun_rect.inflate(10, 10), 4)

        window.blit(pistol_image, pistol_rect)
        window.blit(sniper_image, sniper_rect)
        window.blit(shotgun_image, shotgun_rect)

        # Draw weapon labels
        pistol_label = font.render("Pistol", True, ColorPalette.BLACK)
        sniper_label = font.render("Sniper", True, ColorPalette.BLACK)
        shotgun_label = font.render("Shotgun", True, ColorPalette.BLACK)
        window.blit(pistol_label, (pistol_rect.centerx - pistol_label.get_width() // 2, pistol_rect.bottom + 10))
        window.blit(sniper_label, (sniper_rect.centerx - sniper_label.get_width() // 2 , sniper_rect.bottom + 10))
        window.blit(shotgun_label, (shotgun_rect.centerx - shotgun_label.get_width() // 2, shotgun_rect.bottom + 10))


        pygame.display.flip()

if __name__ == '__main__':
    while True:
        player_id, selected_weapon = main_menu()
        if not player_id:
            pass
        else:
            launch_game(player_id, selected_weapon)
            print("Back to main menu!")