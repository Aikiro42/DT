from game.core import *
from utils.interface import *


def back_button_event():
    gamevars.game_state = uivars.MAIN_MENU


credits_bg = AnimatedBackground('assets/backgrounds/credits_bg.gif', window)
uivars.add_ui_background(uivars.CREDITS, credits_bg)

credits_legacy = Background('assets/backgrounds/credits_bg.png', window)


credits_img = Image('assets/credits/credits.png', x=window.width // 2, y=window.height // 2)
credits_img.rescale(window.height/credits_img.sprite.image.height)
credits_img.center()
credits_img.pyglet_coor(window)
uivars.add_ui_element(uivars.CREDITS, credits_img)

back_button = Button('assets/credits/back.png',
                     image_hover_dir='assets/credits/back_hover.png',
                     image_active_dir='assets/credits/back_active.png')
back_button.set_coor(window.width // 2, 0)
back_button.set_anchor(uivars.CENTER_TOP)
back_button.pyglet_coor(window)
uivars.add_ui_button(uivars.CREDITS, back_button)
back_button.click_event = back_button_event
