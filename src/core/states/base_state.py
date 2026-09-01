from __future__ import annotations
from abc import ABC, abstractmethod
import pygame

class BaseState(ABC):
    def __init__(self) -> None:
        self.next_state: str | None = None  
        self.done:       bool       = False  

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    @abstractmethod
    def update(self, delta: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass