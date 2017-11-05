#!/usr/bin/python
import time
import random
import pygame
from .characters import Characters


class NPC(Characters):
    def __init__(self, initial_action, player_id):
        """Iniciation of the player states"""
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
        self.initialTime = 0
        self.timing2 = True
        self.punch_damage = 2
        self.hit_defended = 0.4
        self.power_damage = 10
        self.player_id = player_id
        self.loading = False
        self.super_punch_state = False
        self.super_kick_state = False
        self.factor_super = 1.4
        self.initial_time1 = time.time()*1000
        self.initial_time2 = time.time()*1000
        self.initial_time3 = time.time()*1000
        self.initial_time4 = time.time()*1000
        self.initial_time5 = time.time()*1000
        self.initial_time6 = time.time()*1000
        self.initial_time7 = time.time()*1000
        self.initial_spark = time.time()*1000
        self.initial_explosion = time.time()*1000
        self.kameham_ms = 160
        self.punch_ms = 90
        self.staticy = 0
        self.initial_kame = time.time()*1000
        self.initial_punch = time.time()*1000
        self.initial_effects = time.time()*1000
        self.is_pc = True
        self.single_kameham = True
        self.teleport_boolean = True
        self.kame_cont = 22
        self.attack_rect = None
        self.hp_rect = None
        self.xp_rect = None
        self.initial_death = 0

    def play_effects(self, effects):
        """
        Animation effects of the fight
        """
        if abs(time.time()*1000-self.initial_effects) < 200:
            if random.random() > 0.5 and abs(time.time()*1000-self.initial_spark) > 1500:
                effects.action = "spark"
                if abs(time.time()*1000 - self.initial_spark) > 2500:
                    effects.action = "void"
                    self.initial_spark = time.time()*1000
            if random.random() < 0.5 and abs(time.time()*1000-self.initial_explosion) > 3500:
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
        Movement of the pc, locking it
        on the visible screen
        """
        if self.facing_right:
            if self.movex <= -1 and self.x > 0:
                self.x += self.movex * delta
            if self.movex >= 1 and self.x < width-50:
                self.x += self.movex * delta
        if not self.facing_right:
            if self.movex <= -1 and self.x > 0:
                self.x += self.movex * delta
            if self.movex >= 1 and self.x < width-50:
                self.x += self.movex * delta
        if self.movey >= 1 and self.y < height-70:
            self.y += self.movey * delta
        if self.movey <= -1 and self.y > 0:
            self.y += self.movey * delta

    def power_placing(self, power, dx1=45, dy1=25, dx2=930, dy2=20):
        """
        Adjusting the power position of npc
        """
        if self.facing_right:
            power.x = self.x+dx1
            power.y = self.y+dy1
        else:
            power.x = self.x-dx2
            power.y = self.y+dy2

    def physical_rect(self):
        """
        Physical Rectangle of the npc
        """
        if self.action != "right":
            self.Rect = pygame.Rect(self.x, self.y, 35, 70)
        elif self.action == "right" and self.facing_right:
            self.Rect = pygame.Rect(self.x+30, self.y, 35, 70)
        elif self.action == "right" and not self.facing_right:
            self.Rect = pygame.Rect(self.x, self.y, 35, 70)

    def status_bar(self, screen, width):
        """
        Hp and XP bars of the npc
        """
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
        Standard stand up position of the npc
        """
        if self.movex or self.movey != 0:
            self.initialTime = time.time()
        if self.defending:
            self.initialTime = time.time()
        if time.time()-self.initialTime > 0.4 and self.hp > 0:
            self.action = "down"
            self.initialTime = time.time()+1000

    def defeated(self, screen, other_player):
        """
        Show the win picture of the npc
        """
        if self.hp <= 0:
            #import pdb; pdb.set_trace()
            self.action = "lose"
            if self.timing2:
                self.initial_death = time.time()
                self.timing2 = False
            if time.time()-self.initial_death > 1:
                screen.blit(other_player.Win, (300, 200))

    def super_punch(self, enemy_player):
        """
        Activate the super punch
        """
        if self.super_punch_state:
            if time.time()*1000-self.initial_punch < 200:
                if self.facing_right:
                    enemy_player.movex = 3
                if not self.facing_right:
                    enemy_player.movex = -3
            else:
                enemy_player.movex = 0
                self.super_punch_state = False
        if self.super_kick_state:
            if time.time()*1000-self.initial_punch < 200:
                enemy_player.movey = -3
            else:
                enemy_player.movey = 0
                self.super_kick_state = False

    def teleport(self, enemy_player, width):
        """
        Teleport to a randon place
        """
        if self.teleport_boolean and time.time()*1000-self.initial_time7 > 1100:
            if self.x > width-50 and abs(self.x-enemy_player.x) < 60 or self.x < -5 and abs(self.x-enemy_player.x) < 60:
                self.action = "teleport"
                self.pressed = True
                self.x = random.randint(0, 1170)
                self.y = random.randint(0, 738)
                self.initialTime = time.time()
            if self.y < 0 and abs(self.y - enemy_player.y) < 40:
                self.action = "teleport"
                self.pressed = True
                self.x = random.randint(0, 1170)
                self.y = random.randint(0, 738)
                self.initialTime = time.time()
            self.initial_time7 = time.time()*1000

    def kameham(self, enemy_player, power2):
        """
        Kameham power
        """
        if time.time()*1000-self.initial_time1 > self.kameham_ms and abs(self.y-enemy_player.y) < 50 and\
                not self.loading and abs(self.x-enemy_player.x) > 65:
            if self.xp >= 10:
                if self.single_kameham:
                    self.initial_kame = time.time()*1000
                    self.action = "kameham"
                    power2.action = "kame"
                    self.pressed = True
                    power2.pressed = True
                    self.pos = 1
                    self.attacking = True
                    self.defending = False
                    if not self.facing_right:
                        self.attack_rect = pygame.Rect(self.x-950, self.y+10, 1000, 60)
                        #pygame.draw.rect(screen, (0,255,0), self.attack_rect)
                    elif self.facing_right:
                        self.attack_rect = pygame.Rect(self.x+45, self.y+10, 1000, 60)
                        #pygame.draw.rect(screen, (0,255,0), self.attack_rect)
                    if self.attack_rect.colliderect(enemy_player.Rect):
                        if not enemy_player.defending:
                            enemy_player.hp -= 10
                            enemy_player.action = 'hited'
                            enemy_player.initialTime = time.time()
                        if enemy_player.defending and not enemy_player.attacking:
                            enemy_player.hp -= 2
                    self.xp -= 10
                    self.initialTime = time.time()
                    self.initial_time1 = time.time()*1000

    def punch_kick(self, enemy_player):
        """
        It punchs or kicks
        """
        if abs(self.x-enemy_player.x) < 55 and abs(self.y-enemy_player.y) < 30 and\
                abs(time.time()*1000-self.initial_time2) > self.punch_ms:
            if random.randint(0, 11) > 5:
                self.action = "punch"
            else:
                self.action = "kick"
            self.pressed = True
            self.pos = 1
            self.attacking = True
            self.defending = False
            if self.facing_right:
                self.attack_rect = pygame.Rect(self.x+15, self.y, 70, 70)
                # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
            if not self.facing_right:
                self.attack_rect = pygame.Rect(self.x-15, self.y, 70, 70)
                # pygame.draw.rect(screen, (0,0,255), self.attack_rect)
            self.initial_punch = time.time()*1000
            if self.attack_rect.colliderect(enemy_player.Rect):
                if not enemy_player.defending:
                    if self.xp <= self.XP_MAX:
                        enemy_player.hp -= self.punch_damage*self.factor_super
                    if self.xp == self.XP_MAX:
                        enemy_player.hp -= self.power_damage
                        if random.randint(0, 11) > 5:
                            self.super_punch_state = True
                        else:
                            self.super_kick_state = True

                    if abs(self.x - enemy_player.x) < 30 and abs(enemy_player.initial_punch-self.initial_punch) < 400:
                        pass
                    else:
                        enemy_player.action = "hited"
                    enemy_player.initialTime = time.time()
                if enemy_player.defending and not enemy_player.attacking:
                    enemy_player.hp -= enemy_player.hit_defended
            self.initialTime = time.time()
            self.initial_time2 = time.time()*1000

    def load(self, enemy_player):
        """
        Load XP
        """
        if abs(time.time()*1000-self.initial_time3) > 2000 and abs(self.x-enemy_player.x) > 100:
            self.action = "load"
            self.pressed = True
            self.pos = 1
            if self.xp < self.XP_MAX:
                self.xp += 1
            self.initialTime = time.time()
            self.loading = True
            if abs(time.time()*1000-self.initial_time4) > 3000:
                self.initial_time3 = time.time()*1000
                self.initial_time4 = time.time()*1000
                self.loading = False

    def play_pc(self, enemy_player, power2, resolution):
        """
        Play npc actions
        """
        width, height = resolution
        if self.hp > 0:
            self.super_punch(enemy_player)
            self.teleport(enemy_player, width)
            self.kameham(enemy_player, power2)
            self.punch_kick(enemy_player)
            self.load(enemy_player)

            if abs(time.time()*1000-self.initial_time5) > 2000:
                if enemy_player.y-self.y < 0:
                    self.action = "up"
                    self.pos = 1
                    self.movey =- 1
                    if abs(time.time()*1000-self.initial_time5) > 2350:
                        self.initial_time5 = time.time()*1000
                        self.movey = 0
                        self.pos = 0
                if enemy_player.y-self.y > 0:
                    self.action = "down"
                    self.pos = 1
                    self.movey = 1
                    if abs(time.time()*1000-self.initial_time5) > 2350:
                        self.initial_time5 = time.time()*1000
                        self.movey = 0
                        self.pos = 0
            if abs(enemy_player.x-self.x) > 15 and abs(time.time()*1000-self.initial_time6) > 2000:
                if not self.facing_right:
                    self.action = "right"
                    self.pos = 1
                    self.movex =- 1
                    if abs(time.time()*1000-self.initial_time6) > 2350:
                        self.initial_time6 = time.time()*1000
                        self.movex = 0
                        self.pos = 0
                if self.facing_right:
                    self.action = "down"
                    self.pos = 1
                    self.movex = 1
                    if abs(time.time()*1000-self.initial_time6) > 2350:
                        self.initial_time6 = time.time()*1000
                        self.movex = 0
                        self.pos = 0
