from game.core import *
from utils.interface import *
from utils.sounds import *

# temporary fix
from game.gamemode import code_textbox

# [main menu elements]=================================================================================================

ui_y_offset = window.height // 100
ui_button_offset = window.height // 12


def start_button_event():
    # stop main menu bgm
    gamevars.codeline_str = "print('Hello World!')"
    gamevars.player_codeline = ''
    if not gamevars.is_daemon:
        gamevars.timer = gamevars.max_time
    # stop main menu bgm
    bgm_main_menu.stop()
    # play sfx_game_mode_bgm
    sfx_game_mode_init.play()
    # play game mode bgm
    bgm_game_mode.play()
    gamevars.game_state = uivars.GAME_MODE
    window.set_focus(code_textbox)


def options_button_event():
    gamevars.game_state = uivars.OPTIONS


def highscores_button_event():
    gamevars.game_state = uivars.HIGHSCORES


def quit_button_event():
    pyglet.app.exit()


# Background
title_bg = AnimatedBackground('assets/backgrounds/title_bg.gif', window)
uivars.add_ui_background(uivars.MAIN_MENU, title_bg)

# Title text
title = Image('assets/title/title.png', x=window.width // 2)
title.rescale(window.width / uivars.rescaling_factor)
title.set_coor(title.sprite.x, title.sprite.height + ui_y_offset)
title.center()
title.pyglet_coor(window)
uivars.add_ui_element(uivars.MAIN_MENU, title)

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

highscores_button = Button('assets/title/highscores.png', x=window.width // 2,
                           image_hover_dir='assets/title/highscores_hover.png',
                           image_active_dir='assets/title/highscores_active.png')
uivars.add_ui_button(uivars.MAIN_MENU, highscores_button)
highscores_button.click_event = highscores_button_event

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
b_rescale = (window.width/uivars.rescaling_factor)
b_rescale += (1 - b_rescale)/1.5
for mmb in uivars.ui_buttons[uivars.MAIN_MENU]:
    mmb.rescale(b_rescale)
    # mmb.set_coor(window.width // 2, title.sprite.height + 100 +
    #              (mmb.sprite.height * ui_button_order) +
    #              (25 * ui_button_order) + ui_y_offset)
    mmb.set_coor(mmb.sprite.x, ui_y_offset * 10 + title.sprite.height + ui_button_order * ui_button_offset)
    mmb.center()
    mmb.pyglet_coor(window)
    ui_button_order += 1

# =====================================================================================================================
