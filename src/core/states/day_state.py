from __future__ import annotations
import random
import pygame

from states.base_state import BaseState
from ui.screens.day_screen import DayScreen
from core.entities.kitchen import Kitchen, CustomerSlots
from core.entities.cake import CreamType, FlavourType
from core.entities.customer import Customer, create_customer, CustomerType
from core.entities.order import create_random_order
from core.systems.level import get_level
from core.systems.save_manager import SaveManager, SaveData

_BASE_FLAVOURS = frozenset([
    FlavourType.VANILLA,
    FlavourType.CHOCOLATE,
])

_BASE_CREAMS = frozenset([
    CreamType.VANILLA,
    CreamType.CHOCOLATE,
    CreamType.STRAWBERRY,
    CreamType.BANANA,
])

class DayState(BaseState):
    def __init__(self, save_data: SaveData | None = None) -> None:
        super().__init__()

        if save_data is None:
            save_data = SaveManager.new_game_data()

        self.day_number:   int   = save_data.day
        self.money_earned: float = save_data.money
        self._purchased:   set   = save_data.purchased
        self._stars:       dict  = save_data.stars

        self._level_config = get_level(self.day_number)

        self.kitchen:      Kitchen = Kitchen()
        
        self.day_timer:    float   = self._level_config.day_duration
        
        self.reputation:   int     = 100
        self.served_count: int     = 0
        self.left_count:   int     = 0

        self._spawn_timer:    float = 0.0
        self._spawn_interval: float = 5.0 
        
        self._patience_sum:   float = 0.0
        self._day_screen: DayScreen | None = None
        self.kitchen.perform_delivery_refill(self._purchased)

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        self._day_screen = DayScreen(screen)
        self._day_screen.set_day_state(self)

    def on_exit(self) -> None:
        pygame.mixer.music.stop()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._day_screen is None:
            return

        action = self._day_screen.handle_event(event)

        if action == "REFILL":
            self.kitchen.perform_delivery_refill(self._purchased)
            return
                
        if action == "PAUSE":
            self.next_state = "pause"
            return

        if not isinstance(action, dict):
            return

        act_type = action.get("action")

        if act_type == "start_cake":
            self.player_start_cake(action["flavour"], action["cream"])

        elif act_type == "brew":
            self.player_brew(action["coffee_type"])

        elif act_type == "serve":
            self.player_serve(action["slot"])

        elif act_type == "move_cake":
            flavour = action.get("flavour")
            cream   = action.get("cream")
            if flavour and cream:
                self.player_move_cake(action["slot_id"], flavour, cream)

    def update(self, delta: float) -> None:
        self.day_timer -= delta
        if self.day_timer <= 0:
            self.day_timer = 0
            self._end_day()
            return

        self._update_spawn(delta)

        self.kitchen.update(delta)
        self._update_customers(delta)

    def draw(self, surface: pygame.Surface) -> None:
        if self._day_screen is None:
            return

        self._day_screen.update_data(self.get_status())
        self._day_screen.draw()

    def _update_spawn(self, delta: float) -> None:
        self._spawn_timer += delta

        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0.0
            
            self._spawn_interval = random.uniform(
                self._level_config.spawn_interval_min, 
                self._level_config.spawn_interval_max
            )
            self._try_spawn_customer()

    def _try_spawn_customer(self) -> None:
        if self.kitchen.customer_slots.is_full():
            return   

        from core.entities.customer import CustomerType
        customer_type = (
            CustomerType.VIP
            if random.random() < self._level_config.vip_chance
            else CustomerType.REGULAR
        )
        customer = create_customer(customer_type)
        customer.set_order(
            create_random_order(
                unlocked_flavours=self._get_unlocked_flavours(),
                unlocked_creams=self._get_unlocked_creams(),
            )
        )
        self.kitchen.customer_slots.add(customer)

    def _update_customers(self, delta: float) -> None:
        for i, customer in self.kitchen.customer_slots.get_active():
            customer.update(delta)

            if customer.has_left:
                self.reputation  -= 10
                self.reputation   = max(0, self.reputation)
                self.left_count  += 1
                self.kitchen.customer_slots.remove(i)

    def player_serve(self, slot_index: int) -> tuple[bool, str]:
        customer = self.kitchen.customer_slots.slots[slot_index]
        if customer is None:
            return False, "no_customer"

        success, reason = self.kitchen.serve_order(slot_index)

        if success:
            order     = customer.order
            price     = order.get_price()
            tip       = customer.calculate_tip(price)
            total     = round(price + tip, 2)

            self.money_earned += total
            self.served_count += 1
            self._patience_sum += customer.patience_ratio

        return success, reason

    def player_brew(self, coffee_type) -> tuple[bool, str]:
        return self.kitchen.brew_espresso(coffee_type)
    
    def _get_unlocked_flavours(self) -> set:
        unlocked = set(_BASE_FLAVOURS)
        if "flavour_red_velvet" in self._purchased:
            unlocked.add(FlavourType.RED_VELVET)
        if "flavour_carrot" in self._purchased:
            unlocked.add(FlavourType.CARROT_CAKE)
        return unlocked

    def _get_unlocked_creams(self) -> set:
        unlocked = set(_BASE_CREAMS)
        if "cream_blueberry" in self._purchased:
            unlocked.add(CreamType.BLUEBERRY)
        if "cream_pistachio" in self._purchased:
            unlocked.add(CreamType.PISTACHIO)
        return unlocked

    def player_start_cake(self, flavour, cream) -> tuple[bool, str]:
        return self.kitchen.start_cake(
            flavour=flavour,
            cream=cream,
            unlocked_flavours=self._get_unlocked_flavours(),
            unlocked_creams=self._get_unlocked_creams(),
        )

    def player_move_cake(self, slot_id: int, flavour, cream) -> bool:
        return self.kitchen.move_cake_to_showcase(slot_id, flavour, cream)

    def _end_day(self) -> None:
        end_stats = self.kitchen.end_of_day()

        avg_patience = (
            self._patience_sum / self.served_count
            if self.served_count > 0
            else 0.0
        )

        from core.systems.level import calculate_stars
        stars = calculate_stars(
            served_count=self.served_count,
            customers_goal=self._level_config.customers_goal,
            avg_patience=round(avg_patience, 2),
        )

        if stars > 0:
            updated_stars = SaveManager.update_stars(
                stars=self._stars,
                day=self.day_number,
                new_stars=stars,
            )
            SaveManager.save(
                day=self.day_number + 1,
                money=self.money_earned,
                purchased=self._purchased,
                stars=updated_stars,
            )

        self._final_stats = {
            "day_number":      self.day_number,
            "customers_goal":  self._level_config.customers_goal,
            "money_earned":    self.money_earned,
            "served_count":    self.served_count,
            "avg_patience":    round(avg_patience, 2),
            "left_count":      self.left_count,
            "reputation":      self.reputation,
            "unsold_items":    end_stats["unsold_items"],
            "purchased":       self._purchased,   
            "stars":           self._stars,       
        }

        self.next_state = "gameover"

    def get_status(self) -> dict:
        return {
            "day_number":    self.day_number,
            "time_left":     round(self.day_timer, 1),
            "money_earned":  round(self.money_earned, 2),
            "reputation":    self.reputation,
            "served_count":  self.served_count,
            "left_count":    self.left_count,
            "kitchen":       self.kitchen.get_status(),
        }