from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import random

from core.decorators.flavour_decorator import FlavourType
from core.decorators.cream_decorator import CreamType
from core.decorators.milk_decorator import MilkType
from core.entities.cake import build_cake
from core.entities.coffee import CoffeeType, build_coffee


class OrderType(Enum):
    CAKE   = "cake"
    COFFEE = "coffee"
    COMBO  = "combo" 


class OrderStatus(Enum):
    WAITING   = "waiting"   
    SERVED    = "served"    
    FAILED    = "failed"     


@dataclass
class Order:
    order_type:  OrderType
    status:      OrderStatus = OrderStatus.WAITING

    flavour:     Optional[FlavourType] = None
    cream:       Optional[CreamType]   = None

    coffee_type: Optional[CoffeeType]  = None
    milk_type:   Optional[MilkType]    = None

    def get_price(self) -> float:
        price = 0.0
        if self.order_type in (OrderType.CAKE, OrderType.COMBO):
            cake = build_cake(flavour=self.flavour, cream=self.cream)
            price += cake.get_price()
            
        if self.order_type in (OrderType.COFFEE, OrderType.COMBO):
            coffee = build_coffee(coffee_type=self.coffee_type, milk_type=self.milk_type or MilkType.REGULAR)
            price += coffee.get_price()
            
        return price

    def matches_cake(self, flavour: FlavourType, cream: CreamType) -> bool:
        if self.order_type != OrderType.CAKE:
            return False
        return self.flavour == flavour and self.cream == cream

    def matches_coffee(self, coffee_type: CoffeeType, milk_type: MilkType = MilkType.REGULAR) -> bool:
        if self.order_type != OrderType.COFFEE:
            return False
        return self.coffee_type == coffee_type and self.milk_type == milk_type

    def matches_combo(
        self, 
        flavour: FlavourType, 
        cream: CreamType, 
        coffee_type: CoffeeType, 
        milk_type: MilkType = MilkType.REGULAR
    ) -> bool:
        if self.order_type != OrderType.COMBO:
            return False
        return (
            self.flavour == flavour 
            and self.cream == cream 
            and self.coffee_type == coffee_type 
            and self.milk_type == milk_type
        )

    def mark_served(self) -> None:
        self.status = OrderStatus.SERVED

    def mark_failed(self) -> None:
        self.status = OrderStatus.FAILED

    def get_display(self) -> dict:
        from entities.cake import build_cake
        from entities.coffee import build_coffee

        names = []
        if self.order_type in (OrderType.CAKE, OrderType.COMBO):
            names.append(build_cake(flavour=self.flavour, cream=self.cream).get_name())
        if self.order_type in (OrderType.COFFEE, OrderType.COMBO):
            m_type = None if self.coffee_type == CoffeeType.ESPRESSO else (self.milk_type or MilkType.REGULAR)
            
            names.append(build_coffee(coffee_type=self.coffee_type, milk_type=m_type).get_name())
        return {
            "type":  self.order_type.value,
            "name":  " + ".join(names),
            "price": self.get_price(),
        }

def create_cake_order(flavour: FlavourType, cream: CreamType) -> Order:
    return Order(order_type=OrderType.CAKE, flavour=flavour, cream=cream)


def create_coffee_order(coffee_type: CoffeeType, milk_type: MilkType = MilkType.REGULAR) -> Order:
    return Order(order_type=OrderType.COFFEE, coffee_type=coffee_type, milk_type=milk_type)


def create_combo_order(flavour: FlavourType, cream: CreamType, coffee_type: CoffeeType, milk_type: MilkType = MilkType.REGULAR) -> Order:
    return Order(
        order_type=OrderType.COMBO,
        flavour=flavour,
        cream=cream,
        coffee_type=coffee_type,
        milk_type=milk_type
    )


def create_random_order(
    unlocked_flavours: set[FlavourType] | None = None,
    unlocked_creams:   set[CreamType]   | None = None,  
) -> Order:
    available_flavours = [
        f for f in FlavourType
        if not _is_rare_flavour(f) or (unlocked_flavours and f in unlocked_flavours)
    ]
    available_creams = [
        c for c in CreamType
        if not _is_rare_cream(c) or (unlocked_creams and c in unlocked_creams) 
    ]

    cake_flavour = random.choice(available_flavours)
    cake_cream = random.choice(available_creams)
    
    coffee_type = random.choice(list(CoffeeType))

    if coffee_type == CoffeeType.ESPRESSO:
        coffee_milk = None
    else:
        coffee_milk = random.choice(list(MilkType))

    roll = random.random()
    
    if roll < 0.33:
        return create_cake_order(flavour=cake_flavour, cream=cake_cream)
    elif roll < 0.66:
        return create_coffee_order(coffee_type=coffee_type, milk_type=coffee_milk)
    else:
        return create_combo_order(flavour=cake_flavour, cream=cake_cream, coffee_type=coffee_type, milk_type=coffee_milk)


def _is_rare_cream(cream: CreamType) -> bool:
    from core.decorators.cream_decorator import CREAM_CONFIGS
    if isinstance(cream, str):
        try:
            cream = CreamType(cream)
        except ValueError:
            return False
            
    return CREAM_CONFIGS[cream].is_rare

def _is_rare_flavour(flavour: FlavourType) -> bool:
    from core.decorators.flavour_decorator import FLAVOUR_CONFIGS
    if isinstance(flavour, str):
        try:
            flavour = FlavourType(flavour)
        except ValueError:
            return False
            
    return FLAVOUR_CONFIGS[flavour].is_rare