from typing import Callable

import arcade
from pyglet.media import Player


class BackgroundMusic:
    """ Background music. It can be turned on and off."""

    def __init__(self,
                 get_music_on: Callable[[], bool] = lambda: False,
                 get_music_speed: Callable[[], float] = lambda: 1.0,
                 get_music_volume: Callable[[], float] = lambda: 0.2,
                 ):
        self.get_music_on = get_music_on
        self.get_music_speed = get_music_speed
        self.get_music_volume = get_music_volume
        self.player: Player = None
        self._is_music_on = True
        self.audio = arcade.load_sound('pytetris/sound/theme.wav', False)

    def on_update(self, delta_time: float):
        if self.get_music_on() and self._is_music_on:
            if not self.player:
                self.player = arcade.play_sound(self.audio,
                                                self.get_music_volume(),
                                                -1,
                                                True,
                                                self.get_music_speed())
            self.player.pitch = self.get_music_speed()
        else:
            if self.player:
                arcade.stop_sound(self.player)
                self.player = None

    def toggle(self):
        self._is_music_on = not self._is_music_on
