import pygame
import time

from windows.quit_window import game_quit

def game_over(screen, screen_width, screen_height):
    
    begin = time.time()
    return_to_game = False
    while not return_to_game:
        
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('fonts/RetroSans.ttf', 60)
        text_surf = font.render('You are dead.', True, (255, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.midtop = (screen_width/2, screen_height/2)
        screen.blit(text_surf, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit(screen, screen_width, screen_height)

        if time.time() - begin >= 3:
            return_to_game = True
            return True