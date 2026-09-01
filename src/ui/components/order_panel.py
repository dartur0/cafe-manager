from __future__ import annotations
import pygame


class OrderPanel:

    def __init__(self, screen: pygame.Surface, small_font: pygame.font.Font) -> None:

        self.screen = screen
        self.small_font = small_font

        self.card_width = 180
        self.line_height = self.small_font.get_linesize()
        self.padding_x = 12
        self.padding_y = 12

        self.card_offset_x = -110
        self.card_offset_y = -20

        self.bg_color = (255, 245, 255)
        self.border_color = (217, 2, 192)
        self.text_color = (82, 26, 75)

    def get_order_text_lines(self, order) -> list[str]:

        if order is None:
            return ["No order"]

        lines = [order.order_type.value.upper()]

        if order.flavour is not None:
            lines.append(order.flavour.value.replace("_", " "))

        if order.cream is not None:
            lines.append(order.cream.value.replace("_", " "))

        if order.coffee_type is not None:
            lines.append(order.coffee_type.value.replace("_", " "))

        if order.milk_type is not None:
            lines.append(order.milk_type.value.replace("_", " "))

        return lines

    def get_card_size(self, lines: list[str]) -> tuple[int, int]:

        width = self.card_width

        for line in lines:
            text_width = self.small_font.size(line)[0]

            width = max(width, text_width + self.padding_x * 2)

        height = (self.padding_y * 2 + len(lines) * self.line_height)

        return width, height

    def get_card_position(self, customer_rect: pygame.Rect, card_width: int, card_height: int) -> tuple[int, int]:

        x = customer_rect.x + 70 + self.card_offset_x
        y = customer_rect.y - card_height - 42 + self.card_offset_y

        if y < 85:
            y = customer_rect.y + 30 + self.card_offset_y

        max_x = self.screen.get_width() - card_width - 10

        if x > max_x:
            x = max_x

        if x < 10:
            x = 10

        return x, y

    def draw_order_card(self, order, x: int, y: int) -> None:

        lines = self.get_order_text_lines(order)

        card_width, card_height = self.get_card_size(lines)

        rect = pygame.Rect(x, y, card_width, card_height)

        pygame.draw.rect(self.screen, self.bg_color, rect, border_radius=12)

        pygame.draw.rect(self.screen, self.border_color, rect, width=2, border_radius=12)

        for i, line in enumerate(lines):

            text = self.small_font.render(line, True, self.text_color)

            self.screen.blit(text, (rect.x + self.padding_x, rect.y + self.padding_y + i * self.line_height))

    def draw(self, customer_rects: list[tuple[int, pygame.Rect]], get_customer_object) -> None:

        for slot_index, customer_rect in customer_rects:

            customer_obj = get_customer_object(slot_index)

            if customer_obj is None:
                continue

            order = customer_obj.order

            lines = self.get_order_text_lines(order)

            card_width, card_height = self.get_card_size(lines)

            x, y = self.get_card_position(customer_rect, card_width, card_height)

            self.draw_order_card(order, x, y)
