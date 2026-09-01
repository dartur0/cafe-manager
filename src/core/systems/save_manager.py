from __future__ import annotations
import json
import os
from dataclasses import dataclass

from config import SAVE_PATH

@dataclass
class SaveData:
    day:       int
    money:     float
    purchased: set[str]
    stars:     dict[int, int]


class SaveManager:
    @staticmethod
    def save(
        day:       int,
        money:     float,
        purchased: set[str],
        stars:     dict[int, int],
    ) -> bool:
        
        try:
            os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

            data = {
                "day":       day,
                "money":     round(money, 2),
                "purchased": list(purchased),       
                "stars":     {str(k): v for k, v in stars.items()},
            }

            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return True

        except (OSError, TypeError) as e:
            print(f"[SaveManager] Failed to save: {e}")
            return False

    @staticmethod
    def load() -> SaveData | None:
        if not SaveManager.exists():
            return None

        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

            return SaveData(
                day=int(data.get("day", 1)),
                money=float(data.get("money", 0.0)),
                purchased=set(data.get("purchased", [])),
                stars={
                    int(k): int(v)
                    for k, v in data.get("stars", {}).items()
                },
            )

        except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"[SaveManager] Failed to load: {e}")
            return None

    @staticmethod
    def exists() -> bool:
        return os.path.exists(SAVE_PATH)

    @staticmethod
    def delete() -> bool:
        try:
            if SaveManager.exists():
                os.remove(SAVE_PATH)
            return True
        except OSError as e:
            print(f"[SaveManager] Failed to delete: {e}")
            return False

    @staticmethod
    def get_best_stars(stars: dict[int, int], day: int) -> int:
        return stars.get(day, 0)

    @staticmethod
    def update_stars(
        stars:     dict[int, int],
        day:       int,
        new_stars: int,
    ) -> dict[int, int]:
        updated = dict(stars)
        current = updated.get(day, 0)
        updated[day] = max(current, new_stars)   
        return updated

    @staticmethod
    def new_game_data() -> SaveData:
        return SaveData(
            day=1,
            money=0.0,
            purchased=set(),
            stars={},
        )