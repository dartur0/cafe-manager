from __future__ import annotations
from dataclasses import dataclass

STAR_3_THRESHOLD = 0.75  
STAR_2_THRESHOLD = 0.50  
STAR_1_THRESHOLD = 0.25  

@dataclass(frozen=True)
class LevelConfig:
   
    day_number:         int
    customers_goal:     int
    day_duration:       float
    vip_chance:         float
    spawn_interval_min: float
    spawn_interval_max: float

LEVEL_CONFIGS: dict[int, LevelConfig] = {
    1: LevelConfig(
        day_number=1,
        customers_goal=5,
        day_duration=180.0,    
        vip_chance=0.0,            
        spawn_interval_min=10.0,
        spawn_interval_max=18.0,
    ),
    2: LevelConfig(
        day_number=2,
        customers_goal=8,
        day_duration=180.0,    
        vip_chance=0.20,          
        spawn_interval_min=7.0, 
        spawn_interval_max=14.0,
    ),
    3: LevelConfig(
        day_number=3,
        customers_goal=12,
        day_duration=210.0,     
        vip_chance=0.30,          
        spawn_interval_min=5.0, 
        spawn_interval_max=12.0,
    ),
    4: LevelConfig(
        day_number=4,
        customers_goal=16,
        day_duration=240.0,     
        vip_chance=0.40,           
        spawn_interval_min=4.0,
        spawn_interval_max=9.0,
    ),
    5: LevelConfig(
        day_number=5,
        customers_goal=20,
        day_duration=300.0,    
        vip_chance=0.50,          
        spawn_interval_min=3.0, 
        spawn_interval_max=7.0, 
    ),
}

def get_level(day_number: int) -> LevelConfig:
    if day_number not in LEVEL_CONFIGS:
        raise ValueError(f"Level {day_number} does not exist. Max level is 5.")
    return LEVEL_CONFIGS[day_number]


def calculate_stars(
    served_count:   int,
    customers_goal: int,
    avg_patience:   float,
) -> int:
    if served_count < customers_goal:
        return 0

    if avg_patience >= STAR_3_THRESHOLD:
        return 3
    elif avg_patience >= STAR_2_THRESHOLD:
        return 2
    elif avg_patience >= STAR_1_THRESHOLD:
        return 1
    else:
        return 1   

def is_last_level(day_number: int) -> bool:
    return day_number == max(LEVEL_CONFIGS.keys())