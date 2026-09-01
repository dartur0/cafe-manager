import pygame
import inspect

from ui.sound_manager import SoundManager
from ui.components.pause_button import PauseButton
from core.entities.cake import FlavourType, build_cake
from ui.components.hud import HUD
from ui.components.coffee_panel import CoffeePanel
from ui.components.cake_panel import CakePanel
from ui.components.order_panel import OrderPanel
from ui.components.customer_panel import CustomerPanel
from ui.components.top_panel import TopPanel
from ui.components.customer_sprite import CustomerSprite


class DayScreen:

    def __init__(self, screen):

        self.screen = screen

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.background = pygame.image.load("assets/images/day_back.png")

        self.table = pygame.image.load("assets/images/table.png").convert_alpha()

        self.background = pygame.transform.scale(self.background, (screen.get_width(), screen.get_height()))

        self.table = pygame.transform.scale(self.table, (screen.get_width(), screen.get_height()))

        SoundManager.play_music("assets/music/day_music.mp3")

        self.title_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 70)

        self.font = pygame.font.Font("assets/fonts/Pacifico.ttf", 30)

        self.big_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 40)

        self.small_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 22)

        self.pause_button = PauseButton()

        self.customer_sprite = None

        self.load_images()
        
        self.order_panel = OrderPanel(self.screen, self.small_font)

        self.coffee_panel = CoffeePanel(
            screen=self.screen,
            small_font=self.small_font,
            coffee_machine_image=self.coffee_machine,
            cup_coffee_icon=self.cup_coffee_icon,
            cup_latte_icon=self.cup_latte_icon,
            milk_regular_icon=self.milk_regular_icon,
            milk_lactose_free_icon=self.milk_lactose_free_icon,
            milk_oat_icon=self.milk_oat_icon,
            set_debug=self.set_debug_message
        )

        self.cake_panel = CakePanel(
            screen=self.screen,
            font=self.font,
            small_font=self.small_font,
            cake_station_image=self.cake_station,
            base_icons=self.base_icons,
            cream_icons=[
                self.cream_vanilla_icon,
                self.cream_chocolate_icon,
                self.cream_strawberry_icon,
                self.cream_banana_icon,
                self.cream_blueberry_icon,
                self.cream_pistachio_icon,
            ],
            storage_icon=self.storage_icon,
            cake_images=self.cake_images,
            set_debug=self.set_debug_message
        )

        self.customer_panel = CustomerPanel(screen=self.screen, font=self.font, small_font=self.small_font, customer_regular_icon=self.customer_regular_icon, customer_vip_icon=self.customer_vip_icon)

        self.top_panel = TopPanel(screen=self.screen, title_font=self.title_font, font=self.font, small_font=self.small_font, star_icon=self.star_icon)

        self.hud = HUD(self.title_font, self.font, self.big_font, self.star_icon)

        self.debug_message = ""

        self.customer_rects = []

        base_x = self.width - 580 

        self.station_rect = pygame.Rect(900, 500, 220, 160)

    def set_debug_message(self, message: str):

        self.debug_message = message
        print(message)

    def set_day_state(self, day_state) -> None:
     self._day_state_ref = day_state

    def _get_day_state(self) ->  None:
     return getattr(self, "_day_state_ref", None)

    def update_data(self, status: dict):

        self.day_number = status["day_number"]

        self.time_left = status["time_left"]

        self.money = status["money_earned"]

        self.kitchen_status = status["kitchen"]

        self.customer_slots = status["kitchen"]["customer_slots"]

        self.served_count = status["served_count"]

    def load_images(self):

        self.coffee_machine = pygame.image.load("assets/images/coffee_machine.png").convert_alpha()

        self.coffee_machine = pygame.transform.scale(self.coffee_machine, (250, 250))

        self.cake_station = pygame.image.load("assets/images/cake_station.png").convert_alpha()

        self.base_icons = {
            FlavourType.VANILLA: pygame.image.load("assets/images/vanilla.png").convert_alpha(),

            FlavourType.CHOCOLATE: pygame.image.load("assets/images/chocolate.png").convert_alpha(),

            FlavourType.RED_VELVET: pygame.image.load("assets/images/red_velvet.png").convert_alpha(),

            FlavourType.CARROT_CAKE: pygame.image.load("assets/images/carrot_cake.png").convert_alpha(),
        }

        self.cream_banana_icon = pygame.image.load("assets/images/cream_banana.png").convert_alpha()

        self.cream_blueberry_icon = pygame.image.load("assets/images/cream_blueberry.png").convert_alpha()

        self.cream_chocolate_icon = pygame.image.load("assets/images/cream_chocolate.png").convert_alpha()

        self.cream_pistachio_icon = pygame.image.load("assets/images/cream_pistachio.png").convert_alpha()

        self.cream_strawberry_icon = pygame.image.load("assets/images/cream_strawberry.png").convert_alpha()

        self.cream_vanilla_icon = pygame.image.load("assets/images/cream_vanilla.png").convert_alpha()

        self.storage_icon = pygame.image.load("assets/images/storage.png").convert_alpha()

        self.cup_coffee_icon = pygame.image.load("assets/images/cup_coffee.png").convert_alpha()

        self.cup_latte_icon = pygame.image.load("assets/images/cup_latte.png").convert_alpha()

        self.milk_regular_icon = pygame.image.load("assets/images/milk_regular.png").convert_alpha()

        self.milk_lactose_free_icon = pygame.image.load("assets/images/milk_lactose_free.png").convert_alpha()

        self.milk_oat_icon = pygame.image.load("assets/images/milk_oat.png").convert_alpha()

        self.milk_soy_icon = pygame.image.load("assets/images/milk_soy.png").convert_alpha()

        self.customer_regular_icon = pygame.image.load("assets/images/customer.png").convert_alpha()

        try:
            self.customer_vip_icon = pygame.image.load("assets/images/customer_vip.png").convert_alpha()
        except FileNotFoundError:
            self.customer_vip_icon = self.customer_regular_icon

        self.customer_sprite = CustomerSprite({"regular": self.customer_regular_icon, "vip": self.customer_vip_icon,}, self.font)

        self.customer_icon = self.customer_regular_icon

        self.star_icon = pygame.image.load("assets/images/star_gold.png").convert_alpha()

        self.star_icon = pygame.transform.scale(self.star_icon, (28, 28))

        self.cake_images = {
            ("vanilla", "vanilla"):
                pygame.image.load("assets/images/cakes/vanilla_vanilla.png").convert_alpha(),

            ("vanilla", "chocolate"):
                pygame.image.load("assets/images/cakes/vanilla_chocolate.png").convert_alpha(),

            ("vanilla", "banana"):
                pygame.image.load("assets/images/cakes/vanilla_banana.png").convert_alpha(),

            ("vanilla", "strawberry"):
                pygame.image.load("assets/images/cakes/vanilla_strawberry.png").convert_alpha(),

            ("vanilla", "pistachio"):
                pygame.image.load("assets/images/cakes/vanilla_pistachio.png").convert_alpha(),

            ("vanilla", "blueberry"):
                pygame.image.load("assets/images/cakes/vanilla_blueberry.png").convert_alpha(),

            ("chocolate", "banana"):
                pygame.image.load("assets/images/cakes/chocolate_banana.png").convert_alpha(),

            ("chocolate", "vanilla"):
                pygame.image.load("assets/images/cakes/chocolate_vanilla.png").convert_alpha(),

            ("chocolate", "chocolate"):
                pygame.image.load("assets/images/cakes/chocolate_chocolate.png").convert_alpha(),

            ("chocolate", "strawberry"):
                pygame.image.load("assets/images/cakes/chocolate_strawberry.png").convert_alpha(),

            ("chocolate", "pistachio"):
                pygame.image.load("assets/images/cakes/chocolate_pistachio.png").convert_alpha(),

            ("chocolate", "blueberry"):
                pygame.image.load("assets/images/cakes/chocolate_blueberry.png").convert_alpha(),

            ("red_velvet", "banana"):
                pygame.image.load("assets/images/cakes/red_velvet_banana.png").convert_alpha(),

            ("red_velvet", "chocolate"):
                pygame.image.load("assets/images/cakes/red_velvet_chocolate.png").convert_alpha(),

            ("red_velvet", "vanilla"):
                pygame.image.load("assets/images/cakes/red_velvet_vanilla.png").convert_alpha(),

            ("red_velvet", "strawberry"):
                pygame.image.load("assets/images/cakes/red_velvet_strawberry.png").convert_alpha(),

            ("red_velvet", "pistachio"):
                pygame.image.load("assets/images/cakes/red_velvet_pistachio.png").convert_alpha(),

            ("red_velvet", "blueberry"):
                pygame.image.load("assets/images/cakes/red_velvet_blueberry.png").convert_alpha(),

            ("carrot_cake", "banana"):
                pygame.image.load(
                    "assets/images/cakes/carrot_cake_banana.png"
                ).convert_alpha(),

            ("carrot_cake", "chocolate"):
                pygame.image.load("assets/images/cakes/carrot_cake_chocolate.png").convert_alpha(),

            ("carrot_cake", "vanilla"):
                pygame.image.load("assets/images/cakes/carrot_cake_vanilla.png").convert_alpha(),

            ("carrot_cake", "strawberry"):
                pygame.image.load("assets/images/cakes/carrot_cake_strawberry.png").convert_alpha(),

            ("carrot_cake", "pistachio"):
                pygame.image.load("assets/images/cakes/carrot_cake_pistachio.png").convert_alpha(),

            ("carrot_cake", "blueberry"):
                pygame.image.load("assets/images/cakes/carrot_cake_blueberry.png").convert_alpha(),
        }


    def draw(self):

        state = self._get_day_state()

        if state is not None:
            self.update_data(state.get_status())

        if state is not None:
            self.coffee_panel.update(state)

        self.screen.blit(self.background, (0, 0))
        
        self.customer_panel.update(self.customer_slots)

        self.customer_rects = self.customer_panel.draw(self.customer_slots)

        self.screen.blit(self.table, (0, 0))

        self.coffee_panel.draw(self.kitchen_status, state)

        self.cake_panel.draw(self.kitchen_status, state)
        
        self.order_panel.draw(self.customer_rects, self.get_customer_object)

        self.top_panel.draw(day_number=self.day_number, time_left=self.time_left, money=self.money, state=state)

        self.draw_debug_message()

        self.pause_button.draw(self.screen)

    def get_customer_object(self, slot_index: int):
        state = self._get_day_state()

        if state is None:
            return None

        try:
            return state.kitchen.customer_slots.slots[slot_index]
        except (AttributeError, IndexError):
            return None


    def can_serve_order_frontend(self, order):
        state = self._get_day_state()

        if state is None or order is None:
            return False, "no_order"

        showcase = state.kitchen.showcase
        order_type = order.order_type.value

        if order_type in ("cake", "combo"):

            if not showcase.find_cake(order.flavour, order.cream):
                return False, "cake_not_on_showcase"

        if order_type in ("coffee", "combo"):
            coffee_found = False

            for coffee in self.coffee_panel.showcase_coffees_ui:
                if coffee["coffee_type"] != order.coffee_type.value:
                    continue

                if order.milk_type is not None:
                    if coffee.get("milk_type") != order.milk_type.value:
                        continue

                coffee_found = True
                break

            if not coffee_found:
                return False, "coffee_not_on_showcase"

        return True, "ok"


    def remove_served_items_from_ui(self, order):

        if order is None:
            return

        order_type = order.order_type.value

        if order_type in ("cake", "combo"):

            for i, cake in enumerate(self.cake_panel.showcase_cakes_ui):
                if (cake["flavour"] == order.flavour.value and cake["cream"] == order.cream.value):
                    self.cake_panel.showcase_cakes_ui.pop(i)
                    break

        if order_type in ("coffee", "combo"):

            for i, coffee in enumerate(self.coffee_panel.showcase_coffees_ui):
                if coffee["coffee_type"] != order.coffee_type.value:
                    continue

                if order.milk_type is not None:
                    if coffee.get("milk_type") != order.milk_type.value:
                        continue

                self.coffee_panel.showcase_coffees_ui.pop(i)
                break
            
    def draw_debug_message(self):

        if not self.debug_message:
            return

        text = self.small_font.render(self.debug_message, True, (255, 255, 255))

        bg_rect = text.get_rect(bottomleft=(40, self.height - 20))

        bg_rect.inflate_ip(20, 10)

        pygame.draw.rect(self.screen, (82, 26, 75), bg_rect, border_radius=10)

        self.screen.blit(text, (bg_rect.x + 10, bg_rect.y + 5))

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "PAUSE"

        if self.pause_button.is_clicked(event):
            return "PAUSE"

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        pos = event.pos

        state = self._get_day_state()

        if state is None:
            self.debug_message = "DayState not found"
            print(self.debug_message)
            return None
        
        if self.coffee_panel.handle_event(event, state):
            return None
        
        if self.cake_panel.handle_event(event, state):
            return None
            
        # obsługa klienta
        for slot_index, rect in self.customer_rects:
            if rect.collidepoint(pos):

                customer_obj = self.get_customer_object(slot_index)

                if customer_obj is None:
                    self.debug_message = "No customer"
                    print(self.debug_message)
                    return None

                order = customer_obj.order

                can_serve, reason = self.can_serve_order_frontend(order)

                if not can_serve:

                    if reason in ("cake_not_on_showcase", "coffee_not_on_showcase"):

                        self.customer_panel.play_cannot_serve_sound()

                    self.debug_message = f"Cannot serve: {reason}"

                    print(self.debug_message)

                    return None

                success, reason = state.player_serve(slot_index)

                if success:

                    self.customer_panel.mark_served(slot_index)

                    self.remove_served_items_from_ui(order)

                    self.debug_message = "Customer served"

                else:

                    self.debug_message = f"Cannot serve customer: {reason}"

                print(self.debug_message)
                return None

        return None
