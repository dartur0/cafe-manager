from core.systems.level import calculate_stars, get_level
import pytest 


def test_three_stars_when_all_happy():
    stars = calculate_stars(served_count=5, customers_goal=5, avg_patience=0.80)
    assert stars == 3


def test_zero_stars_when_goal_not_met():
    stars = calculate_stars(served_count=3, customers_goal=5, avg_patience=0.90)
    assert stars == 0


def test_level_2_has_vip_chance():
    level = get_level(2)
    assert level.vip_chance > 0


def test_level_1_has_no_vip():
    level = get_level(1)
    assert level.vip_chance == 0.0

def test_one_star_minimum_pass():
    stars = calculate_stars(served_count=5, customers_goal=5, avg_patience=0.30)
    assert stars == 1


def test_two_stars_medium_patience():
    stars = calculate_stars(served_count=5, customers_goal=5, avg_patience=0.55)
    assert stars == 2


def test_zero_stars_served_count_exceeds_but_goal_not_reached():
    stars = calculate_stars(served_count=0, customers_goal=5, avg_patience=1.00)
    assert stars == 0


def test_final_level_difficulty_scaling():
    level_1 = get_level(1)
    final_level = get_level(5)
    
    assert final_level.customers_goal > level_1.customers_goal
    assert final_level.spawn_interval_min < level_1.spawn_interval_min


def test_invalid_level_handling():
    with pytest.raises(ValueError):
        get_level(999)