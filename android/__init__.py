from __future__ import annotations

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

from game.config import WIDTH, HEIGHT
Window.size = (WIDTH, HEIGHT)

class FlappyGameWidget(Widget):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bird_y = HEIGHT / 2
        self.bird_vel = 0.0
        self.gravity = -800.0
        self.flap_impulses = 300.0

        with self.canvas:
            Color(0.2, 0.6, 1.0) # sky blue background
            self.bg = Rectangle(pos=(0, 0), size=(WIDTH, HEIGHT))
            Color(1, 1, 1)
            self.bird = Rectangle(pos=(100, self.bird_y), size=(50, 35))

        Clock.schedule_interval(self.update, 1 / 60.0)
    
    def on_touch_down(self, touch): # type: ignore
        
        self.bird_vel = self.flap_impulses

    def update(self, dt: float) -> None:
        self.bird_vel += self.gravity * dt
        self.bird_y += self.bird_vel * dt
        # clamp
        self.bird_y = max(0, min(HEIGHT - self.bird.size[1], self.bird_y))
        self.bird.pos = (100, self.bird_y)


class FlappyKivyApp(App):
    def build(self):
        self.title = "Flappy Game (Kivy prototype)"
        return FlappyGameWidget()


if __name__ == "__main__":
    FlappyKivyApp().run()