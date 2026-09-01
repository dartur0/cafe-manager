import pygame

from ui.sound_manager import SoundManager

class Button:
    def __init__(self, text, x, y, width, height):

        self.rect = pygame.Rect(x, y, width, height)

        self.font = pygame.font.Font("assets/fonts/Pacifico.ttf", 40)

        self.text = text

        self.color = (252, 114, 236)

        self.hover_color = (252, 68, 232) # 252, 129, 239

        self.border_color = (217, 2, 192)

        self.click_sound = pygame.mixer.Sound("assets/sounds/button_click.wav")

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.rect.collidepoint(mouse_pos)

        draw_rect = self.rect.copy()

        if hovered:

            for i in range(4):
                glow_rect = pygame.Rect(
                    draw_rect.x - i * 3,
                    draw_rect.y - i * 3,
                    draw_rect.width + i * 6,
                    draw_rect.height + i * 6
                )

                pygame.draw.rect(screen, (255, 182, 242), glow_rect, width=2, border_radius=25)

        draw_rect.inflate_ip(10, 10)

        current_color = (self.hover_color if hovered else self.color)

        pygame.draw.rect(screen, current_color, self.rect, border_radius=20)

        pygame.draw.rect(screen, self.border_color, self.rect, 3, border_radius=20)

        text_surface = self.font.render(self.text, True, (82, 26, 75))

        text_rect = text_surface.get_rect(center=draw_rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.rect.collidepoint(event.pos):

                    self.click_sound.set_volume(SoundManager.sfx_volume)

                    self.click_sound.play()

                    return True
        return False
