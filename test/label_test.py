import pyglet
from utils.interface import *

window = Window(800, 600)

label = Label('999999', x=0, y=0)
label.pyglet_coor(window)
label.set_anchor(UPPER_LEFT)

label2 = Label("99'99", x=window.width, y=0)
label2.pyglet_coor(window)
label2.set_anchor(UPPER_RIGHT)

@window.event
def on_draw():
    label.draw()
    label2.draw()


pyglet.app.run()
