import pygame
from sounds import play_score_sound, play_slap_sound

# Checks for collision
def check_collision(bird_rect, pipes):
    collisio_detected = False

    for pipe in pipes:
        if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
            collisio_detected = True

    if bird_rect.top <= 0 or bird_rect.bottom >= 600:
        collisio_detected = True

    if collisio_detected:
        play_slap_sound()
        return True

    return False

# for giving points
def update_score(bird_rect, pipes, score):
    for pipe in pipes:
        if not pipe["scored"] and pipe["top"].right < bird_rect.left:
            pipe["scored"] = True
            score += 1
            play_score_sound()
            print(f"Scored pipe id: {pipe["top"].centerx}, total score: {score}")
    return score

def get_pipe_frequency(score):
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

def get_pipe_gap(score):
    if score >= 100:
        return 100
    elif score >= 50:
        return 140
    elif score >= 40:
        return 160
    elif score >= 30:
        return 200
    elif score >= 20:
        return 220
    else:
        return 300

def update_game_speed(score, pipe_speed, scroll_speed, pipe_frequency, SPAWNPIPE):
    new_pipe_speed = pipe_speed
    new_scroll_speed = scroll_speed

    if score >= 100:
        new_pipe_speed = 10
        new_scroll_speed = 5
    elif score >= 90:
        new_pipe_speed = 8
        new_scroll_speed = 4
    elif score >= 60:
        new_pipe_speed = 6
        new_scroll_speed = 3
    elif score >= 40:
        new_pipe_speed = 4
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
        pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

    return new_pipe_speed, new_scroll_speed, new_frequency