from __future__ import annotations
import pygame
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
os.chdir(project_root)
sys.path.append(os.path.abspath(os.path.join(script_dir, "..")))

from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS
from entities.kitchen import Kitchen
from states.base_state import BaseState
from states.menu_state import MenuState
from states.day_state import DayState
from states.pause_state import PauseState
from states.gameover_state import GameoverState
from states.shop_state import ShopState
from states.settings_state import SettingsState
from states.tutorial_state import TutorialState
from systems.save_manager import SaveManager

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(SCREEN_TITLE)

        self.screen = pygame.display.set_mode(
            (0, 0),
            pygame.FULLSCREEN
        )        
        self.clock   = pygame.time.Clock()
        self.running = True

        self.active_day_state: DayState | None = None

        self._current_state: BaseState = MenuState()
        self._current_state.on_enter()
        SettingsState.load_and_apply()

    def run(self) -> None:
        while self.running:
            delta = self.clock.tick(FPS) / 1000.0

            self._handle_events()
            self._update(delta)
            self._draw()
            self._check_state_change()

        pygame.quit()
        sys.exit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self._current_state.handle_event(event)

    def _update(self, delta: float) -> None:
        self._current_state.update(delta)
        if self._current_state.done:
            self.running = False
            
    def _draw(self) -> None:
        self._current_state.draw(self.screen)
        pygame.display.flip()

    def _check_state_change(self) -> None:
        next_name = self._current_state.next_state
        if next_name is None:
            return

        new_state = self._create_state(next_name)

        if new_state is None:
            print(f"[Game] Unknown state: '{next_name}' — ignored")
            self._current_state.next_state = None 
            return

        self._current_state.next_state = None
        self._current_state.on_exit()

        new_state.on_enter()
        self._current_state = new_state

    def _create_state(self, name: str) -> BaseState | None:
        if name == "menu":
            return MenuState()

        elif name == "game" or name == "game_load":
            save_data = SaveManager.load()
            self.active_day_state = DayState(save_data=save_data)
            return self.active_day_state

        elif name == "resume" or name == "resume_game":
            if self.active_day_state is not None:
                return self.active_day_state
            save_data = SaveManager.load()
            return DayState(save_data=save_data)

        elif name == "restart":
            save_data = SaveManager.load()
            self.active_day_state = DayState(save_data=save_data)
            return self.active_day_state

        elif name == "end":
            stats = {}
            day_screen = None
            
            if self.active_day_state is not None:
                if hasattr(self.active_day_state, "_end_day"):
                    self.active_day_state._end_day()
                    stats = self.active_day_state._final_stats
                else:
                    stats = getattr(self.active_day_state, "_final_stats", {})
                
                if hasattr(self.active_day_state, "_day_screen"):
                    day_screen = self.active_day_state._day_screen

            self.active_day_state = None
            
            return GameoverState(stats=stats, day_screen=day_screen)

        elif name == "pause":
            day_screen = None
            if self.active_day_state is not None and hasattr(self.active_day_state, "_day_screen"):
                day_screen = self.active_day_state._day_screen
                
            return PauseState(self.active_day_state)               
        elif name == "gameover":
            stats = {}
            day_screen = None 
            
            if isinstance(self._current_state, DayState):
                stats = self._current_state._final_stats
                if hasattr(self._current_state, "_day_screen"):
                    day_screen = self._current_state._day_screen
            
            return GameoverState(stats=stats, day_screen=day_screen)

        elif name == "shop":
            money     = 0.0
            purchased = set()
            kitchen   = None
            stars     = {}
            from_state = "menu" 

            if self.active_day_state is not None:
                money      = self.active_day_state.money_earned
                purchased  = self.active_day_state._purchased
                kitchen    = self.active_day_state.kitchen
                stars      = self.active_day_state._stars
                from_state = "menu" 

            elif isinstance(self._current_state, GameoverState):
                stats      = self._current_state._stats
                money      = stats.get("money_earned", stats.get("money", 0.0))
                purchased  = stats.get("purchased", set())
                stars      = stats.get("stars", {})
                from_state = "menu" 

            elif isinstance(self._current_state, MenuState):
                save_data = SaveManager.load()
                if save_data:
                    money     = save_data.money
                    purchased = save_data.purchased
                    stars     = save_data.stars
                from_state = "menu"

            if kitchen is None:
                kitchen = Kitchen()

            return ShopState(
                money=money,
                kitchen=kitchen,
                purchased=purchased,
                from_state=from_state,
            )

        elif name == "tutorial":
            return TutorialState()

        elif name == "settings":
            prev_screen = None
            from_state = "menu" 
            
            if isinstance(self._current_state, MenuState):
                prev_screen = self._current_state._menu_screen
                from_state = "menu"
            elif isinstance(self._current_state, PauseState):
                prev_screen = self._current_state._pause_screen
                from_state = "pause" 
                
            return SettingsState(from_state=from_state, prev_screen=prev_screen)

        return None
    
if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
