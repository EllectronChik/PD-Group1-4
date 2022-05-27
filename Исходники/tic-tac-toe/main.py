import pygame as pg
import sys
import lang_en as en
import lang_ru as ru 
import time
from globals import *


pg.init()
game_name_t = en.game_name_t
pg.display.set_caption(game_name_t)


class Game_button:
    '''
    Класс кнопки игрового поля с шириной width, высотой height,
    цветами inactive в неактивном состоянии и active в активном,
    а так же номером num, определяющем позицию кнопки в игровой сетке
    '''
    def __init__(self, width, height, inactive, active, num):
        self.width = width
        self.height = height
        self.inactive = inactive #177
        self.active = active 
        self.was_clicked = False
        self.was_printed = False
        self.num = num


    def draw_button(self, x, y):
        '''
        Метод отрисовки кнопки на координатах (x, y)
        '''
        global figure_now
        global first_step
        global printed_cross
        global printed_zeros
        global winner
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        target_rect = pg.Rect(x, y, self.width, self.height)
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
        if (x <= mouse[0] <= x + self.width and
            y <= mouse[1] <= y + self.height):
            pg.draw.rect(shape_surf, self.active, (0, 0, self.width, self.height))
            if winner is None:
                if click[0] == True and self.was_clicked == False:
                    first_step = False
                    self.was_clicked = True
                if self.was_printed == False:
                    shape_surf.blit(figure_now, (0, 0))
        else:
            pg.draw.rect(shape_surf, self.inactive, (0, 0, self.width, self.height))
        if self.was_clicked == True and self.was_printed == False:
            if winner is None:
                self.surface = figure_now
                if figure_now == cross:
                    printed_cross.append(self.num)
                    figure_now = zero
                else:
                    printed_zeros.append(self.num)
                    figure_now = cross
                self.was_printed = True
        elif self.was_clicked == True and self.was_printed == True and first_step == False:
            shape_surf.blit(self.surface, (0, 0))
        screen.blit(shape_surf, target_rect)
        if first_step == True:
            self.was_clicked = False
            self.was_printed = False


class Information_block:
    '''
    Класс текстового блока шириной width и длиной height
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        

    def print_box(self, x, y, message):
        '''
        Метод помещающий текст message на координатах (x, y)
        '''
        target_rect = pg.Rect(x, y, self.width, self.height)
        surf = pg.Surface(target_rect.size)
        print_text(message, 0, 0, self.height - self.height // 5,  surf, (255, 255, 255))
        screen.blit(surf, target_rect)


class Menu_button:
    '''
    Класс кнопки меню с шириной width, высотой height,
    цветами inactive в неактивном состоянии и active в активном
    '''
    def __init__(self, width, height, inactive, active):
        self.width = width
        self.height = height
        self.inactive = inactive #177
        self.active = active 
        self.playsound = True


    def draw_button(self, x, y, message, surface, action = None):
        '''
        Метод отрисовки кнопок с текстом message на поверхности surface координатах (x, y)
        и вызова действия action по нажатию(По умолчанию не вызывает никакого действия)
        '''
        click = pg.mouse.get_pressed()
        mouse = pg.mouse.get_pos()
        target_rect = pg.Rect(x, y, self.width + 5, self.height)
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
        if (x <= mouse[0] <= x + self.width and
            y <= mouse[1] <= y + self.height):
            pg.draw.polygon(shape_surf, self.active, [(self.width // 6, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
            print_text(message, self.width // 6, -1, self.height - self.height // 5, shape_surf)
            if self.playsound == True:
                button_sound.play(0)
                self.playsound = False
            if click[0] == True and action is not None:
                action()
        else:
            self.playsound = True
            pg.draw.polygon(shape_surf, self.inactive, [(self.width // 6 + display_width // 100, 0), (self.width, 0), (self.width, self.height), (display_width // 100, self.height)])
            print_text(message, self.width // 6 + display_width // 100, -1, self.height - self.height // 5, shape_surf)
        surface.blit(shape_surf, target_rect)


class Settings_button:
    '''
    Класс переключателя настроек с шириной width, высотой height,
    цветами inactive в неактивном состоянии и active в активном
    '''
    def __init__(self, width, height, inactive, active):
        self.width = width
        self.height = height
        self.inactive = inactive #177
        self.active = active 
        self.playsound = True


    def draw_button(self, x, y, message, surface, action = None):
        '''
        Метод отрисовки текста message на поверхности surface координатах (x, y)
        и вызова действия action по нажатию(По умолчанию не вызывает никакого действия)
        '''
        click = pg.mouse.get_pressed()
        mouse = pg.mouse.get_pos()
        target_rect = pg.Rect(x, y, self.width + 5, self.height)
        shape_surf = pg.Surface(target_rect.size)
        if (x <= mouse[0] <= x + self.width and
            y <= mouse[1] <= y + self.height):
            print_text(message, self.width // 12, -1, int(self.height * 0.8) - self.height // 5, shape_surf, (255, 255, 255))
            if self.playsound == True:
                button_sound.play(0)
                self.playsound = False
            if click[0] == True and action is not None:
                action()
        else:
            self.playsound = True
            print_text(message, self.width // 12, -1, int(self.height * 0.8) - self.height // 5, shape_surf, (177, 177, 177))
        surface.blit(shape_surf, target_rect)


def print_text(message, x, y, font_size, surface = screen, font_color = (0, 0, 0), font_type = 'fonts/Caveat-VariableFont_wght.ttf'):
    '''
    Функция вывода текста message на поверхности surface координатах (x, y)
     со шрифтом font_type, размером шрифта font_size и цветом font_color
    '''
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    surface.blit(text, (x, y))    


def quit_game():
    '''
    Функция закрытия программы
    '''
    pg.quit()
    flRunning = False
    sys.exit()


def restart():
    '''
    Функция перезагрузки игрового поля
    '''
    global first_step
    global figure_now
    global printed_cross
    global printed_zeros
    global is_victory
    global last_winner
    global winner
    printed_zeros = []
    printed_cross = []
    figure_now = cross
    first_step = True
    if winner == nought_t:
        last_winner = nought_t
    elif winner == cross_t:
        last_winner = cross_t
    winner = None


def language_change():
    '''
    Функция смены языка
    '''
    global language
    global game_name_t
    global play_t
    global settings_t
    global quit_t
    global back_t
    global restart_t
    global cross_t
    global nought_t
    global cross__turn_t
    global nought_turn_t
    global last_winner_t
    global winner_t
    global resolution_t
    global language_t
    global fulsize_t
    global last_winner
    time.sleep(0.1)
    if language == 'English':
        game_name_t = ru.game_name_t
        play_t = ru.play_t
        settings_t = ru.settings_t
        quit_t = ru.quit_t
        back_t = ru.back_t
        restart_t = ru.restart_t
        cross__turn_t = ru.cross__turn_t
        nought_turn_t = ru.nought_turn_t
        last_winner_t = ru.last_winner_t
        winner_t = ru.winner_t
        resolution_t = ru.resolution_t
        language_t = ru.language_t
        fulsize_t = ru.fulsize_t
        if last_winner == cross_t:
            last_winner = ru.cross_t
        elif last_winner == nought_t:
            last_winner = ru.nought_t
        cross_t = ru.cross_t
        nought_t = ru.nought_t
        language = 'Русский'
        pg.display.set_caption(ru.game_name_t)
    else:
        game_name_t = en.game_name_t
        play_t = en.play_t
        settings_t = en.settings_t
        quit_t = en.quit_t
        back_t = en.back_t
        restart_t = en.restart_t
        cross__turn_t = en.cross__turn_t
        nought_turn_t = en.nought_turn_t
        last_winner_t = en.last_winner_t
        winner_t = en.winner_t
        resolution_t = en.resolution_t
        language_t = en.language_t
        fulsize_t = en.fulsize_t
        if last_winner == cross_t:
            last_winner = en.cross_t
        elif last_winner == nought_t:
            last_winner = en.nought_t
        cross_t = en.cross_t
        nought_t = en.nought_t
        language = 'English'
        pg.display.set_caption(en.game_name_t)
    print(nought_t, cross_t)

def change_resolution():
    '''
    Функция смены разрешения
    '''
    global display_height
    global display_width
    global screen
    global zero
    global cross
    time.sleep(0.1)
    if display_height < pg.display.set_mode((0, 0), pg.FULLSCREEN).get_height():
        if display_height == 720:
            display_width = 1920
            display_height = 1080
        elif display_height == 1080:
            display_width = 2560
            display_height = 1440
        elif display_height == 1440:
            display_width = 3840
            display_height = 2160
        elif display_height == 2160:
            display_height = 720
            display_width = 1280
    else:
        display_height = 720
        display_width = 1280
    cross = pg.transform.scale(pg.image.load('images/cross.png'), (display_height * 0.32, display_height * 0.32))
    zero = pg.transform.scale(pg.image.load('images/zero.png'), (display_height * 0.32, display_height * 0.32))
    screen = pg.display.set_mode((display_width, display_height))
    settings_menu()


def fulsize():
    '''
    Функция перехода в полноэкранный режим
    '''
    global display_height
    global display_width
    global screen
    global zero
    global cross
    time.sleep(0.1)
    pg.display.set_mode((0, 0), pg.FULLSCREEN)
    cross = pg.transform.scale(pg.image.load('images/cross.png'), (screen.get_height() * 0.32, screen.get_height() * 0.32))
    zero = pg.transform.scale(pg.image.load('images/zero.png'), (screen.get_height() * 0.32, screen.get_height() * 0.32))
    display_width = screen.get_width()
    display_height = screen.get_height()
    print(display_height)
    settings_menu()


def game_menu():
    '''
    Функция вызывающая меню игры
    '''
    global first_step
    global figure_now
    global printed_cross
    global printed_zeros
    global is_victory
    global last_winner
    global winner
    global start_game
    menu_background = pg.transform.scale(pg.image.load('animation/22.png'), (display_width, display_height))
    printed_zeros = []
    printed_cross = []
    figure_now = cross
    first_step = True
    if winner == nought_t:
        last_winner = nought_t
    elif winner == cross_t:
        last_winner = cross_t
    winner = None
    menu_is_showing = True
    start_button = Menu_button(display_width // 5, display_height // 20, (177, 177, 177, 127), (177, 177, 177, 200))
    settings_button = Menu_button(display_width // 5, display_height // 20, (177, 177, 177, 127), (177, 177, 177, 200))
    quit_button = Menu_button(display_width // 5, display_height // 20, (177, 177, 177, 127), (177, 177, 177, 200))
    if start_game:
        for i in range(1, 23):
            backimage = pg.transform.scale(pg.image.load(f'animation/{i}.png'), (display_width, display_height))
            screen.blit(backimage, (0, 0))
            pg.display.update()
            start_game = False
        mainClock.tick(FPS)
    while menu_is_showing:
        screen.blit(menu_background, (0, 0))
        start_button.draw_button(display_width - display_width // 5,
                           display_height // 4, play_t, screen, game_process)
        settings_button.draw_button(display_width - display_width // 5,
                           display_height // 4 + display_height // 10, settings_t, screen, settings_menu)
        quit_button.draw_button(display_width - display_width // 5,
                           display_height // 4 + 3 * display_height // 10, quit_t, screen, quit_game)
        for event in pg.event.get():
            
            if event.type == pg.QUIT:
                quit_game()
        pg.display.update()
        mainClock.tick(FPS)


def game_process():
    '''
    Функция вызывающая игровой процесс
    '''
    game_running = True
    global printed_cross
    global printed_zeros
    global last_winner
    global winner

    button1 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 1)
    button2 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 2)
    button3 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 3)
    button4 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 4)
    button5 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 5)
    button6 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 6)
    button7 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 7)
    button8 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 8)
    button9 = Game_button(display_height * 0.32, display_height * 0.32, (177, 177, 177, 127), (177, 177, 177, 200), 9)
    back_button = Menu_button(display_width // 5, display_height // 20, (177, 177, 177, 127), (177, 177, 177, 200))
    new_game = Menu_button(display_width // 5, display_height // 20, (177, 177, 177, 127), (177, 177, 177, 200))
    text_box1 = Information_block(display_width * 0.44, display_height // 12)
    text_box2 = Information_block(display_width * 0.44, display_height // 12)
    text_box3 = Information_block(display_width * 0.44, display_height // 12)
    while game_running:
        if ((1 in printed_cross and 2 in printed_cross and 3 in printed_cross) or 
            (4 in printed_cross and 5 in printed_cross and 6 in printed_cross) or
            (7 in printed_cross and 8 in printed_cross and 9 in printed_cross) or
            (1 in printed_cross and 4 in printed_cross and 7 in printed_cross) or
            (2 in printed_cross and 5 in printed_cross and 8 in printed_cross) or
            (3 in printed_cross and 6 in printed_cross and 9 in printed_cross) or
            (1 in printed_cross and 5 in printed_cross and 9 in printed_cross) or
            (3 in printed_cross and 5 in printed_cross and 7 in printed_cross)):
            winner = cross_t
        elif ((1 in printed_zeros and 2 in printed_zeros and 3 in printed_zeros) or 
            (4 in printed_zeros and 5 in printed_zeros and 6 in printed_zeros) or
            (7 in printed_zeros and 8 in printed_zeros and 9 in printed_zeros) or
            (1 in printed_zeros and 4 in printed_zeros and 7 in printed_zeros) or
            (2 in printed_zeros and 5 in printed_zeros and 8 in printed_zeros) or
            (3 in printed_zeros and 6 in printed_zeros and 9 in printed_zeros) or
            (1 in printed_zeros and 5 in printed_zeros and 9 in printed_zeros) or
            (3 in printed_zeros and 5 in printed_zeros and 7 in printed_zeros)):
            winner = nought_t
        screen.blit(background, (0, 0))
        button1.draw_button(display_height // 144,
                            display_height // 144)
        button2.draw_button(display_height // 144 * 2 + display_height * 0.32,
                            display_height // 144)
        button3.draw_button(display_height // 144 * 3 + 2 * (display_height * 0.32),
                            display_height // 144)
        button4.draw_button(display_height // 144,
                            display_height // 144 * 2 + display_height * 0.32)
        button5.draw_button(display_height // 144 * 2 + display_height * 0.32,
                            display_height // 144 * 2 + display_height * 0.32)
        button6.draw_button(display_height // 144 * 3 + 2 * (display_height * 0.32),
                            display_height // 144 * 2 + display_height * 0.32)
        button7.draw_button(display_height // 144,
                            display_height // 144 * 3 + 2 * display_height * 0.32)
        button8.draw_button(display_height // 144 * 2 + display_height * 0.32,
                            display_height // 144 * 3 + 2 * display_height * 0.32)
        button9.draw_button(display_height // 144 * 3+ 2 * (display_height * 0.32),
                            display_height // 144 * 3 + 2 * display_height * 0.32)
        back_button.draw_button(display_width - display_width // 5,
                                display_height // 144 * 3 + 3 * display_height * 0.32 - display_height // 20,
                                back_t, screen, game_menu)
        new_game.draw_button(display_width - display_width // 5,
                                display_height // 144 * 3 + 3 * display_height * 0.32 - 3 * display_height // 20,
                                restart_t, screen, restart)
        if figure_now == cross:
            text_box1.print_box(display_height // 144 * 4 + 3 * (display_height * 0.32),
                                display_height // 144, cross__turn_t)
        else:
            text_box1.print_box(display_height // 144 * 4 + 3 * (display_height * 0.32),
                                display_height // 144, nought_turn_t)            
        text_box2.print_box(display_height // 144 * 4 + 3 * (display_height * 0.32),
        
                            (display_height // 144 * 2 + display_height * 0.32) // 4, f"{last_winner_t}: {last_winner}")
        if winner is not None:
            text_box3.print_box(display_height // 144 * 4 + 3 * (display_height * 0.32),
            
                                (display_height // 144 * 2 + display_height * 0.32) // 2, f"{winner_t}: {winner}")
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()
        pg.display.update()
        mainClock.tick(FPS)


def settings_menu():
    '''
    Функция вызывающая настройки игры
    '''
    settings = True
    global language
    text_box_1 = Information_block(display_width * 0.5, display_height // 4)
    text_box_2 = Information_block(display_width * 0.3, display_height // 7)
    text_box_3 = Information_block(display_width * 0.3, display_height // 7)
    switch1 = Settings_button(display_width * 0.3, display_height // 7, (177, 177, 177, 127), (177, 177, 177, 200))
    switch2 = Settings_button(display_width * 0.3, display_height // 7, (177, 177, 177, 127), (177, 177, 177, 200))
    switch3 = Settings_button(display_width * 0.4, display_height // 7, (177, 177, 177, 127), (177, 177, 177, 200))
    switch4 = Settings_button(display_width * 0.4, display_height // 7, (177, 177, 177, 127), (177, 177, 177, 200))
    while settings:
        current_resolution = f'  {display_width}x{display_height}'
        screen.blit(background, (0, 0))
        text_box_1.print_box(display_width * 0.25, display_height // 100, settings_t)
        text_box_2.print_box(display_width // 6, display_height // 4, resolution_t)
        text_box_3.print_box(display_width - display_width * 0.3 - display_width // 6, display_height // 4, language_t)
        switch1.draw_button(display_width // 6 - display_width * 0.3 // 9, display_height * 0.4, 
        current_resolution, screen, change_resolution)
        switch2.draw_button(display_width - display_width * 0.3 - display_width // 6 - display_width * 0.3 // 9, display_height * 0.4, language, screen, language_change) 
        switch3.draw_button(display_width * 0.25, display_height * 0.8, back_t, screen, game_menu) 
        switch4.draw_button(display_width * 0.25, display_height * 0.6, 
        fulsize_t, screen, fulsize)     
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()
        pg.display.update()
        mainClock.tick(FPS)


game_menu()