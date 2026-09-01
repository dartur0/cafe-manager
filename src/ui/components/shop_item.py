import pygame


class ShopItem:

    def __init__(self, upgrade, x, y):
        self.id = upgrade["id"]

        self.name = upgrade["name"]

        self.price = upgrade["price"]

        self.purchased = upgrade["purchased"]

        self.can_afford = upgrade["can_afford"]

        self.rect = pygame.Rect(x,y, 300, 200)

        self.font = pygame.font.Font("assets/fonts/Pacifico.ttf", 30)

        self.color = (240, 128, 242)

        self.hover_color = (252, 61, 255) # 252, 129, 239

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        hovered = self.rect.collidepoint(mouse_pos)

        draw_rect = self.rect.copy()

        if hovered:

            for i in range(3):
                glow_rect = pygame.Rect(draw_rect.x - i * 3, draw_rect.y - i * 3, draw_rect.width + i * 6, draw_rect.height + i * 6)
                pygame.draw.rect(screen, (248, 25, 252), glow_rect, width=2, border_radius=25)

        draw_rect.inflate_ip(10, 10)

        current_color = (self.hover_color if hovered else self.color)

        if self.purchased:
            current_color = (120, 120, 120)

        elif not self.can_afford:
            current_color = (180, 100, 140)

        pygame.draw.rect( screen, current_color, self.rect, border_radius=20)

        name = self.font.render(self.name, True, (82, 26, 75))

        price = self.font.render(f"${self.price}", True, (82, 26, 75))

        screen.blit(name, (self.rect.x + 20, self.rect.y + 30))

        screen.blit(price, (self.rect.x + 20, self.rect.y + 90))

        if self.purchased:

            status = self.font.render("BOUGHT", True, (255, 255, 255))

            screen.blit(status, (self.rect.x + 20, self.rect.y + 140))

        elif not self.can_afford:

            status = self.font.render("LOCKED", True, (255, 255, 255))

            screen.blit(status, (self.rect.x + 20, self.rect.y + 140))

        if self.purchased:

            dark_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

            dark_surface.fill((0, 0, 0, 120))

            screen.blit(dark_surface, self.rect.topleft)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            return self.rect.collidepoint(event.pos)

        return False
