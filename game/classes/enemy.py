import pygame
import random

import pygame.surface

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, image):
        super().__init__()
        
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

        self.image_surface = pygame.Surface((width, height))
        self.image = image

        self.rect = self.image_surface.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.speed = 6

        self.on_ground = False
        self.gravity = 0.5
        self.jump_power = -5
        self.max_fall_speed = 15

        self.alive = False

        self.target = None
        self.state = 'IDLE'

    def destroy_enemy(self):
        self.alive = False
        self.rect = pygame.Rect(0, 0, 0, 0)
        
    def create_enemy(self, x, y, state, target):
        self.alive = True
        self.state = state
        self.target = target

        self.rect = self.image_surface.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y

        print('enemy spawned on ', self.x, self.y)

    # метод движения по горизонтали

    def jump(self):
        self.velocity_y = self.jump_power
        self.jumps_remaining -= 1
        self.on_ground = False
    
    def update(self, platforms):

        # гравитация
        if not self.on_ground or self.on_ground:
            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed
            else:
                self.velocity_y += self.gravity
        else:
            self.velocity_y = 0

        #обновление положения по горизонтали
        self.rect.x += self.velocity_x

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

        #обновление положения по вертикали
        self.rect.y += self.velocity_y

        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = False

        # дерево решений