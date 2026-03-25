import pygame

from windows.quit_window import game_quit
from animation_manager import set_animation


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
        
        self.speed = 5

        self.on_ground = False
        self.jumping = True
        self.jumps_remaining = 2
        self.gravity = 0.6
        self.jump_power = -5
        self.jump_count_max = 10
        self.jump_count = 0

        self.max_fall_speed = 20

        self.alive = True

        self.animation = set_animation('player_right_idle')
        self.anim = 'idle'
        self.frame = 0
        self.play_speed = 5 #каждые n кадров меняется фрейм анимации
        self.wait_play = 0

        self.direction = 1

    def update(self,screen, platforms, items, camera, enemy):

        #проверка состояний для смены анимации
        
        if self.on_ground:

            if self.velocity_x != 0: #бег
                self.anim = 'run'
                if self.direction == 1:
                    self.animation = set_animation('player_right_' + self.anim)
                    print('self animation ', self.animation)

                elif self.direction == 0:
                    self.animation = set_animation('player_left_' + self.anim)
                    print('self animation ', self.animation)


        
            elif self.velocity_x == 0: #покой
                if self.direction == 1:
                    self.anim = 'idle'
                    self.animation = set_animation('player_right_idle')
                else:
                    self.anim = 'idle'
                    self.animation = set_animation('player_left_idle')

                self.frame = 0
                self.wait_play = 0

        elif not self.on_ground: #прыжок/падение
            if self.direction == 1:
                self.anim = 'jump'
                self.animation = set_animation('player_right_jump')
            else:
                self.anim = 'jump'
                self.animation = set_animation('player_left_jump')

            self.frame = 0
            self.wait_play = 0


        #смена кадров текущей анимации
        self.image = pygame.image.load(self.animation[self.frame])
        #print('current frame', self.frame)
        if self.frame < len(self.animation)-1:
            if self.wait_play >= self.play_speed:
                self.frame +=1
                self.wait_play = 0
            else:
                self.wait_play += 1
        else:
            if self.wait_play >= self.play_speed:
                self.frame = 0
                self.wait_play = 0
            else:
                self.wait_play += 1

        #обработка контролируемого прыжка
        if self.jumping and self.jump_count < self.jump_count_max:
            self.jump_count += 1
            self.velocity_y = self.jump_power + (self.jump_count / self.jump_count_max)
        else:
            if not self.jumping:
                self.jump_count = 0
        
        #гравитация
        #print('on ground is ', self.on_ground)
        if not self.on_ground or self.on_ground:
            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed
            else:
                self.velocity_y += self.gravity
        else:
            self.velocity_y = 0

            """
            СЮДА ВСТАВИТЬ ЗВУК ПРИЗЕМЛЕНИЯ
            НИЖЕ: ПОДУМАТЬ, КАК ВСТАВИТЬ ЗВУКИ БЕГА
            """

        #обновление положения по горизонтали
        self.rect.x += self.velocity_x

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

        for item in items:
            if self.rect.colliderect(item.rect) and not item.can_pass:
                if self.velocity_x > 0:
                    self.rect.right = item.rect.left
                
                elif self.velocity_x < 0:
                    self.rect.left = item.rect.right

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
                    self.jumping = False
                    self.jumps_remaining = 2
                    self.jump_count = 0
                
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = False
                    #print('jumps remaining ', self.jumps_remaining, 'on ground False')

        for item in items:
            if self.rect.colliderect(item.rect) and not item.can_pass:
                if self.velocity_y > 0:
                    self.rect.bottom = item.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumps_remaining = 2
                    self.jump_count = 0
                
                elif self.velocity_y < 0:
                    self.rect.top = item.rect.bottom
                    self.velocity_y = 0
                    self.on_ground = False

        if enemy:
            if self.rect.colliderect(enemy.rect):
                if self.alive:
                    print('THE PLAYER GOT KILLED')
                    enemy.state, enemy.velocity_x = 'IDLE', 0
                    self.alive = False
                    camera.fade_out(screen)

                    """
                    СЮДА ВСТАВИТЬ ЗВУК СМЕРТИ
                    """
            

    def jump(self):
        if self.jumps_remaining == 2 and self.on_ground:
                
            self.velocity_y = self.jump_power
            
            self.jumps_remaining -= 1

            self.jumping = True
            self.on_ground = False

            return True
        elif self.jumps_remaining == 1 and not self.jumping and not self.on_ground: #если не осталось джамп каунт, то не прыгает повторно ИСПРАВИТЬ
            
            self.velocity_y = self.jump_power

            self.jumps_remaining -= 1

            self.jumping = True
            return True
            
        return False
    
    
    """
    СЮДА ДОБАВИТЬ ЗВУКИ ПРЫЖКОВ
    """


    def jump_stop(self): #для контролируемой силы прыжка
        if self.jumping:
            self.jumping = False




    """def animation_player(self, direction=1, anim='idle'):

        if direction == self.direction:
            if anim == self.anim:
                return
        else:
            if direction == 1:
                self.animation = set_animation('player_right_' + anim)

            elif direction == 0:
                self.animation = set_animation('player_left_' + anim)

        
        self.direction = direction"""