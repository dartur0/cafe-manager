from __future__ import annotations
from abc import ABC, abstractmethod

class ProductComponent(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_prep_time(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    def get_display_info(self) -> dict:
        return {
            "name": self.get_name(),
            "price": round(self.get_price(), 2),
            "prep_time": self.get_prep_time(),
            "description": self.get_description(),
        }

    def __str__(self) -> str:
        return (
            f"{self.get_name()} | "
            f"${self.get_price():.2f} | "
            f"{self.get_prep_time():.1f}s"
        )


class ProductDecorator(ProductComponent):
    def __init__(self, product: ProductComponent) -> None:
        self._product = product

    def get_name(self) -> str:
        return self._product.get_name()

    def get_price(self) -> float:
        return self._product.get_price()

    def get_prep_time(self) -> float:
        return self._product.get_prep_time()

    def get_description(self) -> str:
        return self._product.get_description()