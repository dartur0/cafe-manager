from __future__ import annotations
import pygame

from states.base_state import BaseState
from ui.screens.tutorial_screen import TutorialScreen

TUTORIAL_STEPS = [
    {
        "step":        1,
        "title":       "Welcome to Left No Crumbs!",
        "text":        "You run a cozy café. Serve customers before they lose patience!",
        "highlight":   None,         
        "image":       "tutorial_welcome",
    },
    {
        "step":        2,
        "title":       "Customers",
        "text":        "Up to 4 customers can be in the café. Each has a patience bar — serve them quickly!",
        "highlight":   "customers",
        "image":       "tutorial_customers",
    },
    {
        "step":        3,
        "title":       "Espresso Machine",
        "text":        "Brew espresso first. Then add milk. Place it on the showcase.",
        "highlight":   "coffee_machine",
        "image":       "tutorial_coffee",
    },
    {
        "step":        4,
        "title":       "Assembling Cakes",
        "text":        "Pick a baseб add cream. Wait for it to bake, then move to showcase.",
        "highlight":   "cake_station",
        "image":       "tutorial_cake",
    },
    {
        "step":        5,
        "title":       "Showcase",
        "text":        "Ready products wait here. Click a customer to serve them from the showcase.",
        "highlight":   "showcase",
        "image":       "tutorial_showcase",
    },
    {
        "step":        6,
        "title":       "Stars",
        "text":        "Serve your daily goal to pass. The happier your customers, the more stars you earn!",
        "highlight":   None,
        "image":       "tutorial_stars",
    },
]


class TutorialState(BaseState):
    def __init__(self) -> None:
        super().__init__()
        self._current_step: int = 0  
        self._screen: TutorialScreen | None = None

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        self._screen = TutorialScreen(
            screen=screen,
            steps=TUTORIAL_STEPS,
            current_step=self._current_step,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._screen is None:
            return

        action = self._screen.handle_event(event)

        if action == "next":
            self._next_step()

        elif action == "back":
            self._prev_step()

        elif action == "skip":
            self.next_state = "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self._next_step()
            elif event.key == pygame.K_LEFT:
                self._prev_step()
            elif event.key == pygame.K_ESCAPE:
                self.next_state = "menu"

    def update(self, delta: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self._screen is not None:
            self._screen.draw()

    def _next_step(self) -> None:
        if self._current_step < len(TUTORIAL_STEPS) - 1:
            self._current_step += 1
            self._update_screen()
        else:
            self.next_state = "menu"

    def _prev_step(self) -> None:
        if self._current_step > 0:
            self._current_step -= 1
            self._update_screen()

    def _update_screen(self) -> None:
        if self._screen is not None:
            self._screen.update_step(self._current_step)

    def get_current_step_data(self) -> dict:
        step = TUTORIAL_STEPS[self._current_step]
        return {
            **step,
            "is_first":  self._current_step == 0,
            "is_last":   self._current_step == len(TUTORIAL_STEPS) - 1,
            "progress":  f"{self._current_step + 1} / {len(TUTORIAL_STEPS)}",
        }