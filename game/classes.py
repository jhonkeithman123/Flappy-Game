import pygame as py
import pygame_gui as pyg
from typing import Any, Optional, cast

py.init()

class UITextEntryLinePassword(pyg.elements.UITextEntryLine):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.real_text: str = ""
        self.placeholder: str = ""
        self.show_password: bool = False
        self.in_placeholder_mode: bool = True

    def set_placeholder(self, text: str) -> None:
        self.placeholder= text
        self.in_placeholder_mode = True
        self.real_text= ""
        super().set_text(text)

    def clear_text_for_input(self) -> None:
        if self.in_placeholder_mode:
            self.in_placeholder_mode = False
            self.real_text = ""
            super().set_text("")

    def process_event(self, event: py.event.Event) -> bool:
        focus_set = self.ui_manager.get_focus_set() if self.ui_manager else None
        has_focus = bool(focus_set and self in focus_set)

        rect: Optional[py.Rect] = cast(Optional[py.Rect], getattr(self, "rect", None))
        if self.in_placeholder_mode:
            if event.type == py.MOUSEBUTTONDOWN:
                if rect is not None and rect.collidepoint(event.pos):
                    self.clear_text_for_input()
            elif event.type == py.KEYDOWN:
                focus_set = self.ui_manager.get_focus_set() if self.ui_manager else None
                if focus_set and self in focus_set:
                    self.clear_text_for_input()

        if event.type == py.KEYDOWN and has_focus:
            if event.key == py.K_BACKSPACE:
                self.real_text = self.real_text[:-1]

            elif event.key == py.K_RETURN:
                pass

            elif len(event.unicode) > 0 and event.unicode.isprintable():
                self.real_text += event.unicode

            display_text = self.real_text if self.show_password else "*" * len(self.real_text)
            super().set_text(display_text)

            return True

        return super().process_event(event)
    
    def update(self, time_delta: float) -> None:
        if self.in_placeholder_mode:
            super().set_text(self.placeholder)
        else:
            display_text = self.real_text if self.show_password else "*" * len(self.real_text)
            super().set_text(display_text)

        super().update(time_delta)

    def get_real_text(self):
        return "" if self.in_placeholder_mode else self.real_text
    
class UItextEntryLineWithPlaceholder(pyg.elements.UITextEntryLine):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.placeholder: str = ""
        self.in_placeholder_mode: bool = True

    def set_placeholder(self, text: str) -> None:
        self.placeholder = text
        self.in_placeholder_mode = True
        super().set_text(text)

    def clear_text_for_input(self) -> None:
        if self.in_placeholder_mode:
            self.in_placeholder_mode = False
            super().set_text("")
    
    def process_event(self, event: py.event.Event) -> bool:
        rect: Optional[py.Rect] = cast(Optional[py.Rect], getattr(self, "rect", None))

        if self.in_placeholder_mode:
            if event.type == py.MOUSEBUTTONDOWN:
                # Only clear if mouse is inside this input's rectangle
                if rect is not None and rect.collidepoint(event.pos):
                    self.clear_text_for_input()
            elif event.type == py.KEYDOWN:
                # Only clear if this input is focused
                focus_set = self.ui_manager.get_focus_set() if self.ui_manager else None
                if focus_set and self in focus_set:
                    self.clear_text_for_input()

        return super().process_event(event)
    
    def get_Real_text(self) -> str:
        return "" if self.in_placeholder_mode else self.get_text()
