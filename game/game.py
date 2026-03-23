import pygame

pygame.init()

from windows import dead_window
from windows.quit_window import game_quit
from levels.level_manager import load_level, set_background
from classes.player import Player
from classes.camera import Camera
from classes.enemy import Enemy

current_level = 0

tile_size = 16

def change_level(number, screen, camera):

    """
    СЮДА МОЖНО ВОТКНУТЬ ЗВУК ПЕРЕХОДА НА ДРУГОЙ УРОВЕНЬ
    """

    print('change to level ', number)

    background_color = set_background(number) #пока цвет, потом заменить на картинку
    
    platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level = load_level(number, tile_size) 
    
    camera.set_bounds(level_width, level_height)

    if enemy:
        enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'IDLE', player, level) #заспавнить врага

    screen.fill(background_color)

    

    return background_color, platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level


def main():
    global current_level

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    screen_width, screen_height = 1024, 576
    #screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    

    camera = Camera(screen_width, screen_height)


    '''для отладки, удалить позже'''
    #platforms, level_width, level_height, player, enemy, enemy_spawn_xy, level = load_level(0, tile_size) 
    #background_color = set_background(0)
    #camera.set_bounds(level_width, level_height)
    #enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'CHASE', player, level) #заспавнить врага и назначить следить за игроком

    background_color, platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level = change_level(current_level, screen, camera)

    running = True

    while running:
        clock.tick(fps)
        
        #---ОБРАБОТКА СОБЫТИЙ---
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = game_quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = game_quit()

                if event.key == pygame.K_TAB:
                    background_color, platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level = change_level(1, screen, camera) #ОТЛАДКА, потом удалить
                    current_level = 1

        
        keys = pygame.key.get_pressed()

        jump_pressed = keys[pygame.K_SPACE] or keys[pygame.K_UP]
        player.velocity_x = 0
        if keys[pygame.K_LEFT]:
            player.velocity_x = -player.speed
        if keys[pygame.K_RIGHT]:
            player.velocity_x = player.speed

        if jump_pressed and not jumping:
            player.jump()
        
        
        jumping = jump_pressed


        

        #---ОТРИСОВКА---

        if player.alive:

            screen.fill(background_color)

            for platform in platforms:

                platform_rect_transformed = camera.apply(platform)
                platform_image_transformed = pygame.transform.scale(platform.image, (32, 32))
                screen.blit(platform_image_transformed, platform_rect_transformed)

            for item in items:

                item_rect_transformed = camera.apply(item)
                item_image_transformed = pygame.transform.scale(item.image, (32, 32))
                screen.blit(item_image_transformed, item_rect_transformed)
        
            player_rect_transformed = camera.apply(player)
            player_image_transformed = pygame.transform.scale(player.image, (32, 32))
            screen.blit(player_image_transformed, player_rect_transformed)

            if enemy:
                enemy_rect_transformed = camera.apply(enemy)
                enemy_image_transformed = pygame.transform.scale(enemy.image, (32, 32))
                screen.blit(enemy_image_transformed, enemy_rect_transformed)
        
        if not player.alive:
            print('triggered player not alive')
            should_reset = dead_window.game_over(screen, screen_width, screen_height) #enter не всегда срабатывает с первого раза
            if should_reset:
                print('reset level')
                background_color, platforms, items, level_width, level_height, player, enemy, enemy_spawn_xy, level = change_level(current_level, screen, camera)


        #---ОБНОВЛЕНИЕ ИГРЫ---

        for item in items:
            item.update(screen, camera, player, items)

        player.update(screen, platforms, items, camera, enemy)

        camera.update(player, screen)

        if enemy:
            enemy.update(platforms, camera)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()