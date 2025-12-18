import pygame
from typing import Sequence, Tuple, TypedDict

from sounds import play_score_sound, play_slap_sound, play_coin_collect_sound
from ui import Rect

class PipeDict(TypedDict):
    top: Rect
    bottom: Rect
    coin: Rect
    coin_collected: bool
    scored: bool

# Checks for collision
def check_collision(bird_rect: Rect, pipes: Sequence[PipeDict]) -> Tuple[bool, int]:
    """
    Checks for collisions with pipes and boundaries (game over collisions)
    and also checks for coin collections.

    Returns a tuple:
        (game_over: bool, coins_collected: int)
    """
    game_over: bool = False
    coins_collected: int = 0

    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            game_over = True

        if not pipe.get("coin_collected", False) and bird_rect.colliderect(pipe["coin"]):
            play_coin_collect_sound()
            coins_collected += 1
            pipe["coin_collected"] = True
            print("Coin collected! Total coins:", coins_collected)

    if bird_rect.top <= 0 or bird_rect.bottom >= 580:
        game_over = True

    if game_over:
        play_slap_sound()

    return game_over, coins_collected

# for giving points
def update_score(bird_rect: Rect, pipes: Sequence[PipeDict], score: int) -> int:
    for pipe in pipes:
        if not pipe["scored"] and pipe["top"].right < bird_rect.left:
            pipe["scored"] = True
            score += 1
            play_score_sound()
            print(f"Player scored, total score: {score}")
    return score

def get_pipe_frequency(score: int) -> int:
    if score >= 150:
        return 800
    elif score >= 120:
        return 900
    elif score >= 100:
        return 1000
    elif score >= 75:
        return 1200
    elif score >= 50:
        return 1250
    elif score >= 25:
        return 1300
    elif score >= 20:
        return 1400
    elif score >= 10:
        return 1500
    else:
        return 1600

def get_pipe_gap(score: int) -> int:
    if score >= 100:
        return 160
    elif score >= 50:
        return 190
    elif score >= 40:
        return 210
    elif score >= 30:
        return 240
    elif score >= 20:
        return 260
    else:
        return 300

def update_game_speed(score: int, pipe_frequency: int, spawn_pipe: int) -> Tuple[int, int, int]:

    if score >= 100:
        new_pipe_speed = 9
        new_scroll_speed = 6
    elif score >= 90:
        new_pipe_speed = 8
        new_scroll_speed = 5
    elif score >= 60:
        new_pipe_speed = 7
        new_scroll_speed = 4
    elif score >= 40:
        new_pipe_speed = 6
        new_scroll_speed = 3
    elif score >= 20:
        new_pipe_speed = 5
        new_scroll_speed = 3
    else:
        new_pipe_speed = 5
        new_scroll_speed = 3

    new_frequency = get_pipe_frequency(score)
    if new_frequency != pipe_frequency:
        pipe_frequency = new_frequency
        pygame.time.set_timer(spawn_pipe, pipe_frequency)

    return new_pipe_speed, new_scroll_speed, new_frequency