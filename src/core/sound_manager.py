import pygame.mixer


class SoundManager:
    """
    The sound manager class.
    """

    def __init__(self):
        self._sounds = {}
        self._sound_volume = 0.3
        self._music_volume = 0.1
        self._sound_cooldowns = {}
        self._cooldown_times = {
            "fox-bounce": 150,
            "fox-fly-away": 1000,
            "score": 0,
            "bonus": 0,
        }
        self._load_sounds()
        self._setup_music()

    @property
    def sound_volume(self) -> float:
        return self._sound_volume

    @property
    def music_volume(self) -> float:
        return self._music_volume

    @property
    def sound_muted(self) -> bool:
        return self.sound_volume == 0.0

    @property
    def music_muted(self) -> bool:
        return self.music_volume == 0.0

    @property
    def sounds(self) -> tuple:
        return tuple(self._sounds)

    @property
    def sound_cooldowns(self) -> tuple:
        return tuple(self._sound_cooldowns)

    @property
    def cooldown_times(self) -> tuple:
        return tuple(self._cooldown_times)

    def _load_sounds(self) -> None:
        """
        Load the sounds.
        """
        self._sounds = {
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

        for sound in self._sounds.values():
            sound.set_volume(self.sound_volume)

    def _setup_music(self) -> None:
        """
        Set up the background music.
        """
        pygame.mixer.music.load("assets/sounds/background-music-normalized.mp3")
        pygame.mixer.music.set_volume(self.music_volume)

    def play_sound(self, sound_name: str) -> None:
        """
        Play a sound.
        """
        current_time = pygame.time.get_ticks()

        if sound_name not in self.sounds:
            return

        if sound_name in self._sound_cooldowns:
            last_played = self._sound_cooldowns[sound_name]
            cooldown = self._cooldown_times.get(sound_name, 0)
            if current_time - last_played < cooldown:
                return

        self._sounds[sound_name].play()
        self._sound_cooldowns[sound_name] = current_time

    def start_music(self) -> None:
        """Start the background music."""
        pygame.mixer.music.play(-1)

    def stop_music(self) -> None:
        """Stop the background music."""
        pygame.mixer.music.stop()

    def set_sound_volume(self, volume: float) -> None:
        """
        Set the sound volume.

        Args:
            volume (float): The volume to set
        """
        self._sound_volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.set_volume(self.sound_volume)

    def set_music_volume(self, volume: float) -> None:
        """
        Set the music volume.

        Args:
            volume (float): The volume to set
        """
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def toggle_sound(self) -> None:
        """
        Toggle the sound.
        If sound is muted, set the volume to 0.3, otherwise set it to 0.0.
        """
        if self.sound_muted:
            self.set_sound_volume(0.3)
        else:
            self.set_sound_volume(0.0)

    def toggle_music(self) -> None:
        """
        Toggle the music.
        If music is muted, set the volume to 0.1, otherwise set it to 0.0.
        """
        if self.music_muted:
            self.set_music_volume(0.1)
        else:
            self.set_music_volume(0.0)
