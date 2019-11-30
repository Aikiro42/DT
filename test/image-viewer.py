import pyglet


def get_image_anchor(image_object, anchor_tuple: tuple) -> tuple:
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


class Image:
    def __init__(self, image_dir, x=0, y=0):
        self.image = pyglet.resource.image(image_dir)
        self.sprite = pyglet.sprite.Sprite(self.image)
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
        self.sprite = pyglet.sprite.Sprite(self.image)

    def draw(self):
        # self.image.blit(self.coor.x, self.coor.y)
        self.sprite.draw()
        self.rendered = True


window = pyglet.window.Window()
image = Image('test.png')
x = ('center', 'center')
image.set_anchor(x)


@window.event
def on_draw():
    window.clear()
    image.draw()


pyglet.app.run()
