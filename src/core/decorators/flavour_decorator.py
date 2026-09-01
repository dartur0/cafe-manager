from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from core.decorators.base_product import ProductComponent, ProductDecorator

class FlavourType(Enum):
    VANILLA     = "vanilla"
    CHOCOLATE   = "chocolate"
    RED_VELVET  = "red_velvet"
    CARROT_CAKE = "carrot_cake"


@dataclass(frozen=True)
class FlavourConfig:
    display_name: str
    price_add:    float
    time_add:     float
    description:  str
    color:        tuple[int, int, int]
    is_rare:      bool = False

FLAVOUR_CONFIGS: dict[FlavourType, FlavourConfig] = {
    FlavourType.VANILLA: FlavourConfig(
        display_name="Vanilla",
        price_add=1.50,
        time_add=2.0,
        description="light vanilla sponge",
        color=(255, 248, 220),     
        is_rare=False,
    ),
    FlavourType.CHOCOLATE: FlavourConfig(
        display_name="Chocolate",
        price_add=2.00,
        time_add=3.0,
        description="rich chocolate sponge",
        color=(101, 55, 0),        
        is_rare=False,
    ),
    FlavourType.RED_VELVET: FlavourConfig(
        display_name="Red Velvet",
        price_add=3.00,
        time_add=5.0,
        description="velvety red sponge with cocoa hint",
        color=(180, 30, 30),        
        is_rare=True,              
    ),
    FlavourType.CARROT_CAKE: FlavourConfig(
        display_name="Carrot Cake",
        price_add=3.00,
        time_add=5.0,
        description="moist spiced carrot sponge",
        color=(210, 130, 60),       
        is_rare=True,              
    ),
}


class FlavourDecorator(ProductDecorator):
    def __init__(
        self,
        product: ProductComponent,
        flavour_type: FlavourType,
        unlocked_flavours: set[FlavourType] | None = None,
    ) -> None:

        super().__init__(product)

        if flavour_type not in FLAVOUR_CONFIGS:
            raise ValueError(f"Unknown flavour type: {flavour_type}")

        config = FLAVOUR_CONFIGS[flavour_type]

        if (
            config.is_rare
            and unlocked_flavours is not None
            and flavour_type not in unlocked_flavours
        ):
            raise ValueError(
                f"{config.display_name} is not unlocked yet. "
                f"Buy it in the shop first!"
            )

        self._flavour_type = flavour_type
        self._config       = config

    def get_name(self) -> str:
        return self._config.display_name

    def get_price(self) -> float:
        return self._product.get_price() + self._config.price_add

    def get_prep_time(self) -> float:
        return self._product.get_prep_time() + self._config.time_add

    def get_description(self) -> str:
        return self._config.description

    @property
    def flavour_type(self) -> FlavourType:
        return self._flavour_type

    @property
    def color(self) -> tuple[int, int, int]:
        return self._config.color

    @property
    def is_rare(self) -> bool:
        return self._config.is_rare

    @staticmethod
    def get_available_flavours(
        unlocked_flavours: set[FlavourType] | None = None,
    ) -> list[dict]:
        result = []
        for flavour_type, config in FLAVOUR_CONFIGS.items():
            locked = (
                config.is_rare
                and unlocked_flavours is not None
                and flavour_type not in unlocked_flavours
            )
            result.append({
                "type":      flavour_type,
                "name":      config.display_name,
                "price_add": config.price_add,
                "time_add":  config.time_add,
                "color":     config.color,
                "is_rare":   config.is_rare,
                "locked":    locked,
            })
        return result