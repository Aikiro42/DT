from pyglet.gl import *
from utils.interface import *
from utils.utils import gen_code


# Game Variables
class VarObj:
    def __init__(self):
        self.game_state = MAIN_MENU

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

        self.show_error_time = 1  # seconds

        self.score = 0
        self.display_score = 0
        self.display_increment = 5
        self.max_time = 59
        self.timer_increment = 2
        self.timer = self.max_time
        # self.codeline_str = "Arcade.alternate(is_the_font, [to, be_used])"
        self.code_depth = (self.max_time // 20) + 1
        self.codeline_str = gen_code(self.code_depth)
        self.player_codeline = ''


gamevars = VarObj()

# interface initialization, uses stuff from utils.interface, pyglet and pyglet.gl

config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True, mouse_visible=False)
window = Window(800, 600, config=config)

fps_display = pyglet.window.FPSDisplay(window=window)

glClearColor(0.01, 0.075, 0.1, 0)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)  # transparency
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
