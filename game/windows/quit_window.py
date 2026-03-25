import pygame

import sys

def finish_process():
    pygame.quit()
    sys.exit()

def game_quit(screen, screen_width, screen_height):
    cont = False

    selected_button = 0
    buttons = ['No, I will continue', 'Yes, let me go']

    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))

    window_surface = pygame.Surface((screen_width // 2, screen_height // 3))
    window_rect = window_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    
    try:
        font = pygame.font.Font('fonts/RetroSans.ttf', 20)
    except:
        print("Font not found > use system")
        font = pygame.font.Font(None, 20)
    
    text_surf = font.render('Are you sure you want to quit?', True, (0, 0, 255))
    text_rect = text_surf.get_rect(center=(window_rect.width // 2, window_rect.height // 4))

    button_width = window_rect.width//3
    button_height = window_rect.height//4
    button_x_start = (window_rect.width // 6)
    button_spacing = 10
    button_font = pygame.font.Font('fonts/RetroSans.ttf', 20)

    while not cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit(screen, screen_width, screen_height)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('got esc while on pause')
                    cont = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected_button = (selected_button - 1) % len(buttons)
                
                elif event.key == pygame.K_RETURN:
                    if buttons[selected_button] == 'No, I will continue':
                        cont = True
                        return True
                    elif buttons[selected_button] == 'Yes, let me go':
                        finish_process()
                        
        
        window_surface.fill((255, 255, 255))
        window_surface.blit(text_surf, text_rect)

        for i, button in enumerate(buttons):
            if i == selected_button:
                outline_color = (255, 0, 0)  # Красный контур для активной кнопки
                text_color = (255, 0, 0)
            else:
                outline_color = (0, 0, 0)  # Чёрный контур для неактивной кнопки
                text_color = (0, 0, 0)

            button_x = button_x_start + i * (button_width + button_spacing)
            button_y = ((window_rect.height - button_height) // 3 ) * 2

            button_surface = pygame.Surface((button_width, button_height))
            button_surface.fill((240, 240, 240))

            button_text = button_font.render(button, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=(button_width // 2, button_height // 2))
            button_surface.blit(button_text, button_text_rect)

            window_surface.blit(button_surface, (button_x, button_y))

            pygame.draw.rect(window_surface, outline_color, pygame.Rect(button_x, button_y, button_width, button_height), 3) #толщина контура

            i += 1



        pygame.draw.rect(window_surface, (0, 0, 0), window_surface.get_rect(), 3)

        screen.blit(window_surface, window_rect)
        pygame.display.flip()