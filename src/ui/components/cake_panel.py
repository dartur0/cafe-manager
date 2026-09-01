from __future__ import annotations
import pygame

from ui.sound_manager import SoundManager
from core.entities.cake import FlavourType, build_cake
from core.decorators.cream_decorator import CreamType


class CakePanel:

    def __init__(self, screen, font, small_font, cake_station_image, base_icons, cream_icons, storage_icon, cake_images, set_debug):

        self.screen = screen
        self.font = font
        self.small_font = small_font
        self.set_debug = set_debug

        self.tiny_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 13)

        self.base_labels = {
            FlavourType.VANILLA: "VANILLA",
            FlavourType.CHOCOLATE: "CHOC",
            FlavourType.RED_VELVET: "RED",
            FlavourType.CARROT_CAKE: "CARROT",
        }

        self.cream_labels = {
            CreamType.VANILLA: "VANILLA",
            CreamType.CHOCOLATE: "CHOC",
            CreamType.STRAWBERRY: "STRAWB",
            CreamType.BANANA: "BANANA",
            CreamType.BLUEBERRY: "BLUEB",
            CreamType.PISTACHIO: "PISTACH",
        }

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.cake_station = cake_station_image
        self.base_icons = base_icons
        self.cream_icons = cream_icons
        self.storage_icon = storage_icon
        self.cake_images = cake_images

        self.selected_flavour = None
        self.selected_cream = None

        self.cake_slot_rects = []
        self.cake_slot_recipes = {}

        self.showcase_cakes_ui = []

        self.select_sound = self.load_sound("assets/sounds/click.wav")

        self.cake_ready_sound = self.load_sound("assets/sounds/done_sound.wav")

        self.cake_move_sound = self.load_sound("assets/sounds/click.wav")

        self.cake_sound_generation = 0
        self.cake_slot_generations = {}
        self.ready_sound_played_for = set()

        self.flavours = [
            FlavourType.VANILLA,
            FlavourType.CHOCOLATE,
            FlavourType.RED_VELVET,
            FlavourType.CARROT_CAKE,
        ]

        self.creams = [
            CreamType.VANILLA,
            CreamType.CHOCOLATE,
            CreamType.STRAWBERRY,
            CreamType.BANANA,
            CreamType.BLUEBERRY,
            CreamType.PISTACHIO,
        ]

        self.base_rects = []

        base_x = self.width - 580

        for i in range(4):
            rect = pygame.Rect(base_x + i * 125, self.height - 300, 118, 118)
            self.base_rects.append(rect)

        self.cream_rects = []

        cream_x = self.width - 630

        for i in range(6):
            rect = pygame.Rect(cream_x + i * 105, self.height - 155, 102, 102)

            self.cream_rects.append(rect)

        self.refill_resources_rect = pygame.Rect(self.width - 900, self.height - 80, 190, 42)

    def load_sound(self, path: str):

        return SoundManager.load_sound(path)


    def play_sound(self, sound):

        SoundManager.play_sound(sound)

    def get_base_stock(self, flavour, kitchen_status):

        base_storage = kitchen_status.get("base_storage", {})

        stock = base_storage.get("stock", {})

        return stock.get(flavour.value, 0)

    def get_cream_status(self, state):

        if state is None:
            return None, None

        try:
            return state.kitchen.cream, state.kitchen.max_cream
        except AttributeError:
            return None, None

    def get_selected_cake_time(self, state):

        if self.selected_flavour is None:
            return None

        if self.selected_cream is None:
            return None

        try:
            unlocked_flavours = None
            unlocked_creams = None

            if state is not None:

                if hasattr(state, "_get_unlocked_flavours"):
                    unlocked_flavours = state._get_unlocked_flavours()

                if hasattr(state, "_get_unlocked_creams"):
                    unlocked_creams = state._get_unlocked_creams()

            product = build_cake(self.selected_flavour, self.selected_cream, unlocked_flavours, unlocked_creams)

            return product.get_prep_time()

        except Exception:
            return None

    def draw_refill_button(self):

        pygame.draw.rect(self.screen, (255, 245, 255), self.refill_resources_rect, border_radius=12)

        pygame.draw.rect(self.screen, (217, 2, 192), self.refill_resources_rect, width=3, border_radius=12)

        text = self.small_font.render("REFILL", True, (82, 26, 75))

        text_rect = text.get_rect(center=self.refill_resources_rect.center)

        self.screen.blit(text, text_rect)

    def draw_cream_status(self, state):

        cream, max_cream = self.get_cream_status(state)

        if cream is None:
            return

        text = self.small_font.render(f"Cream: {cream}/{max_cream}", True, (82, 26, 75))

        self.screen.blit(text, (self.refill_resources_rect.x, self.refill_resources_rect.y - 35))

    def draw_cake_slots(self, cake_station, state=None):

        self.cake_slot_rects.clear()

        width = self.screen.get_width()
        center_x = width // 2

        self.screen.blit(self.cake_station, (center_x - 170, 780))

        purchased = getattr(state, "_purchased", set())

        real_slot_count = len(cake_station)

        display_slot_count = real_slot_count

        if "kitchen_cake_slot" in purchased:
            display_slot_count = max(display_slot_count, 3)

        slot_size = 90
        slot_gap = 30

        total_width = (display_slot_count * slot_size + (display_slot_count - 1) * slot_gap)
        
        start_x = center_x - total_width // 2
        y = 700

        for i in range(display_slot_count):

            x = start_x + i * (slot_size + slot_gap)

            rect = pygame.Rect(x, y, slot_size, slot_size)

            is_real_slot = i < real_slot_count

            if is_real_slot:

                slot = cake_station[i]

                self.cake_slot_rects.append((slot["slot_id"], rect))

            else:

                slot = None

            pygame.draw.rect(self.screen, (255, 240, 255), rect, border_radius=12)

            pygame.draw.rect(self.screen, (217, 2, 192), rect, width=3, border_radius=12)

            if not is_real_slot:

                text = self.tiny_font.render("+ SLOT", True, (82, 26, 75))

                text_rect = text.get_rect(center=rect.center)

                self.screen.blit(text, text_rect)

                continue

            if not slot["is_busy"]:
                continue

            time_total = slot.get("time_total", 0)
            time_left = slot.get("time_left", 0)

            if slot["is_ready"]:
                text_value = "READY"
                text_font = self.tiny_font
            else:
                text_value = f"{time_left:.1f}"
                text_font = self.font

            text = text_font.render(text_value, True, (82, 26, 75))

            text_rect = text.get_rect(center=rect.center)

            self.screen.blit(text, text_rect)

            if slot["is_ready"]:

                generation = self.cake_slot_generations.get(slot["slot_id"])

                ready_key = (slot["slot_id"], generation)

                if generation is not None and ready_key not in self.ready_sound_played_for:

                    self.play_sound(self.cake_ready_sound)

                    self.ready_sound_played_for.add(ready_key)

                pygame.draw.rect(self.screen, (0, 255, 0), rect, width=4, border_radius=12)

            else:

                if time_total > 0:
                    progress = 1.0 - (time_left / time_total)
                else:
                    progress = 0.0

                progress = max(0.0, min(1.0, progress))

                bar_rect = pygame.Rect(rect.x + 8, rect.bottom - 14, rect.width - 16, 8)

                pygame.draw.rect(self.screen, (180, 180, 180), bar_rect, border_radius=4)

                fill_rect = pygame.Rect(bar_rect.x, bar_rect.y, int(bar_rect.width * progress), bar_rect.height)

                pygame.draw.rect(self.screen, (0, 220, 100), fill_rect, border_radius=4)

    def draw_showcase(self, kitchen_status):

        width = self.screen.get_width()
        center_x = width // 2

        showcase_status = kitchen_status.get("showcase", {})

        max_slots = showcase_status.get("max_slots", 6)

        slot_size = 65
        slot_gap = 12

        showcase_width = (max_slots * slot_size + (max_slots - 1) * slot_gap)

        showcase_start_x = center_x - (showcase_width // 2)

        for i in range(max_slots):

            showcase_rect = pygame.Rect(showcase_start_x + i * (slot_size + slot_gap), 600, slot_size, slot_size)

            pygame.draw.rect(self.screen, (255, 255, 255), showcase_rect, border_radius=10)

            pygame.draw.rect(self.screen, (217, 2, 192), showcase_rect, width=2, border_radius=10)

            if i < len(self.showcase_cakes_ui):

                cake = self.showcase_cakes_ui[i]

                key = (cake["flavour"], cake["cream"])

                image = self.cake_images.get(key, self.storage_icon)

                image = pygame.transform.scale(image, (60, 60))

                self.screen.blit(image, showcase_rect.topleft)

    def draw_selected_time(self, state):

        selected_time = self.get_selected_cake_time(state)

        if selected_time is None:
            return

        time_text = self.small_font.render(f"Cake time: {selected_time:.1f}s", True, (255, 255, 255))

        self.screen.blit(time_text, (self.refill_resources_rect.x, self.refill_resources_rect.y - 28))

    def draw_button_label(self, rect, text: str):

        label = self.tiny_font.render(text, True, (82, 26, 75))

        label_rect = label.get_rect(midbottom=(rect.centerx, rect.bottom - 4))

        pygame.draw.rect(self.screen, (255, 245, 255), label_rect.inflate(10, 4), border_radius=6)

        self.screen.blit(label, label_rect)

    def draw_base_selection(self,kitchen_status):

        for i, rect in enumerate(self.base_rects):

            flavour = self.flavours[i]

            icon = self.base_icons[flavour]
            
            icon_size = rect.width - 16

            icon = pygame.transform.scale(icon, (icon_size, icon_size))

            icon_rect = icon.get_rect(midtop=(rect.centerx, rect.y + 4))

            self.screen.blit(icon, icon_rect)

            label_text = self.base_labels.get(flavour, flavour.value.upper())

            self.draw_button_label(rect, label_text)

            qty = self.get_base_stock(flavour, kitchen_status)

            qty_text = self.small_font.render(f"x{qty}", True, (255, 255, 255))

            qty_bg = qty_text.get_rect(topright=(rect.right - 6, rect.y + 6))

            qty_bg.inflate_ip(14, 8)

            pygame.draw.rect(self.screen, (82, 26, 75), qty_bg, border_radius=8)

            self.screen.blit(qty_text, (qty_bg.x + 7, qty_bg.y + 4))

            if self.selected_flavour == flavour:

                pygame.draw.rect(self.screen, (0, 255, 0), rect, width=4, border_radius=10)

    def draw_cream_selection(self):

        for i, rect in enumerate(self.cream_rects):

            cream = self.creams[i]

            icon_size = rect.width - 12

            icon = pygame.transform.scale(self.cream_icons[i], (icon_size, icon_size))

            icon_rect = icon.get_rect(midtop=(rect.centerx, rect.y + 2))

            self.screen.blit(icon, icon_rect)

            label_text = self.cream_labels.get(cream, cream.value.upper())

            self.draw_button_label(rect, label_text)

            if self.selected_cream == cream:

                pygame.draw.rect(self.screen, (0, 255, 0), rect, width=4, border_radius=10)


    def draw(self, kitchen_status, state):

        cake_station = kitchen_status["cake_station"]

        self.draw_cake_slots(cake_station, state)

        self.draw_showcase(kitchen_status)

        self.draw_selected_time(state)

        self.draw_cream_status(state)

        self.draw_refill_button()

        self.draw_base_selection(kitchen_status)

        self.draw_cream_selection()

    def handle_event(self, event, state) -> bool:

        if event.type != pygame.MOUSEBUTTONDOWN:
            return False

        if event.button != 1:
            return False

        pos = event.pos

        for i, rect in enumerate(self.base_rects):

            if rect.collidepoint(pos):

                self.selected_flavour = self.flavours[i]

                self.play_sound(self.select_sound)

                self.set_debug(f"Selected flavour: {self.selected_flavour.value}")

                return True

        for i, rect in enumerate(self.cream_rects):

            if rect.collidepoint(pos):

                self.selected_cream = self.creams[i]

                self.play_sound(self.select_sound)

                self.set_debug(f"Selected cream: {self.selected_cream.value}")

                return True

        if state is None:
            self.set_debug("DayState not found")
            return True

        if self.refill_resources_rect.collidepoint(pos):

            state.kitchen.perform_delivery_refill(state._purchased)

            self.selected_flavour = None
            self.selected_cream = None

            self.set_debug("Resources refilled successfully!")

            return True

        for slot_id, rect in self.cake_slot_rects:

            if not rect.collidepoint(pos):
                continue

            if slot_id in self.cake_slot_recipes:

                flavour, cream = self.cake_slot_recipes[slot_id]

                success = state.player_move_cake(slot_id, flavour, cream)

                if success:

                    self.cake_slot_recipes.pop(slot_id, None)

                    generation = self.cake_slot_generations.pop(slot_id, None)

                    if generation is not None:

                        self.ready_sound_played_for.discard((slot_id, generation))

                    self.showcase_cakes_ui.append({"flavour": flavour.value, "cream": cream.value,})

                    self.play_sound(self.cake_move_sound)

                    self.set_debug("Cake moved to showcase")
                else:

                    self.set_debug("Cake is not ready yet")

                return True

            if self.selected_flavour is None:

                self.set_debug("Select cake base first")

                return True

            if self.selected_cream is None:

                self.set_debug("Select cream first")

                return True

            free_slot_id = None

            for slot in state.kitchen.cake_station.slots:

                if not slot.is_busy:
                    free_slot_id = slot.slot_id
                    break

            success, reason = state.player_start_cake(self.selected_flavour, self.selected_cream)

            if success:

                if free_slot_id is not None:

                    self.cake_slot_recipes[free_slot_id] = (self.selected_flavour, self.selected_cream)

                    self.cake_sound_generation += 1

                    self.cake_slot_generations[free_slot_id] = (self.cake_sound_generation)

                self.set_debug("Cake started")

            else:

                if reason == "no_base":

                    self.set_debug("No base: press REFILL")

                elif reason == "no_cream":

                    self.set_debug("No cream: press REFILL")

                elif reason == "no_slot":

                    self.set_debug("No free cake slot")

                else:

                    self.set_debug(f"Cannot start cake: {reason}")

            return True

        return False
