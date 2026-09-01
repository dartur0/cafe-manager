from __future__ import annotations
import pygame


class PopUpAnimation:

    def __init__(self, duration_ms: int = 650, start_offset_y: int = 260, start_scale: float = 0.75):

        self.start_time = pygame.time.get_ticks()
        self.duration_ms = duration_ms
        self.start_offset_y = start_offset_y
        self.start_scale = start_scale

    def get_progress(self) -> float:

        now = pygame.time.get_ticks()

        progress = (now - self.start_time) / self.duration_ms

        return max(0.0, min(1.0, progress))

    def ease_out(self, value: float) -> float:

        return 1.0 - pow(1.0 - value,3)

    def get_offset_y(self) -> int:

        progress = self.ease_out(self.get_progress())

        return int(self.start_offset_y * (1.0 - progress))

    def get_scale(self) -> float:

        progress = self.ease_out(self.get_progress())

        return self.start_scale + (1.0 - self.start_scale) * progress

    def is_finished(self) -> bool:

        return self.get_progress() >= 1.0
    
class PopDownAnimation:

    def __init__(self, duration_ms: int = 550, end_offset_y: int = 260, end_scale: float = 0.75):

        self.start_time = pygame.time.get_ticks()
        self.duration_ms = duration_ms
        self.end_offset_y = end_offset_y
        self.end_scale = end_scale

    def get_progress(self) -> float:

        now = pygame.time.get_ticks()

        progress = (now - self.start_time) / self.duration_ms

        return max(0.0, min(1.0, progress))

    def ease_in(self, value: float) -> float:

        return value * value

    def get_offset_y(self) -> int:

        progress = self.ease_in(self.get_progress())

        return int(self.end_offset_y * progress)

    def get_scale(self) -> float:

        progress = self.ease_in(self.get_progress())

        return 1.0 - (
            1.0 - self.end_scale
        ) * progress

    def is_finished(self) -> bool:

        return self.get_progress() >= 1.0
