import pygame

from ui.components.button import Button
from ui.components.shop_item import ShopItem
from ..sound_manager import SoundManager


class ShopScreen:

    def __init__(self, screen, upgrades, money):


        self.show_warning = False

        self.warning_time = 0

        self.warning_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 40)

        self.screen = screen

        width = screen.get_width()

        self.background = pygame.image.load("assets/images/shop_back.png")

        self.background = pygame.transform.scale(self.background,(screen.get_width(), screen.get_height()))

        self.font = pygame.font.Font("assets/fonts/title_font.ttf", 150)

        self.money_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 50)

        self.money = money

        self.upgrades = upgrades

        self.close_button = Button("X", width // 2 + 680, 35, 60, 60)

        self.items = []

        positions = [(120, 200), (460, 200), (800, 200), (1140, 200), (120, 440), (460, 440), (800, 440), (1140, 440),]

        for upgrade, pos in zip(upgrades, positions):

            self.items.append(ShopItem(upgrade, pos[0], pos[1]))

        SoundManager.play_music("assets/music/shop_music.mp3")

        try:
            self.no_money_sound = pygame.mixer.Sound("assets/sounds/no_money.wav")
        except Exception:
            self.no_money_sound = None
            print("[Sound Warning] Не удалось загрузить эффект 'assets/sounds/no_money.wav'")

    def draw(self):

        if self.show_warning:

            if pygame.time.get_ticks() - self.warning_time > 2000:
                self.show_warning = False

        self.screen.blit(self.background, (0, 0))

        shadow = self.font.render("Shop", True, (82, 26, 75))

        title = self.font.render("Shop", True, (217, 2, 192))

        rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        shadow_rect = title.get_rect(center=(self.screen.get_width() // 2,104))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(title, rect)


        money_text = self.money_font.render(f"${self.money}", True, (224, 172, 105))

        self.screen.blit(money_text, (80, 40))

        for item in self.items:

            item.draw(self.screen)

        self.close_button.draw(self.screen)

        if self.show_warning:

            warning_rect = pygame.Rect(self.screen.get_width() // 2 - 250, self.screen.get_height() // 2 - 80, 500, 160)

            pygame.draw.rect(self.screen, (252, 114, 236), warning_rect, border_radius=20)

            pygame.draw.rect(self.screen, (217, 2, 192), warning_rect, 3, border_radius=20)

            text = self.warning_font.render("Not enough money!", True, (82, 26, 75))

            text_rect = text.get_rect(center=warning_rect.center)

            self.screen.blit(text, text_rect)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                return "back"

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.close_button.is_clicked(event):

                return "back"
            
        for item in self.items:
            

            if item.is_clicked(event):

                if item.can_afford and not item.purchased:

                    return f"buy:{item.id}"

                else:

                    if self.no_money_sound is not None:
                            try:
                                self.no_money_sound.set_volume(SoundManager.sfx_volume)
                                self.no_money_sound.play()
                            except Exception:
                                pass

                    self.show_warning = True

                    self.warning_time = pygame.time.get_ticks()

        return None
    
    def update_data(self, upgrades, money):

        self.money = money

        self.upgrades = upgrades

        positions = [(120, 200), (460, 200), (800, 200), (1140, 200), (120, 440), (460, 440), (800, 440), (1140, 440),]

        self.items = []

        for upgrade, pos in zip(upgrades, positions):

            self.items.append(ShopItem(upgrade, pos[0], pos[1]))
