from __future__ import annotations
import pygame

from ui.sound_manager import SoundManager
from ui.animations import PopUpAnimation, PopDownAnimation

class CustomerPanel:

    def __init__(self, screen, font, small_font, customer_regular_icon, customer_vip_icon,):

        self.screen = screen
        self.font = font
        self.small_font = small_font

        self.customer_regular_icon = customer_regular_icon
        self.customer_vip_icon = customer_vip_icon

        self.customer_size = (400, 500)

        self.customer_positions = [(80, 180), (430, 180), (780, 180), (1130, 180),]

        self.hi_sound = self.load_sound("assets/sounds/hi_sound.wav")

        self.bye_sound = self.load_sound("assets/sounds/bye_sound.wav")

        self.angry_sound = self.load_sound("assets/sounds/angry_sound.wav")

        self.ak_sound = self.load_sound("assets/sounds/ak_sound.wav")

        self.previous_customers = {}
        self.served_slots = set()

        self.appear_animations = {}
        self.exit_animations = {}

    def load_sound(self, path: str):

        return SoundManager.load_sound(path)

    def play_sound(self, sound):

        SoundManager.play_sound(sound)
        
    def play_cannot_serve_sound(self):

        self.play_sound(self.ak_sound)

    def get_customer_signature(self, customer):

        if customer is None:
            return None

        return (customer.get("type", "regular"), customer.get("is_vip", False),)
    
    def get_customer_image_by_signature(self, signature):

        if signature is None:
            return self.customer_regular_icon

        customer_type = signature[0]

        if customer_type == "vip":
            return self.customer_vip_icon

        return self.customer_regular_icon

    def mark_served(self, slot_index: int):

        self.served_slots.add(slot_index)

        self.play_sound(self.bye_sound)

    def update(self, customer_slots):

        current_customers = {}

        for i, customer in enumerate(customer_slots):

            current_signature = self.get_customer_signature(customer)

            previous_signature = self.previous_customers.get(i)

            current_customers[i] = current_signature

            # new client
            if previous_signature is None and current_signature is not None:

                self.exit_animations.pop(i, None)

                self.appear_animations[i] = PopUpAnimation(duration_ms=650, start_offset_y=260, start_scale=0.75)

                self.play_sound(self.hi_sound)

            # leaving client
            if previous_signature is not None and current_signature is None:

                self.appear_animations.pop(i, None)

                self.exit_animations[i] = {"signature": previous_signature, "animation": PopDownAnimation(duration_ms=550, end_offset_y=260, end_scale=0.75)}

                if i in self.served_slots:

                    self.served_slots.discard(i)

                else:

                    self.play_sound(self.angry_sound)

        self.previous_customers = current_customers


    def draw(self, customer_slots):

        customer_rects = []

        # leaving client
        for i, exit_data in list(self.exit_animations.items()):

            if i >= len(self.customer_positions):
                continue

            x, y = self.customer_positions[i]

            signature = exit_data["signature"]
            animation = exit_data["animation"]

            image = self.get_customer_image_by_signature(signature)

            scale = animation.get_scale()
            offset_y = animation.get_offset_y()

            current_width = int(self.customer_size[0] * scale)

            current_height = int(self.customer_size[1] * scale)

            draw_x = x + (self.customer_size[0] - current_width) // 2

            draw_y = y + offset_y

            image = pygame.transform.smoothscale(image, (current_width, current_height))

            self.screen.blit(image, (draw_x, draw_y))

            if animation.is_finished():

                self.exit_animations.pop(i, None)

        # new client
        for i, customer in enumerate(customer_slots):

            if customer is None:
                continue

            if i >= len(self.customer_positions):
                continue

            x, y = self.customer_positions[i]

            customer_type = customer.get("type", "regular")

            if customer_type == "vip":
                image = self.customer_vip_icon
            else:
                image = self.customer_regular_icon

            animation = self.appear_animations.get(i)

            is_animation_finished = True

            draw_x = x
            draw_y = y

            current_width = self.customer_size[0]
            current_height = self.customer_size[1]

            if animation is not None:

                is_animation_finished = animation.is_finished()

                scale = animation.get_scale()
                offset_y = animation.get_offset_y()

                current_width = int(self.customer_size[0] * scale)

                current_height = int(self.customer_size[1] * scale)

                draw_x = x + (self.customer_size[0] - current_width) // 2

                draw_y = y + offset_y

                if is_animation_finished:

                    self.appear_animations.pop(i, None)

                    draw_x = x
                    draw_y = y

                    current_width = self.customer_size[0]
                    current_height = self.customer_size[1]

            image = pygame.transform.smoothscale(image, (current_width, current_height))

            self.screen.blit(image, (draw_x, draw_y))

            if not is_animation_finished:
                continue

            patience = customer.get("patience_ratio", 1.0)

            patience = max(0.0, min(1.0, patience))

            patience_bar_width = 100

            pygame.draw.rect(self.screen, (80, 80, 80), (x + 55, y - 18, patience_bar_width, 10))

            pygame.draw.rect(self.screen, (0, 255, 0), (x + 55, y - 18, int(patience_bar_width * patience), 10))

            if customer.get("is_vip", False):

                vip_text = self.small_font.render("VIP", True, (255, 215, 0))

                self.screen.blit(vip_text, (x, y - 45))

            rect = pygame.Rect(x, y, self.customer_size[0], self.customer_size[1])

            customer_rects.append((i, rect))

        return customer_rects
