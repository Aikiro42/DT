from game.core import *
from utils.interface import *

# temporary fix
from game.gamemode import code_textbox

# [main menu elements]=================================================================================================

ui_y_offset = -50

title = Image('assets/title/title.png', x=window.width // 2)
title.set_coor(title.coor.x, title.image.height + ui_y_offset)
title.center()
title.pyglet_coor(window)
add_ui_element(MAIN_MENU, title)


def game_timer_callback(*args, **kwargs):
    if gamevars.is_game and not gamevars.is_pause:
        gamevars.timer -= 1
        print(gamevars.timer)
    elif not gamevars.is_game:
        gamevars.timer = 60


def start_button_event():
    gamevars.game_state = GAME_MODE
    window.set_focus(code_textbox)


def quit_button_event():
    pyglet.app.exit()


start_button = Button('assets/title/start.png', x=window.width // 2)
add_ui_button(MAIN_MENU, start_button)
start_button.click_event = start_button_event
'''
options_button = Button('assets/title/options.png', x=window.width // 2)
add_ui_button(MAIN_MENU, options_button)

instructions_button = Button('assets/title/instructions.png', x=window.width // 2)
add_ui_button(MAIN_MENU, instructions_button)

credits_button = Button('assets/title/credits.png', x=window.width // 2)
add_ui_button(MAIN_MENU, credits_button)
'''
quit_button = Button('assets/title/quit.png', x=window.width // 2)
add_ui_button(MAIN_MENU, quit_button)
quit_button.click_event = quit_button_event

ui_button_order = 1  # helps with positioning the main menu buttons
for main_menu_buttons in ui_buttons[MAIN_MENU]:
    main_menu_buttons.set_coor(main_menu_buttons.coor.x, title.image.height + 100 +
                               (main_menu_buttons.image.height * ui_button_order) +
                               (5 * ui_button_order) + ui_y_offset)
    main_menu_buttons.center()
    main_menu_buttons.pyglet_coor(window)
    ui_button_order += 1

# =====================================================================================================================
