import pyglet


# from utils.interface import InterfaceVars

class Sound:
    def __init__(self, sound_dir, streaming=False):
        self.sound_obj = pyglet.media.load(sound_dir, streaming=streaming)
        self.is_not_mute = True

    def play(self):
        if self.is_not_mute:
            self.sound_obj.play()


class Music(pyglet.media.Player):
    def __init__(self, sound_dir, streaming=True, loop=False):
        super(Music, self).__init__()
        self.loop = loop
        self.queue(pyglet.media.load(sound_dir, streaming=streaming))
        self.pause()
        self.is_not_mute = True
        self.is_playing = False

    def play(self):
        if self.is_not_mute:
            super(Music, self).play()
            self.is_playing = True

    def pause(self):
        super(Music, self).pause()
        self.is_playing = False

    def stop(self):
        self.pause()
        self.seek(0)
        self.is_playing = False

    def is_loop(self, loop_bool):
        self.loop = loop_bool

    def set_is_not_mute(self, is_not_mute):
        self.is_not_mute = is_not_mute
        if not is_not_mute and self.is_playing:
            self.stop()
        elif is_not_mute and not self.is_playing:
            self.play()


# resource init
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
sfx_click = Sound('assets/sfx/sfx_click.wav')
sfx_hover = Sound('assets/sfx/sfx_hover.wav')
sfx_type = Sound('assets/sfx/sfx_type.wav')
sfx_correct = Sound('assets/sfx/sfx_correct.wav')
sfx_error = Sound('assets/sfx/sfx_error.wav')
sfx_game_mode_init = Sound('assets/sfx/sfx_game_mode_init.wav')
sfx_game_over_m = Sound('assets/sfx/sfx_game_over_musical.wav')
sfx_game_over = Sound('assets/sfx/sfx_game_over.wav')
sfx_pause = Sound('assets/sfx/sfx_pause.wav')
sfx_timer = Sound('assets/sfx/sfx_timer.wav')
sfx_options_click = Sound('assets/sfx/sfx_options_click.wav')

bgm_main_menu = Music('assets/bgm/bgm_main_menu.wav', loop=True)
bgm_game_mode = Music('assets/bgm/bgm_game_mode.wav', loop=True)
bgm_rawstarr = Music('assets/bgm/bgm_rawstarr.wav', loop=True)
