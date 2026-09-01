import pygame


class HUD:

    def __init__(self, title_font, font, big_font, star_icon):
        self.title_font = title_font
        self.font = font
        self.big_font = big_font
        self.star_icon = star_icon

    def draw(self, screen, day_number, money, time_left):

        title = self.title_font.render(f"Day {day_number}", True, (217,2,192))

        title_rect = title.get_rect(center=(screen.get_width() // 2,150))

        screen.blit(title, title_rect)

        money_text = self.font.render(f"${int(money)}", True, (255,255,255))

        screen.blit(money_text, (50,190))

        timer_text = self.big_font.render(str(int(time_left)), True, (255,255,255))

        screen.blit(timer_text, (40,20))
