#!/usr/bin/python
import sys
import time
import ntpath
import pygame
from .spriteanimation import SpriteAnimation
from .npc import NPC
from .player import Player

pygame.init()
joystick_enabled = True

if(joystick_enabled):
    pygame.joystick.init()
    for x in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(x)
        joystick.init()

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
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Main():
    def __init__(self, window=0, resolution=(1200, 768)):
        scenery1_image = "resources/imagens/scenarios/Wasteland-2.jpg"
        scenery2_image = "resources/imagens/scenarios/namek-3d-2.jpg"
        scenery3_image = "resources/imagens/scenarios/trunks-future-2.png"
        scenery4_image = "resources/imagens/scenarios/arena-2-2.gif"
        scenery4 = pygame.image.load(scenery4_image)
        self.background = scenery4
        # self.resolution = self.background.get_size()
        self.resolution = resolution
        self.width, self.height = self.resolution
        if window == 0:
            self.screen = pygame.display.set_mode(self.resolution,
                                                  pygame.FULLSCREEN, 32)
        else:
            self.screen = pygame.display.set_mode(self.resolution)
        scenery1 = pygame.image.load(scenery1_image).convert()
        scenery2 = pygame.image.load(scenery2_image).convert()
        scenery3 = pygame.image.load(scenery3_image).convert()
        scenery4 = scenery4.convert_alpha()
        self.scenery = [scenery1, scenery2,
                        scenery3, scenery4]
        menu_image = "resources/imagens/openning/background/goku-vs-vegeta-2.jpg"
        goku100x100 = "resources/imagens/player/goku/ss4/goku100x100.png"
        vegeta100x100 = "resources/imagens/player/vegeta/vegeta100x100.png"
        trunks100x100 = "resources/imagens/player/trunks/trunks100x100.png"
        frieza100x100 = "resources/imagens/player/frieza/frieza100x100.png"
        gohan100x100 = "resources/imagens/player/gohan/gohan100x100.png"
        self.photos3x4 = [pygame.image.load(goku100x100),
                          pygame.image.load(vegeta100x100), pygame.image.load(gohan100x100),
                          pygame.image.load(trunks100x100), pygame.image.load(frieza100x100)]
        self.ch = pygame.transform.scale(self.photos3x4[0], (100, 100))
        self.background_openning = pygame.image.load(menu_image).convert()
        self.scene1 = pygame.transform.scale(self.scenery[0], (500, 300))
        pygame.mouse.set_visible(0)
        self.game_state = 0  # Menu
        self.previous_game_state = 0
        self.s0Option = range(5)
        self.is0 = 0
        self.s1Option = range(5)
        self.is1 = 0
        self.s3Option = range(7)
        self.is3 = 0
        self.s4Option = range(2)
        self.is4 = 0
        self.s5Option = range(3)
        self.is5 = 0
        self.sc = 0
        self.sc1 = 0
        self.sc2 = 1
        self.sg = 0
        self.df = 2
        self.volume = 0.5
        self.vs_pc = False
        song1 = 'resources/sounds/sparking.ogg'
        song3 = 'resources/sounds/cha-la.ogg'
        self.song = [song1, song3]
        self.level = ['easy', 'Medium', 'Hard', 'Super Sayajin']
        self.xp1 = 400
        self.yp1 = 400
        self.xp1d = self.xp1
        self.yp1d = self.yp1
        self.xp2 = 550
        self.yp2 = 400
        self.xp2d = self.xp2
        self.yp2d = self.yp2
        self.played_once = False
        self.characters = ['goku', 'vegeta', 'gohan', 'trunks', 'frieza']
        player1.load_power(power1)
        player1.load_power(power_dispute)
        player2.load_power(power_dispute2)
        player1.load_power(effects)
        player2.load_power(effects2)
        player2.load_power(power2)
        player_pc.load_power(power3)
        player_pc.load_character(self.characters[1])
        player2.load_character(self.characters[1])
        self.pc_players = [player_pc]
        self.human_players = [player1, player2]
        player_pc.is_pc = True
        self.powers = [power1, power2, power3]
        self.delta = 13  # speed of the game
        player2.facing_right = False
        player2.x = 850
        player2.y = 350
        player_pc.x = 850
        player_pc.y = 350
        player_pc.xp = 0
        self.move_one = True
        self.time1 = 0
        self.time3 = 0
        self.default_axis = 0

    def restart(self):
        """
        Restarts the game
        """
        if self.vs_pc:
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

    def show_splashscreen(self):
        """
        Show the splash screen.
        This is called once when the game is first started.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.mixer.music.load('resources/sounds/splash.ogg')
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.volume)
        white = 250, 250, 250
        self.screen.fill(white)
        # Slowly fade the splash screen image from white to opaque.
        splash = pygame.image.load(
            "resources/imagens/openning/splash/estevaosplash.png").convert()
        for i in range(25):
            splash.set_alpha(i)
            self.screen.blit(splash, (90, 50))
            pygame.display.update()
            pygame.time.wait(100)

        pygame.mixer.fadeout(2000)
        self.screen.blit(splash, (90, 50))
        pygame.display.update()
        pygame.time.wait(1500)
        self.game_state = 0

    def open_menu(self):
        """
        Main Menu
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                buttons = joystick.get_numbuttons()
                axis = joystick.get_axis(1)
                axis = round(axis, 3)
                if axis != 1 and axis != -1:
                    self.default_axis = axis
                if axis > self.default_axis and self.move_one:
                    self.is0 += 1
                    self.time1 = time.time()
                    self.move_one = False
                if axis < self.default_axis and self.move_one:
                    self.is0 += -1
                    self.time1 = time.time()
                    self.move_one = False
                if self.is0 < 0:
                    self.is0 = 0
                if self.is0 > (len(self.s0Option)-1):
                    self.is0 = 4
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.time3 = time.time()*1000
                        if self.s0Option[self.is0] == 0:
                            player2.player_id = 2
                            self.game_state = 5
                            self.vs_pc = True
                            self.restart()
                        if self.s0Option[self.is0] == 1:
                            self.game_state = 5
                            self.restart()
                            self.vs_pc = False
                            player2.player_id = 2
                        if self.s0Option[self.is0] == 2:
                            self.previous_game_state = 0
                            self.game_state = 3
                        if self.s0Option[self.is0] == 3:
                            self.previous_game_state = 0
                            self.game_state = 6
                        if self.s0Option[self.is0] == 4:
                            pygame.quit()
                            sys.exit()

            if time.time()*1000-self.time1*1000 > 200:
                self.move_one = True
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
        my_font = pygame.font.SysFont("monospace", 65)
        bold_font = pygame.font.SysFont("monospace", 75, bold=True)
        player_vs_pc = my_font.render("Play Vs PC", 1, WHITE)
        player_vs_player = my_font.render("Play Vs Player2", 1, WHITE)
        options_word = my_font.render("Options", 1, WHITE)
        credits_word = my_font.render("Credits", 1, WHITE)
        quit_word = my_font.render("Quit", 1, WHITE)

        if self.s0Option[self.is0] == 0:
            player_vs_pc = bold_font.render("Play Vs Pc", 1, WHITE)
        if self.s0Option[self.is0] == 1:
            player_vs_player = bold_font.render("Play Vs Player2", 1, WHITE)
        if self.s0Option[self.is0] == 2:
            options_word = bold_font.render("Options", 1, WHITE)
        if self.s0Option[self.is0] == 3:
            credits_word = bold_font.render("Credits", 1, WHITE)
        if self.s0Option[self.is0] == 4:
            quit_word = bold_font.render("Quit", 1, WHITE)

        self.screen.blit(player_vs_pc, (310, 250))
        self.screen.blit(player_vs_player, (310, 320))
        self.screen.blit(options_word, (310, 390))
        self.screen.blit(credits_word, (310, 460))
        self.screen.blit(quit_word, (310, 530))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state
                if event.key == pygame.K_RETURN:
                    if self.s0Option[self.is0] == 0:
                        player2.player_id = 2
                        self.game_state = 5
                        self.vs_pc = True
                        self.restart()
                    if self.s0Option[self.is0] == 1:
                        self.game_state = 5
                        self.restart()
                        self.vs_pc = False
                        player2.player_id = 2
                    if self.s0Option[self.is0] == 2:
                        self.previous_game_state = 0
                        self.game_state = 3
                    if self.s0Option[self.is0] == 3:
                        self.previous_game_state = 0
                        self.game_state = 6
                    if self.s0Option[self.is0] == 4:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_DOWN:
                    if self.s0Option[self.is0] < self.s0Option[-1]:
                        self.is0 += 1
                if event.key == pygame.K_UP:
                    if self.s0Option[self.is0] > self.s0Option[0]:
                        self.is0 -= 1

    def options(self):
        """
        Option Menu
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                axes = joystick.get_numaxes()
                buttons = joystick.get_numbuttons()
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    axis = round(axis, 3)
                    if i == 0:
                        if axis > self.default_axis and self.move_one:
                            if self.s3Option[self.is3] == 0:
                                self.delta += 1
                            if self.s3Option[self.is3] == 2:
                                if self.volume < 0.9:
                                    self.volume += 0.1
                                    pygame.mixer.music.set_volume(self.volume)
                            if self.s3Option[self.is3] == 1:
                                if self.sg == len(self.song) - 1:
                                    self.sg -= 1
                                self.sg += 1
                                self.load_music(self.song[self.sg])
                            if self.s3Option[self.is3] == 3:
                                if self.df < len(self.level) - 1:
                                    self.df += 1
                            self.time1 = time.time()
                            self.move_one = False
                        if axis < self.default_axis and self.move_one:
                            if self.s3Option[self.is3] == 0:
                                self.delta -= 1
                            if self.s3Option[self.is3] == 2:
                                if self.volume > 0.1:
                                    self.volume -= 0.1
                                    pygame.mixer.music.set_volume(self.volume)
                                if self.volume < 0.2:
                                    self.volume = 0
                                    pygame.mixer.music.set_volume(self.volume)
                            if self.s3Option[self.is3] == 1:
                                if self.sg == 0:
                                    self.sg = len(self.song)
                                self.sg -= 1
                                self.load_music(self.song[self.sg])
                            if self.s3Option[self.is3] == 3:
                                if self.df > 0:
                                    self.df -= 1
                            self.time1 = time.time()
                            self.move_one = False

                    if i == 1:
                        if axis > self.default_axis and self.move_one:
                            if self.s3Option[self.is3] < self.s3Option[-1]:
                                self.is3 += 1
                                self.time1 = time.time()
                                self.move_one = False
                        if axis < self.default_axis and self.move_one:
                            if self.s3Option[self.is3] > self.s3Option[0]:
                                self.is3 -= 1
                                self.time1 = time.time()
                                self.move_one = False
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.time3 = time.time()*1000
                        if self.s3Option[self.is3] == 5:
                            if self.played_once:
                                self.game_state = 2
                            else:
                                pass
                        if self.s3Option[self.is3] == 6:
                            self.game_state = self.previous_game_state
                        if self.s3Option[self.is3] == 4:
                            self.game_state = 7
                        if i == 8:
                            self.game_state = self.previous_game_state

            if time.time()*1000-self.time1*1000 > 200:
                self.move_one = True
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
        my_font = pygame.font.SysFont("monospace", 45)
        bold_font = pygame.font.SysFont("monospace", 55, bold=True)
        player_vs_player = my_font.render("Game Speed " + str(self.delta), 1, WHITE)
        player_vs_pc = my_font.render("Music Volume " + str(self.volume * 100), 1, WHITE)
        options_word = my_font.render("Resume", 1, WHITE)
        music = my_font.render("Music", 1, WHITE)
        back = my_font.render("Back", 1, WHITE)
        mode = my_font.render("Mode", 1, WHITE)
        difficult = my_font.render(self.level[self.df], 1, WHITE)
        keyboard_word = my_font.render("Keyboard", 1, WHITE)
        title = my_font.render(ntpath.basename(self.song[self.sg]), 1, WHITE)

        if self.s3Option[self.is3] == 0:
            player_vs_player = bold_font.render(
                "Game Speed " + str(self.delta), 1, WHITE)
        if self.s3Option[self.is3] == 2:
            player_vs_pc = bold_font.render(
                "Music Volume " + str(self.volume * 100), 1, WHITE)
        if self.s3Option[self.is3] == 3:
            mode = bold_font.render("Mode", 1, WHITE)
            difficult = bold_font.render(self.level[self.df], 1, WHITE)
        if self.s3Option[self.is3] == 4:
            keyboard_word = bold_font.render("Keyboard", 1, WHITE)
        if self.s3Option[self.is3] == 5:
            options_word = bold_font.render("Resume", 1, WHITE)
        if self.s3Option[self.is3] == 6:
            back = bold_font.render("Back", 1, WHITE)
        if self.s3Option[self.is3] == 1:
            music = bold_font.render("Music", 1, WHITE)
            title = bold_font.render(ntpath.basename(self.song[self.sg]), 1, WHITE)
        self.screen.blit(player_vs_player, (340, 250))
        self.screen.blit(player_vs_pc, (340, 350))
        self.screen.blit(mode, (340, 400))
        self.screen.blit(difficult, (540, 400))
        self.screen.blit(music, (340, 300))
        self.screen.blit(title, (540, 300))
        self.screen.blit(keyboard_word, (340, 450))
        self.screen.blit(options_word, (340, 500))
        self.screen.blit(back, (340, 550))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state
                if event.key == pygame.K_RETURN:
                    if self.s3Option[self.is3] == 5:
                        if self.played_once:
                            self.game_state = 2
                        else:
                            pass
                    if self.s3Option[self.is3] == 6:
                        self.game_state = self.previous_game_state
                    if self.s3Option[self.is3] == 4:
                        self.game_state = 7
                if event.key == pygame.K_DOWN:
                    if self.s3Option[self.is3] < self.s3Option[-1]:
                        self.is3 += 1
                if event.key == pygame.K_UP:
                    if self.s3Option[self.is3] > self.s3Option[0]:
                        self.is3 -= 1
                if event.key == pygame.K_RIGHT:
                    if self.s3Option[self.is3] == 0:
                        self.delta += 1
                    if self.s3Option[self.is3] == 2:
                        if self.volume < 0.9:
                            self.volume += 0.1
                            pygame.mixer.music.set_volume(self.volume)
                    if self.s3Option[self.is3] == 1:
                        if self.sg == len(self.song) - 1:
                            self.sg -= 1
                        self.sg += 1
                        self.load_music(self.song[self.sg])
                    if self.s3Option[self.is3] == 3:
                        if self.df < len(self.level) - 1:
                            self.df += 1
                if event.key == pygame.K_LEFT:
                    if self.s3Option[self.is3] == 0:
                        self.delta -= 1
                    if self.s3Option[self.is3] == 2:
                        if self.volume > 0.1:
                            self.volume -= 0.1
                            pygame.mixer.music.set_volume(self.volume)
                        if self.volume < 0.2:
                            self.volume = 0
                            pygame.mixer.music.set_volume(self.volume)
                    if self.s3Option[self.is3] == 1:
                        if self.sg == 0:
                            self.sg = len(self.song)
                        self.sg -= 1
                        self.load_music(self.song[self.sg])
                    if self.s3Option[self.is3] == 3:
                        if self.df > 0:
                            self.df -= 1
        if self.df == 0:
            player_pc.kameham_ms = 450
            player_pc.punch_ms = 200
            player_pc.kame_cont = 15
            player_pc.teleport_boolean = False
        if self.df == 1:
            player_pc.kameham_ms = 160
            player_pc.punch_ms = 90
            player_pc.kame_cont = 22
            player_pc.teleport_boolean = False
        if self.df == 2:
            player_pc.kameham_ms = 160
            player_pc.punch_ms = 90
            player_pc.kame_cont = 22
            player_pc.teleport_boolean = True
        if self.df == 3:
            player_pc.kameham_ms = 70
            player_pc.punch_ms = 70
            player_pc.kame_cont = 23
            player_pc.teleport_boolean = True

    def game_credits(self):
        """
        Credits screen
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                buttons = joystick.get_numbuttons()
                axis = joystick.get_axis(1)
                axis = round(axis, 3)
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.game_state = self.previous_game_state
                        self.time3 = time.time()*1000
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
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

        self.screen.blit(game_developer, (200, 150))
        self.screen.blit(estevao, (200, 210))
        self.screen.blit(supporters, (200, 270))
        self.screen.blit(bru, (200, 330))
        self.screen.blit(hel, (200, 390))
        self.screen.blit(thiago, (200, 450))
        self.screen.blit(art_work, (740, 150))
        self.screen.blit(akira, (740, 210))
        self.screen.blit(artist1, (740, 270))
        self.screen.blit(artist2, (740, 330))
        self.screen.blit(artist3, (740, 390))
        self.screen.blit(artist4, (740, 450))
        self.screen.blit(artist5, (740, 510))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state

    def keyboard(self):
        """
        Screen showing the Keys used to play
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                buttons = joystick.get_numbuttons()
                axis = joystick.get_axis(1)
                axis = round(axis, 3)
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.game_state = self.previous_game_state
                        self.time3 = time.time()*1000

        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
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

        self.screen.blit(player1_word, (300, 100))
        self.screen.blit(left, (300, 180))
        self.screen.blit(right, (300, 230))
        self.screen.blit(up, (300, 280))
        self.screen.blit(down, (300, 330))
        self.screen.blit(kameham, (300, 380))
        self.screen.blit(punch, (300, 430))
        self.screen.blit(kick, (300, 480))
        self.screen.blit(defend, (300, 530))
        self.screen.blit(load, (300, 580))
        self.screen.blit(teleport, (300, 630))

        self.screen.blit(player2_word, (680, 100))
        self.screen.blit(left2, (680, 180))
        self.screen.blit(right2, (680, 230))
        self.screen.blit(up2, (680, 280))
        self.screen.blit(down2, (680, 330))
        self.screen.blit(kameham2, (680, 380))
        self.screen.blit(punch2, (680, 430))
        self.screen.blit(kick2, (680, 480))
        self.screen.blit(defend2, (680, 530))
        self.screen.blit(load2, (680, 580))
        self.screen.blit(teleport2, (680, 630))
        self.screen.blit(back, (780, 680))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state
                if event.key == pygame.K_RETURN:
                    self.game_state = self.previous_game_state

    def choose_character(self):
        """
        Choose character screen
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joynumber = i
                joystick = pygame.joystick.Joystick(i)
                axes = joystick.get_numaxes()
                buttons = joystick.get_numbuttons()
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    axis = round(axis, 3)
                    if i == 0 and joynumber == 1:
                        if axis > self.default_axis and self.move_one:
                            # right
                            self.xp2 += 150
                            self.sc2 += 1
                            self.time1 = time.time()
                            self.move_one = False
                        if axis < self.default_axis and self.move_one:
                            # left
                            self.xp2 -= 150
                            self.sc2 -= 1
                            self.time1 = time.time()
                            self.move_one = False
                    if self.sc2 > len(self.photos3x4) - 1:
                        self.sc2 = len(self.photos3x4) - 1
                        self.xp2 = self.xp1d + 600
                    if self.sc2 < 0:
                        self.sc2 = 0
                        self.xp2 = self.xp1d
                    if i == 0 and joynumber == 0:
                        if axis > self.default_axis and self.move_one:
                            # right
                            self.xp1 += 150
                            self.sc1 += 1
                            self.time1 = time.time()
                            self.move_one = False
                        if axis < self.default_axis and self.move_one:
                            # left
                            self.xp1 -= 150
                            self.sc1 -= 1
                            self.time1 = time.time()
                            self.move_one = False
                    if self.sc1 > len(self.photos3x4) - 1:
                        self.sc1 = len(self.photos3x4) - 1
                        self.xp1 = self.xp1d + 600
                    if self.sc1 < 0:
                        self.sc1 = 0
                        self.xp1 = self.xp1d

                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.game_state = 4
                        if self.vs_pc:
                            player1.load_character(self.characters[self.sc1])
                            player_pc.load_character(self.characters[self.sc2])
                        else:
                            player1.load_character(self.characters[self.sc1])
                            player2.load_character(self.characters[self.sc2])
                        self.time3 = time.time()*1000
                        if i == 8:
                            self.game_state = self.previous_game_state

            if time.time()*1000-self.time1*1000 > 200:
                self.move_one = True
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
        bold_font = pygame.font.SysFont("monospace", 65, bold=True)

        player_vs_player = bold_font.render("P1", 1, RED)
        if self.vs_pc:
            player_vs_player2 = bold_font.render("PC", 1, BLUE)
        else:
            player_vs_player2 = bold_font.render("P2", 1, BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state
                if event.key == pygame.K_RETURN:
                    self.game_state = 4
                    if self.vs_pc:
                        player1.load_character(self.characters[self.sc1])
                        player_pc.load_character(self.characters[self.sc2])
                    else:
                        player1.load_character(self.characters[self.sc1])
                        player2.load_character(self.characters[self.sc2])
                if event.key == pygame.K_d:
                    if self.sc1 >= len(self.photos3x4) - 1:
                        self.sc1 = 0
                        self.xp1 = self.xp1d
                    elif 0 <= self.sc1 < len(self.photos3x4):
                        self.xp1 += 150
                        self.sc1 += 1
                if event.key == pygame.K_RIGHT:
                    if self.sc2 >= len(self.photos3x4) - 1:
                        self.sc2 = 0
                        self.xp2 = self.xp1d
                    elif 0 <= self.sc2 < len(self.photos3x4):
                        self.xp2 += 150
                        self.sc2 += 1

                if event.key == pygame.K_a:
                    if self.sc1 <= 0:
                        self.sc1 = len(self.photos3x4) - 1
                        self.xp1 = self.xp1d + 300
                    elif 0 <= self.sc1 < len(self.photos3x4):
                        self.xp1 -= 150
                        self.sc1 -= 1

                if event.key == pygame.K_LEFT:
                    if self.sc2 <= 0:
                        self.sc2 = len(self.photos3x4) - 1
                        self.xp2 = self.xp1d + 300
                    elif 0 <= self.sc2 < len(self.photos3x4):
                        self.xp2 -= 150
                        self.sc2 -= 1

        x = 350
        y = 350
        dx = 0
        for picture in self.photos3x4:
            ch = pygame.transform.scale(picture, (150, 150))
            self.screen.blit(ch, (x + dx, y))
            dx += 150
        self.screen.blit(player_vs_player, (self.xp1, self.yp1))
        self.screen.blit(player_vs_player2, (self.xp2, self.yp2))
        pygame.display.update()

    def choose_scenery(self):
        """
        Choose scenery screen
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                axes = joystick.get_numaxes()
                buttons = joystick.get_numbuttons()
                for i in range(axes):
                    axis = joystick.get_axis(i)
                    axis = round(axis, 3)
                    if axis > self.default_axis and self.move_one:
                        # right
                        if self.sc == len(self.scenery) - 1:
                            self.sc = -1
                        self.sc += 1
                        self.scene1 = pygame.transform.scale(self.scenery[self.sc], (500, 300))
                        self.time1 = time.time()
                        self.move_one = False
                    if axis < self.default_axis and self.move_one:
                        # left
                        if self.sc == 0:
                            self.sc = len(self.scenery)
                        self.sc -= 1
                        self.scene1 = pygame.transform.scale(self.scenery[self.sc], (500, 300))
                        self.time1 = time.time()
                        self.move_one = False
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        self.game_state = 2
                        self.background = self.scenery[self.sc]
            if time.time()*1000-self.time1*1000 > 200:
                self.move_one = True
        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
        bold_font = pygame.font.SysFont("monospace", 55, bold=True)

        player_vs_player = bold_font.render(">", 1, WHITE)
        player_vs_player2 = bold_font.render("<", 1, WHITE)
        self.screen.blit(player_vs_player, (865, 420))
        self.screen.blit(player_vs_player2, (300, 420))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = self.previous_game_state
                if event.key == pygame.K_RETURN:
                    self.game_state = 2
                    self.background = self.scenery[self.sc]
                if event.key == pygame.K_RIGHT:
                    if self.sc == len(self.scenery) - 1:
                        self.sc = -1
                    self.sc += 1
                    self.scene1 = pygame.transform.scale(self.scenery[self.sc], (500, 300))
                if event.key == pygame.K_LEFT:
                    if self.sc == 0:
                        self.sc = len(self.scenery)
                    self.sc -= 1
                    self.scene1 = pygame.transform.scale(self.scenery[self.sc], (500, 300))
        self.screen.blit(self.scene1, (350, 300))
        pygame.display.update()

    def load_menu(self):
        """
        Menu during the playing game
        """
        if(joystick_enabled):
            for i in range(pygame.joystick.get_count()):
                joystick = pygame.joystick.Joystick(i)
                buttons = joystick.get_numbuttons()
                axis = joystick.get_axis(1)
                axis = round(axis, 3)
                if axis > self.default_axis and self.move_one:
                    self.is1 += 1
                    self.time1 = time.time()
                    self.move_one = False
                if axis < self.default_axis and self.move_one:
                    self.is1 += -1
                    self.time1 = time.time()
                    self.move_one = False
                for i in range(buttons):
                    if time.time()*1000 - self.time3 > 300:
                        button = joystick.get_button(i)
                    else:
                        button = 0
                    if button:
                        if self.s1Option[self.is1] == 0:
                            self.game_state = 0
                            self.time3 = time.time()*1000
                        if self.s1Option[self.is1] == 1:
                            self.game_state = 2
                        if self.s1Option[self.is1] == 2:
                            self.game_state = 3
                            self.previous_game_state = 1
                            self.time3 = time.time()*1000
                        if self.s1Option[self.is1] == 3:
                            self.restart()
                            self.game_state = 2
                        if self.s1Option[self.is1] == 4:
                            pygame.quit()
                            sys.exit()

            if time.time()*1000-self.time1*1000 > 200:
                self.move_one = True

        black = 0, 0, 0
        self.screen.fill(black)
        self.screen.blit(self.background_openning, (-70, 0))
        my_font = pygame.font.SysFont("monospace", 45)
        bold_font = pygame.font.SysFont("monospace", 55, bold=True)
        initial_screen = my_font.render("Initial Screen", 1, WHITE)
        player_vs_player = my_font.render("Resume", 1, WHITE)
        player_vs_pc = my_font.render("Options", 1, WHITE)
        restart_word = my_font.render("Restart", 1, WHITE)
        quit_word = my_font.render("Quit", 1, WHITE)
        self.is1 = int(round(self.is1))
        if self.is1 < 0:
            self.is1 = 0
        if self.is1 > (len(self.s1Option)-1):
            self.is1 = 4

        if self.s1Option[self.is1] == 0:
            initial_screen = bold_font.render("Initial Screen", 1, WHITE)
        if self.s1Option[self.is1] == 1:
            player_vs_player = bold_font.render("Resume", 1, WHITE)
        if self.s1Option[self.is1] == 2:
            player_vs_pc = bold_font.render("Options", 1, WHITE)
        if self.s1Option[self.is1] == 3:
            restart_word = bold_font.render("Restart", 1, WHITE)
        if self.s1Option[self.is1] == 4:
            quit_word = bold_font.render("Quit", 1, WHITE)
        self.screen.blit(initial_screen, (340, 250))
        self.screen.blit(player_vs_player, (340, 305))
        self.screen.blit(player_vs_pc, (340, 360))
        self.screen.blit(restart_word, (340, 415))
        self.screen.blit(quit_word, (340, 470))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = 2
                    self.previous_game_state = 1
                if event.key == pygame.K_RETURN:
                    if self.s1Option[self.is1] == 0:
                        self.game_state = 0
                    if self.s1Option[self.is1] == 1:
                        self.game_state = 2
                    if self.s1Option[self.is1] == 2:
                        self.game_state = 3
                        self.previous_game_state = 1
                    if self.s1Option[self.is1] == 3:
                        self.restart()
                        self.game_state = 2
                    if self.s1Option[self.is1] == 4:
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_DOWN:
                    if self.s1Option[self.is1] < self.s1Option[-1]:
                        self.is1 += 1
                if event.key == pygame.K_UP:
                    if self.s1Option[self.is1] > self.s1Option[0]:
                        self.is1 -= 1

    def load_music(self, music):
        """Load the musics of a list"""
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    def distance(self, xo, yo, x, y):
        """
        distance between players
        """
        dx = x - xo
        dy = y - yo
        d = ((dx ** 2) + (dy ** 2)) ** 0.5
        return d

    def fight_loop(self):
        """
        Game Loop
        """
        self.played_once = True
        self.screen.blit(self.background, (0, 0))
        p1 = [self.human_players[0]]
        p2 = [self.human_players[1]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.vs_pc is False:
                player1.play_player_keyboard(event, p2, power1)
                player2.play_player_keyboard(event, p1, power2)
            if self.vs_pc:
                player1.play_player_keyboard(event, self.pc_players, power1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = 1
                    self.previous_game_state = 2
            if(joystick_enabled):
                for i in range(pygame.joystick.get_count()):
                    joystick = pygame.joystick.Joystick(i)
                    if self.vs_pc is False:
                        player1.play_player_joystick(event, p2,
                                                    power1, joystick, i, self.default_axis)
                        player2.play_player_joystick(event, p1,
                                                    power2, joystick, i, self.default_axis)
                    if self.vs_pc:
                        player1.play_player_joystick(event, self.pc_players,
                                                    power1, joystick, i, self.default_axis)
                    if joystick.get_button(9):
                        self.game_state = 1
                        self.previous_game_state = 2
                        self.time3 = time.time()*1000
        # playerVsplayer
        width, height = self.width, self.height
        if self.vs_pc is False:
            player1.lock_inside_screen(width, height, self.delta)
            player1.physical_rect()
            player1.kameham_dispute(power_dispute, p2, self.powers)
            player1.power_placing(power1)
            player1.status_bar(self.screen, width)
            player1.stand_up_position()
            player1.defeated(self.screen, player2)
            player1.turn_around(player2)
            player1.play_effects(effects)
            player2.lock_inside_screen(width, height, self.delta)
            player2.physical_rect()
            player2.power_placing(power2, dx2=920, dy2=0)
            player2.status_bar(self.screen, width)
            player2.stand_up_position()
            player2.defeated(self.screen, player1)
            player2.turn_around(player1)
            player1.update(self.screen)
            player2.update(self.screen)
            player2.play_effects(effects2)
            power1.update(self.screen)
            power_dispute.update(self.screen)
            power2.update(self.screen)
            effects.update(self.screen)
            effects2.update(self.screen)
        if self.vs_pc:
            player1.lock_inside_screen(width, height, self.delta)
            player1.physical_rect()
            player1.power_placing(power1)
            player1.status_bar(self.screen, width)
            player1.stand_up_position()
            player1.play_effects(effects)
            player1.defeated(self.screen, player_pc)
            player1.update(self.screen)
            player1.kameham_dispute(power_dispute, self.pc_players, self.powers)
            player_pc.lock_inside_screen(width, height, self.delta)
            player_pc.physical_rect()
            player_pc.power_placing(power3)
            player_pc.status_bar(self.screen, width)
            player_pc.stand_up_position()
            player_pc.play_effects(effects2)
            player_pc.update(self.screen)
            power3.update(self.screen)
            player1.turn_around(player_pc)
            player_pc.turn_around(player1)
            player_pc.play_pc(player1, power3, self.resolution)
            player_pc.defeated(self.screen, player1)
            power1.update(self.screen)
            power_dispute.update(self.screen)
            effects.update(self.screen)
            effects2.update(self.screen)
        fps = "fps:%.2f" % clock.get_fps()
        my_font = pygame.font.SysFont("monospace", 25)
        fps_word = my_font.render(fps, 1, WHITE)
        self.screen.blit(fps_word, (0, 730))
        clock.tick(60)
        pygame.display.update()

    def run(self):
        self.show_splashscreen()
        self.load_music(self.song[0])
        while 1:
            if self.game_state == 0:
                self.open_menu()
            elif self.game_state == 1:
                self.load_menu()
            elif self.game_state == 2:
                self.fight_loop()
            elif self.game_state == 3:
                self.options()
            elif self.game_state == 4:
                self.choose_scenery()
            elif self.game_state == 5:
                self.choose_character()
            elif self.game_state == 6:
                self.game_credits()
            elif self.game_state == 7:
                self.keyboard()
