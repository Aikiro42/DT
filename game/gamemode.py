from game.core import *
from utils.interface import *
from utils.sounds import bgm_game_mode, sfx_pause


def update_timer_label():
    global timer_label
    timer_label = Label(str(gamevars.timer), font_name="Arcade Alternate", x=window.width, y=0)
    timer_label.font_size = 36
    timer_label.set_anchor(uivars.UPPER_RIGHT)
    uivars.add_ui_label(uivars.GAME_MODE, timer_label)


def update_score_label():
    global score_label
    score_label = Label(str(gamevars.score), font_name="Arcade Alternate", x=0, y=0)
    score_label.font_size = 24
    score_label.set_anchor(uivars.UPPER_LEFT)
    uivars.add_ui_label(uivars.GAME_MODE, score_label)


def game_timer_callback(*args, **kwargs):
    if gamevars.is_game and not gamevars.is_pause:
        gamevars.timer -= 1
        print(gamevars.timer)
    elif not gamevars.is_game:
        gamevars.timer = 60


def pause_button_event():
    bgm_game_mode.pause()
    bgm_rawstarr.pause()
    sfx_pause.play()
    window.unfocus()
    window.clear()
    gamevars.is_pause = True
    gamevars.game_state = uivars.PAUSE


def code_textbox_click_event():
    window.set_focus(code_textbox)


gamemode_bg = AnimatedBackground('assets/backgrounds/gamemode_bg.gif', window)
uivars.add_ui_background(uivars.GAME_MODE, gamemode_bg)

codeline_label = Label(gamevars.codeline_str, font_name="Consolas")
codeline_label.set_coor(window.width // 2, (window.height // 2) - codeline_label.content_height - 30)
codeline_label.pyglet_coor(window)
codeline_label.center()
uivars.add_ui_element(uivars.GAME_MODE, codeline_label)

pause_button = Button('assets/gamemode/pause.png',
                      image_hover_dir='assets/gamemode/pause_hover.png',
                      image_active_dir='assets/gamemode/pause_active.png')
pause_button.set_coor(0, 0)
pause_button.set_anchor(uivars.UPPER_LEFT)
pause_button.pyglet_coor(window)
uivars.add_ui_button(uivars.GAME_MODE, pause_button)
pause_button.click_event = pause_button_event

score_label = Label(str(gamevars.score), font_name="Arcade Alternate", font_size=24, x=window.width // 2, y=0)
score_label.set_anchor(uivars.CENTER_TOP)
uivars.add_ui_label(uivars.GAME_MODE, score_label)

timer_label = Label(str(gamevars.timer), font_name="Arcade Alternate", font_size=36, x=window.width, y=0)
timer_label.set_anchor(uivars.UPPER_RIGHT)
uivars.add_ui_label(uivars.GAME_MODE, timer_label)

code_textbox = Textbox(window.batch, width=7 * window.width // 8, font_name='Consolas', font_size=11, pad=10)
code_textbox.set_box_color(25, 25, 25, 200)
code_textbox.set_text_color(0, 255, 0, 255)
code_textbox.set_caret_color(0, 255, 0)
code_textbox.set_coor(window.width // 16, window.height // 2)
code_textbox.pyglet_coor(window)
uivars.add_ui_textbox(uivars.GAME_MODE, code_textbox)
code_textbox.click_event = code_textbox_click_event

for gm_ui_label in uivars.ui_labels[uivars.GAME_MODE]:
    gm_ui_label.pyglet_coor(window)
