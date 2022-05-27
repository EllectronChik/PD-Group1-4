import pygame as pg
import lang_en as en


pg.init()

FPS = 60
mainClock = pg.time.Clock() 
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
display_width = screen.get_width()
display_height = screen.get_height()
background = pg.Surface(screen.get_size())
cross = pg.transform.scale(pg.image.load('images/cross.png'), (display_height * 0.32, display_height * 0.32))
zero = pg.transform.scale(pg.image.load('images/zero.png'), (display_height * 0.32, display_height * 0.32))
button_sound = pg.mixer.Sound('sounds/mouse_on_menu_button.wav')
figure_now = cross
game_running = False
first_step = True
printed_cross = []
printed_zeros = []
last_winner = None
winner = None
language = 'English'
play_t = en.play_t
settings_t = en.settings_t
quit_t = en.quit_t
back_t = en.back_t
restart_t = en.restart_t
cross_t = en.cross_t
nought_t = en.nought_t
cross__turn_t = en.cross__turn_t
nought_turn_t = en.nought_turn_t
last_winner_t = en.last_winner_t
winner_t = en.winner_t
resolution_t = en.resolution_t
language_t = en.language_t
fulsize_t = en.fulsize_t
start_game = True