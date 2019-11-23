import pyglet, math, random
from pyglet.gl import *

window = pyglet.window.Window(800, 600)
batch = pyglet.graphics.Batch()


def create_polygon(x, y, radius, sides, batch):
    circle, indices = create_indexed_vertices(x, y, radius, sides)
    vertex_count = len(circle) // 2
    vertex_list = batch.add_indexed(vertex_count, pyglet.gl.GL_TRIANGLES, None,
                                    indices,
                                    ('v2f', circle),
                                    ('c4f', (1, 1, 1, 0.8) * vertex_count))


def create_indexed_vertices(x, y, radius, sides=4):
    vertices = [x, y]
    for side in range(sides):
        angle = side * 2.0 * math.pi / sides
        vertices.append(x + math.cos(angle) * radius)
        vertices.append(y + math.sin(angle) * radius)
    # Add a degenerated vertex
    vertices.append(x + math.cos(0) * radius)
    vertices.append(y + math.sin(0) * radius)

    indices = []
    for side in range(1, sides + 1):
        indices.append(0)
        indices.append(side)
        indices.append(side + 1)
    return vertices, indices


create_polygon(window.width // 2, window.height // 2, 100, 5, batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
