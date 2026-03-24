import pygame

import numpy as np
from classes.platforms import Platform
from classes.player import Player
from classes.enemy import Enemy
from classes.items import Item

placeholder_color = pygame.color.Color(255, 0, 255)

#переменные уровней
berries_count = 0
trigger_next_level = False

def load_level(level_number, tile_size):
    print('got level number ', level_number)
    
    path = ''.join(('levels/', str(level_number), '.csv'))
    print('loading file ', path)
    level = np.genfromtxt(path, delimiter=',', dtype='int')
    print('level loaded')

    level_width, level_height = len(level[0])*tile_size, len(level)*tile_size

    print('level width ', level_width, '| level height ', level_height)

    platforms = pygame.sprite.Group()

    items = []

    enemy = None
    enemy_spawn_xy = None

    for row in range(len(level)):
        for col in range(len(level[row])):
            
            #загрузка платформ
            if level[row][col] == 0:
                
                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/ground_', str(level[row][col]), '.png')))

                    else:
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

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/player_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                player = Player(col*tile_size, row*tile_size, tile_size, tile_size, image)
                

            #загрузка врага
            if level[row][col] == 2:

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/enemy_', str(level[row][col]), '.png')))

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/enemy_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                enemy = Enemy(tile_size, tile_size, image)
                enemy_spawn_xy = [col*tile_size, row*tile_size]
                print('try enemy spawn on ', enemy_spawn_xy)
            
            #загрузка интерактивных предметов
            if level[row][col] == 3: #forest

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/forest_', str(level[row][col]), '.png')))

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/forest_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                #class item сложить в items
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'FOREST', can_interact=True, can_pass=False))

            if level[row][col] == 4: #bush interactable

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/bush_', str(level[row][col]), '.png')))

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/bush_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                #class item сложить в items
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH', can_interact=True))

            if level[row][col] == 5: #bush not interactable

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/bush_', str(level[row][col]), '.png')))

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/bush_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                #class item сложить в items
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH', can_interact=False))



    return platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level

def set_background(number):
    '''
    В будущем тут будет проверяться номер уровня и назначаться фоновое изображение. Но пока что будем просто заливать всё одним цветом.
    '''

    if number == 0:
        color = pygame.color.Color(50, 200, 200)
    else:
        color = pygame.color.Color(163, 70, 56)

    return color

def level_update(number):

    if number == 0:
        if berries_count == 3:
            trigger_next_level = True
            return trigger_next_level

def count_berries():
    global berries_count
    berries_count +=1