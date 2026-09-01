from __future__ import annotations
from core.decorators.base_product import ProductComponent
from core.decorators.flavour_decorator import FlavourDecorator, FlavourType
from core.decorators.cream_decorator import CreamDecorator, CreamType

class BaseCake(ProductComponent):
    BASE_PRICE = 3.00
    BASE_TIME  = 8.0

    def __init__(self) -> None:
        super().__init__() 

    def get_name(self) -> str:   
        return "Cake"
        
    def get_price(self) -> float: 
        return self.BASE_PRICE
        
    def get_prep_time(self) -> float: 
        return self.BASE_TIME
        
    def get_description(self) -> str:   
        return "a slice of cake"

def build_cake(
    flavour:           FlavourType,
    cream:             CreamType,
    unlocked_flavours: set[FlavourType] | None = None,
    unlocked_creams:   set[CreamType]   | None = None,
) -> ProductComponent:
    
    product: ProductComponent = BaseCake()
    
    product = FlavourDecorator(product, flavour, unlocked_flavours)
    product = CreamDecorator(product, cream, unlocked_creams)

    return product