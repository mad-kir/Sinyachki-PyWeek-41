import pygame

import sys

pygame.init()

from windows import dead_window
from windows import menu_window
from windows.quit_window import game_quit
from windows.pause_window import pause
from levels.level_manager import load_level, set_background, level_update
from classes.player import Player
from classes.camera import Camera
from classes.enemy import Enemy
from classes.markers import Marker

running = False

current_level = 0

tile_size = 16

trigger_next_level = False

screen_width, screen_height = 1024, 576
#screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((screen_width, screen_height))

def change_level(number, screen, camera):

    """
    СЮДА МОЖНО ВОТКНУТЬ ЗВУК ПЕРЕХОДА НА ДРУГОЙ УРОВЕНЬ
    """

    print('change to level ', number)

    background_color = set_background(number) #пока цвет, потом заменить на картинку
    
    platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level = load_level(number, tile_size, camera, screen) 
    
    camera.set_bounds(level_width, level_height)

    if enemy:
        enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'IDLE', player, level) #заспавнить врага

    screen.fill(background_color)

    

    return background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level




def main():
    global current_level
    global trigger_next_level
    global runnning
    global screen
    global screen_width, screen_height

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    
    
    camera = Camera(screen_width, screen_height)


    '''для отладки, удалить позже'''
    #platforms, level_width, level_height, player, enemy, enemy_spawn_xy, level = load_level(0, tile_size) 
    #background_color = set_background(0)
    #camera.set_bounds(level_width, level_height)
    #enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'CHASE', player, level) #заспавнить врага и назначить следить за игроком

    background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level = change_level(current_level, screen, camera)

    running = True

    while running:
        clock.tick(fps)
        
        #---ОБРАБОТКА СОБЫТИЙ---
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = game_quit(screen, screen_width, screen_height)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    to_menu = pause(screen, screen_width, screen_height)
                    if to_menu == True:
                        #print('to menu is ', to_menu)
                        to_menu = False
                        running = False

                if event.key == pygame.K_TAB:
                    background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level = change_level(1, screen, camera) #ОТЛАДКА, потом удалить
                    current_level = 1

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    player.jump_stop()
                


        
        keys = pygame.key.get_pressed()

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        player.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velocity_x = -player.speed
            player.direction = 0
            #player.animation_player(0, 'run')
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velocity_x = player.speed
            player.direction = 1
            #player.animation_player(1, 'run')

        if jump_pressed:
            player.jump()

        

        
        
        jumping = jump_pressed


        #---ОТРИСОВКА---

        if player.alive:

            screen.fill(background_color)

            for platform in platforms:

                platform_rect_transformed, platform_image_transformed = camera.apply(platform)
                screen.blit(platform_image_transformed, platform_rect_transformed)

            for marker in markers:
                marker_rect_transformed, marker_image_transformed = camera.apply(marker)
                screen.blit(marker_image_transformed, marker_rect_transformed)

            for item in items:
                item_rect_transformed, item_image_transformed = camera.apply(item)
                if item.alive:
                    screen.blit(item_image_transformed, item_rect_transformed)
        
            player_rect_transformed, player_image_transformed = camera.apply(player)
            screen.blit(player_image_transformed, player_rect_transformed)

            if enemy:
                enemy_rect_transformed, enemy_image_transformed = camera.apply(enemy)
                screen.blit(enemy_image_transformed, enemy_rect_transformed)
        
        if not player.alive:
            should_reset = dead_window.game_over(screen, screen_width, screen_height) #enter не всегда срабатывает с первого раза

            if should_reset:
                background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level = change_level(current_level, screen, camera)


        #---ОБНОВЛЕНИЕ ИГРЫ---
        
        for marker in markers:
            marker.update(screen, player, items, current_level)


        for item in items:
            item.update(screen, camera, player, items)
            if item.is_triggered:
                print('item triggered', current_level, item.type)
                if item.type == 'BUSH_BLUE' and current_level == 0:
                    trigger_next_level = True
                    print('trigger level')
                    


        if trigger_next_level:
            current_level += 1
            background_color, platforms, markers, items, level_width, level_height, player, enemy, mobs, enemy_spawn_xy, level = change_level(current_level, screen, camera)
        

        player.update(screen, platforms, items, camera, enemy)

        camera.update(player, screen)

        if enemy:
            enemy.update(platforms, markers, camera, player)

        if len(mobs)>0:
            for mob in mobs:
                mob.update(platforms, markers, camera, player)
        
        if trigger_next_level:
            camera.fade_in(screen, (0, 0, 0), background_color, platforms, items, player)

        pygame.display.flip()


while True:
    game_start = menu_window.show(screen, screen_width, screen_height)
    if game_start == True:
        game_start = False
        running = True
        main()

    if __name__ == '__main__':
        menu_window.show(screen, screen_width, screen_height)