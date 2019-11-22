import pyglet

time = 0

window = pyglet.window.Window()


def update(dt):
    global time
    time += 1
    print(time)


pyglet.clock.schedule_interval(update, 1)

pyglet.app.run()