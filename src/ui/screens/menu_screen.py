import pygame

from ui.components.button import Button
from ..sound_manager import SoundManager


class MenuScreen:

    def __init__(self, screen, save_exists=False):

        self.save_exists = save_exists

        self.screen = screen

        width = screen.get_width()
        height = screen.get_height()

        self.play_button = Button("Play", width // 2 - 100, 280, 200, 75)

        self.new_game_button = Button("New Game", width // 2 - 100, 370, 200, 75)

        self.tutorial_button = Button("Tutorial", width // 2 - 100, 460, 200, 75)

        self.shop_button = Button("Shop", width // 2 - 100, 550, 200, 75)

        self.settings_button = Button("Settings", width // 2 - 100, 640, 200, 75)

        self.exit_button = Button("Exit", width // 2 - 100, 730, 200, 75)

        self.title_font = pygame.font.Font("assets/fonts/title_font.ttf", 150)

        self.load_background()

        SoundManager.play_music("assets/music/menu_music.mp3")
    
    def load_background(self):

        self.background = pygame.image.load("assets/images/menu_back.png")

        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        
    def draw(self):

        self.screen.blit(self.background, (0, 0))
        
        shadow = self.title_font.render("Left No Crumbs", True, (82, 26, 75))

        title = self.title_font.render("Left No Crumbs", True, (217, 2, 192))

        title_rect = title.get_rect(center=(self.screen.get_width() // 2,150))
        shadow_rect = title.get_rect(center=(self.screen.get_width() // 2,153))
        
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, title_rect)

        if self.save_exists:
            self.play_button.draw(self.screen)

        if not self.save_exists:
            pygame.draw.rect(self.screen, (80, 80, 80), self.play_button.rect, border_radius=20)

        self.new_game_button.draw(self.screen)

        self.tutorial_button.draw(self.screen)

        self.shop_button.draw(self.screen)

        self.settings_button.draw(self.screen)

        self.exit_button.draw(self.screen)

    def handle_event(self, event):
        if self.play_button.is_clicked(event):
            return "play"
        if self.new_game_button.is_clicked(event):
            return "new_game"
        if self.tutorial_button.is_clicked(event):
            return "tutorial"
        if self.shop_button.is_clicked(event):
            return "shop"
        if self.settings_button.is_clicked(event):
            return "settings"
        if self.exit_button.is_clicked(event):
            return "quit"
        return None  
