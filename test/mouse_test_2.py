import pyglet


image = pyglet.resource.image('test.png')
image.anchor_x = image.width // 2
image.anchor_y = image.height // 2

state = True

window = pyglet.window.Window()

def on_draw():
    print('on_draw() called')
    window.clear()
    if state:
        image.blit(window.width // 2, window.height // 2)


def on_mouse_press(x, y, button, modifiers):
    global state
    print('mouse pressed')
    if state:
        state = False
    else:
        state = True


window.on_draw = on_draw
window.on_mouse_press = on_mouse_press

pyglet.app.run()
