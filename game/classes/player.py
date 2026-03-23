import pygame

from windows.quit_window import game_quit


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        
        self.x = x
        self.y = y

        self.width, self.height = width, height

        self.image_surface = pygame.Surface((width, height))

        self.image = image

        self.rect = self.image_surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocity_x = 0
        self.velocity_y = 0
        
        self.speed = 6

        self.on_ground = False
        self.jumps_remaining = 2
        self.gravity = 0.5
        self.jump_power = -5
        self.max_fall_speed = 15

        self.alive = True

    def update(self, platforms, enemy):
        
        #гравитация
        #print('on ground is ', self.on_ground)
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
        #old_on_ground = self.on_ground
        #self.on_ground = False
        
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                #print('collided with a platform')
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumps_remaining = 2
                    #print('jumps remaining 2, on ground True')
                
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = False
                    #print('jumps remaining ', self.jumps_remaining, 'on ground False')

        if self.rect.colliderect(enemy.rect):
            print('THE PLAYER GOT KILLED')

    def jump(self):
        #print('jump is triggered. at start, jumps remaining ', self.jumps_remaining, ' and on ground is ', self.on_ground)
        if self.jumps_remaining == 2 and self.on_ground:
            self.velocity_y = self.jump_power
            self.jumps_remaining -= 1
            self.on_ground = False
            #print('after, jumps remaining ', self.jumps_remaining, ' and on ground is ', self.on_ground)
            return True
        elif self.jumps_remaining == 1 and not self.on_ground:
            self.velocity_y = self.jump_power
            self.jumps_remaining -= 1
            return True
        return False

