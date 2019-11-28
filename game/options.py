from game.core import *
from utils.interface import *

ui_y_offset = 100

options_text = Image('assets/options/options.png', x=window.width // 2)
options_text.set_coor(options_text.coor.x, options_text.image.height + ui_y_offset)
options_text.center()
options_text.pyglet_coor(window)
uivars.add_ui_element(uivars.OPTIONS, options_text)
