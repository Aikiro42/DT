import pyglet
from pyglet.gl import *
from utils.interface import *

window = Window()
pyglet.gl.glClearColor(1, 1, 1, 1)

textbox = Textbox(window.batch)
window.set_focus(textbox)


def on_draw():
    window.clear()
    textbox.draw()

def on_mouse_press():
    global textbox
    window.focus = None
    textbox = Label('hi')


window.on_draw = on_draw

pyglet.app.run()
