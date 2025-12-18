from __future__ import annotations

import pygame as py
import pygame_gui as pyg
import requests
from typing import Dict, Tuple

from config import WIDTH, HEIGHT
from helper import resource_path
from classes import UItextEntryLineWithPlaceholder, UITextEntryLinePassword

type SurfaceType = py.Surface
type Rect = py.Rect
type Font = py.font.Font

py.init()
screen: SurfaceType = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Flappy Game - Login")

manager: pyg.UIManager = pyg.UIManager((WIDTH, HEIGHT))

font: Font = py.font.Font(resource_path("assets/font/font.ttf"), 24)

def draw_text(surface: SurfaceType, text: str, position: Tuple[int, int], color: Tuple[int, int, int]=(255, 255, 255)):
    """Helper function to render text."""
    label = font.render(text, True, color)
    surface.blit(label, position)

def draw_centered_text(surface: SurfaceType, text: str, center_position: Tuple[int, int], font: Font, color: Tuple[int, int, int]=(255, 255, 255)):
    """
    Renders and draws the given text on the surface,
    centered at the specified (x, y) coordinate.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center_position)
    surface.blit(text_surface, text_rect)

username_input: UItextEntryLineWithPlaceholder = UItextEntryLineWithPlaceholder(
    relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 110), (200, 40)),
    manager=manager
)
user_placeholder: str = "Enter Username"
username_input.set_placeholder(user_placeholder)

email_input: UItextEntryLineWithPlaceholder = UItextEntryLineWithPlaceholder(
    relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 70), (200, 40)),
    manager=manager
)
email_placeholder: str = "Enter Email"
email_input.set_placeholder(email_placeholder)

password_input: UITextEntryLinePassword = UITextEntryLinePassword(
    relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 40)),
    manager=manager
)
password_placeholder: str = "Enter Password"
password_input.set_placeholder(password_placeholder)

login_button: pyg.elements.UIButton = pyg.elements.UIButton(
    relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 20), (100, 40)),
    text="Login",
    manager=manager
)
signup_button = pyg.elements.UIButton(
    relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 70), (100, 40)),
    text="SignUp",
    manager=manager
)

close_img: SurfaceType = py.image.load(resource_path("assets/image/X.png"))
close_img = py.transform.scale(close_img, (30, 30))
close_rect: Rect = close_img.get_rect(midtop=(20, 5))

eye_img: SurfaceType = py.image.load(resource_path("assets/image/eye.png"))
eye_img = py.transform.scale(eye_img, (30, 30))

eye_button: pyg.elements.UIButton = pyg.elements.UIButton(
    relative_rect=py.Rect((WIDTH // 2 + 110, HEIGHT // 2 - 30), (30, 30)),
    text='',
    manager=manager,
    tool_tip_text="Show/Hide Password"
)

message: str = ""
message_time: float = 0
message_color: Tuple[int, int, int] = (255, 0, 0)  # Red color for error messages

def handle_account(state: Dict[str, str]) -> Dict[str, str]:
    global message, message_time, message_color

    clock: py.time.Clock = py.time.Clock()
    running: bool = True

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
                    

            if event.type == pyg.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    username = username_input.get_text().strip()
                    email = email_input.get_text().strip()
                    password = password_input.get_real_text().strip()
                    print(f"Debug: username='{username}', email='{email}', password='{password}'")

                    if username in ("", user_placeholder) or password in ("" ,password_placeholder) or email in ("", email_placeholder):
                        message = "Please enter your username, email, and password."
                        message_time = 3
                        message_color = (255, 0, 0)  # Red color for error messages
                        continue

                    try:
                        response = requests.post("http://127.0.0.1:5000/login",
                                                 json={"username": username, "password": password, "email": email})
                        data = response.json()
                    except Exception as e:
                        print("Login failed.", e)
                        message = "Login failed."
                        message_time = 3
                        message_color = (255, 0, 0)
                    else:
                        if "message" in data:
                            message = data.get('message', "Login Successful")
                            message_color = (0, 255, 0)  # Green color for success messages
                        else:
                            print(f"Login failed: {data.get('error', 'Unknown Error')}")
                            message = f"Login Failed {data.get('error', 'Unknown Error')}"
                            message_color = (255, 0, 0)  # Red color for error messages
                        message_time = 3

                elif event.ui_element == signup_button:
                    username = username_input.get_text().strip()
                    email = email_input.get_text().strip()
                    password = password_input.get_real_text().strip()
                    print(f"Debug: username='{username}', email='{email}', password='{password}'")

                    if username in ("", user_placeholder) or password in ("" ,password_placeholder) or email in ("", email_placeholder):
                        message = "Please enter your username, email, and password."
                        message_time = 3
                        message_color = (255, 0, 0)  # Red color for error messages
                        continue

                    try:
                        response = requests.post("http://127.0.0.1:5000/signup",
                                                 json={"username": username, "password": password, "email": email})
                        data = response.json()
                    except Exception as e:
                        print("Signup failed:", e)
                        message = "Signup Failed."
                        message_time = 3
                        message_color = (255, 0, 0)  # Red color for error messages
                    else:
                        if "message" in data:
                            message = data.get('message', "Signup successful, you can now login")
                            message_color = (0, 255, 0)
                        else:
                            print(f"Signup failed: {data.get('error', 'Unknown Error')}")
                            message = f"Signup Failed {data.get('error', 'Unknown Error')}"
                            message_color = (255, 0, 0)  # Red color for error messages
                        message_time = 3

                elif event.ui_element == eye_button:
                    password_input.show_password = not password_input.show_password
                    display_text = password_input.real_text if password_input.show_password else "*" * len(password_input.real_text)
                    password_input.set_text(display_text)

            manager.process_events(event)

        if message_time > 0:
            message_time -= time_delta

        screen.fill((30, 30, 30))
        screen.blit(close_img, close_rect)
        draw_text(screen, "Account Page", (WIDTH // 2 - 55, HEIGHT // 2 - 145))
        draw_text(screen, "Username:", (WIDTH // 2 - 190, HEIGHT // 2 - 105))
        draw_text(screen, "Email:", (WIDTH // 2 - 150, HEIGHT // 2 - 65))
        draw_text(screen, "Password:", (WIDTH // 2 - 190, HEIGHT // 2 - 25))

        if message_time > 0:
            draw_centered_text(screen, message, (WIDTH // 2, HEIGHT // 2 + 120), font, color=message_color)

        manager.update(time_delta)
        manager.draw_ui(screen)
        screen.blit(eye_img, eye_button.relative_rect.topleft)
        py.display.flip()
    return state