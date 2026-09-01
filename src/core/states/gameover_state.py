from __future__ import annotations
import pygame

from core.states.base_state import BaseState
from ui.screens.gameover_screen import GameOverScreen
from core.systems.level import calculate_stars, is_last_level

class GameoverState(BaseState):

    def __init__(self, stats: dict | None = None, day_screen=None) -> None:
        super().__init__()
        self._stats  = stats or {}
        self._stars  = 0
        self._day_screen = day_screen 
        self._screen: GameOverScreen | None = None

    def on_enter(self) -> None:
        self._stars = calculate_stars(
            served_count=self._stats.get("served_count", 0),
            customers_goal=self._stats.get("customers_goal", 1),
            avg_patience=self._stats.get("avg_patience", 0.0),
        )

        screen = pygame.display.get_surface()
        
        self._screen = GameOverScreen(
            screen=screen,
            stats=self._stats,
            stars=self._stars,
            is_loss=self._stars == 0,
            is_last=is_last_level(self._stats.get("day_number", 1)),
            day_screen=self._day_screen 
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._screen is None:
            return

        action = self._screen.handle_event(event)

        if action == "next_day":
            self.next_state = "game"

        elif action == "shop":
            self.next_state = "shop"

        elif action == "menu":
            self.next_state = "menu"

        elif action == "retry":
            self.next_state = "game"   

    def update(self, delta: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self._screen is not None:
            self._screen.draw()

    @property
    def stars(self) -> int:
        return self._stars

    @property
    def is_loss(self) -> bool:
        return self._stars == 0