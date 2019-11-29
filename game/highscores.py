from game.core import *
from utils.interface import *

def main_menu_button_event():
    gamevars.game_state = uivars.MAIN_MENU


highscores_text = Label('HIGH SCORES', font_name='Arcade Alternate', font_size=72, x=window.width // 2, y=0)
highscores_text.set_anchor(uivars.CENTER_TOP)
highscores_text.set_coor(highscores_text.x, highscores_text.y + highscores_text.content_height)
highscores_text.pyglet_coor(window)
uivars.add_ui_label(uivars.HIGHSCORES, highscores_text)

main_menu_button = Button('assets/highscores/main_menu.png', x=window.width // 2,
                          image_hover_dir='assets/highscores/main_menu_hover.png',
                          image_active_dir='assets/highscores/main_menu_active.png')
main_menu_button.set_anchor(uivars.CENTER)
main_menu_button.set_coor(main_menu_button.coor.x, highscores_text.content_height * 2 +
                          main_menu_button.image.height)
main_menu_button.pyglet_coor(window)
uivars.add_ui_button(uivars.HIGHSCORES, main_menu_button)
main_menu_button.click_event = main_menu_button_event
