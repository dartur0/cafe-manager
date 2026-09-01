from __future__ import annotations
import pygame

from core.states.base_state import BaseState
from ui.screens.pause_screen import PauseScreen


class PauseState(BaseState):
    def __init__(self, day_state=None) -> None:
        super().__init__()
        self._day_state = day_state
        self._pause_screen: PauseScreen | None = None

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        
        day_screen = None
        if self._day_state is not None and hasattr(self._day_state, "_day_screen"):
            day_screen = self._day_state._day_screen
            
        self._pause_screen = PauseScreen(screen, day_screen)

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._pause_screen is None:
            return

        action = self._pause_screen.handle_event(event)

        if action == "resume":
            self.next_state = "resume_game"

        elif action == "RESTART" or action == "restart":
            self.next_state = "restart"

        elif action == "settings":
            self.next_state = "settings"

        elif action == "end":
            self.next_state = "end"

    def update(self, delta: float) -> None:
        pass  

    def draw(self, surface: pygame.Surface) -> None:
        if self._pause_screen is not None and self._day_state is not None:
            if hasattr(self._day_state, "_day_screen") and self._day_state._day_screen is not None:
                self._day_state._day_screen.update_data(self._day_state.get_status())
            
            self._pause_screen.draw()