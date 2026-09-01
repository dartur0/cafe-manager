import pytest
from core.entities.order import create_cake_order, create_coffee_order, create_combo_order
from core.decorators.flavour_decorator import FlavourType
from core.decorators.cream_decorator import CreamType
from core.entities.coffee import CoffeeType
from core.decorators.milk_decorator import MilkType


def test_cake_order_matches_correct_cake():
    order = create_cake_order(FlavourType.VANILLA, CreamType.CHOCOLATE)
    assert order.matches_cake(FlavourType.VANILLA, CreamType.CHOCOLATE) is True


def test_cake_order_rejects_wrong_flavour():
    order = create_cake_order(FlavourType.VANILLA, CreamType.CHOCOLATE)
    assert order.matches_cake(FlavourType.CHOCOLATE, CreamType.CHOCOLATE) is False


def test_coffee_order_price_is_positive():
    order = create_coffee_order(CoffeeType.MILK_COFFEE)
    assert order.get_price() > 0


def test_coffee_order_matches_correct_coffee_and_milk():
    order = create_coffee_order(CoffeeType.MILK_COFFEE, MilkType.OAT)
    assert order.matches_coffee(CoffeeType.MILK_COFFEE, MilkType.OAT) is True


def test_coffee_order_rejects_wrong_milk():
    order = create_coffee_order(CoffeeType.MILK_COFFEE, MilkType.OAT)
    assert order.matches_coffee(CoffeeType.MILK_COFFEE, MilkType.REGULAR) is False


def test_espresso_order_expects_no_milk():
    order = create_coffee_order(CoffeeType.ESPRESSO, None)
    assert order.matches_coffee(CoffeeType.ESPRESSO, None) is True


def test_cake_order_rejects_coffee_matching():
    order = create_cake_order(FlavourType.VANILLA, CreamType.CHOCOLATE)
    assert hasattr(order, "matches_coffee") and order.matches_coffee(CoffeeType.ESPRESSO, None) is False


def test_combo_order_total_price_is_sum():
    combo_order = create_combo_order(
        flavour=FlavourType.VANILLA,
        cream=CreamType.VANILLA,
        coffee_type=CoffeeType.ESPRESSO,
        milk_type=None
    )
    assert combo_order.get_price() > 0

