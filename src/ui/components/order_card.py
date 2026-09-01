from __future__ import annotations

import pygame


class OrderCard:
    def __init__(self, font: pygame.font.Font):
        self.font = font

    def draw_text_card(self, screen: pygame.Surface, text: str, x: int, y: int, width: int = 180, height: int = 60,) -> None:
        rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=12)

        pygame.draw.rect(screen, (217, 2, 192), rect, width=2, border_radius=12)

        text_surface = self.font.render(text, True, (82, 26, 75))

        text_rect = text_surface.get_rect(center=rect.center)

        screen.blit(text_surface, text_rect)
