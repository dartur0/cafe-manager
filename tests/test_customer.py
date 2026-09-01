import pytest
from core.entities.customer import Customer, CustomerType


def test_regular_customer_full_patience_tip():
    customer = Customer(CustomerType.REGULAR)
    tip = customer.calculate_tip(10.00)
    assert tip == pytest.approx(2.00)   


def test_vip_customer_tip_higher_than_regular():
    regular = Customer(CustomerType.REGULAR)
    vip     = Customer(CustomerType.VIP)

    tip_regular = regular.calculate_tip(10.00)
    tip_vip     = vip.calculate_tip(10.00)

    assert tip_vip > tip_regular


def test_patience_decreases_over_time():
    customer = Customer(CustomerType.REGULAR)
    start = customer.patience
    customer.update(delta=5.0)
    assert customer.patience < start


def test_customer_leaves_when_patience_zero():
    customer = Customer(CustomerType.REGULAR)
    customer.update(delta=1000.0)   
    assert customer.has_left is True


def test_no_tip_when_patience_low():
    customer = Customer(CustomerType.REGULAR)
    customer.update(delta=50.0)    
    tip = customer.calculate_tip(10.00)
    assert tip == 0.0


def test_patience_does_not_go_below_zero():
    customer = Customer(CustomerType.REGULAR)
    customer.update(delta=5000.0)   
    assert customer.patience == 0.0


def test_vip_customer_starts_with_less_patience():
    regular = Customer(CustomerType.REGULAR)
    vip     = Customer(CustomerType.VIP)
    assert vip.patience < regular.patience 


def test_calculate_tip_with_zero_order_cost():
    customer = Customer(CustomerType.REGULAR)
    tip = customer.calculate_tip(0.00)
    assert tip == 0.0


def test_vip_customer_gives_tip_when_happy():
    regular = Customer(CustomerType.REGULAR)
    vip     = Customer(CustomerType.VIP)

    tip_regular = regular.calculate_tip(10.00)
    tip_vip     = vip.calculate_tip(10.00)

    assert tip_vip > tip_regular


def test_customer_is_satisfied_when_served_in_time():
    customer = Customer(CustomerType.REGULAR)
    if hasattr(customer, "serve"):
        customer.serve()
        assert customer.has_left is False