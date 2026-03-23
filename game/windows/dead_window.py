import pygame

def game_over(screen, screen_width, screen_height):
    
    
    font = pygame.font.SysFont('fonts/RetroSans.ttf', 60)
    text_surf = font.render('Вы мертвы.', True, (255, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.midtop = (screen_width/2, screen_height/2)
    screen.blit(text_surf, text_rect)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True