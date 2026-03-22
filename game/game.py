import pygame

pygame.init()

from windows.quit_window import game_quit

def main():

    fps = 60
    clock = pygame.time.Clock()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
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