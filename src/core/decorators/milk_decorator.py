from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from core.decorators.base_product import ProductComponent, ProductDecorator

class MilkType(Enum):
    REGULAR      = "regular"
    LACTOSE_FREE = "lactose_free"
    OAT          = "oat"

@dataclass(frozen=True)
class MilkConfig:
    display_name: str
    price_add:    float
    time_add:     float
    description:  str
    color:        tuple[int, int, int]

MILK_CONFIGS: dict[MilkType, MilkConfig] = {
    MilkType.REGULAR: MilkConfig(
        display_name="Regular",
        price_add=0.00,
        time_add=0.0,
        description="regular milk",
        color=(245, 245, 245),      
    ),
    MilkType.LACTOSE_FREE: MilkConfig(
        display_name="Lactose-Free",
        price_add=0.50,
        time_add=0.5,
        description="lactose-free milk",
        color=(240, 248, 255),      
    ),
    MilkType.OAT: MilkConfig(
        display_name="Oat",
        price_add=0.70,
        time_add=0.5,
        description="creamy oat milk",
        color=(235, 220, 180),    
    ),
}


class MilkDecorator(ProductDecorator):
   
    def __init__(
        self,
        product: ProductComponent,
        milk_type: MilkType,
    ) -> None:
        super().__init__(product)

        if milk_type not in MILK_CONFIGS:
            raise ValueError(f"Unknown milk type: {milk_type}")

        self._milk_type = milk_type
        self._config    = MILK_CONFIGS[milk_type]

    def get_name(self) -> str:
        if self._milk_type == MilkType.REGULAR:
            return self._product.get_name()
        return f"{self._product.get_name()} ({self._config.display_name})"

    def get_price(self) -> float:
        return self._product.get_price() + self._config.price_add

    def get_prep_time(self) -> float:
        return self._product.get_prep_time() + self._config.time_add

    def get_description(self) -> str:
        if self._milk_type == MilkType.REGULAR:
            return self._product.get_description()
        return f"{self._product.get_description()}, {self._config.description}"

    @property
    def milk_type(self) -> MilkType:
        return self._milk_type

    @property
    def color(self) -> tuple[int, int, int]:
        return self._config.color

    @staticmethod
    def get_available_milks() -> list[dict]:
        return [
            {
                "type":      milk_type,
                "name":      config.display_name,
                "price_add": config.price_add,
                "time_add":  config.time_add,
                "color":     config.color,
            }
            for milk_type, config in MILK_CONFIGS.items()
        ]