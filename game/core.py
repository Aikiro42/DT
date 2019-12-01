from pyglet.gl import *
from utils.interface import *
from utils.utils import gen_code, read_options_ini

'''


This module holds all the core variables and base UI (window variable) of the program proper.
This is depended on by:
    game.core
    game.endgame
    game.gamemode
    game.highscores
    game.options
    game.pause
    game.title

This is dependent on:
    utils.interface
    utils.utils (particularly the function for generating code)

'''


# Gets the options from options.ini
# Called after the initialization of gamevars to immediately edit some of the flag variables
def get_options():
    op_dict = read_options_ini()
    gamevars.allow_bgm = eval(op_dict['allow_bgm'])
    gamevars.allow_sfx = eval(op_dict['allow_sfx'])
    gamevars.allow_bg = eval(op_dict['allow_bg'])


# Game variable class created to retrieve gamevars anywhere within the program
class VarObj:
    def __init__(self):
        # Ini settings
        self.allow_bgm = True  # Determines whether to allow bgm
        self.allow_sfx = True  # Determines whether to allow sfx
        self.allow_bg = True  # Lets animated backgrounds render when true
        self.allow_anim = True  # Determines whether title sprite will animate up and down in main menu
        self.allow_antialiasing = False  # Determines whether there will be opengl antialiasing
        self.allow_transparency = True  # Determines whether to allow opengl transparency effects
                                        # Kinda pointless since the sprites are made transparent
        # Debug flags
        self.debug_bg = False  # Turns background to magenta for debug purposes
        self.debug_res = False  # Turns borderless resolution to 800x600
        self.is_count_dt = False  # Determines whether the program will increment the debug counter every update
        self.debug_dt = 0  # The debug counter - incremented if is_count_dt and update is called

        self.kill_command = "order_66.execute()"  # Cheat for a game over
        self.eggnames = ['luis', 'rain', 'jackie', 'enrico']  # Cheats for easy 100 points
        self.edgar = 'CS11.set_grade(1)'  # This code does nothing, don't enter it in the command line

        # Rawstarr mode - The timer will not tick, and the lose condition is submitting a mismatch
        #               - Deactivates upon restart
        self.rawstarr = 'schedule_until(rawstarr, end=self.death)'  # Code for rawstarr mode
        self.is_rawstarr = False  # Determines if the program is in rawstarr mode

        # Daemon Mode - Schedules a DaemonThread that crashes the game
        # self.daemon = 'DaemonThread<0x29A>.start(self.soul)'  # Code to summon a demon
        self.daemon = 'self.soul'  # Code to summon a demon
        self.is_daemon = False  # Flag for when the DaemonThread is scheduled
        self.daemon_draw = False  # Determines whether to draw the program crasher

        # Title sprite animation variables
        self.bounce_threshold = 10  # Determines how far the sprite will bounce up and down
        self.bounce = 0  # Position offset of the sprite, incremented and decremented depending on...
        self.bounce_increment = 1  # ...this variable.
        self.display_fps = False  # Displays FPS in lower left corner of screen if true

        # Duration (in seconds) of the codeline recolor effects when the player
        # enters a mismatch
        self.show_error_time = 1

        self.score = 0  # The current score of the player - immediately calculated and set
        self.display_score = 0  # The displayed score of the player - this is incremented
        self.display_increment = 5  # The amount the displayed score is incremented when score is recalculated
        self.max_time = 59  # Timer cap - codeline length and timer increment dependent on this variable

        # Amount of time (in seconds) to increment when player submits correctly
        self.timer_increment = self.max_time // 20

        # Game mode timer - decremented by scheduled timer decrement function during game mode
        self.timer = self.max_time

        # Timer redline - low time remaining warning effects activate when timer is below this threshold
        self.timer_redline = 10

        # Code depth - determines depth of code
        self.code_depth = min((self.max_time // 20) + 1, 7)

        # Codeline string - the code entered by the player is compared against this string
        self.codeline_str = gen_code(self.code_depth)

        # The player codeline - updated when the player presses enter, and then almost simultaneously refreshed
        self.player_codeline = ''

        # VARIABLES NO TOUCHIE TOUCHIE BELOW

        self.game_state = uivars.MAIN_MENU  # State flag for game - determines which UI to draw

        self.is_game = False  # Flag for when the game's state is GAME_MODE - used to schedule timer decrement
        self.is_pause = False  # Flag for when the game's state is PAUSE - used to unschedule timer decrement
        self.is_timer = False  # Flag for when the timer is running

        # Flag for when the game is restarted
        # When true, appropriate game variables are reset and this variable is immediately
        # set to false
        self.is_restart = False

        # Flag for when something is entered in the command line
        # Immediately turned off after checking
        self.is_check_code = False

        # Flag for indicating whether textbox is clear
        self.is_textbox_clear = True

        # Flag for when the code is correct
        self.is_code_correct = False

        self.animate_score_update = False  # True when the displayed score must be increased

    """
    This is a function that calculates the player's score, taking into account many relevant factors
    
    :return Integer - A recalculation of the player's score
    """

    def increment_score(self):
        return len(self.codeline_str) * 10 + self.timer * 2


# Variable that is accessible project-wide
gamevars = VarObj()
get_options()

# interface initialization, uses stuff from utils.interface, pyglet and pyglet.gl
display = pyglet.canvas.get_display()
screen = display.get_screens()[0]
window_w = screen.width
window_h = screen.height

if gamevars.debug_res:
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

glClearColor(0, 0, 0, 0)
if gamevars.debug_bg:
    glClearColor(1, 0, 1, 1)

if gamevars.allow_antialiasing:
    glEnable(GL_LINE_SMOOTH) # antialiasing
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)

if gamevars.allow_transparency:
    glEnable(GL_BLEND)  # transparency
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # transparency
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Texture Parameters
