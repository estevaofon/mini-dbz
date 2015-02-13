#!/usr/bin/python
import pygame


class SpriteAnimation:
    def __init__(self, initial_action, speed=15):
        self.action = initial_action
        self.x = 200
        self.y = 0
        self.ani_speed = speed
        self.ani_pos = 0
        self.ani_max = 0
        self.sprite_sheet = None
        self.animation = []
        self.dict_of_rects = {}
        self.animation_speed = {}
        self.local_action = ""
        self.manual_list = []
        # Dictionary to register if the animations is continuous or not.
        self.hold_state = {}
        self.pressed = False
        self.facing_right = True

    def rect_list(self, xo, yo, lx, ly, n):
        """
        Build a list of rectangles sprites
        xo,yo initial points
        lx,ly length of sprites
        n number of sprites
        """
        rect = []
        for i in range(n):
            rect.append(pygame.Rect(xo+lx*i, yo, lx, ly))
        rect.sort()
        return rect

    def insert_frame(self, xo, yo, lx, ly):
        """
        Insert frame by frame manually
        """
        self.manual_list.append(pygame.Rect(xo, yo, lx, ly))

    def build_animation(self, action, hold=False, speed=15):
        """
        Build Animation from the inserted frames and give the animation a label
        """
        self.animation_speed[action] = speed
        self.dict_of_rects[action] = self.manual_list
        self.manual_list = []
        self.hold_state[action] = hold

    def erase_positions(self, action, indexes):
        """
        Erase a rectangle sprite of the self-generated rectangle list
        """
        indexes.sort()
        indexes.reverse()
        local_list = self.dict_of_rects[action]
        for item in indexes:
            local_list.pop(item)
        self.dict_of_rects[action] = local_list

    def repeat_position(self, action, ntimes, indexes):
        """
        Repeat a rectangle sprite of the self-generated rectangle list
        """
        indexes.sort()
        local_list = self.dict_of_rects[action]
        # append at the end n times
        while ntimes != 0:
            for item in indexes:
                local_list.append(local_list[item])
            ntimes = ntimes - 1

    def load_sprites(self, image):
        """
        Load the sprites image
        """
        self.sprite_sheet = (pygame.image.load(image).convert_alpha())

    def create_animation(self, xo, yo, lx, ly, n, action,
                         hold=False, speed=15):
        """
        Create the self-generated list animation and give the animation a label
        """
        self.animation_speed[action] = speed
        # Define Animations
        self.dict_of_rects[action] = self.rect_list(xo, yo, lx, ly, n)
        self.hold_state[action] = hold

    def update(self, screen):
        """
        Run and update the animation
        """
        # new animation starts at 0
        if self.local_action != self.action:
            self.ani_pos = 0
        self.local_action = self.action
        local_rect_list = self.dict_of_rects[self.action]
        self.ani_max = len(local_rect_list)-1
        self.ani_speed -= 1
        if self.ani_speed == 0:
            self.ani_speed = self.animation_speed[self.action]
            # if animation has reached the last position and it is continues
            if self.ani_pos == self.ani_max and self.hold_state[self.action] is False:
                self.ani_pos = 0
            # if its pressed the key and the animation its not continues
            elif self.ani_pos == self.ani_max and self.hold_state[self.action] and self.pressed:
                self.ani_pos = 0
                self.pressed = False
            # if the animation has reached the last position and its continues
            elif self.hold_state[self.action] is False:
                self.ani_pos += 1
            # if the animation has reached the last position and isnt continues
            elif self.hold_state[self.action] and self.ani_pos < self.ani_max:
                self.ani_pos += 1
                self.pressed = False
        if self.facing_right:
            try:
                cropped = self.sprite_sheet.subsurface(local_rect_list[self.ani_pos]).copy()
            except IndexError:
                self.ani_pos = 0
                cropped = self.sprite_sheet.subsurface(local_rect_list[self.ani_pos]).copy()
                print("List index out of range ocurred and treated")
            screen.blit(cropped, (self.x, self.y))
        if self.facing_right is False:
            try:
                cropped = self.sprite_sheet.subsurface(local_rect_list[self.ani_pos]).copy()
                new_image = pygame.transform.flip(cropped, True, False)
            except IndexError:
                self.ani_pos = 0
                cropped = self.sprite_sheet.subsurface(local_rect_list[self.ani_pos]).copy()
                new_image = pygame.transform.flip(cropped, True, False)
                print("List index out of range ocurred and treated")
            screen.blit(new_image, (self.x, self.y))
