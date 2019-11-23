import pyglet

window = pyglet.window.Window()

document = pyglet.text.document.FormattedDocument('Hello there')
flag = False
document.set_style(0, 2, {'color': (255, 0, 0, 255), 'font_size': 63})
layout = pyglet.text.layout.TextLayout(document)


@window.event
def on_draw():
    layout.draw()


@window.event
def on_key_press(symbol, modifiers):
    global layout
    if not flag:
        layout = None
        document.set_style(0, 10, {'color': (255, 0, 0, 255)})
        layout = pyglet.text.layout.TextLayout(document)


pyglet.app.run()
