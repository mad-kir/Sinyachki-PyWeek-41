import pygame

from windows.dialogue_window import DialogueWindow

dialogue_window = DialogueWindow()

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, type, level, markers, can_interact=False, can_pass=True):
        super().__init__()

        self.x = x
        self.y = y
        self.width, self.height = width, height

        

        self.image_surface = pygame.Surface((self.width, self.height))
        self.image = image
        #self.image_surf.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.interact_rect = pygame.Rect(self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.height + 10)

        self.alive = True
        self.type = type
        self.level = level
        self.markers = markers
        self.can_interact = can_interact
        self.can_pass = can_pass

        self.is_triggered = False

    def update(self, screen, camera, player, items):

        if not self.alive:
            return

        #обработка маркеров
        if self.type == 'FOREST':
            if self.level == 1:
                for marker in self.markers:
                    if marker.is_triggered and marker.type == 'TRIGGER_1':
                        self.image_surface.set_alpha(255)
                        self.can_pass = True
                        self.can_interact = False
                        self.alive = False





        #обработка столкновений
        if self.interact_rect.colliderect(player.rect):
            if self.can_interact:
                if self.type == 'FOREST':
                    
                    dw_surf, dw_rect = dialogue_window.show(screen, camera, self, 'Press ENTER')
                    dw_rect_transformed,  dw_surf_transformed = camera.apply(dw_rect, dw_surf)
                    screen.blit(dw_surf_transformed, dw_rect_transformed)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                            dw_surf, dw_rect = dialogue_window.show(screen, camera, player, 'I shouldn’t walk in the forest — it’s too easy to get lost there.')
                            dw_rect_transformed,  dw_surf_transformed = camera.apply(dw_rect, dw_surf)
                            screen.blit(dw_surf_transformed, dw_rect_transformed)

                if self.type == 'BUSH_RED': 
                    dw_surf, dw_rect = dialogue_window.show(screen, camera, self, 'Press ENTER')  #ДИАЛОГОВЫЕ ОКНА СТАЛИ ОГРОМНЫМИ ПОКА ПЫТАЛАСЬ ПОФИКСИТЬ ЗУМ КАМЕРЫ
                    dw_rect_transformed,  dw_surf_transformed = camera.apply(dw_rect, dw_surf)
                    screen.blit(dw_surf_transformed, dw_rect_transformed)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            self.image = pygame.image.load('images/tileset/_50.png')
                            self.type = 'BUSH'
                            self.can_interact = False
                            """
                            СЮДА ВСТАВИТЬ ЗВУК СБОРА ЯГОД
                            """

                if self.type == 'BUSH_BLUE': 
                    dw_surf, dw_rect = dialogue_window.show(screen, camera, self, 'Press ENTER')  #ДИАЛОГОВЫЕ ОКНА СТАЛИ ОГРОМНЫМИ ПОКА ПЫТАЛАСЬ ПОФИКСИТЬ ЗУМ КАМЕРЫ
                    dw_rect_transformed,  dw_surf_transformed = camera.apply(dw_rect, dw_surf)
                    screen.blit(dw_surf_transformed, dw_rect_transformed)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            self.is_triggered = True
                            self.image = pygame.image.load('images/tileset/_50.png')
                            #self.type = 'BUSH'
                            self.can_interact = False
                            """
                            СЮДА ВСТАВИТЬ ЗВУК СБОРА ЯГОД
                            """

                