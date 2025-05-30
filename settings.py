import sys
import pygame
from helper import resource_path
from saves import load_settings, save_settings
from sounds import play_sound_effect, update_sound_fx_volume
from config import VERSION, WIDTH, HEIGHT

font = pygame.font.Font(resource_path('assets/font/font.ttf'), 40)
BG = pygame.image.load(resource_path('assets/image/background.png')).convert()
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

mute_icon = pygame.image.load(resource_path('assets/image/music-close.png')).convert_alpha()
unmute_icon = pygame.image.load(resource_path('assets/image/music-open.png')).convert_alpha()

mute_icon = pygame.transform.scale(mute_icon, (120, 60))
unmute_icon = pygame.transform.scale(unmute_icon, (120, 60))

platform = pygame.image.load(resource_path('assets/image/SettingPlat.png')).convert_alpha()
platform_rect = platform.get_rect(center=(WIDTH - 395, HEIGHT - 300))

close_img = pygame.image.load(resource_path("assets/image/X.png")).convert_alpha()
close_img = pygame.transform.scale(close_img, (40, 40))
close_img_rect = close_img.get_rect(center=(platform_rect.centerx + 180, platform_rect.top + 45))

mute_button_rect = mute_icon.get_rect(center=(WIDTH - 100, HEIGHT - 100))

class Slider:
    def __init__(self, x, y, width, min_value=0, max_value=1, default_value=0.5):
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

    def handle_event(self, event):
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

    def draw(self, screen):
        """Draws the slider."""
        pygame.draw.rect(screen, (180, 180, 180), self.slider_bar)
        pygame.draw.circle(screen, (255, 0, 0), (self.knob_x, self.y), self.knob_radius)


def draw_settings_panel(screen, rect):
    """
    Draws the settings panel on the given screen.
    The panel uses a background image and a dedicated platform image.
    """
    screen.blit(BG, (0, 0))

    platform = pygame.image.load(resource_path('assets/image/SettingPlat.png')).convert_alpha()
    platform_rect = platform.get_rect(center=(WIDTH - 395, HEIGHT - 300))
    screen.blit(platform, platform_rect)
    screen.blit(close_img, close_img_rect)

    title = font.render('Settings', True, (255, 255, 255))
    title_rect = title.get_rect(center=(rect.centerx, rect.top - 20))
    screen.blit(title, title_rect)

    version_text = font.render(VERSION, True, (255, 255, 255))
    screen.blit(version_text, (WIDTH - version_text.get_width() - 20, 20))

def handle_settings_events(state, save_directory):
    """
    Runs the settings panel loop.

    The function updates the state so that when the user exits the
    settings (by pressing ESC), the state["current"] value is reset
    to "menu", returning control to the main menu.

    Returns the updated state.
    """
    state["current"] = "settings"
    running = True
    panel_rect = pygame.Rect(200, 150, 400, 300)
    clock = pygame.time.Clock()

    is_muted = False
    previous_volume = 0.5

    volume_slider = Slider(300, 250, 200, min_value=0, max_value=1, default_value=0.5)
    sound_fx_slider = Slider(300, 340, 200, min_value=0, max_value=1, default_value=0.5)

    settings = load_settings(save_directory)
    if settings:
        volume_slider.value = settings.get("music_volume", previous_volume)
        sound_fx_slider.value = settings.get("sound_fx_volume", 0.5)
        is_muted = settings.get("is_muted", False)
        if is_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(volume_slider.value)

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
                elif event.key == pygame.K_m:
                    is_muted = not is_muted
                    if is_muted:
                        previous_volume = pygame.mixer.music.get_volume()
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(previous_volume)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if mute_button_rect.collidepoint(mouse_pos):
                    is_muted = not is_muted
                    if is_muted:
                        previous_volume = pygame.mixer.music.get_volume()
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(previous_volume)
                elif close_img_rect.collidepoint(mouse_pos):
                    state["current"] = "menu"
                    running = False

            volume_slider.handle_event(event)
            sound_fx_slider.handle_event(event)

            if not is_muted:
                pygame.mixer.music.set_volume(volume_slider.value)
                previous_volume = volume_slider.value
            else:
                pygame.mixer.music.set_volume(0)

        update_sound_fx_volume(sound_fx_slider.value)

        screen = pygame.display.get_surface()
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

    new_settings = {
        "music_volume": volume_slider.value,
        "sound_fx_volume": sound_fx_slider.value,
        "is_muted": is_muted
    }
    save_settings(new_settings, save_directory)
    return state
