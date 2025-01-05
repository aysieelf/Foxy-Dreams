import pygame.mixer


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.sound_volume = 0.3
        self.music_volume = 0.1
        self.sound_cooldowns = {}
        self.cooldown_times = {
            "fox-bounce": 150,
            "fox-fly-away": 1000,
            "score": 0,
            "bonus": 0,
        }
        self._load_sounds()
        self._setup_music()

    def _load_sounds(self):
        self.sounds = {
            "bonus-collect": pygame.mixer.Sound(
                "assets/sounds/bonus-collect-normalized.wav"
            ),
            "fox-bounce": pygame.mixer.Sound("assets/sounds/fox-bounce-normalized.wav"),
            "fox-fly-away": pygame.mixer.Sound(
                "assets/sounds/fox-fly-away-normalized.wav"
            ),
            "mouse-click": pygame.mixer.Sound(
                "assets/sounds/mouse-click-normalized.wav"
            ),
        }

        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)

    def _setup_music(self):
        pygame.mixer.music.load("assets/sounds/background-music-normalized.mp3")
        pygame.mixer.music.set_volume(self.music_volume)

    def play_sound(self, sound_name: str):
        current_time = pygame.time.get_ticks()

        if sound_name not in self.sounds:
            return

        if sound_name in self.sound_cooldowns:
            print("It's in cooldown!")
            last_played = self.sound_cooldowns[sound_name]
            cooldown = self.cooldown_times.get(sound_name, 0)
            print(cooldown)
            if current_time - last_played < cooldown:
                return

        self.sounds[sound_name].play()
        self.sound_cooldowns[sound_name] = current_time

    def start_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_sound_volume(self, volume: float):
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds:
            sound.set_volume(self.sound_volume)

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
