from game.core import *
from utils.interface import *
from utils.sounds import *


def main_menu_button_event():
    gamevars.game_state = uivars.MAIN_MENU


def bgm_toggle_event():
    sfx_options_click.play()
    bgm_toggle.change_state()
    bgm_main_menu.set_is_not_mute(bgm_toggle.state)  # stops and plays main menu upon changing is_not_mute
    bgm_game_mode.is_not_mute = bgm_toggle.state


def sfx_toggle_event():
    sfx_options_click.play()
    sfx_toggle.change_state()
    sfx_click.is_not_mute = sfx_toggle.state
    sfx_game_over_m.is_not_mute = sfx_toggle.state
    sfx_game_over.is_not_mute = sfx_toggle.state
    sfx_game_mode_init.is_not_mute = sfx_toggle.state
    sfx_pause.is_not_mute = sfx_toggle.state
    sfx_click.is_not_mute = sfx_toggle.state
    sfx_correct.is_not_mute = sfx_toggle.state
    sfx_error.is_not_mute = sfx_toggle.state
    sfx_hover.is_not_mute = sfx_toggle.state
    sfx_type.is_not_mute = sfx_toggle.state
    sfx_timer.is_not_mute = sfx_toggle.state


ui_y_offset = 100

options_text = Image('assets/options/options.png', x=window.width // 2)
options_text.set_coor(options_text.coor.x, options_text.image.height + ui_y_offset)
options_text.center()
options_text.pyglet_coor(window)
uivars.add_ui_element(uivars.OPTIONS, options_text)

bgm_toggle = ToggledButton(
    'assets/options/music.png',
    'assets/options/no_music.png',
    image_hover_dir_a='assets/options/music_hover.png',
    image_active_dir_a='assets/options/music_active.png',
    image_hover_dir_b='assets/options/no_music_hover.png',
    image_active_dir_b='assets/options/no_music_active.png',
    x=window.width // 3
)
bgm_toggle.center()
bgm_toggle.set_coor(bgm_toggle.button.coor.x, window.height // 2)
bgm_toggle.pyglet_coor(window)
uivars.add_ui_button(uivars.OPTIONS, bgm_toggle)
bgm_toggle.set_click_event(bgm_toggle_event)

sfx_toggle = ToggledButton(
    'assets/options/sounds.png',
    'assets/options/no_sounds.png',
    image_hover_dir_a='assets/options/sounds_hover.png',
    image_active_dir_a='assets/options/sounds_active.png',
    image_hover_dir_b='assets/options/no_sounds_hover.png',
    image_active_dir_b='assets/options/no_sounds_active.png',
    x=window.width * 2 // 3
)
sfx_toggle.center()
sfx_toggle.set_coor(sfx_toggle.button.coor.x, window.height // 2)
sfx_toggle.pyglet_coor(window)
uivars.add_ui_button(uivars.OPTIONS, sfx_toggle)
sfx_toggle.set_click_event(sfx_toggle_event)

main_menu_button = Button('assets/options/main_menu.png', x=window.width // 2,
                          image_hover_dir='assets/options/main_menu_hover.png',
                          image_active_dir='assets/options/main_menu_active.png')
main_menu_button.center()
main_menu_button.set_coor(main_menu_button.coor.x, window.height // 2)
main_menu_button.pyglet_coor(window)
uivars.add_ui_button(uivars.OPTIONS, main_menu_button)
main_menu_button.click_event = main_menu_button_event
