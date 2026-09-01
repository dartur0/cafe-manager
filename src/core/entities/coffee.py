from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from core.decorators.base_product import ProductComponent
from core.decorators.milk_decorator import MilkDecorator, MilkType

class CoffeeType(Enum):
    ESPRESSO    = "espresso"
    MILK_COFFEE = "milk_coffee" 


@dataclass(frozen=True)
class CoffeeConfig:
    display_name: str
    base_price:   float
    base_time:    float
    description:  str
    color:        tuple[int, int, int]
    needs_beans:  int
    needs_milk:   bool


COFFEE_CONFIGS: dict[CoffeeType, CoffeeConfig] = {
    CoffeeType.ESPRESSO: CoffeeConfig(
        display_name="Espresso",
        base_price=2.00,
        base_time=5.0,
        description="Strong double espresso",
        color=(60, 30, 10),         
        needs_beans=2,
        needs_milk=False,
    ),
    CoffeeType.MILK_COFFEE: CoffeeConfig(
        display_name="Coffee with Milk",
        base_price=3.80,  
        base_time=8.5,
        description="Freshly brewed coffee with steamed milk",
        color=(195, 145, 85),      
        needs_beans=2,
        needs_milk=True,
    ),
}


class BaseCoffee(ProductComponent):

    def __init__(self, coffee_type: CoffeeType) -> None:
        if coffee_type not in COFFEE_CONFIGS:
            raise ValueError(f"Unknown coffee type: {coffee_type}")

        self._coffee_type = coffee_type
        self._config      = COFFEE_CONFIGS[coffee_type]

    def get_name(self) -> str:
        return self._config.display_name

    def get_price(self) -> float:
        return self._config.base_price

    def get_prep_time(self) -> float:
        return self._config.base_time

    def get_description(self) -> str:
        return self._config.description

    @property
    def coffee_type(self) -> CoffeeType:
        return self._coffee_type

    @property
    def color(self) -> tuple[int, int, int]:
        return self._config.color

    @property
    def needs_beans(self) -> int:
        return self._config.needs_beans

    @property
    def needs_milk(self) -> bool:
        return self._config.needs_milk

    @staticmethod
    def get_available_coffees() -> list[dict]:
        return [
            {
                "type":       coffee_type,
                "name":       config.display_name,
                "base_price": config.base_price,
                "base_time":  config.base_time,
                "color":      config.color,
                "needs_milk": config.needs_milk,
            }
            for coffee_type, config in COFFEE_CONFIGS.items()
        ]


def build_coffee(
    coffee_type: CoffeeType,
    milk_type:   MilkType = MilkType.REGULAR,
) -> ProductComponent:
   
    config = COFFEE_CONFIGS[coffee_type]

    if not config.needs_milk and milk_type != MilkType.REGULAR:
        raise ValueError(
            f"Espresso does not use milk. "
            f"Cannot apply {milk_type.value} milk."
        )

    product: ProductComponent = BaseCoffee(coffee_type)
    
    if config.needs_milk:
        product = MilkDecorator(product, milk_type)

    return product