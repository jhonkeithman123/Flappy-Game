import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
import pygame
import sys
from saves import reset_save_directory_config, get_user_save_directory, get_character, load_settings
from shop import character_shop
from play import run_game
from settings import handle_settings_events
from helper import resource_path, character_images
from sounds import init_sounds
from config import VERSION, WIDTH, HEIGHT
from ui import handle_account

pygame.init()
init_sounds()

save_directory = get_user_save_directory()
settings = load_settings(save_directory)

is_muted = settings.get("is_muted", False)
volume = settings.get("music_volume", 0.5)

if is_muted:
    pygame.mixer.music.set_volume(0)
else:
    pygame.mixer.music.set_volume(volume)

angle = 15
padding = 20
os.environ["SDL_RENDER_DRIVER"] = "software"
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('Flappy Game')

BG = pygame.image.load(resource_path('assets/image/background.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

FONT = pygame.font.Font(resource_path("assets/font/font.ttf"), 64)
font = pygame.font.Font(resource_path("assets/font/font.ttf"), 30)

play_btn_img = pygame.image.load(resource_path('assets/image/Play.png')).convert_alpha()
exit_btn_img = pygame.image.load(resource_path('assets/image/Exit.png')).convert_alpha()
setting_btn_img = pygame.image.load(resource_path('assets/image/Setting.png')).convert_alpha()

shop_img = pygame.image.load(resource_path('assets/image/shop.png')).convert_alpha()
shop_img = pygame.transform.scale(shop_img, (50, 50))
shop_rect = shop_img.get_rect(center=(WIDTH / 2 + 355, HEIGHT / 2))

play_btn_img = pygame.transform.scale(play_btn_img, (140, 55))
exit_btn_img = pygame.transform.scale(exit_btn_img, (140, 55))
setting_btn_img = pygame.transform.scale(setting_btn_img, (50, 50))

character_image = pygame.transform.scale(character_images[get_character()], (80, 60))
character_model_rotated = pygame.transform.rotate(character_image, angle)
character_model_rect = character_model_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 145))

play_btn_rect = play_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
exit_btn_rect = exit_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))
setting_btn_rect = setting_btn_img.get_rect(bottomleft=(padding, HEIGHT - padding))

account = pygame.image.load(resource_path('assets/image/account.png')).convert_alpha()
account = pygame.transform.scale(account, (50, 50))
account_rect = account.get_rect(center=(exit_btn_rect.right + 285, exit_btn_rect.top + 120))

bg_x = 0

def draw_menu():
    global bg_x

    bg_speed = 0.5
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    shop_text = font.render("Shop", True, (0, 0, 128))
    shop_text_rect = shop_text.get_rect(center=(shop_rect.centerx, shop_rect.top - 20))

    setting_text = font.render("Settings", True, (0, 0, 128))
    settings_rect = setting_text.get_rect(center=(setting_btn_rect.centerx + 5, setting_btn_rect.top - 20))

    account_text = font.render("Account", True, (0, 0, 128))
    account_text_rect = account_text.get_rect(center=(account_rect.centerx - 2, account_rect.top - 20))

    SCREEN.blit(BG, (bg_x, 0))
    SCREEN.blit(BG, (bg_x + WIDTH, 0))

    character_image = pygame.transform.scale(character_images[get_character()], (80, 60))
    character_model_rotated = pygame.transform.rotate(character_image, angle)
    character_model_rect = character_model_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 145))
    SCREEN.blit(character_model_rotated, character_model_rect)

    title_text = FONT.render("Flappy Game", True, (255, 255, 255))
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

    SCREEN.blit(play_btn_img, play_btn_rect)
    SCREEN.blit(exit_btn_img, exit_btn_rect)
    SCREEN.blit(setting_btn_img, setting_btn_rect)
    SCREEN.blit(shop_img, shop_rect)
    SCREEN.blit(shop_text, shop_text_rect)
    SCREEN.blit(setting_text, settings_rect)
    SCREEN.blit(account, account_rect)
    SCREEN.blit(account_text, account_text_rect)

    version_text = FONT.render(VERSION, True, (255, 255, 255))
    SCREEN.blit(version_text, (WIDTH - version_text.get_width() - 20, 20))

    pygame.display.flip()

def main_menu(state):
    """
        Displays the main menu and updates the state based on user input.

        The state dictionary should use the key "current" to determine which screen is active.
        This function will return when the player chooses to change to "playing" or "settings".
    """
    clock = pygame.time.Clock()
    while state["current"] == "menu":
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if play_btn_rect.collidepoint(mouse_pos):
                    state["current"] = "playing"
                    return state
                elif setting_btn_rect.collidepoint(mouse_pos):
                    state["current"] = "settings"
                    return state
                elif shop_rect.collidepoint(mouse_pos):
                    state["current"] = "shop"
                elif account_rect.collidepoint(mouse_pos):
                    state["current"] = "account"
                elif exit_btn_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state["current"] = "playing"
                    return state
                elif event.key == pygame.K_s:
                    state["current"] = "settings"
                    return state
                elif event.key == pygame.K_e:
                    state["current"] = "shop"
                elif event.key == pygame.K_a:
                    state["current"] = "account"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
    return state

if __name__ == "__main__":
    user_save_directory = get_user_save_directory()
    # reset_save_directory_config()
    state = {"current": "menu"}
    while True:
        if state["current"] == "menu":
            state = main_menu(state)
        elif state["current"] == "playing":
            state = run_game(state)
        elif state["current"] == "settings":
            state = handle_settings_events(state, save_directory=user_save_directory)
        elif state["current"] == "gameover":
            state["current"] = "menu"
        elif state["current"] == "shop":
            state = character_shop(state)
        elif state["current"] == "account":
            state["current"] = handle_account(state)
        else:
            state["current"] = "menu"
