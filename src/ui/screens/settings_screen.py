import pygame

from ui.components.button import Button
from ui.sound_manager import SoundManager


class SettingsScreen:

    def __init__(self, screen, music_volume, sfx_volume):

        self.screen = screen

        self.music_volume = music_volume
        self.sfx_volume = sfx_volume

        self.font = pygame.font.Font("assets/fonts/title_font.ttf", 150)

        self.small_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 40)

        self.back_button = Button("Back", screen.get_width() // 2 - 100, 550, 200, 60)

        self.slider_rect = pygame.Rect(screen.get_width() // 2 - 200, 300, 400, 8)

        self.sfx_slider_rect = pygame.Rect(screen.get_width() // 2 - 200, 430, 400, 8)

        self.knob_x = (self.slider_rect.x + int(music_volume * self.slider_rect.width))

        self.sfx_knob_x = (self.sfx_slider_rect.x + int(sfx_volume * self.sfx_slider_rect.width))

        self.knob_radius = 15

        self.dragging_music = False

        self.dragging_sfx = False

    def draw(self):

        dark_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)

        dark_surface.fill((0, 0, 0, 120))

        self.screen.blit(dark_surface, (0, 0))

        settings_rect = pygame.Rect(self.screen.get_width() // 2 - 350, 120, 700, 500)

        shadow_rect = settings_rect.copy()

        shadow_rect.x += 5
        shadow_rect.y += 5

        pygame.draw.rect(self.screen, (64, 22, 53), shadow_rect, border_radius=30)

        pygame.draw.rect(self.screen, (143, 17, 128), settings_rect, border_radius=30)

        shadow = self.font.render("Settings", True, (82, 26, 75))

        title = self.font.render("Settings", True, (217, 2, 192))

        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 120))
        shadow_rect = title.get_rect(center=(self.screen.get_width() // 2,123))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        volume_text = self.small_font.render("Music Volume", True, (26, 3, 23))

        sfx_text = self.small_font.render("SFX Volume", True, (26, 3, 23))

        self.screen.blit(sfx_text, (self.sfx_slider_rect.x, self.sfx_slider_rect.y - 70))

        self.screen.blit(volume_text, (self.slider_rect.x, self.slider_rect.y - 70))

        pygame.draw.rect(self.screen, (120, 80, 110), self.slider_rect, border_radius=10)

        pygame.draw.rect(self.screen, (120, 80, 110), self.sfx_slider_rect, border_radius=10)

        pygame.draw.circle(self.screen, (252, 114, 236), (self.knob_x, self.slider_rect.centery), self.knob_radius)

        pygame.draw.circle(self.screen, (252, 114, 236), (self.sfx_knob_x, self.sfx_slider_rect.centery), self.knob_radius)

        self.back_button.draw(self.screen)

    def handle_event(self, event):

        if self.back_button.is_clicked(event):
            return "back"

        if event.type == pygame.MOUSEBUTTONDOWN:

            music_knob_rect = pygame.Rect(self.knob_x - self.knob_radius, self.slider_rect.centery - 15, 30, 30)

            sfx_knob_rect = pygame.Rect(self.sfx_knob_x - self.knob_radius, self.sfx_slider_rect.centery - 15, 30, 30)

            if music_knob_rect.collidepoint(event.pos):
                self.dragging_music = True

            elif sfx_knob_rect.collidepoint(event.pos):
                self.dragging_sfx = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging_music = False
            self.dragging_sfx = False

        if event.type == pygame.MOUSEMOTION:

            if self.dragging_music:

                self.knob_x = max(self.slider_rect.left, min(event.pos[0], self.slider_rect.right))

                volume = ((self.knob_x - self.slider_rect.left) / self.slider_rect.width)

                return {"music": volume}

            if self.dragging_sfx:

                self.sfx_knob_x = max(self.sfx_slider_rect.left, min(event.pos[0], self.sfx_slider_rect.right))

                volume = ((self.sfx_knob_x - self.sfx_slider_rect.left) / self.sfx_slider_rect.width)

                return {"sfx": volume}

        return None
    

