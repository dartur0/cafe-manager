from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from core.decorators.base_product import ProductComponent, ProductDecorator

class CreamType(Enum):
    VANILLA    = "vanilla"
    CHOCOLATE  = "chocolate"
    STRAWBERRY = "strawberry"
    BANANA     = "banana"
    BLUEBERRY  = "blueberry"
    PISTACHIO  = "pistachio"


@dataclass(frozen=True)
class CreamConfig:
    display_name: str
    price_add:    float
    time_add:     float
    description:  str
    color:        tuple[int, int, int]
    is_rare:      bool = False

CREAM_CONFIGS: dict[CreamType, CreamConfig] = {
    CreamType.VANILLA: CreamConfig(
        display_name="Vanilla Cream",
        price_add=0.50,
        time_add=1.0,
        description="smooth vanilla cream",
        color=(255, 248, 220),    
        is_rare=False,
    ),
    CreamType.CHOCOLATE: CreamConfig(
        display_name="Chocolate Cream",
        price_add=1.00,
        time_add=2.0,
        description="rich chocolate cream",
        color=(101, 55, 0),         
        is_rare=False,
    ),
    CreamType.STRAWBERRY: CreamConfig(
        display_name="Strawberry Cream",
        price_add=1.50,
        time_add=4.0,
        description="fresh strawberry cream",
        color=(255, 105, 130),     
        is_rare=False,
    ),
    CreamType.BANANA: CreamConfig(
        display_name="Banana Cream",
        price_add=1.50,
        time_add=3.0,
        description="sweet banana cream",
        color=(255, 235, 100),     
        is_rare=False,
    ),
    CreamType.BLUEBERRY: CreamConfig(
        display_name="Blueberry Cream",
        price_add=2.00,
        time_add=3.0,
        description="tangy blueberry cream",
        color=(100, 80, 180),       
        is_rare=True,               
    ),
    CreamType.PISTACHIO: CreamConfig(
        display_name="Pistachio Cream",
        price_add=3.00,
        time_add=3.0,
        description="delicate pistachio cream",
        color=(130, 185, 110),      
        is_rare=True,              
    ),
}


class CreamDecorator(ProductDecorator):

    def __init__(
        self,
        product: ProductComponent,
        cream_type: CreamType,
        unlocked_creams: set[CreamType] | None = None,
    ) -> None:
    
        super().__init__(product)

        if cream_type not in CREAM_CONFIGS:
            raise ValueError(f"Unknown cream type: {cream_type}")

        config = CREAM_CONFIGS[cream_type]

        if (
            config.is_rare
            and unlocked_creams is not None
            and cream_type not in unlocked_creams
        ):
            raise ValueError(
                f"{config.display_name} is not unlocked yet. "
                f"Buy it in the shop first!"
            )

        self._cream_type = cream_type
        self._config     = config

    def get_name(self) -> str:
        return f"{self._product.get_name()} with {self._config.display_name}"

    def get_price(self) -> float:
        return self._product.get_price() + self._config.price_add

    def get_prep_time(self) -> float:
        return self._product.get_prep_time() + self._config.time_add

    def get_description(self) -> str:
        return f"{self._product.get_description()}, {self._config.description}"

    @property
    def cream_type(self) -> CreamType:
        return self._cream_type

    @property
    def color(self) -> tuple[int, int, int]:
        return self._config.color

    @property
    def is_rare(self) -> bool:
        return self._config.is_rare

    @staticmethod
    def get_available_creams(
        unlocked_creams: set[CreamType] | None = None,
    ) -> list[dict]:
        result = []
        for cream_type, config in CREAM_CONFIGS.items():
            locked = (
                config.is_rare
                and unlocked_creams is not None
                and cream_type not in unlocked_creams
            )
            result.append({
                "type":      cream_type,
                "name":      config.display_name,
                "price_add": config.price_add,
                "time_add":  config.time_add,
                "color":     config.color,
                "is_rare":   config.is_rare,
                "locked":    locked,
            })
        return result