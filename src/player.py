#!/usr/bin/python
import time
import random
import pygame
from .characters import Characters

pygame.init()

pygame.joystick.init()
for x in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(x)
    joystick.init()


class Player(Characters):
    def __init__(self, initial_action, player_id):
        """
        Initiation of the player states
        """
        Characters.__init__(self, initial_action, player_id)
        self.pos = 1
        self.pos2 = 1
        self.movex, self.movey = 0, 0
        self.facing_right = True
        self.x = 250
        self.y = 350
        self.Rect = pygame.Rect(self.x, self.y, 35, 70)
        self.hp = 400
        self.xp = 50
        self.XP_MAX = 150
        self.defending = False
        self.attacking = False
        self.initial_time = 0
        self.timing2 = True
        self.timing_dispute = False
        self.punch_damage = 2
        self.kick_damage = 2
        self.hit_defended = 0.4
        self.power_damage = 10
        self.power_damage_defended = 2
        self.combo_damage = 10
        self.player_id = player_id
        self.loading = False
        self.super_punch_state = False
        self.super_kick_state = False
        self.factor_super = 1.4
        if self.player_id == 1:
            self.k_down = pygame.K_s
            self.k_up = pygame.K_w
            self.k_defend = pygame.K_p
            self.k_kameham = pygame.K_u
            self.k_punch = pygame.K_i
            self.k_kick = pygame.K_o
            self.k_load = pygame.K_j
            self.k_rightArrow = pygame.K_d
            self.k_leftArrow = pygame.K_a
            self.k_combo = pygame.K_c
            self.k_teleport = pygame.K_k
        elif self.player_id == 2:
            self.k_down = pygame.K_DOWN
            self.k_up = pygame.K_UP
            self.k_defend = pygame.K_KP5
            self.k_kameham = pygame.K_KP7
            self.k_punch = pygame.K_KP8
            self.k_kick = pygame.K_KP9
            self.k_load = pygame.K_KP4
            self.k_rightArrow = pygame.K_RIGHT
            self.k_leftArrow = pygame.K_LEFT
            self.k_combo = pygame.K_n
            self.k_teleport = pygame.K_KP6
        self.initial_spark = time.time()*1000
        self.initial_explosion = time.time()*1000
        self.initial_time2 = 0
        self.release_power = True
        self.void_power = True
        self.kame_cont = 0
        self.enemy_kame_cont = 0
        self.staticy = 0
        self.initial_kame = time.time()*1000
        self.initial_punch = time.time()*1000
        self.initial_effects = time.time()*1000
        self.is_pc = False
        self.single_kameham = True
        self.dispute_kameham_boolean = True
        self.attack_rect = None
        self.hp_rect = None
        self.xp_rect = None
        self.initial_death = 0
        self.press_counter = 0

    def super_punch(self, player_list):
        """
        Activate the super punch
        """
        if self.super_punch_state:
            if time.time()*1000 - self.initial_punch < 200:
                for player in player_list:
                    if self.facing_right:
                        player.movex = 3
                    if not self.facing_right:
                        player.movex = -3
            else:
                for player in player_list:
                    player.movex = 0
                self.super_punch_state = False

    def super_kick(self, player_list):
        """
        Activate the super kick
        """
        if self.super_kick_state:
            if time.time()*1000 - self.initial_punch < 200:
                for player in player_list:
                    player.movey = -3
            else:
                for player in player_list:
                    player.movey = 0
                self.super_kick_state = False

    def punch(self, player_list):
        """
        Punch action
        """
        self.action = "punch"
        self.pressed = True
        self.attacking = True
        self.defending = False
        if self.facing_right:
            self.attack_rect = pygame.Rect(self.x+30, self.y, 50, 70)
            # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
        if self.facing_right is False:
            self.attack_rect = pygame.Rect(self.x-20, self.y, 50, 70)
            # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
        self.initial_punch = time.time()*1000
        for player in player_list:
            if self.attack_rect.colliderect(player.Rect):
                if not player.defending:
                    if self.xp <= self.XP_MAX:
                        player.hp -= self.punch_damage
                    if self.xp == self.XP_MAX:
                        player.hp -= self.power_damage*self.factor_super
                        self.super_punch_state = True
                    player.initial_time = time.time()*1000
                    if abs(player.initial_punch-self.initial_punch) < 400:
                        self.initial_effects = time.time()*1000
                        # pass
                    else:
                        player.action = "hited"
                if player.defending and not player.attacking:
                    player.hp -= player.hit_defended
        self.initial_time = time.time()*1000

    def kick(self, player_list):
        """
        Kick action
        """
        self.action = "kick"
        self.pressed = True
        self.attacking = True
        self.defending = False
        if self.facing_right:
            self.attack_rect = pygame.Rect(self.x+30, self.y, 35, 70)
            # pygame.draw.rect(screen, (255,0,0), self.attack_rect)
        if not self.facing_right:
            self.attack_rect = pygame.Rect(self.x-20, self.y, 35, 70)
            # pygame.draw.rect(screen, (255,0,0), self.attack_rect)
        self.initial_punch = time.time()*1000
        for player in player_list:
            if self.attack_rect.colliderect(player.Rect):
                if player.defending is False:
                    if self.xp <= self.XP_MAX:
                        player.hp -= self.kick_damage
                    if self.xp == self.XP_MAX:
                        player.hp -= self.power_damage*self.factor_super
                        self.super_kick_state = True
                    if abs(player.initial_punch-self.initial_punch) < 400:
                        self.initial_effects = time.time()*1000
                    else:
                        player.action = "hited"
                    player.initial_time = time.time()*1000
                if player.defending and player.attacking is False:
                    player.hp -= player.hit_defended
        self.initial_time = time.time()*1000

    def combo(self, player_list, power1):
        """
        Attempt to implement combo
        """
        self.action = "combo"
        # self.pressed = True
        self.pos = 1
        self.attacking = True
        self.defending = False
        if self.facing_right:
            self.attack_rect = pygame.Rect(self.x+30, self.y, 50, 70)
            # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
        if not self.facing_right:
            self.attack_rect = pygame.Rect(self.x-15, self.y, 50, 70)
            # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
        for player in player_list:
            if self.attack_rect.colliderect(player.Rect):
                if player.defending is False:
                    player.hp -= self.combo_damage
                    player.action = "hited"
                    player.initial_time = time.time()
                if player.defending and not player.attacking:
                    player.hp -= player.hit_defended

    def kameham(self, player_list, power1):
        """
        Kameham power
        """
        self.initial_kame = time.time()*1000
        self.kame_cont += 1
        if self.xp > 0:
            for player in player_list:
                if (abs(self.y - player.y) < 50 and
                        abs(player.initial_kame-self.initial_kame) < 400):
                    if self.dispute_kameham_boolean:
                        self.release_power = True
                        self.void_power = True
                        self.kame_cont = 0
                        if player.is_pc is False:
                            player.kame_cont = 0
                        self.dispute_kameham_boolean = False
                        self.timing_dispute = True
            if self.single_kameham:
                self.action = "kameham"
                power1.action = "kame"
                self.pressed = True
                power1.pressed = True
                self.attacking = True
                self.defending = False
                if self.facing_right:
                    self.attack_rect = pygame.Rect(self.x+30, self.y+20, 1000, 60)
                    # pygame.draw.rect(screen, (0,255,0), self.attack_rect)
                else:
                    self.attack_rect = pygame.Rect(self.x-1000, self.y+20, 1000, 60)
                    # pygame.draw.rect(screen, (0,255,0), self.attack_rect)
                for player in player_list:
                    if self.attack_rect.colliderect(player.Rect):
                        if not player.defending:
                            player.hp -= self.power_damage
                            player.action = "hited"
                            player.initial_time = time.time()*1000
                        if player.defending and player.attacking is False:
                            player.hp -= player.power_damage_defended
                self.xp -= 10
                self.initial_time = time.time()*1000


    def load(self):
        """
        Load XP
        """
        self.action = "load"
        self.pressed = True
        self.initial_time = time.time()*1000
        if self.xp < self.XP_MAX:
            self.xp += 5

    def teleport(self):
        """
        Teleport to a random place
        """
        self.action = "teleport"
        self.pressed = True
        self.x = random.randint(0, 1170)
        self.y = random.randint(0, 738)
        self.initial_time = time.time()*1000

    def play_player_joystick(self, event, player_list, power1, joystick, joystick_number, default_axis):
        """
        Play player actions
        """
        if self.hp > 0:
            joynumber = joystick_number
            axes = joystick.get_numaxes()
            buttons = joystick.get_numbuttons()
            if pygame.joystick.get_count() > 0:
                if self.player_id == 1 and joynumber == 0:
                    for i in range(axes):
                        axis = joystick.get_axis(i)
                        axis = round(axis, 3)
                        if i == 0 and joynumber == 0:
                            if axis > default_axis:
                                self.action = "right"
                                self.movex = 1
                            if axis < default_axis:
                                self.action = "up"
                                self.movex = -1
                            if axis == default_axis:
                                self.movex = 0
                        if i == 1 and joynumber == 0:
                            if axis > default_axis:
                                self.action = "down"
                                self.movey = 1
                            if axis < default_axis:
                                self.action = "up"
                                self.movey = -1
                            if axis == default_axis:
                                self.movey = 0
                    if event.type == pygame.JOYBUTTONDOWN:
                        for i in range(buttons):
                            button = joystick.get_button(i)
                            if button:
                                if i == 0 and joynumber == 0:
                                    self.load()
                                if i == 1 and joynumber == 0:
                                    self.kameham(player_list, power1)
                                if i == 2 and joynumber == 0:
                                    self.kick(player_list)
                                if i == 3 and joynumber == 0:
                                    self.punch(player_list)
                                if i == 6 and joynumber == 0:
                                    self.action = "defend"
                                    self.defending = True
                                if i == 7 and joynumber == 0:
                                    self.teleport()
                    if event.type == pygame.JOYBUTTONUP:
                        if joynumber == 0:
                            self.defending = False

                elif self.player_id == 2 and joynumber == 1:
                    for i in range(axes):
                        axis = joystick.get_axis(i)
                        axis = round(axis, 3)
                        if i == 0 and joynumber == 1:
                            if axis > default_axis:
                                self.action = "right"
                                self.movex = 1
                            if axis < default_axis:
                                self.action = "up"
                                self.movex = -1
                            if axis == default_axis:
                                self.movex = 0
                        if i == 1 and joynumber == 1:
                            if axis > default_axis:
                                self.action = "down"
                                self.movey = 1
                            if axis < default_axis:
                                self.action = "up"
                                self.movey = -1
                            if axis == default_axis:
                                self.movey = 0
                    if event.type == pygame.JOYBUTTONDOWN:
                        for i in range(buttons):
                            button = joystick.get_button(i)
                            if button:
                                if i == 0 and joynumber == 1:
                                    self.load()
                                if i == 1 and joynumber == 1:
                                    self.kameham(player_list, power1)
                                if i == 2 and joynumber == 1:
                                    self.kick(player_list)
                                if i == 3 and joynumber == 1:
                                    self.punch(player_list)
                                if i == 6 and joynumber == 1:
                                    self.action = "defend"
                                    self.defending = True
                                if i == 7 and joynumber == 1:
                                    self.teleport()
                    if event.type == pygame.JOYBUTTONUP:
                        if joynumber == 0:
                            self.defending = False

    def play_player_keyboard(self, event_arg, player_list, power1):
        """
        Play player actions
        """
        if self.hp > 0:
            event = event_arg
            if event.type == pygame.KEYDOWN:
                if event.key == self.k_down:
                    self.action = "down"
                    self.movey += 1
                if event.key == self.k_up:
                    self.action = "up"
                    self.movey -= 1
                if event.key == self.k_defend:
                    self.action = "defend"
                    self.defending = True
                if self.facing_right:
                    if event.key == self.k_rightArrow:
                        self.action = "right"
                        self.movex += 1
                    if event.key == self.k_leftArrow:
                        self.action = "up"
                        self.movex -= 1
                if self.facing_right is False:
                    if event.key == self.k_rightArrow:
                        self.action = "up"
                        self.movex += 1
                    if event.key == self.k_leftArrow:
                        self.action = "right"
                        self.movex -= 1
                if event.key == self.k_kameham:
                    self.kameham(player_list, power1)
                if event.key == self.k_punch:
                    self.punch(player_list)
                if event.key == self.k_combo:
                    self.kameham(player_list, power1)
                if event.key == self.k_kick:
                    self.kick(player_list)
                if event.key == self.k_load:
                    self.load()
                if event.key == self.k_teleport:
                    self.teleport()
            if event.type == pygame.KEYUP:
                if event.key == self.k_down:
                    self.action = "down"
                    self.movey = 0
                if event.key == self.k_up:
                    self.action = "up"
                    self.movey = 0
                if event.key == self.k_defend:
                    self.action = "defend"
                    self.defending = False
                if event.key == self.k_punch:
                    self.attacking = False
                if self.facing_right:
                    if event.key == self.k_rightArrow:
                        self.action = "right"
                        self.movex = 0
                    if event.key == self.k_leftArrow:
                        self.action = "up"
                        self.movex = 0
                if self.facing_right is False:
                    if event.key == self.k_leftArrow:
                        self.action = "right"
                        self.movex = 0
                    if event.key == self.k_rightArrow:
                        self.action = "up"
                        self.movex = 0
                if event.key == self.k_kameham:
                    self.action = "kameham"
                    power1.action = "void"
                    self.movex = 0
            self.super_punch(player_list)
            self.super_kick(player_list)

    def kameham_dispute(self, local_power, player_list, powers):
        """
        Listener of the kameham dispute
        """
        if self.timing_dispute:
            self.initial_time2 = time.time()*1000
            self.timing_dispute = False
            self.staticy = self.y
            self.single_kameham = False
            player_list[0].single_kameham = False
            self.kame_cont = 0
            if player_list[0].is_pc is False:
                player_list[0].kame_cont = 0
        if time.time()*1000-self.initial_time2 < 4000:
            if self.facing_right:
                local_power.x = self.x+52
                local_power.y = self.y+10
                self.x = 40
                self.y = self.staticy
            if not self.facing_right:
                self.x = 1120
                self.y = self.staticy
            self.action = "dispute"
            self.pressed = True
            local_power.pressed = True
            self.initial_time = time.time()*1000
            powers2 = powers[:]
            for power in powers2:
                power.action = 'void'
            for other_player in player_list:
                if self.facing_right:
                    if self.kame_cont-other_player.kame_cont > 0:
                        local_power.action = "dispute3"
                    if other_player.kame_cont-self.kame_cont > 0:
                        local_power.action = "dispute2"
                    if self.kame_cont-other_player.kame_cont == 0:
                        local_power.action = "dispute"
                if not self.facing_right:
                    if self.kame_cont-other_player.kame_cont > 0:
                        local_power.action = "dispute2"
                    if other_player.kame_cont-self.kame_cont > 0:
                        local_power.action = "dispute3"
                    if self.kame_cont-other_player.kame_cont == 0:
                        local_power.action = "dispute"
                if self.facing_right:
                    other_player.y = self.y + 10
                    other_player.x = self.x + 1080
                if not self.facing_right:
                    other_player.x = 40
                    other_player.y = self.staticy
                    local_power.x = other_player.x + 42
                    local_power.y = other_player.y + 5
                other_player.action = 'dispute'
                other_player.initial_time = time.time()*1000
                other_player.single_kameham = False
        if time.time()*1000 - self.initial_time2 > 4000 and self.release_power:
            for other_player in player_list:
                self.release_power = False
                self.enemy_kame_cont = other_player.kame_cont
                if self.kame_cont > other_player.kame_cont:
                    other_player.hp -= 50
                    if self.facing_right:
                        local_power.action = 'from-right'
                    if not self.facing_right:
                        local_power.action = 'from-left'
                if self.kame_cont < other_player.kame_cont:
                    if self.facing_right:
                        local_power.action = 'from-left'
                    if not self.facing_right:
                        local_power.action = 'from-right'
                if self.kame_cont == other_player.kame_cont:
                    local_power.action = "void"
            if self.kame_cont < self.enemy_kame_cont:
                self.hp -= 50
        if time.time()*1000 - self.initial_time2 > 4500 and self.void_power:
            self.void_power = False
            local_power.action = "void"
            self.single_kameham = True
            for other_player in player_list:
                other_player.single_kameham = True
        if time.time()*1000 - self.initial_time2 > 5000:
            self.dispute_kameham_boolean = True

    def play_effects(self, effects):
        """
        Animation effects of the fight
        """
        if abs(time.time()*1000 - self.initial_effects) < 200:
            if (random.random() > 0.5 and
                    abs(time.time()*1000-self.initial_spark)) > 1500:
                effects.action = "spark"
                if abs(time.time()*1000 - self.initial_spark) > 2500:
                    effects.action = "void"
                    self.initial_spark = time.time()*1000
            if (random.random() < 0.5 and
                    abs(time.time()*1000-self.initial_explosion) > 3500):
                effects.action = "explosion"
                if abs(time.time()*1000 - self.initial_explosion) > 3700:
                    effects.action = "void"
                    self.initial_explosion = time.time()*1000
        else:
            effects.action = "void"

        if self.xp == self.XP_MAX:
            effects.action = "ki"
            if self.facing_right:
                effects.x = self.x-22
                effects.y = self.y-20
            else:
                effects.x = self.x-30
                effects.y = self.y-20
        if self.facing_right:
            if effects.action == "spark":
                effects.x = self.x+20
                effects.y = self.y+15
            if effects.action == "explosion":
                effects.x = self.x
                effects.y = self.y-20
        else:
            if effects.action == "spark":
                effects.x = self.x-5
                effects.y = self.y+15
            if effects.action == "explosion":
                effects.x = self.x-25
                effects.y = self.y-25

    def turn_around(self, other_player):
        """
        Turn around automatically
        """
        if self.x > other_player.x:
            self.facing_right = False
        if self.x < other_player.x:
            self.facing_right = True

    def lock_inside_screen(self, width, height, delta):
        """
        Movement of the player, locking him
        on the visible screen
        """
        if self.facing_right:
            if self.movex <= -1 and self.x > 0:
                self.x += self.movex * delta
            if self.movex >= 1 and self.x < width - 50:
                self.x += self.movex * delta
        if not self.facing_right:
            if self.movex <= - 1 and self.x > 0:
                self.x += self.movex * delta
            if self.movex >= 1 and self.x < width - 50:
                self.x += self.movex * delta
        if self.movey >= 1 and self.y < height - 70:
            self.y += self.movey * delta
        if self.movey <= -1 and self.y > 0:
            self.y += self.movey * delta

    def power_placing(self, power, dx1=45, dy1=25, dx2=930, dy2=20):
        """
        Adjusting the power position of the player
        """
        if self.facing_right:
            power.x = self.x + dx1
            power.y = self.y + dy1
        else:
            power.x = self.x - dx2
            power.y = self.y + dy2

    def physical_rect(self):
        """
        Physical Rectangle of player
        """
        if self.action != "right":
            self.Rect = pygame.Rect(self.x, self.y, 35, 70)
        elif self.action == "right" and self.facing_right:
            self.Rect = pygame.Rect(self.x+30, self.y, 35, 70)
        elif self.action == "right" and not self.facing_right:
            self.Rect = pygame.Rect(self.x, self.y, 35, 70)

    def status_bar(self, screen, width):
        """
        Hp and XP bars of the player
        """
        if self.player_id == 1:
            self.hp_rect = pygame.Rect(80, 20, self.hp, 20)
            self.xp_rect = pygame.Rect(80, 60, self.xp*2, 20)
            screen.blit(self.photo3x4, (0, 20))
        if self.player_id == 2 or self.player_id == 0:
            self.hp_rect = pygame.Rect(width-80, 20, -self.hp, 20)
            self.xp_rect = pygame.Rect(width-80, 60, -self.xp*2, 20)
            screen.blit(self.photo3x4Fliped, (width-70, 20))
        if self.hp >= 0:
            pygame.draw.rect(screen, (255, 0, 0), self.hp_rect)
        pygame.draw.rect(screen, (0, 0, 255), self.xp_rect)
        if self.xp == self.XP_MAX:
            pygame.draw.rect(screen, (0, 255, 0), self.xp_rect)

    def stand_up_position(self):
        """
        Standard stand up position of the player
        """
        if self.movex or self.movey:
            self.initial_time = time.time()*1000
        if self.defending:
            self.initial_time = time.time()*1000
        if time.time()*1000 - self.initial_time > 400 and self.hp > 0:
            self.action = "down"

    def defeated(self, screen, other_player):
        """
        Show the win picture of the player
        """
        if self.hp <= 0:
            self.action = "lose"
            if self.timing2:
                self.initial_death = time.time()
                self.timing2 = False
            if time.time() - self.initial_death > 1:
                screen.blit(other_player.Win, (380, 200))
