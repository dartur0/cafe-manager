import pygame


class PauseButton:

    def __init__(self):

        self.rect = pygame.Rect(20, 20, 70, 70)

        self.font = pygame.font.Font(None, 80)

        self.text = "II"

        self.color = (252, 114, 236)

        self.hover_color = (252, 68, 232)

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.rect.collidepoint(mouse_pos)

        current_color = (self.hover_color if hovered else self.color)

        if hovered:
            
            for i in range(4):
                pygame.draw.circle(screen, (255, 182, 242), self.rect.center, 35 + i * 3, 2)

        pygame.draw.circle(screen, current_color, self.rect.center, 35)

        text_surface = self.font.render(self.text, True, (82, 26, 75))

        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                return self.rect.collidepoint(event.pos)

        return False
