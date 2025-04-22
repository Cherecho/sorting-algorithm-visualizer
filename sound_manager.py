import numpy as np
import pygame
import math

SAMPLE_RATE = 44100
SOUND_DURATION_MS = 30
MIN_FREQ = 100
MAX_FREQ = 1200
VOLUME = 0.1


def generate_sine_wave(freq, duration_samples, sample_rate):
    """Generates a single sine wave cycle."""
    t = np.linspace(0, duration_samples / sample_rate, duration_samples, endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    fade_len = int(0.1 * duration_samples)
    if fade_len > 0:
        fade_curve = np.linspace(1.0, 0.0, fade_len)
        wave[-fade_len:] *= fade_curve
    return (wave * 32767 * VOLUME).astype(np.int16)


class SoundManager:
    """
    Manages the generation and playback of sounds for visualizing sorting algorithms.
    The SoundManager initializes the Pygame mixer and creates a cache of sounds
    corresponding to different values. It generates sine wave sounds with frequencies
    mapped to the input values, allowing for audio feedback during sorting.
    Attributes:
        max_value (int): The maximum value expected in the data to be sorted.
            Used to normalize the frequency of the generated sounds.
        _sound_cache (dict): A dictionary to cache generated sounds,
            where keys are integer representations of values and values are
            Pygame Sound objects.
    Methods:
        __init__(self, max_value):
            Initializes the SoundManager, sets up the Pygame mixer if not already
            initialized, and prepares the sound cache.
        _get_sound(self, value):
            Retrieves a sound from the cache or generates a new one if it doesn't exist.
            The frequency of the sound is determined by mapping the input value to a
            frequency range between MIN_FREQ and MAX_FREQ.
        play_sound(self, value):
            Plays the sound corresponding to the given value using a Pygame channel.
            If the Pygame mixer is not initialized, this method does nothing.
    """

    def __init__(self, max_value):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(
                    frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512
                )
                pygame.mixer.set_num_channels(32)
            except pygame.error as e:
                print(f"Warning: Failed to initialize Pygame Mixer: {e}")
        self.max_value = max_value
        self._sound_cache = {}

    def _get_sound(self, value):
        value_key = int(value)
        if value_key not in self._sound_cache:
            if self.max_value == 0:
                freq = MIN_FREQ
            else:
                norm_val = max(0, min(1, value / self.max_value))
                log_freq = math.log(MIN_FREQ) + norm_val * (
                    math.log(MAX_FREQ) - math.log(MIN_FREQ)
                )
                freq = math.exp(log_freq)
            duration_samples = int(SAMPLE_RATE * SOUND_DURATION_MS / 1000)
            wave_data = generate_sine_wave(freq, duration_samples, SAMPLE_RATE)
            stereo_wave = np.repeat(wave_data[:, np.newaxis], 2, axis=1)
            sound = pygame.sndarray.make_sound(stereo_wave)
            self._sound_cache[value_key] = sound
        return self._sound_cache[value_key]

    def play_sound(self, value):
        if not pygame.mixer.get_init():
            return
        try:
            sound = self._get_sound(value)
            channel = pygame.mixer.find_channel(True)
            if channel:
                channel.play(sound)
        except pygame.error as e:
            print(f"Pygame mixer error playing sound for value {value}: {e}")
        except Exception as e:
            print(f"Error generating/playing sound for value {value}: {e}")
