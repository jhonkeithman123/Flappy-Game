from __future__ import annotations

import pygame as py
import pygame_gui as pyg
from typing import Dict, Tuple

from config import WIDTH, HEIGHT
from helper import resource_path
from classes import UItextEntryLineWithPlaceholder, UITextEntryLinePassword
from services.auth import login, signup

type SurfaceType = py.Surface
type Rect = py.Rect
type Font = py.font.Font

py.init()
screen: SurfaceType = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Flappy Game - Login")

manager: pyg.UIManager = pyg.UIManager((WIDTH, HEIGHT))

font: Font = py.font.Font(resource_path("assets/font/font.ttf"), 24)

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

def draw_text(surface: SurfaceType, text: str, position: Tuple[int, int], color: Tuple[int, int, int]=(255, 255, 255)):
    """Helper function to render text."""
    label = font.render(text, True, color)
    surface.blit(label, position)

def draw_centered_text(surface: SurfaceType, text: str, centered_position: Tuple[int, int], font: Font, color: Tuple[int, int, int]=(255, 255, 255)):
    """Renders and draws text centered at the specific position."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=centered_position)
    surface.blit(text_surface, text_rect)

def _wrap_text_lines(text: str, font: Font, max_width: int) -> list[str]:
    """Split text into lines that fit max_width."""
    if max_width <= 0:
        return [text]
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        try_line = f"{cur} {w}".strip()
        if font.size(try_line)[0] <= max_width or not cur:
            cur = try_line
        else:
            lines.append(cur)
            cur = w

    if cur:
        lines.append(cur)
    return lines

def draw_wrapped_text(surface: SurfaceType, text: str, pos: Tuple[int, int], max_width: int, font: Font, color: Tuple[int, int, int]=(255, 255, 255), line_spacing: int = 4) -> int:
    """Draw word-wrapped text at pos within max_width. Returns total height drawn."""
    lines = _wrap_text_lines(text, font, max_width)
    x, y = pos
    line_h = font.get_linesize()
    for line in lines:
        surf = font.render(line, True, color)
        surface.blit(surf, (x, y))
        y += line_h + line_spacing
    total = len(lines) * line_h + (max(0, len(lines) - 1) * line_spacing)
    return total

def draw_label_above_input(surface: SurfaceType, text: str, label_left_x: int, input_rect: Rect | py.FRect, font: Font, color: Tuple[int, int, int]=(255, 255, 255), padding_right: int = 8) ->  None:
    """
    Draw a label to the left of an input. It wraps when it reaches the input,
    and is positioned so its bottom sits above the impit with a small margin.
    """
    max_width = max(0, int(input_rect.left) - int(label_left_x) - padding_right)
    # Measure wrapped height first to place it above the input.
    lines = _wrap_text_lines(text, font, max_width)
    line_h = font.get_linesize()
    total_h = len(lines) * line_h + (max(0, len(lines) - 1) * 4)


    start_y = int(input_rect.top) - (total_h // 2) + 17
    draw_wrapped_text(surface, text, (int(label_left_x), start_y), max_width, font, color)

def handle_login_page(state: Dict[str, str]) -> Dict[str, str]:
    """Login page - requires username/email + password"""
    py.display.set_caption("Flappy Game - Login")

    manager: pyg.UIManager = pyg.UIManager((WIDTH, HEIGHT))

    identifier_input: UItextEntryLineWithPlaceholder = UItextEntryLineWithPlaceholder(
        relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 80), (200, 40)),
        manager=manager
    )
    identifier_input.set_placeholder("Username or Email")

    password_input: UITextEntryLinePassword = UITextEntryLinePassword(
        relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 40)),
        manager=manager
    )
    password_input.set_placeholder("Enter password")

    login_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 30), (100, 40)),
        text="Login",
        manager=manager
    )

    signup_link_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 80), (150, 35)),
        text="Don't have an account?",
        manager=manager
    )
    
    eye_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 + 110, HEIGHT // 2 - 30), (30, 30)),
        text='',
        manager=manager,
        tool_tip_text="Show/Hide Password"
    )

    close_rect: Rect = close_img.get_rect(midtop=(20, 5))

    message: str = ""
    message_time: float = 0
    message_color: Tuple[int, int, int] = (255, 0, 0)

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
                    identifier = identifier_input.get_Real_text().strip()
                    password = password_input.get_real_text().strip()
                    
                    if not identifier or not password:
                        message = "Please enter username/email and password."
                        message_time = 3
                        message_color = (255, 0, 0)
                        continue
                    
                    data = login(identifier, password)
                    
                    if "error" in data:
                        message = f"Login failed: {data['error']}"
                        message_color = (255, 0, 0)
                    else:
                        message = data.get("message", "Login successful!")
                        message_color = (0, 255, 0)
                    message_time = 3
                    
                elif event.ui_element == signup_link_button:
                    state["current"] = "signup"
                    running = False
                    
                elif event.ui_element == eye_button:
                    password_input.show_password = not password_input.show_password
                    display_text = password_input.real_text if password_input.show_password else "*" * len(password_input.real_text)
                    password_input.set_text(display_text)
                    
            manager.process_events(event)

        if message_time > 0:
            message_time -= time_delta
        
        screen.fill((30, 30, 30))
        screen.blit(close_img, close_rect)
        draw_text(screen, "Login", (WIDTH // 2 - 35, HEIGHT // 2 - 120))
        draw_label_above_input(
            screen,
            "Username/Email:",
            WIDTH // 2 - 240,
            identifier_input.relative_rect,
            font
        )
        draw_label_above_input(
            screen,
            "Password:",
            WIDTH // 2 - 190,
            password_input.relative_rect,
            font
        )
        
        if message_time > 0:
            draw_centered_text(screen, message, (WIDTH // 2, HEIGHT // 2 + 130), font, color=message_color)
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        screen.blit(eye_img, eye_button.relative_rect.topleft)
        py.display.flip()
    
    return state

def handle_signup_page(state: Dict[str, str]) -> Dict[str, str]:
    """Signup page - requires username, email, and password"""
    py.display.set_caption("Flappy Game - Sign Up")
    
    manager: pyg.UIManager = pyg.UIManager((WIDTH, HEIGHT))
    
    username_input: UItextEntryLineWithPlaceholder = UItextEntryLineWithPlaceholder(
        relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 110), (200, 40)),
        manager=manager
    )
    username_input.set_placeholder("Enter Username")
    
    email_input: UItextEntryLineWithPlaceholder = UItextEntryLineWithPlaceholder(
        relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 60), (200, 40)),
        manager=manager
    )
    email_input.set_placeholder("Enter Email")
    
    password_input: UITextEntryLinePassword = UITextEntryLinePassword(
        relative_rect=py.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 10), (200, 40)),
        manager=manager
    )
    password_input.set_placeholder("Enter Password")
    
    signup_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 - 50, HEIGHT // 2 + 50), (100, 40)),
        text="Sign Up",
        manager=manager
    )
    
    login_link_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 100), (150, 35)),
        text="Already have an account?",
        manager=manager
    )
    
    eye_button: pyg.elements.UIButton = pyg.elements.UIButton(
        relative_rect=py.Rect((WIDTH // 2 + 110, HEIGHT // 2 - 10), (30, 30)),
        text='',
        manager=manager,
        tool_tip_text="Show/Hide Password"
    )
    
    close_rect: Rect = close_img.get_rect(midtop=(20, 5))
    
    message: str = ""
    message_time: float = 0
    message_color: Tuple[int, int, int] = (255, 0, 0)
    
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
                if event.ui_element == signup_button:
                    username = username_input.get_Real_text().strip()
                    email = email_input.get_Real_text().strip()
                    password = password_input.get_real_text().strip()
                    
                    if not username or not email or not password:
                        message = "Please fill in all fields."
                        message_time = 3
                        message_color = (255, 0, 0)
                        continue
                    
                    data = signup(username, email, password)
                    
                    if "error" in data:
                        message = f"Signup failed: {data['error']}"
                        message_color = (255, 0, 0)
                    else:
                        message = data.get("message", "Signup successful!")
                        message_color = (0, 255, 0)
                    message_time = 3
                    
                elif event.ui_element == login_link_button:
                    state["current"] = "login"
                    running = False
                    
                elif event.ui_element == eye_button:
                    password_input.show_password = not password_input.show_password
                    display_text = password_input.real_text if password_input.show_password else "*" * len(password_input.real_text)
                    password_input.set_text(display_text)
                    
            manager.process_events(event)
        
        if message_time > 0:
            message_time -= time_delta
        
        screen.fill((30, 30, 30))
        screen.blit(close_img, close_rect)
        draw_text(screen, "Sign Up", (WIDTH // 2 - 50, HEIGHT // 2 - 150))
        
        draw_label_above_input(
            screen,
            "Username:",
            WIDTH // 2 - 190,
            username_input.relative_rect,
            font
        )
        draw_label_above_input(
            screen,
            "Email:",
            WIDTH // 2 - 150,
            email_input.relative_rect,
            font
        )
        draw_label_above_input(
            screen,
            "Password:",
            WIDTH // 2 - 190,
            password_input.relative_rect,
            font
        )
        
        if message_time > 0:
            draw_centered_text(screen, message, (WIDTH // 2, HEIGHT // 2 + 150), font, color=message_color)
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        screen.blit(eye_img, eye_button.relative_rect.topleft)
        py.display.flip()
    
    return state

def handle_account(state: Dict[str, str]) -> Dict[str, str]:
    """Entry point - redirect to login page"""
    return handle_login_page(state)