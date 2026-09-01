from __future__ import annotations
import os
import pygame

from core.states.base_state import BaseState
from ui.screens.menu_screen import MenuScreen
from config import SAVE_PATH
from core.systems.save_manager import SaveManager

class MenuState(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self._menu_screen: MenuScreen | None = None

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        save_exists = os.path.exists(SAVE_PATH)
        self._menu_screen = MenuScreen(screen, save_exists=save_exists)

    def on_exit(self) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._menu_screen is None:
            return

        action = self._menu_screen.handle_event(event)

        if action == "play":
            self.next_state = "game_load"   

        elif action == "new_game":
            SaveManager.delete()
            self.next_state = "game"        

        elif action == "tutorial":
            self.next_state = "tutorial"

        elif action == "shop":
            self.next_state = "shop"

        elif action == "settings":
            self.next_state = "settings"

        elif action == "quit":
            self.done = True               

    def update(self, delta: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self._menu_screen is not None:
            self._menu_screen.draw()
