import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pygame
import sys
import play
import settings
from play import run_game
from settings import handle_settings_events
from helper import resource_path
from sounds import init_sounds, toggle_music, play_sound_effect
from config import VERSION

pygame.init()
init_sounds()

WIDTH, HEIGHT = 800, 600
angle = 15
padding = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)
pygame.display.set_caption('Flappy Game')

BG = pygame.image.load(resource_path('assets/image/background.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
FONT = pygame.font.Font(resource_path("assets/font/font.ttf"), 64)
character_model = pygame.image.load(resource_path('assets/image/bird.png')).convert_alpha()

play_btn_img = pygame.image.load(resource_path('assets/image/Play.png')).convert_alpha()
exit_btn_img = pygame.image.load(resource_path('assets/image/Exit.png')).convert_alpha()
setting_btn_img = pygame.image.load(resource_path('assets/image/Setting.png')).convert_alpha()

play_btn_img = pygame.transform.scale(play_btn_img, (140, 55))
exit_btn_img = pygame.transform.scale(exit_btn_img, (140, 55))
setting_btn_img = pygame.transform.scale(setting_btn_img, (50, 50))

character_model = pygame.transform.scale(character_model, (90, 60))
character_model_rotated = pygame.transform.rotate(character_model, angle)
character_model_rect = character_model_rotated.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 160))

play_btn_rect = play_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
exit_btn_rect = exit_btn_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))
setting_btn_rect = setting_btn_img.get_rect(bottomleft=(padding, HEIGHT - padding))

bg_x = 0

def draw_menu():
    global bg_x

    bg_speed = 0.5
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    SCREEN.blit(BG, (bg_x, 0))
    SCREEN.blit(BG, (bg_x + WIDTH, 0))

    SCREEN.blit(character_model_rotated, character_model_rect)
    title_text = FONT.render("Flappy Game", True, (255, 255, 255))
    SCREEN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    SCREEN.blit(play_btn_img, play_btn_rect)
    SCREEN.blit(exit_btn_img, exit_btn_rect)
    SCREEN.blit(setting_btn_img, setting_btn_rect)

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
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(60)
    return state

def main_loop():
    state = {"current": "menu"}
    while True:
        if state["current"] == "menu":
            state = main_menu(state)
        elif state["current"] == "playing":
            state = run_game(state)
        elif state["current"] == "settings":
            state = handle_settings_events(state)
        elif state["current"] == "gameover":
            state["current"] = "menu"
        else:
            state["current"] = "menu"

main_loop()