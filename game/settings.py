import sys
import pygame
from helper import resource_path
from saves import load_settings, save_settings
from sounds import update_sound_fx_volume
import config
from config import VERSION, RESOLUTIONS
from ui import SurfaceType, Rect, Font

font: Font = pygame.font.Font(resource_path('assets/font/font.ttf'), 40)
BG: SurfaceType = pygame.image.load(resource_path('assets/image/background.png')).convert()
BGround: SurfaceType = pygame.Surface((config.WIDTH, config.HEIGHT))

close_img: SurfaceType = pygame.Surface((config.WIDTH, config.HEIGHT))
close_img_rect: Rect = close_img.get_rect()

mute_icon: SurfaceType = pygame.Surface((config.WIDTH, config.HEIGHT))
unmute_icon: SurfaceType= pygame.Surface((config.WIDTH, config.HEIGHT))

platform: SurfaceType = pygame.Surface((config.WIDTH, config.HEIGHT))
platform_rect: Rect = platform.get_rect()

mute_button_rect: Rect = mute_icon.get_rect()

def rebuild_settings_assets() -> None:
    """Rescale background and platform for current resolution."""
    global BGround, platform, platform_rect, mute_icon, unmute_icon, close_img, close_img_rect, mute_button_rect
    BGround = pygame.transform.scale(BG, (config.WIDTH, config.HEIGHT))

    mute_icon_local: SurfaceType = pygame.image.load(resource_path("assets/image/music-close.png")).convert_alpha()
    unmute_icon_local: SurfaceType = pygame.image.load(resource_path("assets/image/music-open.png")).convert_alpha()
    mute_icon_local = pygame.transform.scale(mute_icon_local, (120, 60))
    unmute_icon_local = pygame.transform.scale(unmute_icon_local, (120, 60))

    platform_local: SurfaceType = pygame.image.load(resource_path("assets/image/SettingPlat.png")).convert_alpha()
    platform_rect_local: Rect = platform_local.get_rect(center=(config.WIDTH - 395, config.HEIGHT - 300))

    close_img_local: SurfaceType = pygame.image.load(resource_path("assets/image/X.png")).convert_alpha()
    close_img_local = pygame.transform.scale(close_img_local, (40, 40))
    close_img_rect_local: Rect = close_img_local.get_rect(center=(platform_rect_local.centerx + 180, platform_rect_local.top + 45))

    mute_button_rect_local: Rect = mute_icon_local.get_rect(center=(config.WIDTH - 100, config.HEIGHT - 100))

    globals().update(
        BGround=BGround,
        platform=platform_local,
        platform_rect=platform_rect_local,
        close_img=close_img_local,
        close_img_rect=close_img_rect_local,
        mute_icon=mute_icon_local,
        unmute_icon=unmute_icon_local,
        mute_button_rect=mute_button_rect_local,
    )

rebuild_settings_assets()

class Slider:
    def __init__(self, x: float, y: float, width: int, min_value: float =0, max_value: float =1, default_value: float =0.5) -> None:
        """
        Creates a draggable slider to adjust values.

        Parameters:
        - x, y: Position of the slider.
        - width: Length of the slider bar.
        - min_value, max_value: Range of values for the slider.
        - default_value: Initial slider position.
        """
        self.x = x
        self.y = y
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.value = default_value

        self.slider_bar = pygame.Rect(self.x, self.y, self.width, 6)
        self.knob_radius = 10
        self.knob_x = self.x + (self.value * width)
        self.dragging = False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles mouse interaction with the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                knob_rect = pygame.Rect(self.knob_x - self.knob_radius, self.y - self.knob_radius,
                                        self.knob_radius * 2, self.knob_radius * 2)

                if knob_rect.collidepoint(mouse_x, mouse_y):
                    self.dragging = True
                elif self.slider_bar.collidepoint(mouse_x, mouse_y):
                    self.knob_x = max(self.x, min(mouse_x, self.x + self.width))
                    self.value = (self.knob_x - self.x) / self.width

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.knob_x = max(self.x, min(event.pos[0], self.x + self.width))
                self.value = (self.knob_x - self.x) / self.width

    def draw(self, screen: SurfaceType) -> None:
        """Draws the slider."""
        pygame.draw.rect(screen, (180, 180, 180), self.slider_bar)
        pygame.draw.circle(screen, (255, 0, 0), (self.knob_x, self.y), self.knob_radius)


def draw_settings_panel(screen: SurfaceType, rect: Rect) -> None:
    """
    Draws the settings panel on the given screen.
    The panel uses a background image and a dedicated platform image.
    """
    screen.blit(BGround, (0, 0))

    platform = pygame.image.load(resource_path('assets/image/SettingPlat.png')).convert_alpha()
    platform_rect = platform.get_rect(center=(config.WIDTH - 395, config.HEIGHT - 300))
    screen.blit(platform, platform_rect)
    screen.blit(close_img, close_img_rect)

    title = font.render('Settings', True, (255, 255, 255))
    title_rect = title.get_rect(center=(rect.centerx, rect.top - 20))
    screen.blit(title, title_rect)

    version_text = font.render(VERSION, True, (255, 255, 255))
    screen.blit(version_text, (config.WIDTH - version_text.get_width() - 20, 20))

def handle_settings_events(state: dict[str, str], save_directory: str):
    """
    Runs the settings panel loop.

    The function updates the state so that when the user exits the
    settings (by pressing ESC), the state["current"] value is reset
    to "menu", returning control to the main menu.

    Returns the updated state.
    """
    state["current"] = "settings"
    running: bool = True
    panel_rect: Rect = pygame.Rect(200, 150, 400, 300)
    clock = pygame.time.Clock()

    is_muted: bool = False
    previous_volume: float = 0.5
    previous_fx_volume: float = 0.5

    volume_slider: Slider = Slider(300, 250, 200, min_value=0, max_value=1, default_value=0.5)
    sound_fx_slider: Slider = Slider(300, 340, 200, min_value=0, max_value=1, default_value=0.5)

    # Build resolution buttons
    res_buttons: list[tuple[pygame.Rect, tuple[int, int]]] = []
    btn_w, btn_h = 150, 40
    start_x, start_y = 80, 200
    gap_y = 50
    for i, (w, h) in enumerate(RESOLUTIONS):
        rect = pygame.Rect(start_x, start_y + i * gap_y, btn_w, btn_h)
        res_buttons.append((rect, (w, h)))

    settings = load_settings(save_directory)
    if settings:
        volume_slider.value = settings.get("music_volume", previous_volume)
        sound_fx_slider.value = settings.get("sound_fx_volume", previous_fx_volume)
        is_muted = bool(settings.get("is_muted", False))

        volume_slider.knob_x = volume_slider.x + (volume_slider.value * volume_slider.width)
        sound_fx_slider.knob_x = sound_fx_slider.x + (sound_fx_slider.value * sound_fx_slider.width)

        if is_muted:
            pygame.mixer.music.set_volume(0)
            update_sound_fx_volume(0)
        else:
            pygame.mixer.music.set_volume(volume_slider.value)
            update_sound_fx_volume(sound_fx_slider.value)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    state["current"] = "menu"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = event.pos
                    
                    if mute_button_rect.collidepoint(mouse_pos):
                        is_muted = not is_muted
                        if is_muted:
                            previous_volume = volume_slider.value
                            previous_fx_volume = sound_fx_slider.value

                            volume_slider.value = 0
                            sound_fx_slider.value = 0

                            volume_slider.knob_x = volume_slider.x
                            sound_fx_slider.knob_x = sound_fx_slider.x

                            pygame.mixer.music.set_volume(0)
                            update_sound_fx_volume(0)
                        else:
                            volume_slider.value = previous_volume
                            sound_fx_slider.value = previous_fx_volume

                            volume_slider.knob_x = volume_slider.x + previous_volume * volume_slider.width
                            sound_fx_slider.knob_x = sound_fx_slider.x + previous_volume * volume_slider.width

                            pygame.mixer.music.set_volume(previous_volume)
                            update_sound_fx_volume(previous_fx_volume)

                    elif close_img_rect.collidepoint(mouse_pos):
                        state["current"] = "menu"
                        running = False

                    # Resolution buttons
                    for btn_rect, (w, h) in res_buttons:
                        if btn_rect.collidepoint(mouse_pos):
                            config.WIDTH, config.HEIGHT = w, h
                            pygame.display.set_mode((w, h), pygame.DOUBLEBUF | pygame.RESIZABLE)
                            rebuild_settings_assets()
                            # Re-center sliders after resize
                            volume_slider.x, volume_slider.y = 300, 250
                            sound_fx_slider.x, sound_fx_slider.y = 300, 340
                            volume_slider.slider_bar.topleft = (volume_slider.x, volume_slider.y)
                            sound_fx_slider.slider_bar.topleft = (sound_fx_slider.x, sound_fx_slider.y)
            

            volume_slider.handle_event(event)
            sound_fx_slider.handle_event(event)

            if not is_muted:
                pygame.mixer.music.set_volume(volume_slider.value)
                previous_volume = volume_slider.value
            else:
                pygame.mixer.music.set_volume(0)

        update_sound_fx_volume(sound_fx_slider.value)

        raw_screen = pygame.display.get_surface()
        if raw_screen is None:
            raise RuntimeError("Display surface not initialized")

        screen: SurfaceType = raw_screen
        screen.fill((0, 0, 0))
        draw_settings_panel(screen, panel_rect)
        volume_slider.draw(screen)
        sound_fx_slider.draw(screen)
        screen.blit(mute_icon if is_muted else unmute_icon, mute_button_rect)

        volume_text = font.render(f'Volume: {round(volume_slider.value, 2)}', True, (255, 255, 255))
        screen.blit(volume_text, (volume_slider.x + 20, volume_slider.y - 45))

        sound_fx_text = font.render(f"Sound FX: {round(sound_fx_slider.value * 100)}%", True, (255, 255, 255))
        screen.blit(sound_fx_text, (sound_fx_slider.x, sound_fx_slider.y - 45))

        pygame.display.flip()

    new_settings: dict[str, float | bool] = {
        "music_volume": volume_slider.value,
        "sound_fx_volume": sound_fx_slider.value,
        "is_muted": is_muted
    }
    save_settings(new_settings, save_directory)
    return state