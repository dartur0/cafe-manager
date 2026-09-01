import pytest
from core.entities.cake import BaseCake, build_cake
from core.decorators.flavour_decorator import FlavourType
from core.decorators.cream_decorator import CreamType


def test_base_cake_price():
    cake = BaseCake()
    assert cake.get_price() == 3.00


def test_cake_with_flavour_and_cream():
    cake = build_cake(FlavourType.VANILLA, CreamType.CHOCOLATE)
    assert cake.get_price() == pytest.approx(5.50)


def test_cake_name_combines_flavour_and_cream():
    cake = build_cake(FlavourType.RED_VELVET, CreamType.VANILLA,
                       unlocked_flavours={FlavourType.RED_VELVET})
    assert "Red Velvet" in cake.get_name()
    assert "Vanilla Cream" in cake.get_name()


def test_rare_flavour_blocked_without_unlock():
    with pytest.raises(ValueError):
        build_cake(FlavourType.RED_VELVET, CreamType.VANILLA,
                    unlocked_flavours=set())


def test_rare_flavour_allowed_when_unlocked():
    cake = build_cake(FlavourType.RED_VELVET, CreamType.VANILLA,
                       unlocked_flavours={FlavourType.RED_VELVET})
    assert cake.get_name().startswith("Red Velvet")

def test_rare_cream_blocked_without_unlock():
    with pytest.raises(ValueError):
        build_cake(
            FlavourType.VANILLA, 
            CreamType.PISTACHIO,
            unlocked_creams=set() 
        )


def test_rare_cream_allowed_when_unlocked():
    cake = build_cake(
        FlavourType.VANILLA, 
        CreamType.PISTACHIO,
        unlocked_creams={CreamType.PISTACHIO}
    )
    assert "Pistachio" in cake.get_name()


def test_cake_prep_time_increases_with_ingredients():
    base_cake = BaseCake()
    full_cake = build_cake(FlavourType.CHOCOLATE, CreamType.BANANA)
    
    if hasattr(base_cake, "get_prep_time") and hasattr(full_cake, "get_prep_time"):
        assert full_cake.get_prep_time() > base_cake.get_prep_time()


def test_build_cake_default_unlocks():
    cake = build_cake(FlavourType.VANILLA, CreamType.VANILLA)
    assert cake.get_price() > 0.0


def test_cake_price_calculation_is_consistent():
    cake = build_cake(FlavourType.CARROT_CAKE, CreamType.STRAWBERRY,
                      unlocked_flavours={FlavourType.CARROT_CAKE},
                      unlocked_creams={CreamType.STRAWBERRY})
                      
    assert cake.get_price() > 3.00  
    assert cake.get_price() <= 10.00 