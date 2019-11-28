import pyglet


# from utils.interface import InterfaceVars

class Sound:
    def __init__(self, sound_dir, streaming=False):
        self.sound_obj = pyglet.media.load(sound_dir, streaming=streaming)

    def play(self):
        self.sound_obj.play()


class Music(pyglet.media.Player):
    def __init__(self, sound_dir, streaming=True, loop=False):
        super(Music, self).__init__()
        self.loop = loop
        self.queue(pyglet.media.load(sound_dir, streaming=streaming))
        self.pause()

    def stop(self):
        self.pause()
        self.seek(0)

    def is_loop(self, loop_bool):
        self.loop = loop_bool


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

bgm_main_menu = Music('assets/bgm/bgm_main_menu.wav', loop=True)
bgm_game_mode = Music('assets/bgm/bgm_game_mode.wav', loop=True)
