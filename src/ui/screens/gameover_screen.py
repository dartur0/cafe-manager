import pygame

from ui.components.button import Button
from ui.sound_manager import SoundManager

class GameOverScreen:

    def __init__(self, screen, stats, stars, is_loss, is_last, day_screen):
        self.screen = screen

        self.stats = stats

        self.stars = stars

        self.is_loss = is_loss

        self.is_last = is_last
        self.day_screen = day_screen

        self.day_number = stats.get("day_number", 1)

        self.served = stats.get("served_count", 0)

        self.total_customers = stats.get("customers_goal", 0)

        self.left = max(0, self.total_customers - self.served)

        self.title_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 70)

        self.star_font = pygame.font.Font(None, 80)

        self.stats_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 50)

        width = screen.get_width()

        self.next_button = Button("Next Day", width // 2 - 260, 580, 180, 75)

        self.retry_button = Button("Retry", width // 2 - 260, 580, 180, 75)

        self.shop_button = Button("Shop", width // 2 + 40, 580, 180, 75)

        self.menu_button = Button("Menu", width // 2 - 110, 680, 180, 75)

        self.gold_star = pygame.image.load( "assets/images/star_gold.png").convert_alpha()

        self.gray_star = pygame.image.load("assets/images/star_gray.png").convert_alpha()

        self.gold_star = pygame.transform.scale(self.gold_star, (200, 200))

        self.gray_star = pygame.transform.scale(self.gray_star, (200, 200))

        if self.is_loss:
            SoundManager.play_music("assets/music/zero_music.mp3")

        elif self.stars == 1:
            SoundManager.play_music("assets/music/one_music.mp3")

        else:
            SoundManager.play_music("assets/music/gameover_music.mp3")

    def draw(self):

        if self.day_screen:
            self.day_screen.draw()

        dark_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)

        dark_surface.fill((0, 0, 0, 140))

        self.screen.blit(dark_surface, (0, 0))

        window_rect = pygame.Rect(self.screen.get_width() // 2 - 400, 80,  800, 720)

        pygame.draw.rect(self.screen, (48, 166, 201), window_rect,border_radius=30)

        if self.is_loss:
            title_text = "Day Failed!"

        else:
            title_text = (f"Day {self.day_number} is Complete!")

        shadow = self.title_font.render(title_text, True, (82, 26, 75))
        title = self.title_font.render(title_text, True, (217, 2, 192))

        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 170))
        shadow_rect = title.get_rect(center=(self.screen.get_width() // 2,173))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title,title_rect)

        star_y = 210
        star_x = self.screen.get_width() // 2 - 300

        for i in range(3):

            if i < self.stars:
                star_image = self.gold_star

            else:
                star_image = self.gray_star

            self.screen.blit(star_image, (star_x + i * 200, star_y))

        served_text = self.stats_font.render(f"Served: {self.served}/{self.total_customers}", True, (255, 255, 255))

        left_text = self.stats_font.render(f"Left: {self.left}", True, (255, 255, 255))

        self.screen.blit(served_text, (self.screen.get_width() // 2 - 150, 400))

        self.screen.blit(left_text, (self.screen.get_width() // 2 - 90, 460))

        if self.is_loss:
            self.retry_button.draw(self.screen)

        elif not self.is_last:
            self.next_button.draw(self.screen)

        self.shop_button.draw(self.screen)

        self.menu_button.draw(self.screen)

    def handle_event(self, event):

        if self.next_button.is_clicked(event):
            return "next_day"
        
        if self.retry_button.is_clicked(event):
            return "retry"

        if self.shop_button.is_clicked(event):
            return "shop"

        if self.menu_button.is_clicked(event):
            return "menu"

        return None

