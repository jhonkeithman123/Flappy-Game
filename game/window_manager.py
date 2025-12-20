"""
Reusable window resize handler for all game screens.
Handles minimum size enforcement and layout rebuilding.
"""
import pygame
from typing import Callable, Optional
import config

# Global reference to the current screen surface
_screen: Optional[pygame.Surface] = None


def init_window(width: int = config.WIDTH, height: int = config.HEIGHT) -> pygame.Surface:
    """
    Initialize the game window with resize capabilities.
    
    Args:
        width: Initial window width
        height: Initial window height
    
    Returns:
        The pygame display surface
    """
    global _screen
    _screen = pygame.display.set_mode(
        (width, height), 
        pygame.DOUBLEBUF | pygame.RESIZABLE
    )
    
    # Set minimum window size if available (pygame-ce)
    set_min_size = getattr(pygame.display, "set_window_min_size", None)
    if callable(set_min_size):
        set_min_size((config.MIN_WIDTH, config.MIN_HEIGHT))
    
    # Set maximum window size if available (pygame-ce)
    set_max_size = getattr(pygame.display, "set_window_max_size", None)
    if callable(set_max_size):
        from config import MAX_WIDTH_CAP, MAX_HEIGHT_CAP
        set_max_size((MAX_WIDTH_CAP, MAX_HEIGHT_CAP))
    
    return _screen


def handle_resize(
    size: tuple[int, int], 
    rebuild_callback: Callable[[], None]
) -> pygame.Surface:
    """
    Handle window resize events with minimum size enforcement.
    
    Args:
        size: New window size (width, height)
        rebuild_callback: Function to call to rebuild layout/assets
    
    Returns:
        The updated screen surface
    """
    global _screen
    w, h = size
    min_w, min_h = config.MIN_WIDTH, config.MIN_HEIGHT

    # If below min, clamp to min size but keep window resizable
    if w < min_w or h < min_h:
        clamped_w = max(w, min_w)
        clamped_h = max(h, min_h)
        
        # Only recreate surface if size actually changed
        if (clamped_w, clamped_h) != (config.WIDTH, config.HEIGHT):
            config.WIDTH, config.HEIGHT = clamped_w, clamped_h
            _screen = pygame.display.set_mode(
                (clamped_w, clamped_h), 
                pygame.DOUBLEBUF | pygame.RESIZABLE
            )
            rebuild_callback()
        return _screen # type: ignore

    # Update logical size; keep current surface for sizes above minimum
    config.WIDTH, config.HEIGHT = w, h
    surf = pygame.display.get_surface() or _screen
    _screen = surf
    rebuild_callback()
    
    return _screen # type: ignore


def get_screen() -> Optional[pygame.Surface]:
    """Get the current screen surface."""
    return _screen


def set_screen(screen: pygame.Surface) -> None:
    """Set the current screen surface."""
    global _screen
    _screen = screen