import pygame

pygame.init()

from windows.quit_window import game_quit
from levels.level_manager import load_level

def main():

    fps = 60
    clock = pygame.time.Clock()

    '''
    https://www.daniweb.com/programming/software-development/threads/54881/pygame-get-screen-size 
    изучить потом, чтобы сделать окно подстраивающимся под размеры экрана. вывести это в окно настройки?
    '''

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    '''для отладки, удалить позже'''
    load_level(0) 

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

        #---ОБНОВЛЕНИЕ ИГРЫ---

        #---ОТРИСОВКА---
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()