import pygame
from windows.quit_window import game_quit
from windows import menu_window

def pause(screen, screen_width, screen_height):
    cont = False

    selected_button = 0
    buttons = ['Continue', 'Return to menu', 'Quit the game']

    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))

    window_surface = pygame.Surface((screen_width // 3, screen_height // 2))
    window_rect = window_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    
    try:
        font = pygame.font.Font('fonts/RetroSans.ttf', 50)
    except:
        print("Font not found > use system")
        font = pygame.font.Font(None, 60)
    
    text_surf = font.render('PAUSED', True, (0, 0, 255))
    text_rect = text_surf.get_rect(center=(window_rect.width // 2, window_rect.height // 4))

    button_width = window_rect.width//2
    button_height = window_rect.height//6
    button_y_start = (window_rect.height // 8) * 3
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
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_button = (selected_button + 1) % len(buttons)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_button = (selected_button - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    
                    if buttons[selected_button] == 'Continue':
                        cont = True 
                    elif buttons[selected_button] == 'Return to menu':
                        return True #will stop running in the main 
                    elif buttons[selected_button] == 'Quit the game':
                        result = game_quit(screen, screen_width, screen_height)
                        if result:  # Если пользователь выбрал "No, I will continue"
                            # Перерисовываем только окно паузы
                            screen.blit(overlay, (0,0))
                            window_surface.fill((255, 255, 255))
                            window_surface.blit(text_surf, text_rect)
                            # Отрисовка кнопок паузы здесь или в цикле ниже
                            # ...
                            screen.blit(window_surface, window_rect)
                            pygame.display.flip()
                            continue
                        else:
                            cont = True
        
        window_surface.fill((255, 255, 255))
        window_surface.blit(text_surf, text_rect)

        for i, button in enumerate(buttons):
            if i == selected_button:
                outline_color = (255, 0, 0)  # Красный контур для активной кнопки
                text_color = (255, 0, 0)
            else:
                outline_color = (0, 0, 0)  # Чёрный контур для неактивной кнопки
                text_color = (0, 0, 0)

            button_x = (window_rect.width - button_width) // 2
            button_y = button_y_start + i * (button_height + button_spacing)

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

