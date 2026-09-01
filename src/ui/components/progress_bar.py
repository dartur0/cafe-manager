from __future__ import annotations

import pygame


class ProgressBar:
    def __init__(self, x: int, y: int, width: int, height: int, bg_color=(70, 70, 70), fill_color=(217, 2, 192), border_color=(255, 255, 255),):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color

    def draw(self, screen: pygame.Surface, value: float, max_value: float = 1.0,) -> None:
        if max_value <= 0:
            ratio = 0
        else:
            ratio = value / max_value

        ratio = max(0.0, min(1.0, ratio))

        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)

        fill_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * ratio), self.rect.height)

        pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=10)

        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=10)
