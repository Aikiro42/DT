from game.core import *
from utils.interface import *
from utils.sounds import *

# temporary fix
from game.gamemode import code_textbox

# [main menu elements]=================================================================================================

ui_y_offset = window.height // 100

title = Image('assets/title/title.png', x=window.width // 2)
title.set_coor(title.coor.x, title.image.height + ui_y_offset)
title.center()
title.pyglet_coor(window)
uivars.add_ui_element(uivars.MAIN_MENU, title)


def game_timer_callback(*args, **kwargs):
    if gamevars.is_game and not gamevars.is_pause:
        gamevars.timer -= 1
        print(gamevars.timer)
    elif not gamevars.is_game:
        gamevars.timer = 60


def start_button_event():
    # stop main menu bgm
    bgm_main_menu.stop()
    sfx_game_mode_init.play()
    # play game mode bgm
    bgm_game_mode.play()
    gamevars.game_state = uivars.GAME_MODE
    window.set_focus(code_textbox)


def options_button_event():
    gamevars.game_state = uivars.OPTIONS


def quit_button_event():
    pyglet.app.exit()


title_bg = AnimatedBackground('assets/animated_bg_07.gif', window)
uivars.add_ui_background(uivars.MAIN_MENU, title_bg)

start_button = Button('assets/title/start.png', x=window.width // 2,
                      image_hover_dir='assets/title/start_hover.png',
                      image_active_dir='assets/title/start_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, start_button)
start_button.click_event = start_button_event

options_button = Button('assets/title/options.png', x=window.width // 2,
                        image_hover_dir='assets/title/options_hover.png',
                        image_active_dir='assets/title/options_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, options_button)
options_button.click_event = options_button_event

'''
instructions_button = Button('assets/title/instructions.png', x=window.width // 2,
                             image_hover_dir='assets/title/instructions_hover.png',
                             image_active_dir='assets/title/instructions_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, instructions_button)

credits_button = Button('assets/title/credits.png', x=window.width // 2,
                        image_hover_dir='assets/title/credits_hover.png',
                        image_active_dir='assets/title/credits_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, credits_button)
# '''
quit_button = Button('assets/title/quit.png', x=window.width // 2,
                     image_hover_dir='assets/title/quit_hover.png',
                     image_active_dir='assets/title/quit_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, quit_button)
quit_button.click_event = quit_button_event

ui_button_order = 1  # helps with positioning the main menu buttons
for main_menu_buttons in uivars.ui_buttons[uivars.MAIN_MENU]:
    main_menu_buttons.set_coor(main_menu_buttons.coor.x, title.image.height + 100 +
                               (main_menu_buttons.image.height * ui_button_order) +
                               (25 * ui_button_order) + ui_y_offset)
    main_menu_buttons.center()
    main_menu_buttons.pyglet_coor(window)
    ui_button_order += 1

# =====================================================================================================================
