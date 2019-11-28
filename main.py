from pyglet.gl import *

from game.core import window, fps_display, gamevars
import game.title
import game.gamemode
import game.pause
import game.endgame
import game.options

from utils.interface import uivars, Textbox, Button
from utils.utils import *
from utils.sounds import *


# [Notes]==========================================================

# todo: FIX LAG PROBLEM
# todo: fix weak references without going fullscreen
# todo: make score saving to file possible, sort scores
# todo: options, instructions, high score, credits
# todo: test pause-restart, pause-resume
# todo: test game over -> try again
# todo: document code, comment in necessary places
# todo: properly undraw textbox rectangle
# todo: save score with name

# =================================================================

def check_for_endgame():
    if gamevars.timer < 0 and gamevars.game_state != uivars.ENDGAME:
        sfx_game_over.play()
        sfx_game_over_m.play()
        bgm_game_mode.stop()
        window.unfocus()
        pyglet.clock.unschedule(timer_countdown)
        gamevars.is_timer = False
        gamevars.timer = gamevars.max_time
        game.endgame.endgame_score_label.text = 'Score: ' + str(gamevars.score)
        update_score_list(gamevars.score)  # stores score to file
        gamevars.display_score = gamevars.score = 0
        gamevars.game_state = uivars.ENDGAME


def timer_countdown(dt):
    gamevars.timer -= 1
    check_for_endgame()


def revert_codeline_color(dt):
    game.gamemode.codeline_label.color(255, 255, 255, 255)


# Checks for changes in the game, basically the game logic
def update(dt):
    # Main Menu Animation
    if gamevars.game_state == uivars.MAIN_MENU:
        # animate title
        game.title.title.coor.y += gamevars.bounce_increment
        gamevars.bounce += gamevars.bounce_increment
        if gamevars.bounce == gamevars.bounce_threshold or gamevars.bounce == 0:
            gamevars.bounce_increment *= -1

    # Schedule timer update if game state is game mode
    if gamevars.game_state == uivars.GAME_MODE:
        game.gamemode.codeline_label.text = gamevars.codeline_str
        game.gamemode.timer_label.text = str(gamevars.timer)
        if not gamevars.is_timer:
            pyglet.clock.schedule_interval(timer_countdown, 1)
            gamevars.is_timer = True
    else:
        if gamevars.is_timer:
            pyglet.clock.unschedule(timer_countdown)
            gamevars.is_timer = False

    # update display score animation
    if gamevars.display_score != gamevars.score:
        gamevars.animate_score_update = True
    if gamevars.animate_score_update:
        if gamevars.display_score < gamevars.score:
            gamevars.display_score += gamevars.display_increment
        else:
            gamevars.display_score = gamevars.score
        game.gamemode.score_label.text = str(gamevars.display_score)

    # Try Again clicked
    if gamevars.is_restart:
        gamevars.is_restart = False
        # reset codeline text
        game.gamemode.codeline_label.text = gamevars.codeline_str
        # reset timer label
        game.gamemode.timer_label.text = str(gamevars.timer)


pyglet.clock.schedule_interval(update, 1 / 30)
bgm_main_menu.play()


# [convenience functions]==============================================================================================


def clear_window():
    window.clear()
    for element in uivars.ui_elements[gamevars.game_state]:
        element.rendered = False


def draw_interface(g_state):
    for background_elem in uivars.ui_backgrounds[g_state]:
        uivars.draw_element(background_elem, window)
    for ui_element in uivars.ui_elements[g_state]:
        uivars.draw_element(ui_element, window)


def change_cursor(cursor_constant):
    window.set_mouse_cursor(window.get_system_mouse_cursor(cursor_constant))


'''
def reset_textbox():
    window.unfocus()
    gamevars.player_codeline = game.gamemode.code_textbox.get_text()
    game.gamemode.code_textbox.set_text('')
    window.set_focus(game.gamemode.code_textbox)
'''


# =====================================================================================================================
# [event handling functions]===========================================================================================


def on_draw():
    clear_window()
    if gamevars.game_state == uivars.GAME_MODE:
        window.batch.draw()
    draw_interface(gamevars.game_state)
    if gamevars.display_fps:
        fps_display.draw()


def on_resize(width, height):
    print('on_resize_called')
    on_draw()


def on_key_press(symbol, modifiers):
    if gamevars.game_state == uivars.GAME_MODE:
        # check code when enter is pressed
        if symbol == pyglet.window.key.ENTER and window.focus:
            player_codeline = game.gamemode.code_textbox.get_text()
            # if code matches kill command
            if player_codeline == gamevars.kill_command and gamevars.admin:
                # end timer
                gamevars.timer = -1
                check_for_endgame()
            # If code is correct, add to score and reset timer
            elif gamevars.codeline_str == player_codeline or (player_codeline == gamevars.konami):
                # play sound
                sfx_correct.play()
                # reset code textbox
                game.gamemode.code_textbox.set_text('')
                # recolor codeline label
                game.gamemode.codeline_label.color(255, 255, 255, 255)
                # add to score
                gamevars.score += len(gamevars.codeline_str) * 7 // 2
                # increment timer
                gamevars.timer = min(gamevars.max_time, gamevars.timer + gamevars.timer_increment)
                # set codeline text
                gamevars.codeline_str = gen_code(gamevars.code_depth)
                game.gamemode.codeline_label.text = gamevars.codeline_str
                # change flags
            else:  # if code is incorrect
                # play sound
                sfx_error.play()
                # recolor code appropriately
                diff_index = get_differing_index(gamevars.codeline_str, player_codeline)
                if diff_index < len(gamevars.codeline_str):
                    game.gamemode.codeline_label.color_from(diff_index, 255, 0, 0, 255)
                else:
                    game.gamemode.codeline_label.color(255, 255, 0, 255)
                # revert codeline color after show error time specified
                pyglet.clock.schedule_once(revert_codeline_color, gamevars.show_error_time)
        # play sfx when typing
        sfx_type.play()


def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.ENTER and window.focus:
        return True


def on_mouse_press(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)
    for interactable in uivars.ui_buttons[gamevars.game_state]:
        if interactable.hit(x, y):
            interactable.active_event()


def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if window.focus:
        window.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


def on_mouse_release(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)
    on_mouse_motion(x, y, 0, 0)
    for interactable in uivars.ui_buttons[gamevars.game_state] + uivars.ui_textboxes[gamevars.game_state]:
        if interactable.hit(x, y):
            interactable.click_event()
    if window.focus:
        window.focus.caret.on_mouse_press(x, y, button, modifiers)


def on_mouse_motion(x, y, dx, dy):
    for interactable in uivars.ui_buttons[gamevars.game_state] + uivars.ui_textboxes[gamevars.game_state]:
        if interactable.hit(x, y):
            if isinstance(interactable, Button):
                window.cursor = window.CURSOR_HAND
                interactable.hover_event()
            elif isinstance(interactable, Textbox):
                window.cursor = window.CURSOR_TEXT
            break
        else:
            if isinstance(interactable, Button):
                interactable.default_event()
            window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)


# =====================================================================================================================

window.on_draw = on_draw
window.on_key_press = on_key_press
window.on_key_release = on_key_release
window.on_mouse_press = on_mouse_press
window.on_mouse_drag = on_mouse_drag
window.on_mouse_release = on_mouse_release
window.on_mouse_motion = on_mouse_motion
pyglet.app.run()
