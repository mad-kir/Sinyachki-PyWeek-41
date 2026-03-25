from re import I, L
import pygame

import numpy as np
import time

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
        
        self.speed = 5

        self.on_ground = False
        self.gravity = 0.5
        self.jump_power = -7
        self.max_fall_speed = 10

        self.alive = False

        self.target = None
        self.state = 'IDLE'

        self.detect_timer = None
        self.detect_delay = 1

        self.cannot_reach_count = 0

        level = np.array([])

    def destroy_enemy(self):
        self.alive = False
        self.rect = pygame.Rect(0, 0, 0, 0)
        print('enemy destroyed')
        
    def create_enemy(self, x, y, state, target, level):
        self.alive = True
        self.state = state
        self.target = target

        self.rect = self.image_surface.get_rect()
        self.x, self.y = x, y
        self.rect.x, self.rect.y = x, y

        self.level = level

        print('enemy spawned on ', self.x, self.y)

    # метод движения по горизонтали

    def move_x(self, direction):
        if direction == -1:
            self.velocity_x = -self.speed
        elif direction == 1:
            self.velocity_x = self.speed

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
    
    def update(self, platforms, markers, camera, player):

        if not self.alive or not self.target.alive:
            return


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
        
        if self.cannot_reach_count >= 1000:
            self.cannot_reach_count = 0
            self.target = player
            self.destroy_enemy()
            self.create_enemy(self.target.rect.x-(camera.width/(camera.zoom*0.5)), self.target.rect.y, self.state, self.target, self.level)

        if self.state == 'IDLE':
            if abs(self.rect.x - self.target.rect.x) < camera.width/(camera.zoom*2): #условие для начала погони
                print('distance ', abs(self.rect.x - self.target.rect.x), 'camera width /zoom*2 ', camera.width/(camera.zoom*2), '| can see the player')
                
                if self.detect_timer == None:
                    self.detect_timer = time.time()

                print('the enemy is processing...')
                time_passed = time.time() - self.detect_timer
                if time_passed >= self.detect_delay:
                    print('start chasing')
                    self.state = 'CHASE'

        if self.state == 'SEARCH':
            
            target_location_x = int(self.target.rect.x / 16) #делим на размер тайла
            target_location_y = int(self.target.rect.y / 16)

            self_location_x = int(self.rect.x / 16)
            self_location_y = int(self.rect.y / 16)

            can_pass = self.check_platforms(self_location_x, self_location_y, target_location_x, target_location_y, markers)
            #print('can pass = ', can_pass)

        if self.state == 'CHASE':
            if abs(self.rect.x - self.target.rect.x) > camera.width/(camera.zoom): #условие для исчезновения и спавна за пределами экрана
                
                found, create_on_y = self.find_place_to_create(camera, platforms)
                if found:
                    
                    self.create_enemy(self.target.rect.x-(camera.width/(camera.zoom*0.5)), self.target.rect.y, 'SEARCH', player, self.level)
                else:
                    return

            target_location_x = int(self.target.rect.x / 16) #делим на размер тайла
            target_location_y = int(self.target.rect.y / 16)

            self_location_x = int(self.rect.x / 16)
            self_location_y = int(self.rect.y / 16)

            can_pass = self.check_platforms(self_location_x, self_location_y, target_location_x, target_location_y, markers)

            
    def find_place_to_create(self, camera, platforms):
        check_rect = pygame.Rect(self.target.rect.x-int(camera.width/(camera.zoom*4)), self.target.rect.y, self.rect.width, self.rect.height)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                check_rect.y -= check_rect.height
            else:
                return True, check_rect.y
        return False, 0
        

    def check_platforms(self, self_location_x, self_location_y, target_location_x, target_location_y, markers):
        #print('checking for platforms..')

        level = self.level

        dist_x = abs(self_location_x - target_location_x) #count distance
        dist_y = abs(self_location_y - target_location_y)

        if self_location_x == target_location_x: #доработать, что делать если игрок находится под
            self.jump()

        if self_location_x <= target_location_x:
            step = 1
        else:
            step = -1

        check_y = self_location_y
        road_found_x = 0
        road_found_y = 0

        
        for check_x in range(self_location_x, target_location_x, step):
            if level[check_y][check_x] == -1:
                if level[check_y+1][check_x] == 0: #way is free with a floor
                    road_found_x += 1
                else: #way is free but no floor, starting to search for the floor
                    check_y += 1
                    while level[check_y][check_x] != 0:
                        check_y += 1
                self.move_x(step)
            else: #block ahead
                if level[check_y-2][check_x] == -1: #the second tile from above is free
                    check_y -= 2
                    self.jump()
                    self.move_x(step)
                else:
                    self.cannot_reach_count += 1
                    #print('cannot reach ', self.cannot_reach_count)
                    #set target (create some sort of target in the oposite direction)
                    if self.cannot_reach_count == 1000:
                        return False




