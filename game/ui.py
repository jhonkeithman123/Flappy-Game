import pygame
import pygame as py
import pygame_gui as pyg
import requests
from config import WIDTH, HEIGHT
from game.helper import resource_path

class UITextEntryLinePassword(pyg.elements.UITextEntryLine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.real_text = ""
        self.placeholder = ""
        self.in_placeholder_mode = True

    def set_placeholder(self, text):
        self.placeholder = text
        self.in_placeholder_mode = True
        super().set_text(text)

    def clear_text_for_input(self):
        if self.in_placeholder_mode:
            self.real_text = ""
            self.in_placeholder_mode = False
            super().set_text("")

    def process_event(self, event):
        if event.type == pyg.UI_TEXT_ENTRY_CHANGED and event.ui_element == self:
            return True

        if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if self.relative_rect.collidepoint(event.pos):
                self.clear_text_for_input()

        if event.type == py.KEYDOWN:
            if self in self.ui_manager.get_focus_set():
                if event.key == py.K_BACKSPACE:
                    self.real_text = self.real_text[:-1]
            elif event.type == py.K_RETURN:
                self.real_text += event.unicode
            super().set_text("*" * len(self.real_text))
            return True

        return super().process_event(event)

    def get_real_text(self):
        return self.real_text


py.init()
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Flappy Game - Login")

manager = pyg.UIManager((WIDTH, HEIGHT))

font = py.font.Font(resource_path("../assets/font/font.ttf"), 24)

def draw_text(surface, text, position, color=(255, 255, 255)):
    """Helper function to render text."""
    label = font.render(text, True, color)
    surface.blit(label, position)

def draw_centered_text(surface, text, center_position, font, color=(255, 255, 255)):
    """
    Renders and draws the given text on the surface,
    centered at the specified (x, y) coordinate.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_position)
    surface.blit(text_surface, text_rect)

username_input = pyg.elements.UITextEntryLine(
    relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 80), (200, 40)),
    manager=manager
)
user_placeholder = "Enter Username"
username_input.set_text(user_placeholder)

password_input = UITextEntryLinePassword(
    relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 40)),
    manager=manager
)
password_placeholder = "Enter Password"
password_input.set_text(password_placeholder)

login_button = pyg.elements.UIButton(
    relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 20), (100, 40)),
    text="Login",
    manager=manager
)
signup_button = pyg.elements.UIButton(
    relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 70), (100, 40)),
    text="SignUp",
    manager=manager
)

close_img = py.image.load(resource_path("../assets/image/X.png"))
close_img = py.transform.scale(close_img, (30, 30))
close_rect = close_img.get_rect(midtop=(20, 5))

message = ""
message_time = 0

def handle_account(state):
    global message, message_time
    clock = py.time.Clock()
    running = True

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    state["current"] = "menu"
                    running = False

            elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                if close_rect.collidepoint(event.pos):
                    state["current"] = "menu"
                    running = False

                if username_input.relative_rect.collidepoint(event.pos):
                    if username_input.get_text() == user_placeholder:
                        username_input.set_text("")

                if password_input.relative_rect.collidepoint(event.pos):
                    if password_input.get_text() == password_placeholder:
                        password_input.set_text("")

            if event.type == pyg.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    username = username_input.get_text().strip()
                    password = password_input.get_real_text().strip()
                    print(f"Debug: username='{username}', password='{password}'")

                    if username in ("", user_placeholder) or password in ("" ,password_placeholder):
                        message = "Please enter your username and password."
                        message_time = 3
                        continue

                    try:
                        response = requests.post("http://127.0.0.1:5000/login",
                                                 json={"username": username, "password": password})
                        data = response.json()
                    except Exception as e:
                        print("Login failed.", e)
                        message = "Login failed."
                        message_time = 3
                    else:
                        if "message" in data:
                             message = data.get('message', "Login Successful")
                        else:
                            print(f"Login failed: {data.get('error', 'Unknown Error')}")
                            message = f"Login Failed {data.get('error', 'Unknown Error')}"
                        message_time = 3

                elif event.ui_element == signup_button:
                    username = username_input.get_text().strip()
                    password = password_input.get_real_text().strip()
                    print(f"Debug: username='{username}', password='{password}'")

                    if username in ("", user_placeholder) or password in ("" ,password_placeholder):
                        message = "Please enter your username and password."
                        message_time = 3
                        continue

                    try:
                        response = requests.post("http://127.0.0.1:5000/signup",
                                                 json={"username": username, "password": password})
                        data = response.json()
                    except Exception as e:
                        print("Signup failed:", e)
                        message = "Signup Failed."
                        message_time = 3
                    else:
                        if "message" in data:
                            message = data.get('message', "Signup successful, you can now login")
                        else:
                            print(f"Signup failed: {data.get('error', 'Unknown Error')}")
                            message = f"Signup Failed {data.get('error', 'Unknown Error')}"
                        message_time = 3

            manager.process_events(event)

        if message_time > 0:
            message_time -= time_delta

        screen.fill((30, 30, 30))
        screen.blit(close_img, close_rect)
        draw_text(screen, "Account Page", (WIDTH // 2 - 55, HEIGHT // 2 - 120))
        draw_text(screen, "Username:", (WIDTH // 2 - 190, HEIGHT // 2 - 70))
        draw_text(screen, "Password:", (WIDTH // 2 - 190, HEIGHT // 2 - 20))

        if message_time > 0:
            draw_centered_text(screen, message, (WIDTH // 2, HEIGHT // 2 + 120), font, color=(255, 0, 0))

        manager.update(time_delta)
        manager.draw_ui(screen)
        py.display.flip()
    return state