import pygame

pygame.init()

from windows.quit_window import game_quit
from levels.level_manager import load_level, set_background
from classes.player import Player

def main():

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    screen_width, screen_height = 1000, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    tile_size = 16


    '''для отладки, удалить позже'''
    platforms, level_width, level_height, player = load_level(0, tile_size) 
    background_color = set_background(0)

    

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

        player.update(platforms)

        #---ОТРИСОВКА---

        screen.fill(background_color)

        for platform in platforms:

            screen.blit(platform.image, platform.rect)
        
        screen.blit(player.image, player.rect)

        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()