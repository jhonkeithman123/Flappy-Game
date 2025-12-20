import os
import pygame
import sys
from typing import Dict

# Forcing SDL to use software and avoid problematic GLX paths
os.environ["SDL_RENDER_DRIVER"] = "software"
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"
os.environ.setdefault("SDL_VIDEODRIVER", "x11") # defaults to "x11" or "wayland" 

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from saves import get_user_save_directory, get_character, load_settings
from shop import character_shop
from play import run_game
from settings import handle_settings_events
from helper import resource_path, character_images
from sounds import init_sounds
import config
from config import VERSION
from ui import handle_account, handle_login_page, handle_signup_page
from window_manager import init_window, handle_resize

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

screen = init_window()
pygame.display.set_caption('Flappy Game')
BG = pygame.image.load(resource_path('assets/image/background.png')).convert()

# Initialize global surfaces, fonts, and rects with safe defaults so they are always bound.
BGround = pygame.Surface((config.WIDTH, config.HEIGHT))
font = pygame.font.Font(resource_path("assets/font/font.ttf"), 30)

play_btn_img = pygame.Surface((140, 55), pygame.SRCALPHA)
exit_btn_img = pygame.Surface((140, 55), pygame.SRCALPHA)
setting_btn_img = pygame.Surface((50, 50), pygame.SRCALPHA)
shop_img = pygame.Surface((50, 50), pygame.SRCALPHA)
account = pygame.Surface((50, 50), pygame.SRCALPHA)

shop_rect = play_btn_img.get_rect()
play_btn_rect = play_btn_img.get_rect()
exit_btn_rect = exit_btn_img.get_rect()
setting_btn_rect = setting_btn_img.get_rect()
account_rect = account.get_rect()

character_image = pygame.Surface((80, 60), pygame.SRCALPHA)
character_model_rotated = character_image
character_model_rect = character_model_rotated.get_rect()

# UI scale helpers
BASE_W, BASE_H = 1280, 720

def _clamp(val: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, val))

def _scaled(px: float, scale: float, lo: int, hi: int) -> int:
    """Scale px by scale and clamp to [lo, hi] pixels."""
    return int(_clamp(px * scale, lo, hi))

ui_scale: float = 1.0
safe_margin: int = 16
# Copy of unrotated bird
_character_image_base = character_image

# Compute max UI scale cao from desktop size (fallback to 1080p)
info = pygame.display.Info()
desktop_w, desktop_h = info.current_w, info.current_h
from config import MAX_WIDTH_CAP, MAX_HEIGHT_CAP
max_w_cap = min(desktop_w or MAX_WIDTH_CAP, MAX_WIDTH_CAP)
max_h_cap = min(desktop_h or MAX_HEIGHT_CAP, MAX_HEIGHT_CAP)
MAX_UI_SCALE = min(max_w_cap / BASE_W, max_h_cap / BASE_H)

def rebuild_layout() -> None:
    global BGround, FONT, font, ui_scale, safe_margin
    global play_btn_img, exit_btn_img, setting_btn_img, shop_img, shop_rect
    global play_btn_rect, exit_btn_rect, setting_btn_rect, account_rect, account
    global character_model_rect, character_model_rotated, _character_image_base

    # Aspect-aware UI scale capped to 1080p equivalent
    ui_scale = _clamp(min(config.WIDTH / BASE_W, config.HEIGHT / BASE_H), 0.6, MAX_UI_SCALE)
    safe_margin = _scaled(20, ui_scale, 10, 36)

    # Bird (unrotated base scaled; rotated each frame)
    bird_w = _scaled(96, ui_scale, 56, 180)
    bird_h = _scaled(72, ui_scale, 42, 140)
    _character_image_base = pygame.transform.scale(character_images[get_character()], (bird_w, bird_h))

    # Background and fonts
    BGround = pygame.transform.scale(BG, (config.WIDTH, config.HEIGHT))
    FONT = pygame.font.Font(resource_path("assets/font/font.ttf"), _scaled(56, ui_scale, 28, 80))
    font = pygame.font.Font(resource_path("assets/font/font.ttf"), _scaled(24, ui_scale, 14, 36))

    # Load images
    play_btn_img_local = pygame.image.load(resource_path("assets/image/Play.png")).convert_alpha()
    exit_btn_img_local = pygame.image.load(resource_path("assets/image/Exit.png")).convert_alpha()
    setting_btn_img_local = pygame.image.load(resource_path("assets/image/Setting.png")).convert_alpha()
    shop_img_local = pygame.image.load(resource_path("assets/image/shop.png")).convert_alpha()
    account_local = pygame.image.load(resource_path("assets/image/account.png")).convert_alpha()

    # Scale assets with clamps
    play_btn_img_local = pygame.transform.scale(
        play_btn_img_local, (_scaled(200, ui_scale, 120, 320), _scaled(70, ui_scale, 40, 120))
    )
    exit_btn_img_local = pygame.transform.scale(
        exit_btn_img_local, (_scaled(200, ui_scale, 120, 320), _scaled(70, ui_scale, 40, 120))
    )
    icon_w = _scaled(56, ui_scale, 32, 96)
    icon_h = _scaled(56, ui_scale, 32, 96)
    setting_btn_img_local = pygame.transform.scale(setting_btn_img_local, (icon_w, icon_h))
    shop_img_local = pygame.transform.scale(shop_img_local, (icon_w, icon_h))
    account_local = pygame.transform.scale(account_local, (icon_w, icon_h))

    globals().update(
        play_btn_img=play_btn_img_local,
        exit_btn_img=exit_btn_img_local,
        setting_btn_img=setting_btn_img_local,
        shop_img=shop_img_local,
        account=account_local,
    )

    # Anchors
    globals().update(
        setting_btn_rect=setting_btn_img_local.get_rect(
            bottomleft=(safe_margin, config.HEIGHT - safe_margin)
        ),
        shop_rect=shop_img_local.get_rect(
            midright=(config.WIDTH - safe_margin, config.HEIGHT // 2)
        ),
        account_rect=account_local.get_rect(
            bottomright=(config.WIDTH - safe_margin, config.HEIGHT - safe_margin)
        ),
        play_btn_rect=play_btn_img_local.get_rect(
            center=(config.WIDTH // 2, int(config.HEIGHT * 0.58))
        ),
        exit_btn_rect=exit_btn_img_local.get_rect(
            center=(config.WIDTH // 2, int(config.HEIGHT * 0.68))
        ),
    )

rebuild_layout()

bg_x = 0

def draw_menu():
    global bg_x, character_model_rotated, character_model_rect

    # Parallax background scroll
    bg_speed = 60 * ui_scale / 120.0
    bg_x -= bg_speed
    if bg_x <= -config.WIDTH:
        bg_x = 0

    screen.blit(BGround, (bg_x, 0))
    screen.blit(BGround, (bg_x + config.WIDTH, 0))

    # Title
    title_text = FONT.render("Flappy Game", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(config.WIDTH // 2, int(config.HEIGHT * 0.18)))
    screen.blit(title_text, title_rect)

    # Bird nesting above title
    nest_gap = _scaled(2, ui_scale, 0, 8)
    character_model_rotated = pygame.transform.rotate(_character_image_base, angle)
    character_model_rect = character_model_rotated.get_rect(
        midbottom=(title_rect.centerx, title_rect.top - nest_gap)
    )
    screen.blit(character_model_rotated, character_model_rect)

    # Buttons
    screen.blit(play_btn_img, play_btn_rect)
    screen.blit(exit_btn_img, exit_btn_rect)

    # Icons
    screen.blit(setting_btn_img, setting_btn_rect)
    screen.blit(shop_img, shop_rect)
    screen.blit(account, account_rect)

    # Labels ABOVE icons
    label_gap = _scaled(8, ui_scale, 4, 16)
    label_col = (0, 0, 128)

    setting_text = font.render("Settings", True, label_col)
    screen.blit(setting_text, setting_text.get_rect(midbottom=(setting_btn_rect.centerx, setting_btn_rect.top - label_gap)))

    shop_text = font.render("Shop", True, label_col)
    screen.blit(shop_text, shop_text.get_rect(midbottom=(shop_rect.centerx, shop_rect.top - label_gap)))

    account_text = font.render("Account", True, label_col)
    screen.blit(account_text, account_text.get_rect(midbottom=(account_rect.centerx, account_rect.top - label_gap)))

    # Version
    version_text = FONT.render(VERSION, True, (255, 255, 255))
    screen.blit(version_text, (config.WIDTH - version_text.get_width() - safe_margin, safe_margin))

    pygame.display.flip()

def main_menu(state: Dict[str, str]) -> Dict[str, str]:
    global screen
    clock = pygame.time.Clock()
    
    while state["current"] == "menu":
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type in (pygame.VIDEORESIZE, getattr(pygame, "WINDOWSIZE_CHANGED", 0)):
                size = getattr(event, "size", pygame.display.get_window_size())
                screen = handle_resize(size, rebuild_layout)
                continue
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if play_btn_rect.collidepoint(mouse_pos):
                    state["current"] = "playing"; return state
                elif setting_btn_rect.collidepoint(mouse_pos):
                    state["current"] = "settings"; return state
                elif shop_rect.collidepoint(mouse_pos):
                    state["current"] = "shop"
                elif account_rect.collidepoint(mouse_pos):
                    state["current"] = "account"
                elif exit_btn_rect.collidepoint(mouse_pos):
                    pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state["current"] = "playing"; return state
                elif event.key == pygame.K_s:
                    state["current"] = "settings"; return state
                elif event.key == pygame.K_e:
                    state["current"] = "shop"
                elif event.key == pygame.K_a:
                    state["current"] = "account"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
        clock.tick(60)
    return state

if __name__ == "__main__":
    user_save_directory = get_user_save_directory()
    # reset_save_directory_config()
    state: Dict[str, str] = {"current": "menu"}
    while True:
        if state["current"] == "menu":
            state = main_menu(state)
        elif state["current"] == "playing":
            state = run_game(state)
        elif state["current"] == "settings":
            state = handle_settings_events(state, save_directory=str(user_save_directory))
        elif state["current"] == "gameover":
            state["current"] = "menu"
        elif state["current"] == "shop":
            state = character_shop(state)
        elif state["current"] == "account":
            state = handle_account(state)
        elif state["current"] == "login":
            state = handle_login_page(state)
        elif state["current"] == "signup":
            state = handle_signup_page(state)
        else:
            state["current"] = "menu"
