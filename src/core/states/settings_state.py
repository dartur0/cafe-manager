from __future__ import annotations
import json
import os
import pygame

from core.states.base_state import BaseState
from ui.screens.settings_screen import SettingsScreen
from ui.sound_manager import SoundManager 
from config import SETTINGS_PATH, DEFAULT_MUSIC_VOLUME, DEFAULT_SFX_VOLUME

class SettingsState(BaseState):
    def __init__(self, from_state: str = "menu", prev_screen=None) -> None:
        self._prev_screen = prev_screen 
        super().__init__()
        self._from_state = from_state
        self._screen: SettingsScreen | None = None

        self.music_volume: float = SoundManager.music_volume
        self.sfx_volume:   float = SoundManager.sfx_volume

    def on_enter(self) -> None:
        screen = pygame.display.get_surface()
        
        self._screen = SettingsScreen(
            screen=screen,
            music_volume=SoundManager.music_volume,
            sfx_volume=SoundManager.sfx_volume,
        )
        self._apply_music(SoundManager.music_volume)
        self._apply_sfx(SoundManager.sfx_volume)

    def on_exit(self) -> None:
        self._save()

    def handle_event(self, event: pygame.event.Event) -> None:
        if self._screen is None:
            return

        action = self._screen.handle_event(event)

        if action is None:
            return

        if isinstance(action, dict) and "music" in action:
            self.music_volume = float(action["music"])
            self._apply_music(self.music_volume)

        elif isinstance(action, dict) and "sfx" in action:
            self.sfx_volume = float(action["sfx"])
            self._apply_sfx(self.sfx_volume)

        elif action == "back":
            self.next_state = self._from_state

    def update(self, delta: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self._prev_screen is not None:
            self._prev_screen.draw()      
        if self._screen is not None:
            self._screen.draw()

    def _apply_music(self, volume: float) -> None:
        volume = max(0.0, min(1.0, volume))   
        SoundManager.music_volume = volume 
        pygame.mixer.music.set_volume(volume)

    def _apply_sfx(self, volume: float) -> None:
        volume = max(0.0, min(1.0, volume))
        SoundManager.sfx_volume = volume 
        for i in range(pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(i).set_volume(volume)

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
            data = {
                "music_volume": round(SoundManager.music_volume, 2),
                "sfx_volume":   round(SoundManager.sfx_volume,   2),
            }
            with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"[SettingsState] Failed to save: {e}")

    @staticmethod
    def _load() -> dict:
        try:
            if os.path.exists(SETTINGS_PATH):
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[SettingsState] Failed to load: {e}")
        return {}

    @staticmethod
    def load_and_apply() -> None:
        try:
            if os.path.exists(SETTINGS_PATH):
                with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                music = float(data.get("music_volume", DEFAULT_MUSIC_VOLUME))
                sfx = float(data.get("sfx_volume", DEFAULT_SFX_VOLUME))
                
                SoundManager.music_volume = music
                SoundManager.sfx_volume = sfx
                
                pygame.mixer.music.set_volume(music)
        except (OSError, json.JSONDecodeError):
            pass