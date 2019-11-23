from pyglet.gl import *

from game.core import window, fps_display, gamevars
import game.title
import game.gamemode
import game.pause
import game.endgame

from utils.interface import *
from utils.utils import *


# [Notes]==========================================================

# todo: fix text selection
# todo: make score saving to file possible, sort scores
# todo: save score with name
# todo: make code generator (just in case Rain won't be able to do it)
# todo: options, music, instructions, high score, credits
# todo: button hover and active states
# todo: test pause-restart, pause-resume
# todo: test game over -> try again
# todo: document code, comment in necessary places
# todo: fix text selection

# =================================================================

def timer_countdown(dt):
    gamevars.timer -= 1


def revert_codeline_color(dt):
    game.gamemode.codeline_label.color(255, 255, 255, 255)


# Checks for changes in the game, basically the game logic
def update(dt):
    if gamevars.game_state == MAIN_MENU:
        game.title.title.coor.y += gamevars.bounce_increment
        gamevars.bounce += gamevars.bounce_increment
        if gamevars.bounce == gamevars.bounce_threshold or gamevars.bounce == 0:
            gamevars.bounce_increment *= -1

    # Timer update
    if gamevars.game_state == GAME_MODE:
        game.gamemode.timer_label.text = str(gamevars.timer)
        if not gamevars.is_timer:
            pyglet.clock.schedule_interval(timer_countdown, 1)
            gamevars.is_timer = True
    else:
        if gamevars.is_timer:
            pyglet.clock.unschedule(timer_countdown)
            gamevars.is_timer = False

    # Game Over
    if gamevars.timer < 0 and gamevars.game_state != ENDGAME:
        window.unfocus()
        pyglet.clock.unschedule(timer_countdown)
        gamevars.is_timer = False
        gamevars.timer = gamevars.max_time
        gamevars.game_state = ENDGAME

    # updates display score
    if gamevars.display_score < gamevars.score:
        gamevars.display_score += gamevars.display_increment
        game.gamemode.score_label.text = str(gamevars.display_score)
    elif gamevars.display_score != gamevars.score:
        gamevars.display_score = gamevars.score
        game.gamemode.score_label.text = str(gamevars.display_score)

    if gamevars.is_restart:
        gamevars.is_restart = False
        game.gamemode.timer_label.text = str(gamevars.timer)

    # Checks code
    if gamevars.is_check_code:
        # If code is correct, add to score and reset timer
        if gamevars.codeline_str == gamevars.player_codeline:
            game.gamemode.code_textbox.set_text('')
            game.gamemode.codeline_label.color(255, 255, 255, 255)
            gamevars.score += len(gamevars.codeline_str) * 7 // 2
            gamevars.timer = gamevars.max_time
            # generate new line
            gamevars.is_check_code = False
            gamevars.is_code_correct = True
        else:  # if code is incorrect
            diff_index = get_differing_index(gamevars.codeline_str, gamevars.player_codeline)
            game.gamemode.codeline_label.color_from(diff_index, 255, 0, 0, 255)
            pyglet.clock.schedule_once(revert_codeline_color, gamevars.show_error_time)
            gamevars.is_check_code = False


pyglet.clock.schedule_interval(update, 1 / 15)


# [convenience functions]==============================================================================================


def clear_window():
    window.clear()
    for element in ui_elements[gamevars.game_state]:
        element.rendered = False


def draw_interface(g_state):
    for ui_element in ui_elements[g_state]:
        draw_element(ui_element, window)


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
    if gamevars.game_state == GAME_MODE:
        window.batch.draw()
    draw_interface(gamevars.game_state)
    fps_display.draw()


def on_key_press(symbol, modifiers):
    if gamevars.game_state == GAME_MODE:
        if symbol == pyglet.window.key.ENTER and window.focus:
            gamevars.player_codeline = game.gamemode.code_textbox.get_text()
            gamevars.is_check_code = True


def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.ENTER and window.focus:
        return True


def on_mouse_press(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)
    for interactable in ui_buttons[gamevars.game_state] + ui_textboxes[gamevars.game_state]:
        if interactable.hit(x, y):
            if window.focus is not interactable:
                interactable.click_event()


def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if window.focus:
        window.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


def on_mouse_release(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)
    on_mouse_motion(x, y, 0, 0)


def on_mouse_motion(x, y, dx, dy):
    for interactable in ui_buttons[gamevars.game_state] + ui_textboxes[gamevars.game_state]:
        if interactable.hit(x, y):
            if isinstance(interactable, Button):
                window.cursor = window.CURSOR_HAND
            elif isinstance(interactable, Textbox):
                window.cursor = window.CURSOR_TEXT
            break
        else:
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
