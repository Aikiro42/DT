import pyglet

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(800, 600)
        self.image = pyglet.resource.image('test.png')

        self.image = pyglet.resource.image('test.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.state = True

    def on_draw(self):
        print('on_draw() called')
        window.clear()
        if self.state:
            self.image.blit(self.width // 2, self.height // 2)

    def on_mouse_press(self, x, y, button, modifiers):
        print('mouse pressed')
        if self.state:
            self.state = False
        else:
            self.state = True


window = Window()

pyglet.app.run()
