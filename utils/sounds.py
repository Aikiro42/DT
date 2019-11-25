import pyglet

# resource init
pyglet.options['audio'] = ('openal', 'pulse', 'directsound', 'silent')
activate_sfx = pyglet.media.load('assets/activate_sfx.wav', streaming=False)
hover_sfx = pyglet.media.load('assets/hover_sfx.wav', streaming=False)
type_sfx = pyglet.media.load('assets/type_sfx.wav', streaming=False)
execute_sfx = pyglet.media.load('assets/correct_sfx.wav', streaming=False)
error_sfx = pyglet.media.load('assets/error_sfx.wav', streaming=False)
game_over_sfx = pyglet.media.load('assets/game_over_sfx.wav', streaming=False)