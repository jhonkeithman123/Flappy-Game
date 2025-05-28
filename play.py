from game_logic import check_collision, update_score, get_pipe_gap, update_game_speed
import pygame
import sys
import random
from saves import get_high_score, save_high_score
from helper import resource_path
from sounds import play_flap_sound, play_death_sound

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF, vsync=True)
pygame.display.set_caption('Flappy Game - Play')

BG = pygame.image.load(resource_path('assets/image/background.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

font = pygame.font.Font(resource_path('assets/font/font.ttf'), 48)

bird_img = pygame.image.load(resource_path("assets/image/bird.png")).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (70, 50))
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

def move_pipes(pipes):
    new_pipes = []
    for pipe in pipes:
        pipe["top"].centerx -= pipe_speed
        pipe["bottom"].centerx -= pipe_speed
        if pipe["top"].right > -pipe_width:
            new_pipes.append(pipe)
    return new_pipes


def draw_pipes(pipes):
    for pipe in pipes:
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

def draw_gameover():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    SCREEN.blit(overlay, (0, 0))

    game_over_text = font.render("Game Over", True, (255, 0, 0))
    retry_text = font.render("Press R or SPACE to Retry, Q to Quit, M for Menu", True, (255, 255, 255))

    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))
    SCREEN.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))

def draw_background():
    SCREEN.blit(BG, (bg_x1, 0))
    SCREEN.blit(BG, (bg_x2, 0))

def rotate_bird():
    angle = max(-30, min(30, -bird_vel * 3))
    rotated_bird = pygame.transform.rotozoom(bird_img, angle, 1)
    rotated_bird_rect = rotated_bird.get_rect(center=bird_rect.center)
    SCREEN.blit(rotated_bird, rotated_bird_rect)

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
                    elif event.key == pygame.K_m:
                        state["current"] = "menu"
                        return state
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        if not game_over and not paused:
            jump_resumed = False
            pipe_speed, scroll_speed, pipe_frequency = update_game_speed(score, pipe_speed, scroll_speed,
                                                                             pipe_frequency, SPAWNPIPE)
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
                play_death_sound()
                print("Collision detected!")
                game_over = True
                save_high_score(score)

        draw_background()
        draw_pipes(pipes)
        rotate_bird()

        score_surface = font.render(f"Score: {score} ", True, (255, 255, 255))
        SCREEN.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        if paused:
            pause_text = font.render("PAUSED - Press P or SPACE to Resume", True, (255, 255, 255))
            SCREEN.blit(pause_text, (WIDTH // 2 - pause_text.get_width(), HEIGHT // 2))

        current_high = get_high_score()
        high_score_surface = font.render(f"High Score: {current_high} ", True, (255, 255, 0))
        SCREEN.blit(high_score_surface, (10, 10))

        if game_over:
            draw_gameover()
        pygame.display.flip()

    return state