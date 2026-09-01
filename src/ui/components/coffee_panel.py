from __future__ import annotations
import pygame

from ui.sound_manager import SoundManager
from core.entities.coffee import CoffeeType, COFFEE_CONFIGS
from core.decorators.milk_decorator import MilkType


class CoffeePanel:

    def __init__(self, screen, small_font, coffee_machine_image, cup_coffee_icon, cup_latte_icon, milk_regular_icon, milk_lactose_free_icon, milk_oat_icon, set_debug):
        self.screen = screen
        self.small_font = small_font

        self.label_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 20)

        self.tiny_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 15)
        self.set_debug = set_debug

        self.coffee_machine = coffee_machine_image
        self.cup_coffee_icon = cup_coffee_icon
        self.cup_latte_icon = cup_latte_icon

        self.milk_regular_icon = milk_regular_icon
        self.milk_lactose_free_icon = milk_lactose_free_icon
        self.milk_oat_icon = milk_oat_icon

        self.selected_coffee_type = None
        self.selected_milk_type = None

        self.showcase_coffees_ui = []

        self.coffee_brewing = False
        self.coffee_brew_started_at = 0
        self.coffee_brew_pending_type = None
        self.coffee_brew_pending_milk = None

        self.ready_cup_rects = []

        self.select_sound = self.load_sound("assets/sounds/click.wav")

        self.brew_sound = self.load_sound("assets/sounds/pour_sound.wav")

        self.ready_sound = self.load_sound("assets/sounds/done_sound.wav")

        self.ready_sound_played_for = set()

        self.coffee_buttons = [
            (CoffeeType.ESPRESSO, pygame.Rect(300, 680, 75, 65)),
            (CoffeeType.MILK_COFFEE, pygame.Rect(395, 680, 75, 65)),
        ]

        self.milk_rects = [
            (MilkType.REGULAR, pygame.Rect(270, 750, 70, 85)),
            (MilkType.LACTOSE_FREE, pygame.Rect(350, 750, 70, 85)),
            (MilkType.OAT, pygame.Rect(430, 750, 70, 85)),
        ]

        self.coffee_cup_rect = pygame.Rect(115, 715, 70, 70)

    def load_sound(self, path: str):

        return SoundManager.load_sound(path)


    def play_sound(self, sound):

        SoundManager.play_sound(sound)

    def get_ready_cup_slot_count(self, state) -> int:

        default_slots = 3

        if state is None:
            return default_slots

        coffee_machine = state.kitchen.coffee_machine

        for attr_name in ("max_ready_cups", "max_cups", "MAX_READY_CUPS"):

            if hasattr(coffee_machine, attr_name):

                try:
                    return int(getattr(coffee_machine, attr_name))

                except (TypeError, ValueError):
                    pass

        purchased = getattr(state, "_purchased", set())

        if "kitchen_coffee_slot" in purchased:
            return 4

        return default_slots

    def update(self, state):

        if state is None:
            return

        coffee_machine = state.kitchen.coffee_machine

        for cup in coffee_machine.ready_cups:

            cup_id = id(cup)

            if cup.is_ready and cup_id not in self.ready_sound_played_for:

                self.play_sound(self.ready_sound)

                self.ready_sound_played_for.add(cup_id)
                
    def start_brewing(self, state):

        if state is None:
            self.set_debug("DayState not found")
            return

        coffee_machine = state.kitchen.coffee_machine
        config = COFFEE_CONFIGS[self.selected_coffee_type]

        if coffee_machine.beans < config.needs_beans:
            self.set_debug("No beans: press REFILL")
            return

        max_ready_slots = self.get_ready_cup_slot_count(state)

        if len(coffee_machine.ready_cups) >= max_ready_slots:
            self.set_debug("Ready cups are full")
            return

        success, reason = state.player_brew(self.selected_coffee_type)

        if not success:
            self.set_debug(f"Cannot brew coffee: {reason}")
            return

        cup_index = len(coffee_machine.ready_cups) - 1

        if cup_index >= 0:
            cup = coffee_machine.ready_cups[cup_index]

            if self.selected_coffee_type == CoffeeType.ESPRESSO:
                cup.milk_type = None
            else:
                cup.milk_type = self.selected_milk_type

        self.play_sound(self.brew_sound)

        self.set_debug("Coffee brewing...")


    def move_ready_cup_to_showcase(self, state, cup_index) -> bool:

        if state is None:
            self.set_debug("DayState not found")
            return True

        coffee_machine = state.kitchen.coffee_machine
        showcase = state.kitchen.showcase

        if cup_index >= len(coffee_machine.ready_cups):
            self.set_debug("No ready cup in this slot")
            return True

        ready_cup = coffee_machine.ready_cups[cup_index]

        if not ready_cup.is_ready:
            self.set_debug("Coffee is not ready yet")
            return True

        total_showcase_items = (len(showcase.cake_items) + len(showcase.coffee_items))

        if total_showcase_items >= showcase.max_slots:
            self.set_debug("Showcase is full")
            return True

        coffee_type = ready_cup.coffee_type
        milk_type = ready_cup.milk_type

        if coffee_type == CoffeeType.ESPRESSO:
            ready_cup.milk_type = None
            milk_type = None

        is_milk_coffee = (coffee_type == CoffeeType.MILK_COFFEE)

        if is_milk_coffee:
            if milk_type is None:
                milk_type = self.selected_milk_type
                ready_cup.milk_type = milk_type

            if not ready_cup.milk_added:
                milk_added = coffee_machine.add_milk(cup_index, milk_type)
                if not milk_added:
                    self.set_debug("No milk: press REFILL")
                    return True

        product = coffee_machine.take_cup(cup_index)

        if product is None:
            self.set_debug("Could not take coffee cup")
            return True

        success = showcase.add_coffee(product, coffee_type)

        if success:
            self.showcase_coffees_ui.append({"coffee_type": coffee_type.value, "milk_type": milk_type.value if milk_type is not None else None,})

            self.play_sound(self.select_sound)

            self.set_debug("Coffee moved to showcase")

        else:
            self.set_debug("Could not move coffee to showcase")

        return True
    
    def draw(self, kitchen_status, state=None):
        self.ready_cup_rects.clear()

        self.screen.blit(self.coffee_machine, (30, 600))

        coffee_info = kitchen_status["coffee_machine"]

        if state is not None:
            backend_ready_cups = state.kitchen.coffee_machine.ready_cups
        else:
            backend_ready_cups = []

        beans = coffee_info["beans"]
        max_beans = coffee_info["max_beans"]

        beans_text = self.small_font.render(f"Beans: {beans}/{max_beans}",True, (0, 0, 0))

        self.screen.blit(beans_text, (87, 590))

        # wybor typu kawy
        for coffee_type, rect in self.coffee_buttons:

            pygame.draw.rect(self.screen, (255, 245, 255), rect, border_radius=10)

            pygame.draw.rect(self.screen, (217, 2, 192), rect, width=2, border_radius=10)

            if coffee_type == CoffeeType.ESPRESSO:
                icon = self.cup_coffee_icon
            else:
                icon = self.cup_latte_icon

            icon = pygame.transform.scale(icon, (42, 42))

            self.screen.blit(icon, (rect.centerx - 21, rect.y + 2))

            if coffee_type == CoffeeType.ESPRESSO:
                label_value = "ESP"
            else:
                label_value = "MILK"

            label = self.tiny_font.render(label_value, True, (82, 26, 75))

            label_rect = label.get_rect(midbottom=(rect.centerx, rect.bottom - 2))

            self.screen.blit(label, label_rect)

            if self.selected_coffee_type == coffee_type:
                pygame.draw.rect(self.screen, (0, 255, 0), rect, width=4, border_radius=10)

        # wybor mleka-
        milk_icons = {
            MilkType.REGULAR: self.milk_regular_icon,
            MilkType.LACTOSE_FREE: self.milk_lactose_free_icon,
            MilkType.OAT: self.milk_oat_icon,
        }

        for milk_type, rect in self.milk_rects:

            pygame.draw.rect(self.screen, (255, 245, 255), rect, border_radius=10)

            icon = milk_icons[milk_type]

            icon = pygame.transform.scale(icon, (80, 80))

            self.screen.blit(icon, (rect.x , rect.y - 5 ))

            if milk_type == MilkType.REGULAR:
                label_value = "REG"
            elif milk_type == MilkType.LACTOSE_FREE:
                label_value = "LACT_FR"
            else:
                label_value = "OAT"

            label = self.tiny_font.render(label_value, True, (82, 26, 75))

            label_rect = label.get_rect(midbottom=(rect.centerx, rect.bottom - 2))

            self.screen.blit(label, label_rect)

            if self.selected_milk_type == milk_type:
                pygame.draw.rect(self.screen, (0, 255, 0), rect, width=4, border_radius=10)

        # button brew
        brew_rect = self.coffee_cup_rect

        pygame.draw.rect(self.screen, (255, 245, 255), brew_rect, border_radius=12)

        pygame.draw.rect(self.screen, (217, 2, 192), brew_rect, width=2, border_radius=12)

        brew_icon = pygame.transform.scale(self.cup_coffee_icon, (40, 40))

        self.screen.blit(brew_icon, (brew_rect.centerx - 20, brew_rect.y + 4))

        brew_text = self.tiny_font.render("BREW", True, (82, 26, 75))

        brew_text_rect = brew_text.get_rect(midbottom=(brew_rect.centerx, brew_rect.bottom - 4))

        self.screen.blit(brew_text, brew_text_rect)

        # gotowe filizanki
        ready_slot_count = self.get_ready_cup_slot_count(state)

        if ready_slot_count <= 3:
            slot_size = 60
            slot_gap = 10
            start_x = 45
        else:
            slot_size = 52
            slot_gap = 8
            start_x = 35

        for i in range(ready_slot_count):

            rect = pygame.Rect(start_x + i * (slot_size + slot_gap), 645, slot_size, slot_size)

            pygame.draw.rect(self.screen, (255, 255, 255), rect, border_radius=10)

            pygame.draw.rect(self.screen, (217, 2, 192), rect, width=2, border_radius=10)

            if i >= len(backend_ready_cups):
                continue

            cup_obj = backend_ready_cups[i]

            if cup_obj.coffee_type == CoffeeType.MILK_COFFEE:
                cup_icon = self.cup_latte_icon
            else:
                cup_icon = self.cup_coffee_icon

            cup_icon_size = max(34, slot_size - 16)

            cup_icon = pygame.transform.scale(cup_icon, (cup_icon_size, cup_icon_size))

            self.screen.blit(cup_icon, (rect.centerx - cup_icon_size // 2, rect.y + 3))
            
            if cup_obj.is_ready:

                pygame.draw.rect(self.screen,
                    (0, 255, 0), rect, width=4, border_radius=10)
                ready_text = self.small_font.render("OK", True, (0, 120, 0))

                ready_rect = ready_text.get_rect(center=rect.center)

                self.screen.blit(ready_text, ready_rect)

                self.ready_cup_rects.append((i, rect))

            else:

                pygame.draw.rect(self.screen, (255, 180, 0), rect, width=4, border_radius=10)
                
                time_left = max(0.0, cup_obj.time_left)

                total_time = COFFEE_CONFIGS[cup_obj.coffee_type].base_time

                if total_time > 0:
                    progress = 1.0 - (time_left / total_time)
                else:
                    progress = 0.0

                progress = max(0.0, min(1.0, progress))

                bar_rect = pygame.Rect(rect.x + 5, rect.bottom - 9, rect.width - 10, 5)

                pygame.draw.rect(self.screen, (180, 180, 180), bar_rect, border_radius=3)

                fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * progress), bar_rect.height)

                pygame.draw.rect(self.screen, (0, 220, 100), fill_rect, border_radius=3)
                
                time_text = self.small_font.render(f"{time_left:.1f}", True, (82, 26, 75))

                time_rect = time_text.get_rect(center=rect.center)

                self.screen.blit(time_text, time_rect)

        # kawa do oddawania
        for i in range(3):
            rect = pygame.Rect(270 + i * 75, 600, 65, 65)

            pygame.draw.rect(self.screen, (240, 240, 240), rect, border_radius=10)

            pygame.draw.rect(self.screen, (217, 2, 192), rect, width=2, border_radius=10)

            if i < len(self.showcase_coffees_ui):

                coffee = self.showcase_coffees_ui[i]

                if coffee["coffee_type"] == CoffeeType.MILK_COFFEE.value:
                    icon = self.cup_latte_icon
                else:
                    icon = self.cup_coffee_icon

                icon = pygame.transform.scale(icon, (58, 58))

                self.screen.blit(icon, rect.topleft)

    def handle_event(self, event, state) -> bool:

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        pos = event.pos

        for coffee_type, rect in self.coffee_buttons:
            if rect.collidepoint(pos):
                self.selected_coffee_type = coffee_type

                if coffee_type == CoffeeType.ESPRESSO:
                    self.selected_milk_type = None

                self.play_sound(self.select_sound)
                self.set_debug(f"Selected coffee: {coffee_type.value}")
                return True

        for milk_type, rect in self.milk_rects:
            if rect.collidepoint(pos):
                
                if self.selected_coffee_type == CoffeeType.ESPRESSO:
                    self.set_debug("Espresso doesn't need milk!")
                    return True  

                self.selected_milk_type = milk_type
                self.play_sound(self.select_sound)
                self.set_debug(f"Selected milk: {milk_type.value}")
                return True

        for cup_index, rect in self.ready_cup_rects:
            if rect.collidepoint(pos):
                return self.move_ready_cup_to_showcase(state, cup_index)

        if self.coffee_cup_rect.collidepoint(pos):
            if self.selected_coffee_type is None:
                self.set_debug("Select coffee type first!")
                return True
                
            if self.selected_coffee_type == CoffeeType.MILK_COFFEE and self.selected_milk_type is None:
                self.set_debug("Select milk type for Milk Coffee!")
                return True

            self.start_brewing(state)
            return True

        return False
