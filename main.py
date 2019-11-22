import pyglet
from pyglet.gl import *

from game.core import window, gamevars
import game.title
import game.gamemode
import game.pause

from utils.interface import *
from utils.utils import *


def timer_countdown(dt):
    gamevars.timer -= 1
    game.gamemode.timer_label.text = str(gamevars.timer)


# Checks for changes in the game
def update(dt):
    if gamevars.game_state == GAME_MODE:
        if not gamevars.is_timer:
            pyglet.clock.schedule_interval(timer_countdown, 1)
            gamevars.is_timer = True
    else:
        if gamevars.is_timer:
            pyglet.clock.unschedule(timer_countdown)
            gamevars.is_timer = False
    if gamevars.timer < 0 and gamevars.game_state != ENDGAME:
        gamevars.game_state = ENDGAME
        pyglet.clock.unschedule(timer_countdown)
        gamevars.is_timer = False
        gamevars.timer = 59
    if gamevars.display_score != gamevars.score:
        gamevars.display_score += 1
        game.gamemode.score_label.text = str(gamevars.display_score)
    if gamevars.is_restart:
        gamevars.is_restart = False
        game.gamemode.timer_label.text = str(gamevars.timer)


pyglet.clock.schedule_interval(update, 1 / 60)


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


# =====================================================================================================================
# [event handling functions]===========================================================================================


def on_draw():
    clear_window()
    window.batch.draw()
    draw_interface(gamevars.game_state)


def on_key_press(symbol, modifiers):
    print("keys: {} + {}".format(symbol, modifiers))


def on_mouse_press(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)
    for button in ui_buttons[gamevars.game_state]:
        if button.hit(x, y):
            button.click_event()


def on_mouse_release(x, y, button, modifiers):
    window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)


def on_mouse_motion(x, y, dx, dy):
    for button in ui_buttons[gamevars.game_state]:
        if button.hit(x, y):
            window.cursor = window.CURSOR_HAND
            break
        else:
            window.cursor = window.CURSOR_DEFAULT
    change_cursor(window.cursor)


# =====================================================================================================================

window.on_draw = on_draw
window.on_key_press = on_key_press
window.on_mouse_press = on_mouse_press
window.on_mouse_motion = on_mouse_motion
pyglet.app.run()
