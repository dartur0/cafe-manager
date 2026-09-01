import pygame

from ui.components.button import Button


class PauseScreen:

    def __init__(self, screen, day_screen):

        self.screen = screen

        self.day_screen = day_screen

        width = screen.get_width()

        self.resume_button = Button("Resume", width // 2 - 150, 250, 300, 75)

        self.restart_button = Button("Restart", width // 2 - 150, 350, 300, 75)

        self.settings_button = Button("Settings", width // 2 - 150, 450, 300, 75)

        self.end_button = Button("End", width // 2 - 150, 550, 300, 75)

        self.font = pygame.font.Font("assets/fonts/title_font.ttf", 150)

    def draw(self):

        self.day_screen.draw()

        dark_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)

        dark_surface.fill((0, 0, 0, 100))

        self.screen.blit(dark_surface, (0, 0))

        shadow = self.font.render("Pause", True, (82, 26, 75))
        title = self.font.render("Pause", True, (217, 2, 192))

        rect = title.get_rect(center=(self.screen.get_width() // 2, 150))
        shadow_rect = title.get_rect(center=(self.screen.get_width() // 2,153))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, rect)

        self.resume_button.draw(self.screen)

        self.restart_button.draw(self.screen)

        self.settings_button.draw(self.screen)

        self.end_button.draw(self.screen)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                return "resume"

        if self.resume_button.is_clicked(event):
            return "resume"
        
        if self.restart_button.is_clicked(event):

            return "RESTART"
        
        if self.settings_button.is_clicked(event):

            return "settings"
        
        if self.end_button.is_clicked(event):

            return "end"

        return None
