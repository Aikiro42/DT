from pyglet.gl import *
from utils.interface import *
from utils.utils import gen_code


# Game Variables
class VarObj:
    def __init__(self):
        self.debug = False
        self.admin = True
        self.kill_command = "order_66.execute()"
        self.konami = 'hi'
        self.eggnames = ['luis', 'rain', 'jackie', 'enrico']
        self.edgar = 'CS11.set_grade(1)'
        self.rawstarr = 'schedule_until(rawstarr, end=self.death)'
        self.is_rawstarr = False

        self.game_state = uivars.MAIN_MENU
        self.is_music_playing = False

        self.is_game = False
        self.is_pause = False
        self.is_timer = False
        self.is_restart = False
        self.is_check_code = False

        self.is_textbox_clear = True
        self.is_code_correct = False

        self.bounce_threshold = 10
        self.bounce = 0
        self.bounce_increment = 1
        self.animate_score_update = False
        self.display_fps = False

        self.show_error_time = 1  # seconds

        self.score = 0
        self.display_score = 0
        self.display_increment = 5
        self.max_time = 150
        self.timer_increment = self.max_time // 20
        self.timer = self.max_time
        self.timer_redline = 10
        # self.codeline_str = "Arcade.alternate(is_the_font, [to, be_used])"
        self.code_depth = min((self.max_time // 20) + 1, 7)
        self.codeline_str = gen_code(self.code_depth)
        self.player_codeline = ''

    def increment_score(self):
        return len(self.codeline_str) * 10 + self.timer*2


gamevars = VarObj()


# interface initialization, uses stuff from utils.interface, pyglet and pyglet.gl
display = pyglet.canvas.get_display()
screen = display.get_screens()[0]
window_w = screen.width
window_h = screen.height

if gamevars.debug:
    window_w = 800
    window_h = 600

window_x = screen.width - window_w // 2
window_y = screen.height - window_h // 2

config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True, mouse_visible=False)
window = Window(window_w, window_h,
                config=config, resizable=False, fullscreen=False,
                screen=screen, style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS,
                caption="DataType - A programmer's game")
icon1 = pyglet.image.load('assets/icon_16.png')
icon2 = pyglet.image.load('assets/icon_32.png')
icon3 = pyglet.image.load('assets/icon.png')
window.set_location(0, 0)
window.set_icon(icon1, icon2, icon3)

fps_display = pyglet.window.FPSDisplay(window=window)

glClearColor(0.01, 0.075, 0.1, 0)
# glEnable(GL_LINE_SMOOTH) # antialiasing
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)  # transparency
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
