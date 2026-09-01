from __future__ import annotations
import pygame

from states.base_state import BaseState
from ui.screens.shop_screen import ShopScreen
from core.entities.kitchen import Kitchen
from core.systems.save_manager import SaveManager


UPGRADES = [
    {
        "id":          "flavour_red_velvet",
        "category":    "flavours",
        "name":        "Red Velvet",
        "description": "Unlock Red Velvet cake base",
        "price":       200,
        "icon":        "red_velvet",
    },
    {
        "id":          "flavour_carrot",
        "category":    "flavours",
        "name":        "Carrot Cake",
        "description": "Unlock Carrot Cake base",
        "price":       200,
        "icon":        "carrot_cake",
    },
    {
        "id":          "cream_blueberry",
        "category":    "creams",
        "name":        "Blueberry Cream",
        "description": "Unlock Blueberry Cream",
        "price":       150,
        "icon":        "blueberry",
    },
    {
        "id":          "cream_pistachio",
        "category":    "creams",
        "name":        "Pistachio Cream",
        "description": "Unlock Pistachio Cream",
        "price":       150,
        "icon":        "pistachio",
    },
    {
        "id":          "kitchen_cake_slot",
        "category":    "kitchen",
        "name":        "+1 Cake Table",
        "description": "Add one more assembly table",
        "price":       300,
        "icon":        "cake_table",
    },
    {
        "id":          "kitchen_storage_slot",
        "category":    "kitchen",
        "name":        "+1 Storage Slot",
        "description": "Store more cake bases",
        "price":       250,
        "icon":        "storage",
    },
    {
        "id":          "kitchen_auto_machine",
        "category":    "kitchen",
        "name":        "Auto Espresso",
        "description": "Machine brews automatically",
        "price":       400,
        "icon":        "auto_machine",
    },
    {
        "id":          "kitchen_more_beans",
        "category":    "kitchen",
        "name":        "More Beans",
        "description": "Double the bean capacity",
        "price":       200,
        "icon":        "beans",
    },
]

class ShopState(BaseState):
    def __init__(
        self,
        money:           float,
        kitchen:         Kitchen,
        purchased:       set[str] | None = None,
        from_state:      str = "menu",
    ) -> None:
        super().__init__()
        self.money:      float      = money
        self.kitchen:    Kitchen    = kitchen
        self.purchased:  set[str]   = purchased or set()
        self._from:      str        = from_state
        self._screen:    ShopScreen | None = None

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        self._screen = ShopScreen(
            screen=screen,
            upgrades=self._get_upgrades_status(),
            money=self.money,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._screen is None:
            return

        action = self._screen.handle_event(event)

        if action == "back":
            self.next_state = self._from

        elif action and action.startswith("buy:"):
            upgrade_id = action.split("buy:")[1]
            self._try_buy(upgrade_id)
            if self._screen:
                self._screen.update_data(
                    upgrades=self._get_upgrades_status(),
                    money=self.money,
                )

    def update(self, delta: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self._screen is not None:
            self._screen.draw()

    def _try_buy(self, upgrade_id: str) -> bool:
        upgrade = next((u for u in UPGRADES if u["id"] == upgrade_id), None)
        if upgrade is None:
            return False

        if self._is_max_level(upgrade_id):
            return False

        if self.money < upgrade["price"]:
            return False

        self.money -= upgrade["price"]
        self.purchased.add(upgrade_id)

        self._apply_upgrade(upgrade_id)

        current_save = SaveManager.load()
        current_day = current_save.day if current_save else 1
        current_stars = current_save.stars if current_save else {}

        SaveManager.save(
            day=current_day,
            money=self.money,
            purchased=self.purchased,
            stars=current_stars
        )
        return True
    
    def _is_max_level(self, upgrade_id: str) -> bool:
        from core.entities.kitchen import MAX_CAKE_SLOTS, MAX_STORAGE_SLOTS

        if upgrade_id == "kitchen_cake_slot":
            return len(self.kitchen.cake_station.slots) >= MAX_CAKE_SLOTS

        elif upgrade_id == "kitchen_storage_slot":
            return self.kitchen.base_storage._slot_count >= MAX_STORAGE_SLOTS

        elif upgrade_id == "kitchen_auto_machine":
            return self.kitchen.coffee_machine.is_auto

        elif upgrade_id == "kitchen_more_beans":
            return self.kitchen.coffee_machine.max_beans > 20

        return upgrade_id in self.purchased

    def _apply_upgrade(self, upgrade_id: str) -> None:
        if upgrade_id == "kitchen_cake_slot":
            self.kitchen.upgrade_cake_slot()

        elif upgrade_id == "kitchen_storage_slot":
            self.kitchen.upgrade_storage_slot()

        elif upgrade_id == "kitchen_auto_machine":
            self.kitchen.upgrade_auto_machine()

        elif upgrade_id == "kitchen_more_beans":
            self.kitchen.upgrade_beans_capacity()
            
        elif upgrade_id.startswith(("flavour_", "cream_")):
            pass

    def _get_upgrades_status(self) -> list[dict]:
        result = []
        for upgrade in UPGRADES:
            result.append({
                **upgrade,
                "purchased":  self._is_max_level(upgrade["id"]),
                "can_afford": self.money >= upgrade["price"],
            })
        return result