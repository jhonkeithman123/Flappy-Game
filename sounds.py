import pygame
from helper import resource_path

pygame.mixer.init()

def init_sounds():
    """
    Initializes the mixer, loads background music, and starts playing it on loop.
    Call this once at the beginning of your game (e.g. in main).
    """
    music_path = resource_path('assets/sounds/bg-music.mp3')
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

flap_sound = pygame.mixer.Sound(resource_path('assets/sounds/flap.mp3'))
score_sound = pygame.mixer.Sound(resource_path('assets/sounds/score.mp3'))
slap_sound = pygame.mixer.Sound(resource_path('assets/sounds/slap.mp3'))
death_sound = pygame.mixer.Sound(resource_path('assets/sounds/death.mp3'))

sound_fx_volume = 0.5

sound_enabled = True

def toggle_music():
    """
    Toggles the background music between paused and unpaused.
    """
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def play_sound_effect(effect_filename, volume=0.5):
    """
    Plays a one-shot sound effect. For example, a click sound when a button is pressed.
    The filename should be relative to your asset's location.
    """
    sound_effect = pygame.mixer.Sound(resource_path(effect_filename))
    sound_effect.set_volume(volume)
    sound_effect.play()

def update_sound_fx_volume(volume):
    global sound_fx_volume
    sound_fx_volume = volume
    flap_sound.set_volume(volume)
    score_sound.set_volume(volume)
    death_sound.set_volume(volume)
    slap_sound.set_volume(volume)

def play_flap_sound():
    """Plays the flap sound if sound is enabled."""
    flap_sound.set_volume(sound_fx_volume)
    if sound_enabled:
        flap_sound.stop()
        flap_sound.play()

def play_score_sound():
    """Plays the score sound if sound is enabled."""
    score_sound.set_volume(sound_fx_volume)
    if sound_enabled:
        score_sound.stop()
        score_sound.play()

def play_slap_sound():
    """Plays the slap sound if sound is enabled."""
    slap_sound.set_volume(sound_fx_volume)
    if sound_enabled:
        slap_sound.stop()
        slap_sound.play()

def play_death_sound():
    """Plays the death sound if sound is enabled."""
    death_sound.set_volume(sound_fx_volume)
    if sound_enabled:
        death_sound.stop()
        death_sound.play()

def toggle_sounds():
    """Plays the scoring effect on or off."""
    global sound_enabled
    sound_enabled = not sound_enabled