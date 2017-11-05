#!/usr/bin/python
import pygame
from .spriteanimation import SpriteAnimation


class Characters(SpriteAnimation):
    def __init__(self, initial_action, player_id):
        """Initiation of the player states"""
        SpriteAnimation.__init__(self, initial_action)
        self.pos = 1
        self.pos2 = 1
        self.movex, self.movey = 0, 0
        self.facing_right = True
        self.x = 250
        self.y = 350
        self.Rect = pygame.Rect(self.x, self.y, 35, 70)
        self.Win = None
        self.player_id = player_id
        self.photo3x4 = None
        self.photo3x4Fliped = None

    def load_character(self, character):
        """
        Load the images of a specific character
        """
        if character == 'goku':
            photo3x4_img = "resources/imagens/player/goku/ss4/gokuPhoto.png"
            self.photo3x4 = pygame.image.load(photo3x4_img).convert_alpha()
            self.photo3x4Fliped = pygame.transform.flip(self.photo3x4, 1, 0)
            win_img = "resources/imagens/player/goku/ss4/gokuWin.png"
            self.Win = pygame.image.load(win_img).convert_alpha()
            sprite = "resources/imagens/player/goku/ss4/goku-ss4.png"
            self.load_sprites(sprite)
            self.create_animation(0, 0, 48, 70, 4, "down", hold=False)
            self.create_animation(6, 200, 51, 70, 4, "up")
            self.erase_positions("up", [0, 2])
            self.repeat_position("up", 1, [1])
            self.create_animation(0, 72, 65, 70, 4, "right")
            self.create_animation(164, 2272, 56, 70, 4, "defend")
            self.erase_positions("defend", [0, 1, 3])
            self.create_animation(164, 1500, 57, 80, 10,
                                  "kameham", hold=True, speed=1)
            self.erase_positions("kameham", [6, 7, 8, 9])
            # Punch
            self.insert_frame(120, 367, 58, 60)
            self.insert_frame(180, 367, 58, 60)
            self.insert_frame(211, 1674, 65, 60)
            self.insert_frame(249, 367, 65, 60)
            # hold to maintain last frame
            self.build_animation("punch", hold=True, speed=5)
            # kick
            self.insert_frame(113, 443, 57, 60)
            self.insert_frame(166, 443, 60, 60)
            self.insert_frame(235, 443, 66, 60)
            self.insert_frame(303, 443, 66, 60)
            self.insert_frame(375, 443, 68, 60)
            self.insert_frame(448, 443, 68, 60)
            self.insert_frame(375, 443, 58, 60)
            self.build_animation("kick", hold=True, speed=5)
            # lose
            self.insert_frame(855, 3354, 40, 60)
            self.build_animation("lose", hold=False, speed=10)
            # loading
            self.insert_frame(115, 1400, 83, 90)
            self.insert_frame(195, 1400, 83, 90)
            self.build_animation("load", hold=True, speed=15)
            # hited
            self.insert_frame(65, 900, 52, 90)
            self.insert_frame(170, 900, 80, 90)
            self.build_animation("hited", hold=False, speed=15)
            # combo
            self.insert_frame(119, 1653, 50, 80)
            self.insert_frame(167, 1653, 47, 80)
            self.insert_frame(114, 1728, 50, 80)
            self.insert_frame(168, 1730, 50, 80)
            self.insert_frame(217, 1730, 70, 80)
            self.insert_frame(284, 1730, 70, 80)
            self.insert_frame(349, 1730, 50, 80)
            self.insert_frame(402, 1730, 50, 80)
            # puch-combo
            self.insert_frame(120, 367, 58, 60)
            self.insert_frame(180, 367, 58, 60)
            self.insert_frame(211, 1674, 65, 60)
            self.insert_frame(249, 367, 65, 60)
            # kick-combo
            self.insert_frame(113, 443, 57, 60)
            self.insert_frame(166, 443, 60, 60)
            self.insert_frame(235, 443, 66, 60)
            self.insert_frame(303, 443, 66, 60)
            self.insert_frame(375, 443, 68, 60)
            self.insert_frame(448, 443, 68, 60)
            self.insert_frame(375, 443, 58, 60)
            self.insert_frame(454, 1730, 50, 80)
            self.build_animation("combo", hold=True, speed=5)
            # teleport
            self.insert_frame(119, 1653, 50, 80)
            self.insert_frame(167, 1653, 47, 80)
            self.build_animation("teleport", hold=True, speed=5)
            # dispute
            self.insert_frame(498, 1815, 55, 60)
            self.insert_frame(560, 1815, 55, 60)
            self.build_animation("dispute", hold=True, speed=5)
        if character == 'vegeta':
            photo3x4_img = "resources/imagens/player/vegeta/vegeta-2.png"
            self.photo3x4 = pygame.image.load(photo3x4_img).convert_alpha()
            self.photo3x4Fliped = pygame.transform.flip(self.photo3x4, 1, 0)
            win_img = "resources/imagens/player/vegeta/vegetaWin.jpeg"
            self.Win = pygame.image.load(win_img).convert_alpha()
            sprite = "resources/imagens/player/vegeta/vegeta-ss4-2.png"
            self.load_sprites(sprite)
            self.insert_frame(381, 68, 40, 80)
            self.insert_frame(419, 68, 36, 80)
            self.insert_frame(453, 68, 40, 80)
            self.insert_frame(491, 68, 40, 80)
            self.build_animation("down", hold=False, speed=10)
            # lose
            self.insert_frame(840, 1407, 40, 80)
            self.build_animation("lose", hold=False, speed=10)
            # back
            self.insert_frame(49, 982, 48, 80)
            self.build_animation("up", hold=False, speed=10)
            # left
            self.insert_frame(0, 161, 55, 55)
            self.build_animation("right", hold=False, speed=10)
            # right
            self.insert_frame(634, 84, 46, 55)
            self.build_animation("defend", hold=False, speed=10)
            # punch
            self.insert_frame(57, 417, 55, 55)
            self.insert_frame(110, 417, 70, 55)
            self.insert_frame(175, 417, 65, 55)
            self.build_animation("punch", hold=True, speed=5)
            # kick
            self.insert_frame(56, 594, 41, 75)
            self.insert_frame(96, 594, 55, 75)
            self.insert_frame(155, 594, 65, 75)
            self.build_animation("kick", hold=True, speed=4)
            # kameham
            self.insert_frame(225, 2007, 55, 75)
            self.insert_frame(274, 2007, 55, 75)
            self.insert_frame(325, 2007, 70, 75)
            self.build_animation("kameham", hold=True, speed=5)
            # loading
            self.insert_frame(112, 1274, 95, 85)
            self.insert_frame(200, 1274, 95, 85)
            self.build_animation("load", hold=True, speed=5)
            # hited
            self.insert_frame(0, 1400, 48, 75)
            self.insert_frame(48, 1400, 43, 75)
            self.build_animation("hited", hold=False, speed=15)
            # teleport
            self.insert_frame(642, 289, 50, 80)
            self.build_animation("teleport", hold=True, speed=5)
            # dispute
            self.insert_frame(333, 2012, 55, 60)
            self.insert_frame(390, 2012, 55, 60)
            self.build_animation("dispute", hold=False, speed=10)
        if character == 'trunks':
            photo3x4_img = "resources/imagens/player/trunks/trunks3x4.png"
            self.photo3x4 = pygame.image.load(photo3x4_img).convert_alpha()
            self.photo3x4Fliped = pygame.transform.flip(self.photo3x4, 1, 0)
            if self.player_id == 2:
                win_img = "resources/imagens/player/trunks/win2.jpg"
                self.Win = pygame.image.load().convert_alpha(win_img)
                self.Win = pygame.transform.flip(self.Win, 1, 0)
            else:
                win_img = "resources/imagens/player/trunks/win2.jpg"
                self.Win = pygame.image.load(win_img).convert_alpha()
            self.load_sprites("resources/imagens/player/trunks/trunks.png")
            self.insert_frame(37, 18, 50, 75)
            self.insert_frame(84, 18, 50, 75)
            self.build_animation("down", hold=False, speed=15)
            self.insert_frame(760, 118, 50, 85)
            self.build_animation("up", hold=False, speed=15)
            self.insert_frame(28, 994, 60, 95)
            self.build_animation("right", hold=False, speed=15)
            self.insert_frame(226, 1630, 50, 85)
            self.insert_frame(272, 1630, 50, 85)
            self.insert_frame(318, 1630, 50, 85)
            self.build_animation("kameham", hold=True, speed=5)
            self.insert_frame(272, 1630, 50, 85)
            self.insert_frame(318, 1630, 50, 85)
            self.build_animation("dispute", hold=False, speed=5)
            self.insert_frame(239, 2524, 50, 85)
            self.build_animation("hited", hold=True, speed=5)
            self.insert_frame(814, 2772, 130, 135)
            self.insert_frame(940, 2772, 130, 135)
            self.build_animation("load", hold=True, speed=5)
            self.insert_frame(553, 2752, 100, 75)
            self.build_animation("lose", hold=False, speed=15)
            self.insert_frame(85, 2304, 48, 95)
            self.build_animation("defend", hold=False, speed=15)
            self.insert_frame(155, 1124, 60, 95)
            self.insert_frame(216, 1103, 90, 130)
            self.insert_frame(304, 1140, 90, 130)
            self.insert_frame(401, 1122, 100, 130)
            self.build_animation("punch", hold=False, speed=5)
            self.insert_frame(370, 682, 50, 85)
            self.insert_frame(536, 500, 70, 85)
            self.build_animation("kick", hold=True, speed=5)
            self.insert_frame(597, 1115, 70, 90)
            self.build_animation("teleport", hold=True, speed=5)
        if character == 'frieza':
            photo3x4_img = "resources/imagens/player/frieza/frieza3x4.png"
            self.photo3x4 = pygame.image.load(photo3x4_img).convert_alpha()
            self.photo3x4Fliped = pygame.transform.flip(self.photo3x4, 1, 0)
            win_img = "resources/imagens/player/frieza/win.png"
            self.Win = pygame.image.load(win_img).convert_alpha()
            self.load_sprites("resources/imagens/player/frieza/frieza-3.png")
            self.insert_frame(29, 98, 40, 65)
            self.insert_frame(73, 98, 40, 65)
            self.build_animation("down", hold=False, speed=10)
            self.insert_frame(110, 1170, 55, 85)
            self.insert_frame(163, 1170, 55, 85)
            self.build_animation("up", hold=False, speed=10)
            self.insert_frame(23, 200, 65, 75)
            self.insert_frame(91, 200, 65, 75)
            self.build_animation("right", hold=False, speed=10)
            self.insert_frame(75, 2490, 65, 75)
            self.build_animation("hited", hold=False, speed=10)
            self.insert_frame(256, 2500, 80, 90)
            self.build_animation("lose", hold=False, speed=10)
            self.insert_frame(289, 1742, 120, 90)
            self.insert_frame(408, 1742, 120, 90)
            self.build_animation("load", hold=False, speed=10)
            self.insert_frame(23, 522, 50, 80)
            self.insert_frame(80, 522, 50, 80)
            self.insert_frame(143, 522, 78, 80)
            self.insert_frame(234, 522, 78, 80)
            self.insert_frame(306, 522, 50, 80)
            self.insert_frame(358, 522, 50, 80)
            self.build_animation("kick", hold=False, speed=5)
            self.insert_frame(148, 1888, 100, 60)
            self.insert_frame(262, 1888, 100, 60)
            self.insert_frame(456, 2598, 60, 60)
            self.insert_frame(522, 2598, 60, 60)
            self.insert_frame(580, 2598, 60, 60)
            self.insert_frame(640, 2598, 60, 60)
            self.build_animation("punch", hold=True, speed=4)
            self.insert_frame(405, 100, 55, 65)
            self.build_animation("defend", hold=False, speed=15)
            self.insert_frame(318, 193, 70, 80)
            self.build_animation("teleport", hold=True, speed=5)
            self.insert_frame(331, 2165, 70, 100)
            self.insert_frame(395, 2147, 65, 120)
            self.insert_frame(458, 2180, 65, 90)
            self.insert_frame(609, 2180, 75, 80)
            self.build_animation("kameham", hold=False, speed=5)
            self.insert_frame(443, 2080, 90, 75)
            self.insert_frame(544, 2080, 80, 85)
            self.build_animation("dispute", hold=True, speed=5)
        if character == 'gohan':
            photo3x4_img = "resources/imagens/player/gohan/gohan3x4.png"
            self.photo3x4 = pygame.image.load(photo3x4_img).convert_alpha()
            self.photo3x4Fliped = pygame.transform.flip(self.photo3x4, 1, 0)
            win_img = "resources/imagens/player/gohan/win.png"
            self.Win = pygame.image.load(win_img).convert_alpha()
            self.load_sprites("resources/imagens/player/gohan/gohan.png")
            self.insert_frame(10, 53, 50, 80)
            self.insert_frame(57, 53, 50, 80)
            self.build_animation("down", hold=False, speed=10)
            self.insert_frame(167, 330, 50, 85)
            self.insert_frame(65, 330, 50, 85)
            self.build_animation("up", hold=False, speed=10)
            self.insert_frame(12, 150, 70, 85)
            self.insert_frame(83, 150, 70, 85)
            self.build_animation("right", hold=False, speed=10)
            self.insert_frame(83, 947, 57, 85)
            self.insert_frame(190, 947, 57, 85)
            self.build_animation("hited", hold=False, speed=10)
            self.insert_frame(28, 1105, 90, 105)
            self.insert_frame(118, 1105, 90, 105)
            self.build_animation("load", hold=False, speed=10)
            self.insert_frame(74, 442, 57, 80)
            self.build_animation("defend", hold=False, speed=10)
            self.insert_frame(15, 1412, 57, 80)
            self.build_animation("teleport", hold=True, speed=10)
            self.insert_frame(70, 564, 60, 80)
            self.insert_frame(127, 564, 60, 80)
            self.insert_frame(182, 564, 75, 80)
            self.build_animation("punch", hold=True, speed=2)
            self.insert_frame(122, 656, 60, 80)
            self.insert_frame(180, 656, 64, 80)
            self.insert_frame(255, 656, 64, 80)
            self.insert_frame(326, 656, 69, 80)
            self.insert_frame(406, 656, 69, 80)
            self.insert_frame(479, 656, 69, 80)
            self.build_animation("kick", hold=True, speed=5)
            self.insert_frame(495, 1740, 69, 80)
            self.insert_frame(160, 1740, 69, 80)
            self.insert_frame(292, 1740, 69, 80)
            self.build_animation("kameham", hold=False, speed=5)
            self.insert_frame(216, 1420, 72, 80)
            self.insert_frame(346, 1420, 72, 80)
            self.build_animation("dispute", hold=False, speed=10)
            self.insert_frame(460, 1065, 80, 80)
            self.build_animation("lose", hold=False, speed=10)

    def load_power(self, power):
        """
        Load power images
        """
        sprite = "resources/imagens/player/goku/ss4/power-1.png"
        power.load_sprites(sprite)
        power.create_animation(1300, 1604, 146, 40, 1, "void")
        power.insert_frame(0, 132, 1100, 50)  # Full Power
        power.insert_frame(0, 132, 1100, 50)  # Full Power
        power.insert_frame(0, 132, 1100, 50)  # Full Power
        power.insert_frame(1300, 1604, 146, 40)  # void
        power.build_animation("kame", hold=True, speed=10)
        power.insert_frame(10, 370, 1200, 50)
        power.insert_frame(10, 480, 1200, 50)
        power.insert_frame(10, 370, 1200, 50)
        power.insert_frame(10, 540, 1200, 50)
        power.build_animation("dispute", hold=False, speed=10)
        power.insert_frame(10, 851, 1200, 50)
        power.insert_frame(10, 914, 1200, 50)
        power.build_animation("dispute2", hold=False, speed=10)
        power.insert_frame(10, 972, 1200, 50)
        power.insert_frame(10, 1037, 1200, 50)
        power.build_animation("dispute3", hold=False, speed=10)
        power.insert_frame(10, 600, 1200, 50)  # void
        power.insert_frame(10, 660, 1200, 50)  # void
        power.build_animation("from-right", hold=True, speed=10)
        power.insert_frame(3, 720, 1200, 50)  # void
        power.build_animation("from-left", hold=True, speed=10)
        power.insert_frame(266, 1580, 50, 50)
        power.insert_frame(108, 1486, 40, 40)
        power.insert_frame(72, 1486, 40, 40)
        power.insert_frame(295, 1486, 40, 40)
        power.build_animation("spark", hold=False, speed=10)
        power.insert_frame(506, 2850, 100, 110)
        power.insert_frame(506, 2850, 100, 110)
        power.insert_frame(358, 2883, 77, 90)
        power.insert_frame(1300, 1604, 146, 40)  # void
        power.build_animation("explosion", hold=False, speed=20)
        power.insert_frame(358, 2434, 98, 90)
        power.insert_frame(449, 2434, 98, 90)
        power.build_animation("ki", hold=False, speed=20)
