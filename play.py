from game_logic import check_collision, update_score, get_pipe_gap, update_game_speed
import pygame
import sys
import random
import os

from saves import get_high_score, save_high_score, get_character
from helper import resource_path, character_images
from sounds import play_flap_sound, play_death_sound, play_gameover_sound
from config import VERSION, WIDTH, HEIGHT

pygame.init()

os.environ["SDL_RENDER_DRIVER"] = "software"
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption('Flappy Game - Play')

BG = pygame.image.load(resource_path('assets/image/background.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

font = pygame.font.Font(resource_path('assets/font/font.ttf'), 48)
fontTxt = pygame.font.Font(resource_path('assets/font/font.ttf'), 25)

bird_img = pygame.transform.scale(character_images[get_character()], (70, 50))
bird_rect = bird_img.get_rect(center=(150, HEIGHT // 2))
bird_vel = 0
gravity = 0.5
flap_strength = -10

pipe_width = 80
pipe_height = 500

pipe_top_img = pygame.image.load(resource_path("assets/image/Top.png")).convert_alpha()
pipe_top_img = pygame.transform.scale(pipe_top_img, (pipe_width, pipe_height))

pipe_bottom_img = pygame.image.load(resource_path("assets/image/Bottom.png")).convert_alpha()
pipe_bottom_img = pygame.transform.scale(pipe_bottom_img, (90, pipe_height))

pipe_gap = 300
pipe_speed = 4
scroll_speed = 2
pipe_frequency = 1600

chain1 = pygame.image.load(resource_path("assets/image/chain.png")).convert_alpha()
chain1 = pygame.transform.scale(chain1, (50, 90))
chain1_rect = chain1.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 - 275))

chain2 = pygame.image.load(resource_path("assets/image/chain.png")).convert_alpha()
chain2 = pygame.transform.scale(chain2, (50, 90))
chain2_rect = chain2.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 - 275))

retry_img = pygame.image.load(resource_path("assets/image/retry.png")).convert_alpha()
retry_img = pygame.transform.scale(retry_img, (130, 60))
retry_img_rect = retry_img.get_rect(center=(WIDTH // 2 + 80, HEIGHT // 2 + 240))

menu_img = pygame.image.load(resource_path("assets/image/Menu.png")).convert_alpha()
menu_img = pygame.transform.scale(menu_img, (130, 60))
menu_img_rect = menu_img.get_rect(center=(WIDTH // 2 - 80, HEIGHT // 2 + 240))

retry_label = fontTxt.render("Retry Button", True, (0, 0, 0))
menu_label = fontTxt.render("Menu Button", True, (0, 0, 0))

retry_label_rect = retry_label.get_rect(center=(retry_img_rect.centerx, retry_img_rect.top + 73))
menu_label_rect = menu_label.get_rect(center=(menu_img_rect.centerx, menu_img_rect.top + 73))

gameover_platform_img = pygame.image.load(resource_path("assets/image/gameoverPlat.png")).convert_alpha()
platfrom_width = int(WIDTH * 0.6)
platform_height = int(platfrom_width * (gameover_platform_img.get_height() / gameover_platform_img.get_width()))
gameover_platform_img = pygame.transform.scale(gameover_platform_img, (platfrom_width - 130, platform_height - 250))
gameover_platform_rect = gameover_platform_img.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 30))

pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

bg_x1 = 0
bg_x2 = WIDTH

clock = pygame.time.Clock()

def create_pipe(score=0):
    margin = 50
    current_gap = get_pipe_gap(score)
    center_y =random.randint(pipe_gap // 2 + margin, HEIGHT - pipe_gap // 2 - margin)
    top_pipe = pipe_top_img.get_rect(
        midbottom=(WIDTH + 100, center_y - current_gap // 2)
    )
    bottom_pipe = pipe_bottom_img.get_rect(
        midtop=(WIDTH + 100, center_y + current_gap // 2)
    )
    return {"top": top_pipe, "bottom": bottom_pipe, "scored": False}

def move_pipes(tubo):
    new_pipes = []
    for pipe in tubo:
        pipe["top"].centerx -= pipe_speed
        pipe["bottom"].centerx -= pipe_speed
        if pipe["top"].right > -pipe_width:
            new_pipes.append(pipe)
    return new_pipes


def draw_pipes(tubo):
    for pipe in tubo:
        SCREEN.blit(pipe_top_img, pipe["top"])
        SCREEN.blit(pipe_bottom_img, pipe["bottom"])

def reset_game():
    global bird_rect, bird_vel, pipes, bg_x1, bg_x2
    bird_rect = bird_img.get_rect(center=(150, HEIGHT // 2))
    bird_vel = 0
    pipes = []
    bg_x1 = 0
    bg_x2 = WIDTH
    pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

def draw_gameover(score):
    SCREEN.blit(chain1, chain1_rect)
    SCREEN.blit(chain2, chain2_rect)
    SCREEN.blit(gameover_platform_img, gameover_platform_rect)

    text_x = gameover_platform_rect.centerx
    text_y = gameover_platform_rect.top + 30
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    text_rect = game_over_text.get_rect(center=(text_x, text_y))
    SCREEN.blit(game_over_text, text_rect)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {get_high_score()}", True, (0, 0, 0))

    score_rect = score_text.get_rect(center=(gameover_platform_rect.centerx, gameover_platform_rect.top + 90))
    high_score_rect = high_score_text.get_rect(center=(gameover_platform_rect.centerx, gameover_platform_rect.top + 135))

    retry_text = fontTxt.render("'R' or Retry Button - Retry", True, (0, 0, 0))
    menu_text = fontTxt.render("'M' or Menu Button - Menu", True, (0, 0, 0))
    quit_text = fontTxt.render("'Q' - Quit (PC only)", True, (0, 0, 0))

    retry_rect = retry_text.get_rect(center=(gameover_platform_rect.centerx, gameover_platform_rect.top + 180))
    menu_rect = menu_text.get_rect(center=(gameover_platform_rect.centerx, gameover_platform_rect.top + 220))
    quit_rect = quit_text.get_rect(center=(gameover_platform_rect.centerx - 35, gameover_platform_rect.top + 260))

    SCREEN.blit(score_text, score_rect)
    SCREEN.blit(high_score_text, high_score_rect)

    SCREEN.blit(retry_img, retry_img_rect)
    SCREEN.blit(menu_img, menu_img_rect)

    SCREEN.blit(retry_label, retry_label_rect)
    SCREEN.blit(menu_label, menu_label_rect)

    SCREEN.blit(retry_text, retry_rect)
    SCREEN.blit(menu_text, menu_rect)
    SCREEN.blit(quit_text, quit_rect)

def draw_background():
    SCREEN.blit(BG, (bg_x1, 0))
    SCREEN.blit(BG, (bg_x2, 0))

def draw_version():
    transparent_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 150))

    version_text = font.render(VERSION, True, (255, 255, 255))
    transparent_surface.blit(version_text, (version_text.get_width() - 25, 0))
    SCREEN.blit(transparent_surface, (WIDTH - transparent_surface.get_width() - 20, 20))

def rotate_bird(bird_rect):
    angle = max(-30, min(30, -bird_vel * 3))
    old_center = bird_rect.center
    bird_img = pygame.transform.scale(character_images[get_character()], (70, 50))
    bird_rect = bird_img.get_rect(center=(old_center))
    rotated_bird = pygame.transform.rotozoom(bird_img, angle, 1)
    rotated_bird_rect = rotated_bird.get_rect(center=bird_rect.center)
    SCREEN.blit(rotated_bird, rotated_bird_rect)

def calculate_chain_offsets():
    chain1_offset = chain1_rect.y - gameover_platform_rect.y
    chain2_offset = chain2_rect.y - gameover_platform_rect.y
    return chain1_offset, chain2_offset

def run_game(state):
    """
    Runs the main game loop.

    The state dictionary should contain a key "current" which is initially "playing".
    This function handles the countdown timer, game events, update of physics, drawing, and the game over events.

    Transition option in game over:
        - Press R or SPACE to restart and continue the playing.
        - Press M to return to the main menu.
        - Press Q to quit.

    Returns the updated state dictionary.
    """
    global bird_vel, pipes, bg_x1, bg_x2
    global pipe_speed, scroll_speed, pipe_frequency

    reset_game()

    countdown_font = pygame.font.Font(resource_path("assets/font/font.ttf"), 64)
    countdown = 3
    countdown_start = pygame.time.get_ticks()

    gameover_y = -platform_height
    fall_speed = 10
    gameover_anim_done = False

    chain1_offset, chain2_offset = calculate_chain_offsets()

    while countdown > 0:
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - countdown_start) / 1000
        countdown = 3 - int(elapsed)

        draw_background()

        countdown_text = countdown_font.render(str(max(countdown, 0)), True, (255, 255, 255))
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(countdown_text, text_rect)
        pygame.display.flip()

    pygame.event.clear(SPAWNPIPE)
    game_over = False
    score = 0
    paused = False
    jump_resumed = False

    while state["current"] == "playing":
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = not paused
                    jump_resumed = paused

                if paused and event.key == pygame.K_SPACE:
                    paused = False
                    jump_resumed = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over:
                    if retry_img_rect.collidepoint(event.pos):
                        reset_game()
                        game_over = False
                        score = 0
                        pygame.mixer.music.play(-1)

                        gameover_y = -platform_height
                        gameover_anim_done = False

                    elif menu_img_rect.collidepoint(event.pos):
                        state["current"] = "menu"
                        return state

            if not game_over and not paused:
                    if event.type == pygame.KEYDOWN and not jump_resumed and event.key == pygame.K_SPACE:
                        bird_vel = flap_strength
                        play_flap_sound()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bird_vel = flap_strength
                        play_flap_sound()

                    if event.type == SPAWNPIPE:
                        pipes.append(create_pipe(score))
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_r, pygame.K_SPACE):
                        reset_game()
                        game_over = False
                        score = 0
                        pygame.mixer.music.play(-1)
                        gameover_y = -platform_height
                        gameover_anim_done = False
                    elif event.key == pygame.K_m:
                        state["current"] = "menu"
                        return state
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if not game_over and not paused:
            jump_resumed = False
            pipe_speed, scroll_speed, pipe_frequency = update_game_speed(score, pipe_frequency, SPAWNPIPE)
            bg_x1 -= scroll_speed
            bg_x2 -= scroll_speed
            if bg_x1 <= -WIDTH:
                bg_x1 = WIDTH
            if bg_x2 <= -WIDTH:
                    bg_x2 = WIDTH

            bird_vel += gravity
            bird_rect.centery += bird_vel

            pipes = move_pipes(pipes)
            score = update_score(bird_rect, pipes, score)

            if check_collision(bird_rect, pipes):
                if score >= 30 or (get_high_score() - score) <= 5:
                    pygame.mixer.music.stop()
                    play_death_sound()
                    play_gameover_sound()
                else:
                    play_death_sound()
                print("Collision detected!")
                save_high_score(score)
                pygame.time.delay(1500)

                game_over = True
                gameover_y = -platform_height
                gameover_anim_done = False

        draw_background()
        draw_pipes(pipes)
        draw_version()
        rotate_bird(bird_rect)

        score_surface = font.render(f"Score: {score} ", True, (255, 255, 255))
        SCREEN.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        if paused:
            pause_text = font.render("PAUSED - Press P or SPACE to Resume", True, (255, 255, 255))
            SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width(), HEIGHT // 2))

        current_high = get_high_score()
        high_score_surface = font.render(f"High Score: {current_high} ", True, (255, 255, 0))
        SCREEN.blit(high_score_surface, (10, 10))

        if game_over:
            if not gameover_anim_done:
                while gameover_y < gameover_platform_rect.y:
                    clock.tick(60)
                    gameover_y += fall_speed
                    draw_background()
                    draw_pipes(pipes)
                    draw_version()
                    rotate_bird(bird_rect)

                    current_chain1_y = gameover_y + chain1_offset
                    current_chain2_y = gameover_y + chain2_offset

                    SCREEN.blit(chain1, (chain1_rect.x, current_chain1_y))
                    SCREEN.blit(chain2, (chain2_rect.x, current_chain2_y))

                    SCREEN.blit(gameover_platform_img, (gameover_platform_rect.x, gameover_y))
                    pygame.display.flip()

                gameover_anim_done = True

            draw_gameover(score)

            pygame.event.clear()

        pygame.display.flip()

    return state