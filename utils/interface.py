import pyglet
from copy import copy, deepcopy
from utils.sounds import *


class InterfaceVars:

    def __init__(self):
        # CONSTANTS
        # game states
        self.MAIN_MENU = 1
        self.GAME_MODE = 2
        self.ENDGAME = 3  # game over
        self.OPTIONS = 4
        self.INSTRUCTIONS = 5
        self.CREDITS = 6
        self.PAUSE = 7
        self.HIGHSCORES = 8

        # label anchors
        self.UPPER_RIGHT = ('right', 'top')
        self.LOWER_RIGHT = ('right', 'bottom')
        self.UPPER_LEFT = ('left', 'top')
        self.LOWER_LEFT = ('left', 'bottom')
        self.CENTER_TOP = ('center', 'top')
        self.CENTER_BOTTOM = ('center', 'bottom')
        self.CENTER_LEFT = ('left', 'center')
        self.CENTER_RIGHT = ('right', 'center')
        self.CENTER = ('center', 'center')

        # colors
        self.RED = (255, 0, 0, 255)
        self.GREEN = (0, 255, 0, 255)
        self.WHITE = (255, 255, 255, 255)

        self.ui_elements = {
            self.MAIN_MENU: [],
            self.GAME_MODE: [],
            self.OPTIONS: [],
            self.CREDITS: [],
            self.INSTRUCTIONS: [],
            self.PAUSE: [],
            self.ENDGAME: [],
            self.HIGHSCORES: []
        }
        self.ui_buttons = deepcopy(self.ui_elements)
        self.ui_labels = deepcopy(self.ui_elements)
        self.ui_textboxes = deepcopy(self.ui_elements)
        self.ui_backgrounds = deepcopy(self.ui_elements)
        self.rescaling_factor = 1536

    def add_ui_element(self, view_str, ui_element):
        self.ui_elements[view_str].append(ui_element)

    def add_ui_button(self, view_str, ui_element):
        self.ui_elements[view_str].append(ui_element)
        self.ui_buttons[view_str].append(ui_element)

    def add_ui_label(self, view_str, ui_element):
        self.ui_elements[view_str].append(ui_element)
        self.ui_labels[view_str].append(ui_element)

    def add_ui_textbox(self, view_str, ui_element):
        self.ui_elements[view_str].append(ui_element)
        self.ui_textboxes[view_str].append(ui_element)

    def add_ui_background(self, view_str, ui_element):
        self.ui_backgrounds[view_str].append(ui_element)

    def reset_ui_textboxes(self, view_str):
        for textbox in self.ui_textboxes[view_str]:
            textbox.set_text('')

    def draw_element(self, ui_element, window_obj):
        try:
            ui_element.draw(window_obj)
        except TypeError:
            ui_element.draw()

    def get_image_anchor(self, image_object, anchor_tuple: tuple) -> tuple:
        img_anchor = []
        if anchor_tuple[0] == 'left':
            img_anchor.append(0)
        elif anchor_tuple[0] == 'center':
            img_anchor.append(image_object.sprite.image.width // 2)
        elif anchor_tuple[0] == 'right':
            img_anchor.append(image_object.sprite.image.width)
        if anchor_tuple[1] == 'top':
            img_anchor.append(image_object.sprite.image.height)
        elif anchor_tuple[1] == 'center':
            img_anchor.append(image_object.sprite.image.height // 2)
        elif anchor_tuple[1] == 'bottom':
            img_anchor.append(0)

        return tuple(img_anchor)


uivars = InterfaceVars()


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
        self.vertex_list = pyglet.graphics.vertex_list(4,
                                                       ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                                       ('c4B', color * 4)
                                                       )

    def draw(self):
        self.vertex_list.draw(pyglet.gl.GL_QUADS)


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
            self.document, width, height, multiline=False)
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
        self.rectangle.draw()
        self.layout.draw()
        self.rendered = True

    def click_event(self):
        pass


class Image:
    def __init__(self, image_dir, x=0, y=0, batch=None):
        self.image_default = pyglet.resource.image(image_dir)
        self.sprite = pyglet.sprite.Sprite(self.image_default, x, y, batch=batch)
        self.rendered = False

    def set_coor(self, x, y):
        self.sprite.update(x=x, y=y)

    def set_x(self, x):
        self.sprite.update(x=x)

    def get_x(self):
        return self.sprite.x

    def set_y(self, y):
        self.sprite.update(y=y)

    def get_y(self):
        return self.sprite.y

    def resize(self, width, height):
        width /= self.sprite.width
        height /= self.sprite.height
        self.sprite.update(scale_x=width, scale_y=height)

    def rescale(self, scale):
        self.sprite.update(scale=scale)

    def pyglet_coor(self, window_obj):
        self.sprite.update(y=window_obj.height - self.sprite.y)

    def center(self):
        """Sets an image's anchor point to its center"""
        self.sprite.image.anchor_x = self.image_default.width // 2
        self.sprite.image.anchor_y = self.image_default.height // 2

    def set_anchor(self, anchor_tuple: tuple):
        anchors = uivars.get_image_anchor(self, anchor_tuple)
        self.sprite.image.anchor_x = anchors[0]
        self.sprite.image.anchor_y = anchors[1]

    def draw(self):
        self.sprite.draw()
        self.rendered = True


class Background(Image):
    def __init__(self, background_dir, window_obj, batch=None, fill=True):
        super(Background, self).__init__(background_dir,
                                         x=window_obj.width // 2,
                                         y=window_obj.height // 2,
                                         batch=batch)
        self.set_anchor(uivars.CENTER)
        if fill:
            self.fill_dimensions(window_obj)
        self.pyglet_coor(window_obj)

    def set_dimensions(self, width, height):
        height_scale = height / self.sprite.height
        width_scale = width / self.sprite.width
        self.sprite.update(scale_x=width_scale, scale_y=height_scale)

    def fill_dimensions(self, window_obj):
        self.set_dimensions(window_obj.width, window_obj.height)


class AnimatedBackground:
    def __init__(self, gif_dir, window_obj, full_scale=True, batch=None):
        self.animation = pyglet.image.load_animation(gif_dir)
        self.sprite = pyglet.sprite.Sprite(self.animation, batch=batch)
        if full_scale:
            self.fill_dimensions(window_obj)
        else:
            self.center()
            self.set_coor(window_obj.width // 2, window_obj.height // 2)

    def set_coor(self, x, y):
        self.sprite.x = x
        self.sprite.y = y

    def center(self):
        self.sprite.image.anchor_x = self.sprite.width // 2
        self.sprite.image.anchor_y = self.sprite.height // 2

    def set_dimensions(self, width, height):
        height_scale = height / self.sprite.height
        width_scale = width / self.sprite.width
        self.sprite.update(scale_x=width_scale, scale_y=height_scale)

    def draw(self):
        self.sprite.draw()

    def fill_dimensions(self, window_obj):
        self.set_dimensions(window_obj.width, window_obj.height)


class Button(Image):
    def __init__(self, image_dir, x=0, y=0, image_hover_dir=None, image_active_dir=None, batch=None):
        super(Button, self).__init__(image_dir, x, y, batch)
        self.image_hover = None
        self.image_active = None
        self.is_default = True
        if image_hover_dir:
            self.image_hover = pyglet.resource.image(image_hover_dir)
        if image_active_dir:
            self.image_active = pyglet.resource.image(image_active_dir)

    def center(self):
        """Sets an image's anchor point to its center"""
        ax = self.sprite.image.width // 2
        ay = self.sprite.image.height // 2
        self.sprite.image.anchor_x = ax
        self.sprite.image.anchor_y = ay
        if self.image_hover:
            self.image_hover.anchor_x = ax
            self.image_hover.anchor_y = ay
        if self.image_active:
            self.image_active.anchor_x = ax
            self.image_active.anchor_y = ay

    def set_anchor(self, anchor_tuple: tuple):
        super().set_anchor(anchor_tuple)
        anchors = uivars.get_image_anchor(self, anchor_tuple)
        self.sprite.image.anchor_x = anchors[0]
        self.sprite.image.anchor_y = anchors[1]
        if self.image_hover:
            self.image_hover.anchor_x = anchors[0]
            self.image_hover.anchor_y = anchors[1]
        if self.image_active:
            self.image_active.anchor_x = anchors[0]
            self.image_active.anchor_y = anchors[1]

    def hit(self, cursor_x, cursor_y, check_render=True):
        ox = self.sprite.x - self.sprite.image.anchor_x * self.sprite.scale
        oy = self.sprite.y - self.sprite.image.anchor_y * self.sprite.scale
        ow = self.sprite.width
        oh = self.sprite.height
        if check_render:
            check_render = self.rendered
        else:
            check_render = True
        if check_render and ox < cursor_x < ox + ow and oy < cursor_y < oy + oh:
            return True
        else:
            return False

    def click_event(self):
        pass

    def default_event(self):
        if not self.is_default:
            self.sprite.image = self.image_default

    def hover_event(self):
        if self.image_hover and self.sprite.image != self.image_hover:
            self.sprite.image = self.image_hover
            self.is_default = False
            sfx_hover.play()

    def active_event(self):
        if self.image_active and self.sprite.image != self.image_active:
            self.sprite.image = self.image_active
            self.is_default = False
            sfx_click.play()


class ToggledButton:
    def __init__(self, image_dir_a, image_dir_b,
                 x=0, y=0,
                 image_hover_dir_a=None, image_hover_dir_b=None,
                 image_active_dir_a=None, image_active_dir_b=None,
                 batch=None):
        self.button_a = Button(image_dir_a, x=x, y=y,
                               image_hover_dir=image_hover_dir_a, image_active_dir=image_active_dir_a, batch=batch)
        self.button_b = Button(image_dir_b, x=x, y=y,
                               image_hover_dir=image_hover_dir_b, image_active_dir=image_active_dir_b, batch=batch)
        self.button = self.button_a
        self.state = True  # True = on, False = off
        self.rendered = False

    def center(self):
        self.button_a.center()
        self.button_b.center()

    def set_anchor(self, anchor_tuple):
        self.button_a.set_anchor(anchor_tuple)
        self.button_b.set_anchor(anchor_tuple)

    def rescale(self, scale):
        self.button_a.rescale(scale)
        self.button_b.rescale(scale)

    def hit(self, cursor_x, cursor_y):
        if self.rendered:
            return self.button.hit(cursor_x, cursor_y, check_render=False)

    def change_state(self):
        if self.state:
            self.button = self.button_b
        else:
            self.button = self.button_a
        self.state = not self.state

    def set_coor(self, x, y):
        self.button_a.set_coor(x, y)
        self.button_b.set_coor(x, y)

    def pyglet_coor(self, window_obj):
        self.button_a.pyglet_coor(window_obj)
        self.button_b.pyglet_coor(window_obj)

    def draw(self):
        self.button.draw()
        self.rendered = True

    def click_event(self):
        self.button.click_event()

    def hover_event(self):
        self.button.hover_event()

    def active_event(self):
        self.button.active_event()

    def default_event(self):
        self.button.default_event()

    def set_on_click_event(self, event_func):
        self.button_a.click_event = event_func

    def set_off_click_event(self, event_func):
        self.button_b.click_event = event_func

    def set_click_event(self, event_func):
        self.button_a.click_event = event_func
        self.button_b.click_event = event_func


class Label:

    def __init__(self, text='',
                 font_name=None, font_size=None, bold=False, italic=False,
                 color=(255, 255, 255, 255),
                 x=0, y=0, width=None, height=None, batch=None,
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
        self.layout = pyglet.text.layout.TextLayout(self.document, batch=batch)
        self.content_height = self.layout.content_height
        self.rendered = False

    def set_coor(self, x, y):
        self.x = x
        self.y = y

    def rescale(self, scale):
        font_size = self.document.get_style('font_size')
        self.document.set_style(0, len(self.document.text), {
            'font_size': font_size * scale,
        })

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
        self.rendered = True


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


try:
    pyglet.font.add_file('assets/arcade_alternate.ttf')  # Arcade Alternate
    print('All custom fonts successfully loaded.')
except FileNotFoundError:
    print('File not found - please run main.py')
