import pyglet

window = pyglet.window.Window()

label = pyglet.text.Label("DataType",
                          font_name="Segoe UI",
                          font_size=36,
                          x=0, y=0,
                          anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    label.draw()


pyglet.app.run()
