from game.core import *
from utils.interface import *
from utils.utils import get_score_list

ui_y_offset = window.height // 100
ui_button_offset = window.height // 12


def main_menu_button_event():
    gamevars.game_state = uivars.MAIN_MENU


def update_highscores():
    score_list = get_score_list()
    while len(score_list) < 5:
        score_list.append('0')
    i = 0
    len_max = len('---{}'.format(score_list[0]))
    for lbl in uivars.ui_labels[uivars.HIGHSCORES]:
        new_str = '{}. {}'.format(i, score_list[i])
        lbl.text = '{}. {}{}'.format(i + 1, '0' * (len_max - len(new_str)), score_list[i])
        i += 1



highscores_bg = AnimatedBackground('assets/highscores_bg.gif', window)
uivars.add_ui_background(uivars.HIGHSCORES, highscores_bg)

highscores_text = Label('HIGH SCORES', font_name='Arcade Alternate',
                        font_size=72, x=window.width // 2, y=0)
highscores_text.set_anchor(uivars.CENTER_TOP)
highscores_text.set_coor(highscores_text.x, highscores_text.y + highscores_text.content_height)
highscores_text.pyglet_coor(window)
uivars.add_ui_element(uivars.HIGHSCORES, highscores_text)

main_menu_button = Button('assets/highscores/main_menu.png', x=window.width // 2,
                          image_hover_dir='assets/highscores/main_menu_hover.png',
                          image_active_dir='assets/highscores/main_menu_active.png')
main_menu_button.set_anchor(uivars.CENTER)
main_menu_button.set_coor(main_menu_button.sprite.x, highscores_text.content_height * 2 +
                          main_menu_button.sprite.height)
main_menu_button.pyglet_coor(window)
uivars.add_ui_button(uivars.HIGHSCORES, main_menu_button)
main_menu_button.click_event = main_menu_button_event

score_separation = 10


score_1 = Label('1. 00000000', font_name='Arcade Alternate', font_size=24, x=window.width // 2, y=0)
uivars.add_ui_label(uivars.HIGHSCORES, score_1)

score_2 = Label('2. 00000000', font_name='Arcade Alternate', font_size=24, x=window.width // 2, y=0)
uivars.add_ui_label(uivars.HIGHSCORES, score_2)

score_3 = Label('3. 00000000', font_name='Arcade Alternate', font_size=24, x=window.width // 2, y=0)
uivars.add_ui_label(uivars.HIGHSCORES, score_3)

score_4 = Label('4. 00000000', font_name='Arcade Alternate', font_size=24, x=window.width // 2, y=0)
uivars.add_ui_label(uivars.HIGHSCORES, score_4)

score_5 = Label('5. 00000000', font_name='Arcade Alternate', font_size=24, x=window.width // 2, y=0)
uivars.add_ui_label(uivars.HIGHSCORES, score_5)

l_order = 1
b_rescale = (window.width / uivars.rescaling_factor)
b_rescale += (1 - b_rescale) / 1.5
for l in uivars.ui_labels[uivars.HIGHSCORES]:
    l.rescale(b_rescale)
    l.set_anchor(uivars.CENTER)
    # l.set_coor(l.x, highscores_text.content_height * 2 +
    #           main_menu_button.sprite.height * 2 +
    #           l.content_height * 2 * l_order)
    l.set_coor(l.x, main_menu_button.sprite.height +
               ui_y_offset * 16 +
               highscores_text.content_height +
               l_order * ui_button_offset)
    l.pyglet_coor(window)
    l_order += 1

update_highscores()