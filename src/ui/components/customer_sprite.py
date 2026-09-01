import pygame


class CustomerSprite:

    def __init__(self, images, font, size=(120, 150)):
        if isinstance(images, dict):
            self.images = images
        else:
            self.images = {"regular": images, "vip": images,}

        self.font = font
        self.size = size

        self.scaled_images = {}

        for key, image in self.images.items():
            self.scaled_images[key] = pygame.transform.smoothscale(image, self.size)

    def draw(self, screen, customer, x, y):

        customer_type = customer.get("type", "regular")

        image = self.scaled_images.get(customer_type, self.scaled_images["regular"])

        screen.blit(image, (x, y))

        patience = customer["patience_ratio"]

        bar_width = self.size[0]

        pygame.draw.rect(screen, (80, 80, 80), (x, y - 18, bar_width, 10))

        pygame.draw.rect(screen, (0, 255, 0), (x, y - 18, int(bar_width * patience), 10))

        if customer.get("is_vip", False):

            text = self.font.render("VIP", True, (255, 215, 0))

            screen.blit(text, (x, y - 50))
