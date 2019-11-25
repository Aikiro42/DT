from typing import overload

import pyglet
import copy

# CONSTANTS
# game states
MAIN_MENU = 'main-menu'
GAME_MODE = 'game-mode'
ENDGAME = 'endgame'  # game over
OPTIONS = 'options'
INSTRUCTIONS = 'instructions'
CREDITS = 'credits'
PAUSE = 'pause'

# label anchors
UPPER_RIGHT = ('right', 'top')
LOWER_RIGHT = ('right', 'bottom')
UPPER_LEFT = ('left', 'top')
LOWER_LEFT = ('left', 'bottom')
CENTER_TOP = ('center', 'top')
CENTER_BOTTOM = ('center', 'bottom')
CENTER_LEFT = ('left', 'center')
CENTER_RIGHT = ('right', 'center')

# colors
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
WHITE = (255, 255, 255, 255)


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coor(self):
        return self.x, self.y

    def set_coor(self):
        return self.x, self.y

    def pyglet_coor(self, window_obj):
        self.y = window_obj.height - self.y


# Don't alter me
class Rectangle(object):
    """Draws a rectangle into a batch."""

    def __init__(self, x1, y1, x2, y2, batch, color=(200, 200, 220, 255)):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
                                     ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                     ('c4B', color * 4)
                                     )


class Textbox(object):
    def __init__(self, batch, text='', x=0, y=0, width=200,
                 text_color=(0, 0, 0, 255), font_name='Arial', pad=2, font_size=12):

        self.rendered = False
        self.batch = batch

        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=text_color, font_name=font_name, font_size=font_size)
                                )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        self.rectangle = None
        self.pad = pad
        self.has_outline = False
        self.box_color = [200, 200, 220, 255]

    def hit(self, cursor_x, cursor_y):
        ox = self.layout.x
        oy = self.layout.y
        if self.rendered and ox < cursor_x < ox + self.layout.width and oy < cursor_y < oy + self.layout.height:
            return True
        else:
            return False

    def get_text(self):
        return self.document.text

    def set_text(self, new_text):
        self.document.text = new_text

    def strip_text(self):
        self.document.text = self.document.text.strip()

    def set_text_color(self, r, g, b, a=255):
        self.document.set_style(0, len(self.document.text),
                                dict(color=(r, g, b, a))
                                )

    def set_box_color(self, r, g, b, a=255):
        self.box_color = [r, g, b, a]

    def set_caret_color(self, r, g, b):
        self.caret.color = [r, g, b]

    def draw_rectangle(self):
        self.rectangle = Rectangle(self.layout.x - self.pad,
                                   self.layout.y - self.pad,
                                   self.layout.x + self.layout.width + self.pad,
                                   self.layout.y + self.layout.height + self.pad,
                                   self.batch, color=self.box_color)
        self.has_outline = True

    def set_coor(self, x, y):
        self.layout.x = x
        self.layout.y = y
        self.has_outline = False

    def pyglet_coor(self, window_obj):
        self.layout.y = window_obj.height - self.layout.y
        self.has_outline = False

    def draw(self):
        if not self.has_outline:
            self.draw_rectangle()
        self.batch.draw()
        self.rendered = True

    def click_event(self):
        pass


class Image:
    def __init__(self, image_dir, x=0, y=0):
        self.image = pyglet.resource.image(image_dir)
        self.coor = Coordinates(x, y)
        self.rendered = False

    def set_coor(self, x, y):
        self.coor.x = x
        self.coor.y = y

    def pyglet_coor(self, window_obj):
        self.coor.pyglet_coor(window_obj)

    def center(self):
        """Sets an image's anchor point to its center"""
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

    def set_anchor(self, anchor_tuple: tuple):
        anchors = get_image_anchor(self, anchor_tuple)
        self.image.anchor_x = anchors[0]
        self.image.anchor_y = anchors[1]

    def draw(self):
        self.image.blit(self.coor.x, self.coor.y)
        self.rendered = True


class Button(Image):
    def __init__(self, image_dir, x=0, y=0):
        super(Button, self).__init__(image_dir, x=x, y=y)
        self.event_function = lambda _: _

    def hit(self, cursor_x, cursor_y):
        ox = self.coor.x - self.image.anchor_x
        oy = self.coor.y - self.image.anchor_y
        if self.rendered and ox < cursor_x < ox + self.image.width and oy < cursor_y < oy + self.image.height:
            return True
        else:
            return False

    def click_event(self):
        pass


class StyLabel:

    def __init__(self, text='',
                 font_name=None, font_size=None, bold=False, italic=False,
                 color=(255, 255, 255, 255),
                 x=0, y=0, width=None, height=None,
                 anchor_x='left', anchor_y='baseline',
                 align='left',
                 multiline=False, dpi=None, batch=None, group=None):
        self.document = pyglet.text.document.UnformattedDocument(text)
        super(StyLabel, self).__init__(self.document, x, y, width, height,
                                       anchor_x, anchor_y,
                                       multiline, dpi, batch, group)

        self.document.set_style(0, len(self.document.text), {
            'font_name': font_name,
            'font_size': font_size,
            'bold': bold,
            'italic': italic,
            'color': color,
            'align': align,
        })


class Label:

    def __init__(self, text='',
                 font_name=None, font_size=None, bold=False, italic=False,
                 color=(255, 255, 255, 255),
                 x=0, y=0, width=None, height=None,
                 anchor_x='left', anchor_y='baseline',
                 align='left'):
        self.document = pyglet.text.document.FormattedDocument(text)

        self.document.set_style(0, len(self.document.text), {
            'font_name': font_name,
            'font_size': font_size,
            'bold': bold,
            'italic': italic,
            'color': color,
            'align': align,
        })

        self.text = text
        self.x = x
        self.y = y
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.layout = pyglet.text.layout.TextLayout(self.document)
        self.content_height = self.layout.content_height

    def set_coor(self, x, y):
        self.x = x
        self.y = y

    def pyglet_coor(self, window_obj):
        self.y = window_obj.height - self.y

    def center(self):
        self.anchor_x = 'center'
        self.anchor_y = 'center'

    def set_anchor(self, anchor_tuple: tuple):
        self.anchor_x = anchor_tuple[0]
        self.anchor_y = anchor_tuple[1]

    def decorate(self, char_i: int, char_o: int, attributes: dict):
        self.layout = None
        self.document.set_style(char_i, char_o, attributes)
        self.update_layout(False)

    # Exclusive to this program
    def color_until(self, char_o: int, r, g, b, a):
        self.decorate(0, char_o, {'color': (r, g, b, a)})

    def color_from(self, char_i: int, r, g, b, a):
        self.decorate(char_i, len(self.document.text), {'color': (r, g, b, a)})

    def color(self, r, g, b, a):
        self.decorate(0, len(self.document.text), {'color': (r, g, b, a)})

    def update_layout(self, properties_only=True):
        if not properties_only:
            self.layout = pyglet.text.layout.TextLayout(self.document)
        self.layout.x = self.x
        self.layout.y = self.y
        self.layout.anchor_x = self.anchor_x
        self.layout.anchor_y = self.anchor_y

    def draw(self):
        self.document.text = self.text
        self.update_layout(True)
        self.layout.draw()


class Window(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.cursor = self.CURSOR_DEFAULT
        self.focus = None

    def set_focus(self, focus: Textbox):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0

        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

    def unfocus(self):
        self.focus.caret.visible = False
        self.focus.caret.mark = self.focus.caret.position = 0
        self.focus = None

    def on_text(self, text):
        if self.focus:
            text = text.replace('\r', '')
            self.focus.caret.on_text(text)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)


ui_elements = {
    MAIN_MENU: [],
    GAME_MODE: [],
    OPTIONS: [],
    CREDITS: [],
    INSTRUCTIONS: [],
    PAUSE: [],
    ENDGAME: []
}
ui_buttons = copy.deepcopy(ui_elements)
ui_labels = copy.deepcopy(ui_elements)
ui_textboxes = copy.deepcopy(ui_elements)


def add_ui_element(view_str, ui_element):
    ui_elements[view_str].append(ui_element)


def add_ui_button(view_str, ui_element):
    ui_elements[view_str].append(ui_element)
    ui_buttons[view_str].append(ui_element)


def add_ui_label(view_str, ui_element):
    ui_elements[view_str].append(ui_element)
    ui_labels[view_str].append(ui_element)


def add_ui_textbox(view_str, ui_element):
    ui_elements[view_str].append(ui_element)
    ui_textboxes[view_str].append(ui_element)


def reset_ui_textboxes(view_str):
    for textbox in ui_textboxes[view_str]:
        textbox.set_text('')


def draw_element(ui_element, window_obj: Window):
    try:
        print(window_obj)
        ui_element.draw(window_obj)
    except TypeError:
        ui_element.draw()


def get_image_anchor(image_object: Image, anchor_tuple: tuple) -> tuple:
    img_anchor = []
    if anchor_tuple[0] == 'left':
        img_anchor.append(0)
    elif anchor_tuple[0] == 'center':
        img_anchor.append(image_object.image.width // 2)
    elif anchor_tuple[0] == 'right':
        img_anchor.append(image_object.image.width)
    if anchor_tuple[1] == 'top':
        img_anchor.append(image_object.image.height)
    elif anchor_tuple[1] == 'center':
        img_anchor.append(image_object.image.height // 2)
    elif anchor_tuple[1] == 'bottom':
        img_anchor.append(0)

    return tuple(img_anchor)


try:
    pyglet.font.add_file('assets/arcade_alternate.ttf')  # Arcade Alternate
    print('All custom fonts successfully loaded.')
except FileNotFoundError:
    print('File not found - please run main.py')
