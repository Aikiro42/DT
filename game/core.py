from pyglet.gl import *
from utils.interface import *


# Game Variables
class VarObj:
    def __init__(self):
        self.game_state = MAIN_MENU

        self.is_game = False
        self.is_pause = False
        self.is_timer = False
        self.is_restart = False
        self.is_check_code = False

        self.score = 0
        self.display_score = 0
        self.display_increment = 5
        self.max_time = 1
        self.timer = self.max_time
        # self.codeline_str = "Arcade.alternate(is_the_font, [to, be_used])"
        self.codeline_str = "test"
        self.player_codeline = ''


gamevars = VarObj()

# interface initialization, uses stuff from utils.interface, pyglet and pyglet.gl

config = Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True, mouse_visible=False)
window = Window(800, 600, config=config)
glClearColor(0.01, 0.075, 0.1, 0)
glEnable(GL_LINE_SMOOTH)
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable(GL_BLEND)  # transparency
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
