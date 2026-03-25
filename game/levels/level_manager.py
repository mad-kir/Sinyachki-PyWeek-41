import pygame

import numpy as np
from classes.platforms import Platform
from classes.player import Player
from classes.enemy import Enemy
from classes.items import Item
from classes.markers import Marker

placeholder_color = pygame.color.Color(255, 0, 255)

#переменные уровней
berries_count = 0
trigger_next_level = False

def load_level(level_number, tile_size, camera, screen):
    print('got level number ', level_number)
    
    path = ''.join(('levels/', str(level_number), '.csv'))
    print('loading file ', path)
    level = np.genfromtxt(path, delimiter=',', dtype='int')
    print('level loaded')

    level_width, level_height = len(level[0])*tile_size, len(level)*tile_size

    print('level width ', level_width, '| level height ', level_height)

    platforms = pygame.sprite.Group()

    items = []
    markers = []

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
                    image = pygame.image.load('images/animations/enemy_0.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*2, tile_size*2))
                    image.fill(placeholder_color)
                
                enemy = Enemy(tile_size*2, tile_size*2, image)
                enemy_spawn_xy = [col*tile_size, row*tile_size]
                #print('try enemy spawn on ', enemy_spawn_xy)
            
            #загрузка маркеров
            if level[row][col] == 6: #триггер действий, пока только чтобы убрать преграду на 1 уровне

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'TRIGGER'))

            if level[row][col] == 7: #триггер перехода на следующий уровень

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'NEXTLEVEL'))


            #загрузка интерактивных предметов
            if level[row][col] == 3: #forest

                try:
                    if level_number == 0:
                        image = pygame.image.load(''.join(('images/tileset_day/forest_', str(level[row][col]), '.png')))

                    else:
                        image = pygame.image.load(''.join(('images/tileset_night/forest_', str(level[row][col]), '.png')))

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'FOREST', level_number, markers, can_interact=True, can_pass=False))

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
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH', level_number, markers, can_interact=True))

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
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH', level_number, markers, can_interact=False))

            


            


    #camera.fade_in(screen)
    return platforms, markers, items, level_width, level_height, player, enemy, enemy_spawn_xy, level

def set_background(number):
    '''
    В будущем тут будет проверяться номер уровня и назначаться фоновое изображение. Но пока что будем просто заливать всё одним цветом.
    '''

    if number == 0:
        color = pygame.color.Color(50, 200, 200)
    else:
        color = pygame.color.Color(163, 70, 56)

    return color

def level_update(number, camera, screen, markers): ######## СЮДА ДОБАВИТЬ ЗВУКИ ПЕРЕХОДА НА СЛЕДУЮЩИЙ УРОВЕНЬ

    if number == 0:
        if berries_count == 3:
            trigger_next_level = True
            camera.fade_out(screen, (255, 255, 255))
            camera.fade_out(screen, (255, 0, 0))
            camera.fade_out(screen, (0, 0, 0))
            return trigger_next_level

    elif number == 1:
        for marker in markers:
            if marker.type == 'NEXTLEVEL':
                if marker.is_triggered:
                    trigger_next_level = True
                    camera.fade_out(screen, (0, 0, 0))
                    return trigger_next_level

def count_berries():
    global berries_count
    berries_count +=1