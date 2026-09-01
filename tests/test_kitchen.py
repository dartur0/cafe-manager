from core.entities.kitchen import Kitchen
from core.decorators.flavour_decorator import FlavourType
from core.decorators.cream_decorator import CreamType
from core.entities.coffee import CoffeeType


def test_kitchen_starts_with_resources():
    kitchen = Kitchen()
    status = kitchen.get_status()
    assert status["coffee_machine"]["beans"] > 0


def test_start_cake_uses_base_storage():
    kitchen = Kitchen()
    kitchen.perform_delivery_refill(set())

    before = kitchen.base_storage.stock[FlavourType.VANILLA]
    success, reason = kitchen.start_cake(FlavourType.VANILLA, CreamType.CHOCOLATE)

    assert success is True
    assert kitchen.base_storage.stock[FlavourType.VANILLA] == before - 1


def test_start_cake_fails_without_base():
    kitchen = Kitchen()
    kitchen.base_storage.stock[FlavourType.VANILLA] = 0

    success, reason = kitchen.start_cake(FlavourType.VANILLA, CreamType.CHOCOLATE)
    assert success is False
    assert reason == "no_base"


def test_brew_espresso_consumes_beans():
    kitchen = Kitchen()
    before = kitchen.coffee_machine.beans

    success, reason = kitchen.brew_espresso(CoffeeType.ESPRESSO)

    assert success is True
    assert kitchen.coffee_machine.beans == before - 2


def test_customer_slots_max_four():
    kitchen = Kitchen()
    from core.entities.customer import create_customer

    for _ in range(4):
        assert kitchen.customer_slots.add(create_customer()) is True

    assert kitchen.customer_slots.add(create_customer()) is False


def test_upgrade_cake_slots_increases_capacity():
    kitchen = Kitchen()
    initial_slots = len(kitchen.cake_station.slots)
    
    if hasattr(kitchen, "upgrade_cake_slot"):
        kitchen.upgrade_cake_slot()
        assert len(kitchen.cake_station.slots) == initial_slots + 1


def test_delivery_refill_respects_max_cream_upgrade():
    kitchen = Kitchen()
    purchased_upgrades = {"kitchen_more_cream"}
    
    kitchen.cream = 0
    kitchen.perform_delivery_refill(purchased_upgrades)
    
    assert kitchen.cream == kitchen.max_cream
    assert kitchen.cream >= 10


def test_showcase_slots_max_capacity():
    kitchen = Kitchen()
    showcase = kitchen.showcase
    max_slots = showcase.max_slots
    
    from core.entities.cake import BaseCake
    for _ in range(max_slots):
        showcase.add_cake(BaseCake(), FlavourType.VANILLA, CreamType.VANILLA)
        
    success = showcase.add_cake(BaseCake(), FlavourType.VANILLA, CreamType.VANILLA)
    assert success is False
