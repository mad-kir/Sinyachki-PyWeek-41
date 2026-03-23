import pygame

pygame.init()

from windows.quit_window import game_quit
from levels.level_manager import load_level, set_background
from classes.player import Player
from classes.camera import Camera
from classes.enemy import Enemy

def main():

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    screen_width, screen_height = 512*2, 288*2
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    tile_size = 16

    camera = Camera(screen_width, screen_height)


    '''для отладки, удалить позже'''
    platforms, level_width, level_height, player, enemy, enemy_spawn_xy = load_level(0, tile_size) 
    background_color = set_background(0)
    camera.set_bounds(level_width, level_height)
    enemy.create_enemy(enemy_spawn_xy[0], enemy_spawn_xy[1], 'IDLE', player) #заспавнить врага и назначить следить за игроком


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


        #---ОБНОВЛЕНИЕ ИГРЫ---

        player.update(platforms, enemy)

        camera.update(player)

        enemy.update(platforms)

        #---ОТРИСОВКА---

        screen.fill(background_color)

        for platform in platforms:

            platform_rect_transformed = camera.apply(platform)
            platform_image_transformed = pygame.transform.scale(platform.image, (32, 32))
            screen.blit(platform_image_transformed, platform_rect_transformed)
        
        player_rect_transformed = camera.apply(player)
        player_image_transformed = pygame.transform.scale(player.image, (32, 32))
        screen.blit(player_image_transformed, player_rect_transformed)

        enemy_rect_transformed = camera.apply(enemy)
        enemy_image_transformed = pygame.transform.scale(enemy.image, (32, 32))
        screen.blit(enemy_image_transformed, enemy_rect_transformed)
        

        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()