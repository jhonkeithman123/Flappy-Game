import os
import pygame
import sys

pygame.init()
os.environ["SDL_RENDER_DRIVER"] = "software"
SCREEN = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

character_images = {
    "default": pygame.transform.scale(pygame.image.load(resource_path(
        '../assets/image/birds/bird.png')).convert_alpha(), (70, 50)),
    "Blue": pygame.transform.scale(pygame.image.load(resource_path(
        "../assets/image/birds/blue-bird.png")).convert_alpha(), (70, 50)),
    "Green": pygame.transform.scale(pygame.image.load(resource_path(
        "../assets/image/birds/green-bird.png")).convert_alpha(), (70, 50)),
    "Yellow": pygame.transform.scale(pygame.image.load(resource_path(
        "../assets/image/birds/yellow-bird.png")).convert_alpha(), (70, 50)),
    "Navy": pygame.transform.scale(pygame.image.load(resource_path(
        "../assets/image/birds/navy-bird.png")).convert_alpha(), (70, 50)),
    "Glitch": pygame.transform.scale(pygame.image.load(resource_path(
        "../assets/image/birds/glitch-bird.png")).convert_alpha(), (70, 50)),
}