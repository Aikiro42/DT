from game.core import *
from utils.interface import *


def back_button_event():
    gamevars.game_state = uivars.MAIN_MENU


instructions_bg = AnimatedBackground('assets/backgrounds/instructions_bg.gif', window)
uivars.add_ui_background(uivars.INSTRUCTIONS, instructions_bg)

instructions_img = Image('assets/instructions/instructions.png', x=window.width // 2, y=window.height // 2)
instructions_img.center()
img_scale = window.height/instructions_img.sprite.image.height
instructions_img.rescale(img_scale)
instructions_img.set_coor(instructions_img.sprite.x, instructions_img.sprite.y + 100*img_scale)
instructions_img.pyglet_coor(window)
uivars.add_ui_element(uivars.INSTRUCTIONS, instructions_img)

back_button = Button('assets/instructions/back.png',
                     image_hover_dir='assets/instructions/back_hover.png',
                     image_active_dir='assets/instructions/back_active.png')
back_button.set_coor(window.width // 2, 0)
back_button.set_anchor(uivars.CENTER_TOP)
back_button.pyglet_coor(window)
uivars.add_ui_button(uivars.INSTRUCTIONS, back_button)
back_button.click_event = back_button_event
