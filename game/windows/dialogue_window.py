import pygame

def show(screen, camera, target, text):


    window_surface = pygame.Surface((100, 50))
    window_surface.fill((200, 200, 100))
    window_rect = window_surface.get_rect()
    window_rect.midbottom = target.rect.midtop
    window_rect.y -= 5
    #screen.blit(window_surface, window_rect)

    font = pygame.font.Font('fonts/RetroSans.ttf', 18)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midbottom = target.rect.midtop
    text_rect.y -= 10
    #screen.blit(text_surface, text_rect)

    #window_rect_transformed = camera.apply(window_rect)
    #window_transformed = pygame.transform.scale(window_surface, (window_rect.width*2, window_rect.height*2))
    #screen.blit(window_transformed, window_rect_transformed)

    text_rect_transformed = camera.apply(text_rect)
    text_transformed = pygame.transform.scale(text_surface, (text_rect.width*2, text_rect.height*2))
    screen.blit(text_transformed, text_rect_transformed)

    print('dialogue show')

    '''
    Идея на будущее: добавить белую обводку?
    '''