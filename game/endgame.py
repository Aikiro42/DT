from game.core import *
from utils.interface import *

from game.core import *
from utils.interface import *

ui_y_offset = 100


def quit_button_event():
    gamevars.is_game = False
    gamevars.is_pause = False
    gamevars.game_state = MAIN_MENU


def restart_button_event():
    # restart gamemode variables
    gamevars.timer = gamevars.max_time
    gamevars.score = 0
    gamevars.is_pause = False
    gamevars.game_state = GAME_MODE
    gamevars.is_restart = True


def resume_button_event():
    gamevars.is_pause = False
    gamevars.game_state = GAME_MODE


pause_text = Image('assets/pause/pause.png', x=window.width // 2)
pause_text.set_coor(pause_text.coor.x, pause_text.image.height + ui_y_offset)
pause_text.center()
pause_text.pyglet_coor(window)
add_ui_element(PAUSE, pause_text)

resume_button = Button('assets/pause/resume.png', x=window.width // 2)
add_ui_button(PAUSE, resume_button)
resume_button.click_event = resume_button_event

restart_button = Button('assets/pause/restart.png', x=window.width // 2)
add_ui_button(PAUSE, restart_button)
restart_button.click_event = restart_button_event

quit_button = Button('assets/pause/quit.png', x=window.width // 2)
add_ui_button(PAUSE, quit_button)
quit_button.click_event = quit_button_event

button_order = 1
for pause_button in ui_buttons[PAUSE]:
    pause_button.center()
    pause_button.set_coor(pause_button.coor.x, button_order * pause_button.image.height +
                          pause_text.image.height +
                          ui_y_offset * 2 +
                          10 * button_order)
    pause_button.pyglet_coor(window)
    button_order += 1
