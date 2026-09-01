from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from core.decorators.base_product import ProductComponent
from core.decorators.cream_decorator import CreamType
from core.decorators.flavour_decorator import FlavourType
from core.decorators.milk_decorator import MilkType
from core.entities.cake import build_cake
from core.entities.coffee import CoffeeType, build_coffee
from core.entities.customer import Customer
from core.entities.order import Order

MAX_QUEUE_SIZE        = 4    
MAX_READY_CUPS        = 3   
DEFAULT_CAKE_SLOTS    = 2    
DEFAULT_STORAGE_SLOTS = 2  
MAX_CAKE_SLOTS        = 4    
MAX_STORAGE_SLOTS     = 4 
MAX_CUSTOMER_SLOTS    = 4   
DEFAULT_BEANS         = 20 
DEFAULT_MILK          = 10  
DEFAULT_CREAM         = 10  
DEFAULT_SHOWCASE_SLOTS = 6  

@dataclass
class CookingSlot:
    slot_id:    int
    product:    Optional[ProductComponent] = None
    time_total: float = 0.0
    time_left:  float = 0.0
    is_ready:   bool  = False

    @property
    def is_busy(self) -> bool:
        return self.product is not None

    def update(self, delta: float) -> bool:
        if not self.is_busy or self.is_ready:
            return False

        self.time_left -= delta
        if self.time_left <= 0:
            self.time_left = 0.0
            self.is_ready  = True
            return True
        return False

    def clear(self) -> None:
        self.product    = None
        self.time_total = 0.0
        self.time_left  = 0.0
        self.is_ready   = False


@dataclass
class ShowcaseItem:
    product:     ProductComponent
    flavour:     Optional[FlavourType] = None
    cream:       Optional[CreamType]   = None
    is_coffee:   bool                  = False
    coffee_type: Optional[CoffeeType]  = None


@dataclass
class ReadyCup:
    coffee_type: CoffeeType
    time_left:   float = 0.0 
    is_ready:    bool  = False
    milk_added:  bool                  = False
    milk_type:   Optional[MilkType]    = None
    cream_type:  Optional[CreamType]   = None

class CoffeeMachine:
    def __init__(self) -> None:
        self.beans:           int        = DEFAULT_BEANS
        self.milk:            int        = DEFAULT_MILK
        self.max_beans:       int        = DEFAULT_BEANS
        self.ready_cups:      list[ReadyCup] = []
        self.is_auto:         bool       = False
        self.unlimited_cream: bool       = False
        self._brew_timer:     float      = 0.0
        self._brew_time:      float      = 5.0   


    def can_brew(self) -> bool:
        return (
            self.beans >= 2
            and len(self.ready_cups) < MAX_READY_CUPS
        )

    def brew(self, coffee_type: CoffeeType) -> bool:
        if not self.can_brew():
            return False

        self.beans -= 2
        self.ready_cups.append(ReadyCup(
            coffee_type=coffee_type,
            time_left=self._brew_time, 
            is_ready=False
        ))
        return True

    def update(self, delta: float) -> None:
        for cup in self.ready_cups:
            if not cup.is_ready:
                cup.time_left -= delta
                if cup.time_left <= 0:
                    cup.time_left = 0.0
                    cup.is_ready = True 

        if not self.is_auto:
            return

        self._brew_timer += delta
        if self._brew_timer >= self._brew_time:
            self._brew_timer = 0.0
            if self.can_brew():
                self.brew(CoffeeType.ESPRESSO)


    def add_milk(self, cup_index: int, milk_type: MilkType) -> bool:
        if cup_index >= len(self.ready_cups):
            return False

        cup = self.ready_cups[cup_index]
        
        if not cup.is_ready:
            return False

        if cup.milk_added or self.milk <= 0:
            return False  

        self.milk -= 1
        cup.milk_added = True
        cup.milk_type  = milk_type
        return True
    
    def take_cup(self, cup_index: int) -> Optional[ProductComponent]:
        if cup_index >= len(self.ready_cups):
            return None

        cup = self.ready_cups[cup_index]
        
        if not cup.is_ready:
            return None

        self.ready_cups.pop(cup_index)
        return build_coffee(
            coffee_type=cup.coffee_type,
            milk_type=cup.milk_type or MilkType.REGULAR,
        )
    
    def refill_beans(self, amount: int) -> None:
        self.beans = min(self.beans + amount, self.max_beans)

    def refill_milk(self, amount: int) -> None:
        self.milk += amount

    def get_status(self) -> dict:
        return {
            "beans":      self.beans,
            "max_beans":  self.max_beans,
            "milk":       self.milk,
            "ready_cups": len(self.ready_cups),
            "is_auto":    self.is_auto,
        }

class CakeStation:
    def __init__(self) -> None:
        self.slots: list[CookingSlot] = [
            CookingSlot(slot_id=i)
            for i in range(DEFAULT_CAKE_SLOTS)
        ]

    def _free_slot(self) -> Optional[CookingSlot]:
        for slot in self.slots:
            if not slot.is_busy:
                return slot
        return None

    def can_assemble(self) -> bool:
        return self._free_slot() is not None

    def assemble(
        self,
        flavour:           FlavourType,
        cream:             CreamType,
        unlocked_flavours: set[FlavourType] | None = None,
        unlocked_creams:   set[CreamType]   | None = None,
    ) -> Optional[int]:
        slot = self._free_slot()
        if slot is None:
            return None

        product = build_cake(
            flavour=flavour,
            cream=cream,
            unlocked_flavours=unlocked_flavours,
            unlocked_creams=unlocked_creams,
        )

        slot.product    = product
        slot.time_total = product.get_prep_time()
        slot.time_left  = product.get_prep_time()
        slot.is_ready   = False
        return slot.slot_id

    def update(self, delta: float) -> list[CookingSlot]:
        just_ready = []
        for slot in self.slots:
            if slot.update(delta):
                just_ready.append(slot)
        return just_ready

    def take_ready(self, slot_id: int) -> Optional[ProductComponent]:
        for slot in self.slots:
            if slot.slot_id == slot_id and slot.is_ready:
                product = slot.product
                slot.clear()
                return product
        return None

    def upgrade_add_slot(self) -> bool:
        if len(self.slots) >= MAX_CAKE_SLOTS:
            return False
        new_id = len(self.slots)
        self.slots.append(CookingSlot(slot_id=new_id))
        return True

    def get_status(self) -> list[dict]:
        return [
            {
                "slot_id":    s.slot_id,
                "is_busy":    s.is_busy,
                "is_ready":   s.is_ready,
                "time_left":  round(s.time_left, 1),
                "time_total": s.time_total,
                "name":       s.product.get_name() if s.product else None,
            }
            for s in self.slots
        ]

class BaseStorage:
    def __init__(self) -> None:
        self._slot_count: int = DEFAULT_STORAGE_SLOTS
        self.max_capacity: int = 5
        self.stock: dict[FlavourType, int] = {
            FlavourType.VANILLA:    3,
            FlavourType.CHOCOLATE:  3,
            FlavourType.RED_VELVET: 0,   
            FlavourType.CARROT_CAKE: 0,  
        }

    def has(self, flavour: FlavourType, qty: int = 1) -> bool:
        return self.stock.get(flavour, 0) >= qty

    def use(self, flavour: FlavourType, qty: int = 1) -> bool:
        if not self.has(flavour, qty):
            return False
        self.stock[flavour] -= qty
        return True

    def refill(self, flavour: FlavourType, qty: int) -> None:
        current = self.stock.get(flavour, 0)
        self.stock[flavour] = min(current + qty, self.max_capacity)

    def upgrade_add_slot(self) -> bool:
        if self._slot_count >= MAX_STORAGE_SLOTS:
            return False
        self._slot_count += 1
        self.max_capacity += 2 
        return True

    def get_status(self) -> dict:
        return {
            "slots":      self._slot_count,
            "max_slots":  MAX_STORAGE_SLOTS,
            "max_capacity": self.max_capacity,
            "stock":      {f.value: qty for f, qty in self.stock.items()},
        }

class Showcase:
    def __init__(self) -> None:
        self.max_slots:    int                  = DEFAULT_SHOWCASE_SLOTS
        self.cake_items:   list[ShowcaseItem]   = []
        self.coffee_items: list[ShowcaseItem]   = []


    def add_cake(
        self,
        product: ProductComponent,
        flavour: FlavourType,
        cream:   CreamType,
        count:   int = 1,
    ) -> bool:
        if len(self.cake_items) + count > self.max_slots:
            return False

        for _ in range(count):
            self.cake_items.append(ShowcaseItem(
                product=product,
                flavour=flavour,
                cream=cream,
                is_coffee=False,
            ))
        return True

    def find_cake(
        self,
        flavour: FlavourType,
        cream:   CreamType,
    ) -> Optional[ShowcaseItem]:
        for item in self.cake_items:
            if item.flavour == flavour and item.cream == cream:
                return item
        return None

    def take_cake(
        self,
        flavour: FlavourType,
        cream:   CreamType,
    ) -> Optional[ProductComponent]:
        for i, item in enumerate(self.cake_items):
            if item.flavour == flavour and item.cream == cream:
                return self.cake_items.pop(i).product
        return None

    def add_coffee(
        self,
        product:     ProductComponent,
        coffee_type: CoffeeType,
    ) -> bool:
        total = len(self.cake_items) + len(self.coffee_items)
        if total >= self.max_slots:
            return False

        self.coffee_items.append(ShowcaseItem(
            product=product,
            is_coffee=True,
            coffee_type=coffee_type,
        ))
        return True

    def take_coffee(
        self,
        coffee_type: CoffeeType,
    ) -> Optional[ProductComponent]:
        for i, item in enumerate(self.coffee_items):
            if item.coffee_type == coffee_type:
                return self.coffee_items.pop(i).product
        return None

    def clear_unsold(self) -> int:
        count = len(self.cake_items) + len(self.coffee_items)
        self.cake_items.clear()
        self.coffee_items.clear()
        return count

    def upgrade_add_slot(self) -> None:
        self.max_slots += 1

    def get_status(self) -> dict:
        return {
            "max_slots":    self.max_slots,
            "cakes":  [
                {
                    "name":    item.product.get_name(),
                    "flavour": item.flavour.value if item.flavour else None,
                }
                for item in self.cake_items
            ],
            "coffees": [
                {
                    "name":        item.product.get_name(),
                    "coffee_type": item.coffee_type.value if item.coffee_type else None,
                }
                for item in self.coffee_items
            ],
        }

class CustomerSlots:
    def __init__(self):
        self.slots: list[Customer | None] = [None] * MAX_CUSTOMER_SLOTS

    def add(self, customer: Customer) -> bool:
        for i, slot in enumerate(self.slots):
            if slot is None:
                self.slots[i] = customer
                return True
        return False

    def remove(self, index: int) -> None:
        self.slots[index] = None

    def is_full(self) -> bool:
        return all(s is not None for s in self.slots)

    def has_space(self) -> bool:
        return any(s is None for s in self.slots)

    def get_active(self) -> list[tuple[int, Customer]]:
        return [(i, s) for i, s in enumerate(self.slots) if s is not None]

    def get_status(self) -> list[dict | None]:
        return [
            s.get_status() if s is not None else None
            for s in self.slots
        ]


class Kitchen:

    def __init__(self) -> None:
        self.coffee_machine: CoffeeMachine  = CoffeeMachine()
        self.cake_station:   CakeStation    = CakeStation()
        self.base_storage:   BaseStorage    = BaseStorage()
        self.showcase:       Showcase       = Showcase()
        self.customer_slots: CustomerSlots = CustomerSlots()
        self.cream:     int = DEFAULT_CREAM
        self.max_cream: int = DEFAULT_CREAM

    def refill_cream(self, amount: int) -> None:
        self.cream = min(self.cream + amount, self.max_cream)    

    def update(self, delta: float) -> list[str]:
        events = []

        self.coffee_machine.update(delta)

        just_ready = self.cake_station.update(delta)
        for slot in just_ready:
            events.append(f"cake_ready:{slot.slot_id}")

        return events
    
    def start_cake(
        self,
        flavour: FlavourType,
        cream:   CreamType,
        unlocked_flavours: set[FlavourType] | None = None,
        unlocked_creams:   set[CreamType]   | None = None,
    ) -> tuple[bool, str]:
        if not self.base_storage.has(flavour):
            return False, "no_base"

        if not self.coffee_machine.unlimited_cream and self.cream <= 0:
            return False, "no_cream"

        if not self.cake_station.can_assemble():
            return False, "no_slot"

        self.base_storage.use(flavour)
        if not self.coffee_machine.unlimited_cream:
            self.cream -= 1 

        self.cake_station.assemble(
            flavour=flavour,
            cream=cream,
            unlocked_flavours=unlocked_flavours,
            unlocked_creams=unlocked_creams,
        )
        return True, "ok"

    def move_cake_to_showcase(self, slot_id: int, flavour, cream) -> bool:
        product = self.cake_station.take_ready(slot_id)
        if product is None:
            return False
        return self.showcase.add_cake(product, flavour, cream, count=1)

    def brew_espresso(self, coffee_type: CoffeeType) -> tuple[bool, str]:
        if self.coffee_machine.beans < 2:
            return False, "no_beans"
        if not self.coffee_machine.brew(coffee_type):
            return False, "cups_full"
        return True, "ok"

    def serve_order(self, slot_index: int) -> tuple[bool, str]:
        customer = self.customer_slots.slots[slot_index]
        if customer is None:
            return False, "no_customer"

        order: Order = customer.order
        if order is None:
            return False, "no_order"

        cake_product = None
        coffee_product = None

        if order.order_type.value in ("cake", "combo"):
            if not self.showcase.find_cake(order.flavour, order.cream):
                return False, "cake_not_on_showcase"

        if order.order_type.value in ("coffee", "combo"):
            coffee_found = any(item.coffee_type == order.coffee_type for item in self.showcase.coffee_items)
            if not coffee_found:
                return False, "coffee_not_on_showcase"

        if order.order_type.value in ("cake", "combo"):
            cake_product = self.showcase.take_cake(order.flavour, order.cream)

        if order.order_type.value in ("coffee", "combo"):
            coffee_product = self.showcase.take_coffee(order.coffee_type)

        tip   = customer.calculate_tip(order.get_price())
        total = order.get_price() + tip

        customer.mark_served()
        order.mark_served()
        self.customer_slots.remove(slot_index)

        return True, "ok"

    def end_of_day(self) -> dict:
        unsold = self.showcase.clear_unsold()
        return {"unsold_items": unsold}

    def upgrade_cake_slot(self) -> bool:
        return self.cake_station.upgrade_add_slot()

    def upgrade_storage_slot(self) -> bool:
        return self.base_storage.upgrade_add_slot()

    def upgrade_beans_capacity(self) -> None:
        self.coffee_machine.max_beans *= 2

    def upgrade_auto_machine(self) -> None:
       self.coffee_machine.is_auto = True
       self.coffee_machine._brew_time = 2.5

    def upgrade_unlimited_cream(self) -> None:
        self.coffee_machine.unlimited_cream = True

    def upgrade_showcase_slot(self) -> None:
        self.showcase.upgrade_add_slot()

    def perform_delivery_refill(self, purchased_upgrades: set[str]) -> None:
       
        self.base_storage.refill(FlavourType.VANILLA, self.base_storage.max_capacity)
        self.base_storage.refill(FlavourType.CHOCOLATE, self.base_storage.max_capacity)

        if "flavour_red_velvet" in purchased_upgrades:
            self.base_storage.refill(FlavourType.RED_VELVET, self.base_storage.max_capacity)
            
        if "flavour_carrot" in purchased_upgrades:
            self.base_storage.refill(FlavourType.CARROT_CAKE, self.base_storage.max_capacity)

        self.refill_cream(self.max_cream)
        self.coffee_machine.refill_milk(DEFAULT_MILK)
        self.coffee_machine.refill_beans(self.coffee_machine.max_beans)

    def get_status(self) -> dict:
        return {
            "coffee_machine": self.coffee_machine.get_status(),
            "cake_station":   self.cake_station.get_status(),
            "base_storage":   self.base_storage.get_status(),
            "showcase":       self.showcase.get_status(),
            "customer_slots": self.customer_slots.get_status()
        }