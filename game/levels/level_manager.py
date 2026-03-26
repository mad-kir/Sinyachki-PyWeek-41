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

    mobs = []
    mobs_spawn_xy = []

    for row in range(len(level)):
        for col in range(len(level[row])):
            
            #загрузка платформ
            if level[row][col] in range(16) or level[row][col] == 31:
                
                try:
                    
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                    
                platforms.add(Platform(col*tile_size, row*tile_size, tile_size, image))

            #загрузка игрока
            if level[row][col] == 32:

                try:
                    image = pygame.image.load('images/animations/player_0.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                player = Player(col*tile_size, row*tile_size, tile_size, tile_size, image)
                

            #загрузка врага
            if level[row][col] == 33: #вампир

                try:
                    image = pygame.image.load('images/animations/enemy_0.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*2, tile_size*2))
                    image.fill(placeholder_color)
                
                enemy = Enemy(tile_size*2, tile_size*2, image, 'VAMPIRE')
                enemy_spawn_xy = [col*tile_size, row*tile_size]
                #print('try enemy spawn on ', enemy_spawn_xy)

            if level[row][col] == 34: #волк

                try:
                    image = pygame.image.load('images/animations/wolf_0.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*2, tile_size*2))
                    image.fill(placeholder_color)
                
                mobs_spawn_xy.append([col*tile_size, row*tile_size])
                mobs.append(Enemy(tile_size*2, tile_size*2, image, 'WOLF'))

                
                #enemy_spawn_xy = [col*tile_size, row*tile_size]

            if level[row][col] == 35: #терновый куст

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')

                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                
                mobs_spawn_xy.append([col*tile_size, row*tile_size])
                mobs.append(Enemy(tile_size, tile_size, image, 'THORNS'))
                #enemy_spawn_xy = [col*tile_size, row*tile_size]
            
            #загрузка маркеров
            if level[row][col] == 80: #триггер перехода на следующий уровень

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'NEXTLEVEL'))

            
            if level[row][col] == 81: #триггер действий 1

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'TRIGGER_1'))

            if level[row][col] == 82: #триггер действий 2

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'TRIGGER_2'))

            if level[row][col] == 83: #триггер действий 2

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'TRIGGER_3'))

            if level[row][col] == 84: #триггер действий 2

                image = pygame.Surface((tile_size, tile_size*6)) #16x96
                image.fill(placeholder_color)
                
                markers.append(Marker(col*tile_size, row*tile_size, tile_size, tile_size*6, image, 'TRIGGER_4'))

            

            #загрузка интерактивных предметов
            if level[row][col] == 16: #bridge 1

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'BRIDGE_1', level_number, markers, can_interact=False, can_pass=False))
            if level[row][col] == 18: #bridge 2

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'BRIDGE_2', level_number, markers, can_interact=False, can_pass=False))
            if level[row][col] == 20: #bridge 3

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'BRIDGE_3', level_number, markers, can_interact=False, can_pass=False))
            if level[row][col] == 22: #bridge 4

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'BRIDGE_4', level_number, markers, can_interact=False, can_pass=False))


            if level[row][col] == 23: #forest

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size*10, tile_size*10))
                    image.fill(placeholder_color)
                
                items.append(Item(col * tile_size, row * tile_size - (tile_size*10 - tile_size), tile_size*10, tile_size*10, image, 'FOREST', level_number, markers, can_interact=True, can_pass=False))

            if level[row][col] == 48: #bush interactable red

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH_RED', level_number, markers, can_interact=True))

            if level[row][col] == 49: #bush interactable blue

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH_BLUE', level_number, markers, can_interact=True))

            if level[row][col] == 50: #bush not interactable

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH', level_number, markers, can_interact=False))

            if level[row][col] == 64: #lever 1

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'LEVER_1', level_number, markers, can_interact=True))

            if level[row][col] == 66: #lever 2

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'LEVER_2', level_number, markers, can_interact=True))

            if level[row][col] == 68: #lever 3

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'LEVER_3', level_number, markers, can_interact=True))

            if level[row][col] == 96: #tree big 1

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_BIG_1', level_number, markers, can_interact=False))

            if level[row][col] == 97: #tree big 2

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_BIG_2', level_number, markers, can_interact=False))

            if level[row][col] == 98: #tree big 3

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_BIG_3', level_number, markers, can_interact=False))

            if level[row][col] == 99: #tree giant

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_GIANT', level_number, markers, can_interact=False))

            if level[row][col] == 100: #tree medium 1

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_MEDIUM_1', level_number, markers, can_interact=False))

            if level[row][col] == 101: #tree medium 2

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_MEDIUM_2', level_number, markers, can_interact=False))

            if level[row][col] == 102: #tree small

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'TREE_SMALL', level_number, markers, can_interact=False))

            if level[row][col] == 103: #bush small red

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH_SMALL_RED', level_number, markers, can_interact=False))

            if level[row][col] == 104: #bush small

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH_SMALL', level_number, markers, can_interact=False))

            if level[row][col] == 105: #bush small blue

                try:
                    image = pygame.image.load('images/tileset/_' + str(level[row][col]) + '.png')
                
                except:
                    print('failed to load textures on tile ', row, col, ' with index ', level[row][col], '. Filling with pink color instead')
                    image = pygame.Surface((tile_size, tile_size))
                    image.fill(placeholder_color)
                
                items.append(Item(col*tile_size, row*tile_size, tile_size, tile_size, image, 'BUSH_SMALL_BLUE', level_number, markers, can_interact=False))



    camera.fade_in(screen, (0, 0, 0), set_background(level_number), platforms, items, player)
    return platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, mobs_spawn_xy, level

def set_background(number):
    '''
    В будущем тут будет проверяться номер уровня и назначаться фоновое изображение. Но пока что будем просто заливать всё одним цветом.
    '''

    if number == 0:
        color = pygame.color.Color(50, 200, 200)
    elif number == 1:
        color = pygame.color.Color(163, 70, 56)
    else:
        color = pygame.color.Color(20, 0, 100)

    return color

def level_update(number, camera, screen, markers, items): ######## СЮДА ДОБАВИТЬ ЗВУКИ ПЕРЕХОДА НА СЛЕДУЮЩИЙ УРОВЕНЬ

    if number == 0:
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