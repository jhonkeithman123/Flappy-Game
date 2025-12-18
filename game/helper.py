import os
import sys
from typing import Dict

import pygame

pygame.init()
os.environ["SDL_RENDER_DRIVER"] = "software"
SCREEN: pygame.Surface = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)

def resource_path(relative_path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path: str = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))

    pyinstaller_path = os.path.join(base_path, relative_path.replace("../", ""))
    normal_path = os.path.abspath(relative_path)

    if os.path.exists(pyinstaller_path):
        return os.path.normpath(pyinstaller_path)
    elif os.path.exists(normal_path):
        return os.path.normpath(normal_path)
    else:
        raise FileNotFoundError(f"Resource not found: {relative_path}")
    

character_images: Dict[str, pygame.Surface] = {
    "default": pygame.transform.scale(
        pygame.image.load(
            resource_path('assets/image/birds/bird.png')
        ).convert_alpha(), 
        (70, 50)
    ),
    "Blue": pygame.transform.scale(
        pygame.image.load(
            resource_path("assets/image/birds/blue-bird.png")
        ).convert_alpha(), 
        (70, 50)
    ),
    "Green": pygame.transform.scale(
        pygame.image.load(
            resource_path("assets/image/birds/green-bird.png")
        ).convert_alpha(), 
        (70, 50)
    ),
    "Yellow": pygame.transform.scale(
        pygame.image.load(
            resource_path("assets/image/birds/yellow-bird.png")
        ).convert_alpha(), 
        (70, 50)
    ),
    "Navy": pygame.transform.scale(
        pygame.image.load(
            resource_path("assets/image/birds/navy-bird.png")
        ).convert_alpha(), 
        (70, 50)
    ),
    "Glitch": pygame.transform.scale(
        pygame.image.load(
            resource_path("assets/image/birds/glitch-bird.png")
        ).convert_alpha(), 
        (70, 50)
    ),
}

print("DEBUG: Loading image from path:", resource_path("assets/image/birds/bird.png"))