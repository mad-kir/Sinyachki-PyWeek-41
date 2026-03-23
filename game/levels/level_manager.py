import pygame

import numpy as np
from classes.platforms import Platform
from classes.player import Player
from classes.enemy import Enemy

placeholder_color = pygame.color.Color(255, 0, 255)

def load_level(level_number, tile_size):
    
    level = np.genfromtxt(''.join(('levels/', str(level_number), '.csv')), delimiter=',', dtype='int')
    
    print('level loaded')

    level_width, level_height = len(level[0])*tile_size, len(level)*tile_size

    print('level width ', level_width, '| level height ', level_height)

    platforms = pygame.sprite.Group()

    for row in range(len(level)):
        for col in range(len(level[row])):
            
            #загрузка платформ
            if level[row][col] == 0:
                
                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/ground_', str(level[row][col]), '.png')))
                    else:

                        '''
                        нарисовать плейсхолдер для ночи, сделать 1 уровень
                        '''

                        image = pygame.image.load(''.join(('images/tileset_night/ground_', str(level[row][col]), '.png')))
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                    
                platforms.add(Platform(col*tile_size, row*tile_size, tile_size, image))

            #загрузка игрока
            if level[row][col] == 1:

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/player_', str(level[row][col]), '.png')))
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                player = Player(col*tile_size, row*tile_size, tile_size, tile_size, image)
                

            #врага
            if level[row][col] == 2:

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/enemy_', str(level[row][col]), '.png')))
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                enemy = Enemy(tile_size, tile_size, image)
                enemy_spawn_xy = [col*tile_size, row*tile_size]
                print('try enemy spawn on ', enemy_spawn_xy)
            #интерактивных предметов



    return platforms, level_width, level_height, player, enemy, enemy_spawn_xy, level

def set_background(number):
    '''
    В будущем тут будет проверяться номер уровня и назначаться фоновое изображение. Но пока что будем просто заливать всё одним цветом.
    '''
    return pygame.color.Color(50, 200, 200)