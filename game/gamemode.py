from game.core import *
from utils.interface import *


def update_timer_label():
    global timer_label
    timer_label = Label(str(gamevars.timer), font_name="Arcade Alternate", x=window.width, y=0)
    timer_label.font_size = 36
    timer_label.set_anchor(UPPER_RIGHT)
    add_ui_label(GAME_MODE, timer_label)


def update_score_label():
    global score_label
    score_label = Label(str(gamevars.score), font_name="Arcade Alternate", x=0, y=0)
    score_label.font_size = 24
    score_label.set_anchor(UPPER_LEFT)
    add_ui_label(GAME_MODE, score_label)


def game_timer_callback(*args, **kwargs):
    if gamevars.is_game and not gamevars.is_pause:
        gamevars.timer -= 1
        print(gamevars.timer)
    elif not gamevars.is_game:
        gamevars.timer = 60


def pause_button_event():
    gamevars.is_pause = True
    gamevars.game_state = PAUSE


codeline_label = Label(gamevars.codeline_str, font_name="Consolas")
codeline_label.set_coor(window.width // 2, (window.height // 2) - codeline_label.content_height - 100)
codeline_label.pyglet_coor(window)
codeline_label.center()
add_ui_element(GAME_MODE, codeline_label)

pause_button = Button('assets/gamemode/pause.png')
pause_button.set_coor(0, window.height)
pause_button.set_anchor(LOWER_LEFT)
pause_button.pyglet_coor(window)
add_ui_button(GAME_MODE, pause_button)
pause_button.click_event = pause_button_event

score_label = Label(str(gamevars.score), font_name="Arcade Alternate", x=0, y=0)
score_label.font_size = 24
score_label.set_anchor(UPPER_LEFT)
add_ui_label(GAME_MODE, score_label)

timer_label = Label(str(gamevars.timer), font_name="Arcade Alternate", x=window.width, y=0)
timer_label.font_size = 36
timer_label.set_anchor(UPPER_RIGHT)
add_ui_label(GAME_MODE, timer_label)

code_textbox = Textbox(window.batch, width=7*window.width//8, font_name='Consolas')
code_textbox.set_coor(window.width//16, window.height//2)
code_textbox.pyglet_coor(window)
add_ui_textbox(GAME_MODE, code_textbox)

for gm_ui_label in ui_labels[GAME_MODE]:
    gm_ui_label.pyglet_coor(window)
