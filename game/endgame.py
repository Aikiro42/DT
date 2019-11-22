from game.core import *
from utils.interface import *

ui_y_offset = 100


def main_menu_button_event():
    gamevars.is_game = False
    gamevars.is_pause = False
    gamevars.game_state = MAIN_MENU


def try_again_button_event():
    # restart gamemode variables
    gamevars.timer = gamevars.max_time
    gamevars.score = 0
    gamevars.is_pause = False
    gamevars.game_state = GAME_MODE
    gamevars.is_restart = True


time_up_text = Image('assets/endgame/time_up.png', x=window.width // 2)
time_up_text.set_coor(time_up_text.coor.x, time_up_text.image.height + ui_y_offset)
time_up_text.center()
time_up_text.pyglet_coor(window)
add_ui_element(ENDGAME, time_up_text)

try_again_button = Button('assets/endgame/try_again.png', x=window.width // 2)
add_ui_button(ENDGAME, try_again_button)
try_again_button.click_event = try_again_button_event

main_menu_button = Button('assets/endgame/main_menu.png', x=window.width // 2)
add_ui_button(ENDGAME, main_menu_button)
main_menu_button.click_event = main_menu_button_event

button_order = 1
for endgame_button in ui_buttons[ENDGAME]:
    endgame_button.center()
    endgame_button.set_coor(endgame_button.coor.x, button_order * endgame_button.image.height +
                            time_up_text.image.height +
                            ui_y_offset * 2 +
                            10 * button_order)
    endgame_button.pyglet_coor(window)
    button_order += 1
