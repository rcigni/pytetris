from typing import Callable

import arcade


class BackgroundMusic:
    """ Background music. It can be turned on and off."""

    def __init__(self, get_music_on: Callable[[], bool]):
        self.get_music_on = get_music_on
        self.player = None
        self.is_background_music_on = True
        self.audio = arcade.load_sound('pytetris/sound/theme.wav', False)

    def on_update(self):
        if self.get_music_on() and self.is_background_music_on:
            if not self.player:
                self.player = arcade.play_sound(self.audio, 0.3, -1, True)
        else:
            if self.player:
                arcade.stop_sound(self.player)
                self.player = None

    def toggle(self):
        self.is_background_music_on = not self.is_background_music_on
