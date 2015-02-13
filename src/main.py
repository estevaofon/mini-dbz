#!/usr/bin/python
import sys
import time
import ntpath
import pygame
from spriteanimation import SpriteAnimation
from npc import NPC
from player import Player
#import pygame._view

pygame.init()
pygame.joystick.init()
for x in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(x)
    joystick.init()
scenery1_image = "resources/imagens/scenarios/Wasteland-2.jpg"
scenery2_image = "resources/imagens/scenarios/namek-3d-2.jpg"
scenery3_image = "resources/imagens/scenarios/trunks-future-2.png"
scenery4_image = "resources/imagens/scenarios/arena-2-2.gif"
scenery4 = pygame.image.load(scenery4_image)
background = scenery4
resolution = background.get_size()
width, height = resolution
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN, 32)
# screen = pygame.display.set_mode(resolution)
scenery1 = pygame.image.load(scenery1_image).convert()
scenery2 = pygame.image.load(scenery2_image).convert()
scenery3 = pygame.image.load(scenery3_image).convert()
scenery4 = scenery4.convert_alpha()
scenery = [scenery1, scenery2,
           scenery3, scenery4]
menu_image = "resources/imagens/openning/background/goku-vs-vegeta-2.jpg"
goku100x100 = "resources/imagens/player/goku/ss4/goku100x100.png"
vegeta100x100 = "resources/imagens/player/vegeta/vegeta100x100.png"
trunks100x100 = "resources/imagens/player/trunks/trunks100x100.png"
frieza100x100 = "resources/imagens/player/frieza/frieza100x100.png"
gohan100x100 = "resources/imagens/player/gohan/gohan100x100.png"
photos3x4 = [pygame.image.load(goku100x100), pygame.image.load(vegeta100x100),
             pygame.image.load(gohan100x100), pygame.image.load(trunks100x100),
             pygame.image.load(frieza100x100)]
ch = pygame.transform.scale(photos3x4[0], (100, 100))
background_openning = pygame.image.load(menu_image).convert()
scene1 = pygame.transform.scale(scenery[0], (500, 300))
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)
game_state = 0  # Menu
previous_game_state = 0
s0Option = range(5)
is0 = 0
s1Option = range(5)
is1 = 0
s3Option = range(7)
is3 = 0
s4Option = range(2)
is4 = 0
s5Option = range(3)
is5 = 0
sc = 0
sc1 = 0
sc2 = 1
sg = 0
df = 2
volume = 0.5
vs_pc = False
song1 = 'resources/sounds/sparking.mp3'
song3 = 'resources/sounds/cha-la.mp3'
song = [song1, song3]
level = ['easy', 'Medium', 'Hard', 'Super Sayajin']
xp1 = 400
yp1 = 400
xp1d = xp1
yp1d = yp1
xp2 = 550
yp2 = 400
xp2d = xp2
yp2d = yp2
played_once = False
characters = ['goku', 'vegeta', 'gohan', 'trunks', 'frieza']
player1 = Player(initial_action="down", player_id=1)
player2 = Player(initial_action="down", player_id=2)
player_pc = NPC(initial_action="down", player_id=0)
power1 = SpriteAnimation(initial_action="void")
power2 = SpriteAnimation(initial_action="void")
power3 = SpriteAnimation(initial_action="void")
power_dispute = SpriteAnimation(initial_action="void")
power_dispute2 = SpriteAnimation(initial_action="void")
effects = SpriteAnimation(initial_action="void")
effects2 = SpriteAnimation(initial_action="void")
player1.load_power(power1)
player1.load_power(power_dispute)
player2.load_power(power_dispute2)
player1.load_power(effects)
player2.load_power(effects2)
player2.load_power(power2)
player_pc.load_power(power3)
player_pc.load_character(characters[1])
player2.load_character(characters[1])
pc_players = [player_pc]
human_players = [player1, player2]
player_pc.is_pc = True
powers = [power1, power2, power3]
delta = 13  # speed of the game
player2.facing_right = False
player2.x = 850
player2.y = 350
player_pc.x = 850
player_pc.y = 350
player_pc.xp = 0
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
move_one = True
time1 = 0
time2 = 0
time3 = 0
default_axis = 0


def restart():
    """
    Restarts the game
    """
    global vs_pc
    if vs_pc:
        player_pc.action = "down"
        player1.action = "down"
        player1.pos = 1
        player_pc.pos = 1
        player1.movex, player1.movey = 0, 0
        player_pc.movex, player_pc.movey = 0, 0
        player1.facing_right = True
        player_pc.facing_right = False
        player1.x = 250
        player1.y = 350
        player_pc.x = 850
        player_pc.y = 350
        player1.hp = 400
        player2.hp = 400
        player2.xp = 50
        player_pc.hp = 400
        player1.xp = 50
        player_pc.xp = 0
        player1.timing_dispute = False
    else:
        player2.action = "down"
        player1.action = "down"
        player1.pos = 1
        player2.pos = 1
        player1.movex, player1.movey = 0, 0
        player2.movex, player2.movey = 0, 0
        player1.facing_right = True
        player2.facing_right = False
        player2.timing_dispute = False
        player1.kame_cont = 0
        player2.kame_cont = 0
        player1.x = 250
        player1.y = 350
        player2.x = 850
        player2.y = 350
        player1.hp = 400
        player2.hp = 400
        player1.xp = 50
        player2.xp = 50


def show_splashscreen():
    """
    Show the splash screen.
    This is called once when the game is first started.
    """
    global volume
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.mixer.music.load('resources/sounds/splash.ogg')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)
    white = 250, 250, 250
    screen.fill(white)
    # Slowly fade the splash screen image from white to opaque.
    splash = pygame.image.load(
        "resources/imagens/openning/splash/estevaosplash.png").convert()
    for i in range(25):
        splash.set_alpha(i)
        screen.blit(splash, (90, 50))
        pygame.display.update()
        pygame.time.wait(100)

    pygame.mixer.fadeout(2000)
    screen.blit(splash, (90, 50))
    pygame.display.update()
    pygame.time.wait(1500)
    global game_state
    game_state = 0


def show_video():
    """
    Show the opening video
    """
    initial = time.time()
    load_music(song[0])
    global screen
    global time3
    pygame.init()
    # pygame.mixer.quit()
    screen.fill((0, 0, 0))
    pygame.display.update()
    movie = pygame.movie.Movie("resources/videos/goku-vs-vegeta.mpg")
    w, h = movie.get_size()
    w = int(w * 1.3 + 0.5)
    h = int(h * 1.3 + 0.5)
    msize = (w + 745, h + 200)
    movie.set_display(screen, pygame.Rect((0, 80), msize))
    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    movie.play()
    while movie.get_busy():
        if abs(time.time() - initial) >= 30:
            movie.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # break
                    time3 = time.time()*1000
                    movie.stop()
                if event.key == pygame.K_ESCAPE:
                    time3 = time.time()*1000
                    movie.stop()
                pygame.time.set_timer(pygame.USEREVENT, 0)
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if button:
                    time3 = time.time()*1000
                    movie.stop()


def open_menu():
    """
    Main Menu
    """
    global game_state
    global previous_game_state
    global vs_pc
    global time1
    global time3
    global is0
    global move_one
    global default_axis
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        buttons = joystick.get_numbuttons()
        axis = joystick.get_axis(1)
        axis = round(axis, 3)
        if axis != 1 and axis != -1:
            default_axis = axis
        if axis > default_axis and move_one:
            is0 += 1
            time1 = time.time()
            move_one = False
        if axis < default_axis and move_one:
            is0 += -1
            time1 = time.time()
            move_one = False
        if is0 < 0:
            is0 = 0
        if is0 > (len(s0Option)-1):
            is0 = 4
        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                time3 = time.time()*1000
                if s0Option[is0] == 0:
                    player2.player_id = 2
                    game_state = 5
                    vs_pc = True
                    restart()
                if s0Option[is0] == 1:
                    game_state = 5
                    restart()
                    vs_pc = False
                    player2.player_id = 2
                if s0Option[is0] == 2:
                    previous_game_state = 0
                    game_state = 3
                if s0Option[is0] == 3:
                    previous_game_state = 0
                    game_state = 6
                if s0Option[is0] == 4:
                    pygame.quit()
                    sys.exit()

    if time.time()*1000-time1*1000 >200:
        move_one = True


    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 65)
    bold_font = pygame.font.SysFont("monospace", 75, bold=True)
    player_vs_pc = my_font.render("Play Vs PC", 1, WHITE)
    player_vs_player = my_font.render("Play Vs Player2", 1, WHITE)
    options_word = my_font.render("Options", 1, WHITE)
    credits_word = my_font.render("Credits", 1, WHITE)
    quit_word = my_font.render("Quit", 1, WHITE)

    if s0Option[is0] == 0:
        player_vs_pc = bold_font.render("Play Vs Pc", 1, WHITE)
    if s0Option[is0] == 1:
        player_vs_player = bold_font.render("Play Vs Player2", 1, WHITE)
    if s0Option[is0] == 2:
        options_word = bold_font.render("Options", 1, WHITE)
    if s0Option[is0] == 3:
        credits_word = bold_font.render("Credits", 1, WHITE)
    if s0Option[is0] == 4:
        quit_word = bold_font.render("Quit", 1, WHITE)

    screen.blit(player_vs_pc, (310, 250))
    screen.blit(player_vs_player, (310, 320))
    screen.blit(options_word, (310, 390))
    screen.blit(credits_word, (310, 460))
    screen.blit(quit_word, (310, 530))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                if s0Option[is0] == 0:
                    player2.player_id = 2
                    game_state = 5
                    vs_pc = True
                    restart()
                if s0Option[is0] == 1:
                    game_state = 5
                    restart()
                    vs_pc = False
                    player2.player_id = 2
                if s0Option[is0] == 2:
                    previous_game_state = 0
                    game_state = 3
                if s0Option[is0] == 3:
                    previous_game_state = 0
                    game_state = 6
                if s0Option[is0] == 4:
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_DOWN:
                if s0Option[is0] < s0Option[-1]:
                    is0 += 1
            if event.key == pygame.K_UP:
                if s0Option[is0] > s0Option[0]:
                    is0 -= 1


def options():
    """
    Option Menu
    """
    global game_state
    global delta
    global previous_game_state
    global volume
    global song
    global sg
    global df
    global level
    global played_once
    global move_one
    global time1
    global time3
    global is3
    global defaul_axis

    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        axes = joystick.get_numaxes()
        buttons = joystick.get_numbuttons()
        for i in range(axes):
            axis = joystick.get_axis(i)
            axis = round(axis, 3)
            if i == 0:
                if axis > default_axis and move_one:
                    if s3Option[is3] == 0:
                        delta += 1
                    if s3Option[is3] == 2:
                        if volume < 0.9:
                            volume += 0.1
                            pygame.mixer.music.set_volume(volume)
                    if s3Option[is3] == 1:
                        if sg == len(song) - 1:
                            sg -= 1
                        sg += 1
                        load_music(song[sg])
                    if s3Option[is3] == 3:
                        if df < len(level) - 1:
                            df += 1
                    time1 = time.time()
                    move_one = False
                if axis < default_axis and move_one:
                    if s3Option[is3] == 0:
                        delta -= 1
                    if s3Option[is3] == 2:
                        if volume > 0.1:
                            volume -= 0.1
                            pygame.mixer.music.set_volume(volume)
                        if volume < 0.2:
                            volume = 0
                            pygame.mixer.music.set_volume(volume)
                    if s3Option[is3] == 1:
                        if sg == 0:
                            sg = len(song)
                        sg -= 1
                        load_music(song[sg])
                    if s3Option[is3] == 3:
                        if df > 0:
                            df -= 1
                    time1 = time.time()
                    move_one = False

            if i == 1:
                if axis > default_axis and move_one:
                    if s3Option[is3] < s3Option[-1]:
                        is3 += 1
                        time1 = time.time()
                        move_one = False
                if axis < default_axis and move_one:
                    if s3Option[is3] > s3Option[0]:
                        is3 -= 1
                        time1 = time.time()
                        move_one = False
        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                time3 = time.time()*1000
                if s3Option[is3] == 5:
                    if played_once:
                        game_state = 2
                    else:
                        pass
                if s3Option[is3] == 6:
                    game_state = previous_game_state
                if s3Option[is3] == 4:
                    game_state = 7
                if i == 8:
                    game_state = previous_game_state

    if time.time()*1000-time1*1000 >200:
        move_one = True
    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 45)
    bold_font = pygame.font.SysFont("monospace", 55, bold=True)
    player_vs_player = my_font.render("Game Speed " + str(delta), 1, WHITE)
    player_vs_pc = my_font.render("Music Volume " + str(volume * 100), 1, WHITE)
    options_word = my_font.render("Resume", 1, WHITE)
    music = my_font.render("Music", 1, WHITE)
    back = my_font.render("Back", 1, WHITE)
    mode = my_font.render("Mode", 1, WHITE)
    difficult = my_font.render(level[df], 1, WHITE)
    keyboard_word = my_font.render("Keyboard", 1, WHITE)
    title = my_font.render(ntpath.basename(song[sg]), 1, WHITE)

    if s3Option[is3] == 0:
        player_vs_player = bold_font.render(
            "Game Speed " + str(delta), 1, WHITE)
    if s3Option[is3] == 2:
        player_vs_pc = bold_font.render(
            "Music Volume " + str(volume * 100), 1, WHITE)
    if s3Option[is3] == 3:
        mode = bold_font.render("Mode", 1, WHITE)
        difficult = bold_font.render(level[df], 1, WHITE)
    if s3Option[is3] == 4:
        keyboard_word = bold_font.render("Keyboard", 1, WHITE)
    if s3Option[is3] == 5:
        options_word = bold_font.render("Resume", 1, WHITE)
    if s3Option[is3] == 6:
        back = bold_font.render("Back", 1, WHITE)
    if s3Option[is3] == 1:
        music = bold_font.render("Music", 1, WHITE)
        title = bold_font.render(ntpath.basename(song[sg]), 1, WHITE)
    screen.blit(player_vs_player, (340, 250))
    screen.blit(player_vs_pc, (340, 350))
    screen.blit(mode, (340, 400))
    screen.blit(difficult, (540, 400))
    screen.blit(music, (340, 300))
    screen.blit(title, (540, 300))
    screen.blit(keyboard_word, (340, 450))
    screen.blit(options_word, (340, 500))
    screen.blit(back, (340, 550))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                if s3Option[is3] == 5:
                    if played_once:
                        game_state = 2
                    else:
                        pass
                if s3Option[is3] == 6:
                    game_state = previous_game_state
                if s3Option[is3] == 4:
                    game_state = 7
            if event.key == pygame.K_DOWN:
                if s3Option[is3] < s3Option[-1]:
                    is3 += 1
            if event.key == pygame.K_UP:
                if s3Option[is3] > s3Option[0]:
                    is3 -= 1
            if event.key == pygame.K_RIGHT:
                if s3Option[is3] == 0:
                    delta += 1
                if s3Option[is3] == 2:
                    if volume < 0.9:
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)
                if s3Option[is3] == 1:
                    if sg == len(song) - 1:
                        sg -= 1
                    sg += 1
                    load_music(song[sg])
                if s3Option[is3] == 3:
                    if df < len(level) - 1:
                        df += 1
            if event.key == pygame.K_LEFT:
                if s3Option[is3] == 0:
                    delta -= 1
                if s3Option[is3] == 2:
                    if volume > 0.1:
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)
                    if volume < 0.2:
                        volume = 0
                        pygame.mixer.music.set_volume(volume)
                if s3Option[is3] == 1:
                    if sg == 0:
                        sg = len(song)
                    sg -= 1
                    load_music(song[sg])
                if s3Option[is3] == 3:
                    if df > 0:
                        df -= 1
    if df == 0:
        player_pc.kameham_ms = 450
        player_pc.punch_ms = 200
        player_pc.kame_cont = 15
        player_pc.teleport_boolean = False
    if df == 1:
        player_pc.kameham_ms = 160
        player_pc.punch_ms = 90
        player_pc.kame_cont = 22
        player_pc.teleport_boolean = False
    if df == 2:
        player_pc.kameham_ms = 160
        player_pc.punch_ms = 90
        player_pc.kame_cont = 22
        player_pc.teleport_boolean = True
    if df == 3:
        player_pc.kameham_ms = 70
        player_pc.punch_ms = 70
        player_pc.kame_cont = 23
        player_pc.teleport_boolean = True


def game_credits():
    """
    Credits screen
    """
    global game_state
    global previous_game_state
    global sg
    global time3
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        buttons = joystick.get_numbuttons()
        axis = joystick.get_axis(1)
        axis = round(axis, 3)
        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                game_state = previous_game_state
                time3 = time.time()*1000
    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 45)
    bold_font = pygame.font.SysFont("monospace", 55, bold=True)
    game_developer = bold_font.render("Game Developer", 1, WHITE)
    estevao = my_font.render("Estevao Fonseca", 1, WHITE)
    supporters = bold_font.render("Special Thanks", 1, WHITE)
    bru = my_font.render("Bruno Fonseca", 1, WHITE)
    hel = my_font.render("Helena A. Lisboa", 1, WHITE)
    art_work = bold_font.render("Art Work", 1, WHITE)
    akira = my_font.render("Akira Torayama", 1, WHITE)
    thiago = my_font.render("Thiago Sfredo", 1, WHITE)
    artist1 = my_font.render("ANGI1997", 1, WHITE)
    artist2 = my_font.render("Nightmare", 1, WHITE)
    artist3 = my_font.render("AidinBey", 1, WHITE)
    artist4 = my_font.render("Grim", 1, WHITE)
    artist5 = my_font.render("Hyperlon", 1, WHITE)

    screen.blit(game_developer, (200, 150))
    screen.blit(estevao, (200, 210))
    screen.blit(supporters, (200, 270))
    screen.blit(bru, (200, 330))
    screen.blit(hel, (200, 390))
    screen.blit(thiago, (200, 450))
    screen.blit(art_work, (740, 150))
    screen.blit(akira, (740, 210))
    screen.blit(artist1, (740, 270))
    screen.blit(artist2, (740, 330))
    screen.blit(artist3, (740, 390))
    screen.blit(artist4, (740, 450))
    screen.blit(artist5, (740, 510))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state


def keyboard():
    """
    Screen showing the Keys used to play
    """
    global game_state
    global previous_game_state
    global sg
    global time3
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        buttons = joystick.get_numbuttons()
        axis = joystick.get_axis(1)
        axis = round(axis, 3)
        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                game_state = previous_game_state
                time3 = time.time()*1000

    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 45, bold=True)
    bold_font = pygame.font.SysFont("monospace", 55, bold=True)
    player1_word = bold_font.render("Player 1", 1, WHITE)
    left = my_font.render("a - Left", 1, YELLOW)
    right = my_font.render("d - Right", 1, YELLOW)
    up = my_font.render("w - Up", 1, YELLOW)
    down = my_font.render("s - Down", 1, YELLOW)
    kameham = my_font.render("u - kameham", 1, YELLOW)
    punch = my_font.render("i - Punch", 1, YELLOW)
    kick = my_font.render("o - Kick", 1, YELLOW)
    defend = my_font.render("p - Defend", 1, YELLOW)
    load = my_font.render("j - Load", 1, YELLOW)
    teleport = my_font.render("k - Teleport", 1, YELLOW)

    player2_word = bold_font.render("Player 2", 1, WHITE)
    left2 = my_font.render("left arrow - Left", 1, YELLOW)
    right2 = my_font.render("right arrow - Right", 1, YELLOW)
    up2 = my_font.render("up arrow - Up", 1, YELLOW)
    down2 = my_font.render("down arrow - Down", 1, YELLOW)
    kameham2 = my_font.render("7 - kameham", 1, YELLOW)
    punch2 = my_font.render("8 - Punch", 1, YELLOW)
    kick2 = my_font.render("9 - Kick", 1, YELLOW)
    defend2 = my_font.render("6 - Defend", 1, YELLOW)
    load2 = my_font.render("5 - Load", 1, YELLOW)
    back = bold_font.render("OK", 1, WHITE)
    teleport2 = my_font.render("6 - Teleport", 1, YELLOW)

    screen.blit(player1_word, (300, 100))
    screen.blit(left, (300, 180))
    screen.blit(right, (300, 230))
    screen.blit(up, (300, 280))
    screen.blit(down, (300, 330))
    screen.blit(kameham, (300, 380))
    screen.blit(punch, (300, 430))
    screen.blit(kick, (300, 480))
    screen.blit(defend, (300, 530))
    screen.blit(load, (300, 580))
    screen.blit(teleport, (300, 630))

    screen.blit(player2_word, (680, 100))
    screen.blit(left2, (680, 180))
    screen.blit(right2, (680, 230))
    screen.blit(up2, (680, 280))
    screen.blit(down2, (680, 330))
    screen.blit(kameham2, (680, 380))
    screen.blit(punch2, (680, 430))
    screen.blit(kick2, (680, 480))
    screen.blit(defend2, (680, 530))
    screen.blit(load2, (680, 580))
    screen.blit(teleport2, (680, 630))
    screen.blit(back, (780, 680))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                game_state = previous_game_state


def choose_character():
    """
    Choose character screen
    """
    global game_state
    global previous_game_state
    global sc1
    global sc2
    global characters
    global ch
    global xp1
    global yp1
    global xp1d
    global yp1d
    global xp2
    global yp2
    global xp2d
    global yp2d
    global time1
    global time3
    global move_one
    global photos3x4
    global default_axis

    for i in range(pygame.joystick.get_count()):
        joynumber = i
        joystick = pygame.joystick.Joystick(i)
        axes = joystick.get_numaxes()
        buttons = joystick.get_numbuttons()
        for i in range(axes):
            axis = joystick.get_axis(i)
            axis = round(axis, 3)
            if i == 0 and joynumber == 1:
                if axis > default_axis and move_one:
                    # right
                    xp2 += 150
                    sc2 += 1
                    time1 = time.time()
                    move_one = False
                if axis < default_axis and move_one:
                    # left
                    xp2 -= 150
                    sc2 -= 1
                    time1 = time.time()
                    move_one = False
            if sc2 > len(photos3x4) - 1:
                sc2 = len(photos3x4) - 1
                xp2 = xp1d + 600
            if sc2 < 0:
                sc2 = 0
                xp2 = xp1d
            if i == 0 and joynumber == 0:
                if axis > default_axis and move_one:
                    # right
                    xp1 += 150
                    sc1 += 1
                    time1 = time.time()
                    move_one = False
                if axis < default_axis and move_one:
                    # left
                    xp1 -= 150
                    sc1 -= 1
                    time1 = time.time()
                    move_one = False
            if sc1 > len(photos3x4) - 1:
                sc1 = len(photos3x4) - 1
                xp1 = xp1d + 600
            if sc1 < 0:
                sc1 = 0
                xp1 = xp1d

        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                game_state = 4
                if vs_pc:
                    player1.load_character(characters[sc1])
                    player_pc.load_character(characters[sc2])
                else:
                    player1.load_character(characters[sc1])
                    player2.load_character(characters[sc2])
                time3 = time.time()*1000
                if i == 8:
                    game_state = previous_game_state

    if time.time()*1000-time1*1000 >200:
        move_one = True


    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    bold_font = pygame.font.SysFont("monospace", 65, bold=True)

    player_vs_player = bold_font.render("P1", 1, RED)
    if vs_pc:
        player_vs_player2 = bold_font.render("PC", 1, BLUE)
    else:
        player_vs_player2 = bold_font.render("P2", 1, BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                game_state = 4
                if vs_pc:
                    player1.load_character(characters[sc1])
                    player_pc.load_character(characters[sc2])
                else:
                    player1.load_character(characters[sc1])
                    player2.load_character(characters[sc2])
            if event.key == pygame.K_d:
                if sc1 >= len(photos3x4) - 1:
                    sc1 = 0
                    xp1 = xp1d
                elif 0 <= sc1 < len(photos3x4):
                    xp1 += 150
                    sc1 += 1
            if event.key == pygame.K_RIGHT:
                if sc2 >= len(photos3x4) - 1:
                    sc2 = 0
                    xp2 = xp1d
                elif 0 <= sc2 < len(photos3x4):
                    xp2 += 150
                    sc2 += 1

            if event.key == pygame.K_a:
                if sc1 <= 0:
                    sc1 = len(photos3x4) - 1
                    xp1 = xp1d + 300
                elif 0 <= sc1 < len(photos3x4):
                    xp1 -= 150
                    sc1 -= 1

            if event.key == pygame.K_LEFT:
                if sc2 <= 0:
                    sc2 = len(photos3x4) - 1
                    xp2 = xp1d + 300
                elif 0 <= sc2 < len(photos3x4):
                    xp2 -= 150
                    sc2 -= 1

    x = 350
    y = 350
    dx = 0
    for picture in photos3x4:
        ch = pygame.transform.scale(picture, (150, 150))
        screen.blit(ch, (x + dx, y))
        dx += 150
    screen.blit(player_vs_player, (xp1, yp1))
    screen.blit(player_vs_player2, (xp2, yp2))
    pygame.display.update()


def choose_scenery():
    """
    Choose scenery screen
    """
    global game_state
    global previous_game_state
    global sc
    global background
    global scenery
    global scene1
    global time1
    global time3
    global move_one
    global default_axis
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        axes = joystick.get_numaxes()
        buttons = joystick.get_numbuttons()
        for i in range(axes):
            axis = joystick.get_axis(i)
            axis = round(axis, 3)
            if axis > default_axis and move_one:
                # right
                if sc == len(scenery) - 1:
                    sc = -1
                sc += 1
                scene1 = pygame.transform.scale(scenery[sc], (500, 300))
                time1 = time.time()
                move_one = False
            if axis < default_axis and move_one:
                # left
                if sc == 0:
                    sc = len(scenery)
                sc -= 1
                scene1 = pygame.transform.scale(scenery[sc], (500, 300))
                time1 = time.time()
                move_one = False
        for i in range(buttons):
            if time.time()*1000 - time3 > 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                game_state = 2
                background = scenery[sc]
    if time.time()*1000-time1*1000 > 200:
        move_one = True
    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    bold_font = pygame.font.SysFont("monospace", 55, bold=True)

    player_vs_player = bold_font.render(">", 1, WHITE)
    player_vs_player2 = bold_font.render("<", 1, WHITE)
    screen.blit(player_vs_player, (865, 420))
    screen.blit(player_vs_player2, (300, 420))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = previous_game_state
            if event.key == pygame.K_RETURN:
                game_state = 2
                background = scenery[sc]
            if event.key == pygame.K_RIGHT:
                if sc == len(scenery) - 1:
                    sc = -1
                sc += 1
                scene1 = pygame.transform.scale(scenery[sc], (500, 300))
            if event.key == pygame.K_LEFT:
                if sc == 0:
                    sc = len(scenery)
                sc -= 1
                scene1 = pygame.transform.scale(scenery[sc], (500, 300))
    screen.blit(scene1, (350, 300))
    pygame.display.update()


def load_menu():
    """
    Menu during the playing game
    """
    global is1
    global move_one
    global time1
    global time2
    global time3
    global game_state
    global previous_game_state
    global default_axis
    for i in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(i)
        buttons = joystick.get_numbuttons()
        axis = joystick.get_axis(1)
        axis = round(axis, 3)
        if axis > default_axis and move_one:
            is1 += 1
            time1 = time.time()
            move_one = False
        if axis < default_axis and move_one:
            is1 += -1
            time1 = time.time()
            move_one = False
        for i in range(buttons):
            if time.time()*1000 - time3> 300:
                button = joystick.get_button(i)
            else:
                button = 0
            if button:
                if s1Option[is1] == 0:
                    game_state = 0
                    time3 = time.time()*1000
                if s1Option[is1] == 1:
                    game_state = 2
                if s1Option[is1] == 2:
                    game_state = 3
                    previous_game_state = 1
                    time3 = time.time()*1000
                if s1Option[is1] == 3:
                    restart()
                    game_state = 2
                if s1Option[is1] == 4:
                    pygame.quit()
                    sys.exit()


    if time.time()*1000-time1*1000 > 200:
        move_one = True

    black = 0, 0, 0
    screen.fill(black)
    screen.blit(background_openning, (-70, 0))
    my_font = pygame.font.SysFont("monospace", 45)
    bold_font = pygame.font.SysFont("monospace", 55, bold=True)
    initial_screen = my_font.render("Initial Screen", 1, WHITE)
    player_vs_player = my_font.render("Resume", 1, WHITE)
    player_vs_pc = my_font.render("Options", 1, WHITE)
    restart_word = my_font.render("Restart", 1, WHITE)
    quit_word = my_font.render("Quit", 1, WHITE)
    is1 = int(round(is1))
    if is1 < 0:
        is1 = 0
    if is1 > (len(s1Option)-1):
        is1 = 4

    if s1Option[is1] == 0:
        initial_screen = bold_font.render("Initial Screen", 1, WHITE)
    if s1Option[is1] == 1:
        player_vs_player = bold_font.render("Resume", 1, WHITE)
    if s1Option[is1] == 2:
        player_vs_pc = bold_font.render("Options", 1, WHITE)
    if s1Option[is1] == 3:
        restart_word = bold_font.render("Restart", 1, WHITE)
    if s1Option[is1] == 4:
        quit_word = bold_font.render("Quit", 1, WHITE)
    screen.blit(initial_screen, (340, 250))
    screen.blit(player_vs_player, (340, 305))
    screen.blit(player_vs_pc, (340, 360))
    screen.blit(restart_word, (340, 415))
    screen.blit(quit_word, (340, 470))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = 2
                previous_game_state = 1
            if event.key == pygame.K_RETURN:
                if s1Option[is1] == 0:
                    game_state = 0
                if s1Option[is1] == 1:
                    game_state = 2
                if s1Option[is1] == 2:
                    game_state = 3
                    previous_game_state = 1
                if s1Option[is1] == 3:
                    restart()
                    game_state = 2
                if s1Option[is1] == 4:
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_DOWN:
                if s1Option[is1] < s1Option[-1]:
                    is1 += 1
            if event.key == pygame.K_UP:
                if s1Option[is1] > s1Option[0]:
                    is1 -= 1


def load_music(music):
    """Load the musics of a list"""
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)


def distance(xo, yo, x, y):
    """
    distance between players
    """
    dx = x - xo
    dy = y - yo
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def play_loop():
    """
    Game Loop
    """
    global vs_pc
    global played_once
    global game_state
    global previous_game_state
    global time3
    global default_axis
    played_once = True
    screen.blit(background, (0, 0))
    p1 = [human_players[0]]
    p2 = [human_players[1]]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if vs_pc is False:
            player1.play_player_keyboard(event, p2, power1)
            player2.play_player_keyboard(event, p1, power2)
        if vs_pc:
            player1.play_player_keyboard(event, pc_players, power1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = 1
                previous_game_state = 2
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            if vs_pc is False:
                player1.play_player_joystick(event, p2, power1, joystick, i, default_axis)
                player2.play_player_joystick(event, p1, power2, joystick, i, default_axis)
            if vs_pc:
                player1.play_player_joystick(event, pc_players, power1, joystick, i, default_axis)
            if joystick.get_button(9):
                game_state = 1
                previous_game_state = 2
                time3 = time.time()*1000

    global width
    global height
    # playerVsplayer
    if vs_pc is False:
        player1.lock_inside_screen(width, height, delta)
        player1.physical_rect()
        player1.kameham_dispute(power_dispute, p2, powers)
        player1.power_placing(power1)
        player1.status_bar(screen, width)
        player1.stand_up_position()
        player1.defeated(screen, player2)
        player1.turn_around(player2)
        player1.play_effects(effects)
        player2.lock_inside_screen(width, height, delta)
        player2.physical_rect()
        player2.power_placing(power2, dx2=920, dy2=0)
        player2.status_bar(screen, width)
        player2.stand_up_position()
        player2.defeated(screen, player1)
        player2.turn_around(player1)
        player1.update(screen)
        player2.update(screen)
        player2.play_effects(effects2)
        power1.update(screen)
        power_dispute.update(screen)
        power2.update(screen)
        effects.update(screen)
        effects2.update(screen)
    if vs_pc:
        player1.lock_inside_screen(width, height, delta)
        player1.physical_rect()
        player1.power_placing(power1)
        player1.status_bar(screen, width)
        player1.stand_up_position()
        player1.play_effects(effects)
        player1.defeated(screen, player_pc)
        player1.update(screen)
        player1.kameham_dispute(power_dispute, pc_players, powers)
        player_pc.lock_inside_screen(width, height, delta)
        player_pc.physical_rect()
        player_pc.power_placing(power3)
        player_pc.status_bar(screen, width)
        player_pc.stand_up_position()
        player_pc.play_effects(effects2)
        player_pc.update(screen)
        power3.update(screen)
        player1.turn_around(player_pc)
        player_pc.turn_around(player1)
        player_pc.play_pc(player1, power3, resolution)
        player_pc.defeated(screen, player1)
        power1.update(screen)
        power_dispute.update(screen)
        effects.update(screen)
        effects2.update(screen)
    fps = "fps:%.2f" % clock.get_fps()
    my_font = pygame.font.SysFont("monospace", 25)
    fps_word = my_font.render(fps, 1, WHITE)
    screen.blit(fps_word, (0, 730))
    clock.tick(60)
    pygame.display.update()

show_splashscreen()
#show_video()
load_music(song[0])
while 1:
    if game_state == 0:
        open_menu()
    elif game_state == 1:
        load_menu()
    elif game_state == 2:
        play_loop()
    elif game_state == 3:
        options()
    elif game_state == 4:
        choose_scenery()
    elif game_state == 5:
        choose_character()
    elif game_state == 6:
        game_credits()
    elif game_state == 7:
        keyboard()
