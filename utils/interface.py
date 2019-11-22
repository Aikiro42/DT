from abc import ABCMeta

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

    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
                                     ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                     ('c4B', [200, 200, 220, 255] * 4)
                                     )


class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text),
                                dict(color=(0, 0, 0, 255))
                                )
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 2
        self.rectangle = Rectangle(x - pad, y - pad,
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)


class Textbox:
    def __init__(self, window_obj, x=0, y=0, width=200):
        self.coor = Coordinates(x, y)
        self.width = width
        self.window_batch = window_obj.batch  # See Window class in this module
        self.widget = None

    def set_coor(self, x, y):
        self.coor.x = x
        self.coor.y = y

    def pyglet_coor(self, window_obj):
        self.coor.pyglet_coor(window_obj)

    def draw(self):
        self.widget = TextWidget('', self.coor.x, self.coor.y, self.width, self.window_batch)
        self.window_batch.draw()


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


class Label(pyglet.text.Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_coor(self, x, y):
        self.x = x
        self.y = y

    def pyglet_coor(self, window_obj):
        self.y = window_obj.height - self.y

    def center(self):
        self.anchor_x = 'center'
        self.anchor_y = 'center'

    def set_anchor(self, anchor_x: int, anchor_y: int):
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y

    def set_anchor(self, anchor_tuple: tuple):
        self.anchor_x = anchor_tuple[0]
        self.anchor_y = anchor_tuple[1]


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.cursor = self.CURSOR_DEFAULT


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


def draw_element(ui_element, window_obj: Window):
    try:
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
