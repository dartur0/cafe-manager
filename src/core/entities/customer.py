from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from entities.order import Order

class CustomerType(Enum):
    REGULAR = "regular"
    VIP     = "vip"


class CustomerMood(Enum):
    HAPPY    = "happy"    
    NEUTRAL  = "neutral"   
    ANGRY    = "angry"     

@dataclass(frozen=True)
class CustomerConfig:
    max_patience: float
    tip_q1:       float   
    tip_q2:       float   
    drain_rate:   float   


CUSTOMER_CONFIGS: dict[CustomerType, CustomerConfig] = {
    CustomerType.REGULAR: CustomerConfig(
        max_patience=60.0,
        tip_q1=0.20,       
        tip_q2=0.10,     
        drain_rate=1.0,    
    ),
    CustomerType.VIP: CustomerConfig(
        max_patience=40.0,  
        tip_q1=0.50,      
        tip_q2=0.25,        
        drain_rate=1.5,    
    ),
}

REGULAR_NAMES = [
    "Alice", "Bob", "Carol", "Dave", "Emma",
    "Frank", "Grace", "Henry", "Iris", "Jack",
]
VIP_NAMES = [
    "Lady Rose", "Lord Grey", "Miss Pearl",
    "Sir Edmund", "Duchess Kay",
]


class Customer:
    name: str
    order: Optional[Order]

    def __init__(
        self,
        customer_type: CustomerType,
        name: str | None = None,
    ) -> None:
        self._type   = customer_type
        self._config = CUSTOMER_CONFIGS[customer_type]

        if name:
            self.name = name
        elif customer_type == CustomerType.VIP:
            self.name = random.choice(VIP_NAMES)
        else:
            self.name = random.choice(REGULAR_NAMES)

        self._patience:     float = self._config.max_patience
        self._max_patience: float = self._config.max_patience

        self.order = None

        self._is_served: bool = False  
        self._has_left:  bool = False  

    def update(self, delta: float) -> None:
        if self._is_served or self._has_left:
            return

        self._patience -= self._config.drain_rate * delta
        self._patience  = max(0.0, self._patience)

        if self._patience <= 0:
            self._has_left = True

    def calculate_tip(self, base_price: float) -> float:
        ratio = self._patience / self._max_patience 

        if ratio >= 0.75:
            tip_rate = self._config.tip_q1  
        elif ratio >= 0.50:
            tip_rate = self._config.tip_q2   
        else:
            tip_rate = 0.0                 

        return round(base_price * tip_rate, 2)

    @property
    def mood(self) -> CustomerMood:
        ratio = self._patience / self._max_patience

        if ratio > 0.50:
            return CustomerMood.HAPPY
        elif ratio > 0.25:
            return CustomerMood.NEUTRAL
        else:
            return CustomerMood.ANGRY

    @property
    def customer_type(self) -> CustomerType:
        return self._type

    @property
    def patience(self) -> float:
        return self._patience

    @property
    def patience_ratio(self) -> float:
        return self._patience / self._max_patience

    @property
    def is_vip(self) -> bool:
        return self._type == CustomerType.VIP

    @property
    def is_served(self) -> bool:
        return self._is_served

    @property
    def has_left(self) -> bool:
        return self._has_left

    def set_order(self, order: Order) -> None:
        self.order = order

    def mark_served(self) -> None:
        self._is_served = True

    def get_status(self) -> dict:
        return {
            "name":           self.name,
            "type":           self._type.value,
            "patience":       round(self._patience, 1),
            "patience_ratio": round(self.patience_ratio, 2),
            "mood":           self.mood.value,
            "is_vip":         self.is_vip,
            "is_served":      self._is_served,
            "has_left":       self._has_left,
        }

def create_customer(customer_type: CustomerType | None = None) -> Customer:
    if customer_type is None:
        customer_type = (
            CustomerType.VIP
            if random.random() < 0.20
            else CustomerType.REGULAR
        )
    return Customer(customer_type)