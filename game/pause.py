from game.core import *
from utils.interface import *
from utils.sounds import bgm_game_mode, sfx_game_mode_init, sfx_game_over_m

ui_y_offset = 100


def quit_button_event():
    bgm_game_mode.stop()
    bgm_main_menu.play()
    gamevars.is_game = False
    gamevars.is_pause = False
    sfx_game_over_m.play()
    gamevars.game_state = uivars.MAIN_MENU


def restart_button_event():
    # reset gamemode music
    bgm_game_mode.stop()
    bgm_game_mode.play()
    # reset gamemode textboxes
    uivars.reset_ui_textboxes(uivars.GAME_MODE)
    # reset variables
    gamevars.timer = gamevars.max_time
    gamevars.score = 0
    gamevars.codeline_str = gen_code(gamevars.code_depth)
    gamevars.is_pause = False
    gamevars.is_restart = True
    window.set_focus(uivars.ui_textboxes[uivars.GAME_MODE][0])
    sfx_game_mode_init.play()
    gamevars.game_state = uivars.GAME_MODE


def resume_button_event():
    bgm_game_mode.play()
    gamevars.is_pause = False
    window.set_focus(uivars.ui_textboxes[uivars.GAME_MODE][0])
    gamevars.game_state = uivars.GAME_MODE


pause_text = Image('assets/pause/pause.png', x=window.width // 2)
pause_text.set_coor(pause_text.coor.x, pause_text.image.height + ui_y_offset)
pause_text.center()
pause_text.pyglet_coor(window)
uivars.add_ui_element(uivars.PAUSE, pause_text)

resume_button = Button('assets/pause/resume.png', x=window.width // 2,
                       image_hover_dir='assets/pause/resume_hover.png',
                       image_active_dir='assets/pause/resume_active.png')
uivars.add_ui_button(uivars.PAUSE, resume_button)
resume_button.click_event = resume_button_event

restart_button = Button('assets/pause/restart.png', x=window.width // 2,
                        image_hover_dir='assets/pause/restart_hover.png',
                        image_active_dir='assets/pause/restart_active.png')
uivars.add_ui_button(uivars.PAUSE, restart_button)
restart_button.click_event = restart_button_event

quit_button = Button('assets/pause/quit.png', x=window.width // 2,
                     image_hover_dir='assets/pause/quit_hover.png',
                     image_active_dir='assets/pause/quit_active.png')
uivars.add_ui_button(uivars.PAUSE, quit_button)
quit_button.click_event = quit_button_event

button_order = 1
for pause_button in uivars.ui_buttons[uivars.PAUSE]:
    pause_button.center()
    pause_button.set_coor(pause_button.coor.x, button_order * pause_button.image.height +
                          pause_text.image.height +
                          ui_y_offset * 2 +
                          25 * button_order)
    pause_button.pyglet_coor(window)
    button_order += 1
