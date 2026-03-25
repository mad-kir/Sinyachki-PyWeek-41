import pygame
from windows.quit_window import finish_process

def show(screen, screen_width, screen_height):
    print('show menu')
    
    background_color = pygame.color.Color((101, 0, 11))
    window_color = pygame.color.Color((66, 0, 8))
    header_color = pygame.color.Color((168, 42, 127))
    button_color = pygame.color.Color((76, 19, 26))
    inactive_color = pygame.color.Color((105, 43, 0))
    active_color = pygame.color.Color((70, 172, 43))
    
    selected_button = 0
    buttons = ['To the forest', 'Reset save', 'Quit the game']
    
    window_surface = pygame.Surface((screen_width // 3, screen_height))
    window_rect = window_surface.get_rect(topleft=(0, 0))
    
    try:
        header_font = pygame.font.Font('fonts/RetroSans.ttf', 60)
        button_font = pygame.font.Font('fonts/RetroSans.ttf', 20)
    except:
        print("Font not found > use system")
        header_font = pygame.font.Font(None, 60)
        button_font = pygame.font.Font(None, 20)
    
    button_width = window_rect.width // 2
    button_height = window_rect.height // 6
    button_y_start = (window_rect.height // 8) * 3
    button_spacing = 10
    
    cont = False
    while not cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit(screen, screen_width, screen_height) 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('got esc while on pause')
                    cont = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if buttons[selected_button] == 'To the forest': # Баг: если вернуться из игры в меню, то переход в игру требует выбрать кнопку дважды
                        return True
                    elif buttons[selected_button] == 'Reset save':
                        print('tried to reset save. But nothing happened. Seems like save system is not present yet.')
                    elif buttons[selected_button] == 'Quit the game':
                        finish_process()
        
        screen.fill(background_color)
        
        window_surface.fill(window_color)
        
        header_surf = header_font.render('RANDOM GAME', True, header_color)
        header_rect = header_surf.get_rect(center=(window_rect.width // 2, window_rect.height // 8))
        window_surface.blit(header_surf, header_rect)
        
        for i, button in enumerate(buttons):
            if i == selected_button:
                outline_color = active_color  
                text_color = active_color
            else:
                outline_color = inactive_color 
                text_color = inactive_color
            
            button_x = (window_rect.width - button_width) // 2
            button_y = button_y_start + i * (button_height + button_spacing)
            
            button_surface = pygame.Surface((button_width, button_height))
            button_surface.fill(button_color)
            
            button_text = button_font.render(button, True, text_color)
            button_text_rect = button_text.get_rect(center=(button_width // 2, button_height // 2))
            button_surface.blit(button_text, button_text_rect)
            
            window_surface.blit(button_surface, (button_x, button_y))
            
            pygame.draw.rect(window_surface, outline_color, 
                           pygame.Rect(button_x, button_y, button_width, button_height), 3)
        
        screen.blit(window_surface, window_rect)
        
        pygame.display.flip()