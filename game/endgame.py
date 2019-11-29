from game.core import *
from utils.interface import *
from utils.sounds import sfx_game_mode_init, bgm_main_menu, bgm_game_mode

ui_y_offset = 100


def main_menu_button_event():
    bgm_main_menu.play()
    gamevars.is_game = False
    gamevars.is_pause = False
    gamevars.game_state = uivars.MAIN_MENU


def try_again_button_event():
    # restart gamemode variables
    uivars.reset_ui_textboxes(uivars.GAME_MODE)
    gamevars.timer = gamevars.max_time
    gamevars.score = 0
    gamevars.is_pause = False
    gamevars.is_restart = True
    window.set_focus(uivars.ui_textboxes[uivars.GAME_MODE][0])
    sfx_game_mode_init.play()
    bgm_game_mode.play()
    gamevars.game_state = uivars.GAME_MODE


endgame_bg = AnimatedBackground('assets/endgame_bg.gif', window)
uivars.add_ui_background(uivars.ENDGAME, endgame_bg)

time_up_text = Image('assets/endgame/time_up.png', x=window.width // 2)
time_up_text.set_coor(time_up_text.coor.x, time_up_text.image.height + ui_y_offset)
time_up_text.center()
time_up_text.pyglet_coor(window)
uivars.add_ui_element(uivars.ENDGAME, time_up_text)

endgame_score_label = Label('Score: 0', font_size=24, font_name='Arcade Alternate', x=window.width // 2)
endgame_score_label.set_coor(endgame_score_label.x, time_up_text.image.height*2 + ui_y_offset + 25)
endgame_score_label.center()
endgame_score_label.pyglet_coor(window)
uivars.add_ui_element(uivars.ENDGAME, endgame_score_label)

try_again_button = Button('assets/endgame/try_again.png', x=window.width // 2,
                          image_hover_dir='assets/endgame/try_again_hover.png',
                          image_active_dir='assets/endgame/try_again_active.png')
uivars.add_ui_button(uivars.ENDGAME, try_again_button)
try_again_button.click_event = try_again_button_event

main_menu_button = Button('assets/endgame/main_menu.png', x=window.width // 2,
                          image_hover_dir='assets/endgame/main_menu_hover.png',
                          image_active_dir='assets/endgame/main_menu_active.png')
uivars.add_ui_button(uivars.ENDGAME, main_menu_button)
main_menu_button.click_event = main_menu_button_event

button_order = 1
for endgame_button in uivars.ui_buttons[uivars.ENDGAME]:
    endgame_button.center()
    endgame_button.set_coor(endgame_button.coor.x, button_order * endgame_button.image.height +
                            time_up_text.image.height +
                            ui_y_offset * 2 +
                            25 * button_order)
    endgame_button.pyglet_coor(window)
    button_order += 1
