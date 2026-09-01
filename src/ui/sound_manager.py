import pygame


class SoundManager:

    music_volume = 0.5
    sfx_volume = 0.5

    @staticmethod
    def clamp_volume(value: float) -> float:

        return max(0.0, min(1.0, value))

    @staticmethod
    def set_music_volume(value: float):

        SoundManager.music_volume = SoundManager.clamp_volume(value)

        pygame.mixer.music.set_volume(SoundManager.music_volume)

    @staticmethod
    def set_sfx_volume(value: float):

        SoundManager.sfx_volume = SoundManager.clamp_volume(value)

    @staticmethod
    def play_music(path):

        pygame.mixer.music.stop()

        pygame.mixer.music.load(path)

        pygame.mixer.music.set_volume(SoundManager.music_volume)

        pygame.mixer.music.play(-1)

    @staticmethod
    def load_sound(path: str):

        try:
            return pygame.mixer.Sound(path)

        except pygame.error:
            print(f"Cannot load sound: {path}")
            return None

        except FileNotFoundError:
            print(f"Sound file not found: {path}")
            return None

    @staticmethod
    def play_sound(sound):

        if sound is None:
            return

        try:
            sound.set_volume(SoundManager.sfx_volume)

            sound.play()

        except pygame.error:
            pass
