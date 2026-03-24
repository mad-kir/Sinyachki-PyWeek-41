import pygame

from windows.dialogue_window import DialogueWindow

dialogue_window = DialogueWindow()

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, type, can_interact=False, can_pass=True):
        super().__init__()
        
        self.x = x
        self.y = y

        self.width, self.height = width, height

        self.image_surface = pygame.Surface((width, height))

        self.image = image

        self.rect = self.image_surface.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.interact_rect = pygame.Rect(self.rect.x-5, self.rect.y-5, self.rect.width+10, self.rect.height+10)
        
        #self.velocity_x = 0 (probably won't move but I'll keep it anyway just in case)
        #self.velocity_y = 0
        
        #self.speed = 6

        #self.on_ground = False
        #self.jumps_remaining = 2
        #self.gravity = 0.5
        #self.jump_power = -7
        #self.max_fall_speed = 15

        self.alive = True

        self.type = type

        self.can_interact = can_interact
        self.can_pass = can_pass

    def update(self, screen, camera, player, items):

        if not self.alive:
            return

        if self.interact_rect.colliderect(player.rect):
            if self.can_interact:
                if self.type == 'FOREST':

                    dw_surf, dw_rect = dialogue_window.show(screen, camera, self, 'Press ENTER')
                    dw_rect_transformed = camera.apply(dw_rect)
                    screen.blit(dw_surf, dw_rect_transformed)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                            dw_surf, dw_rect = dialogue_window.show(screen, camera, player, 'I shouldn’t walk in the forest — it’s too easy to get lost there.')
                            dw_rect_transformed = camera.apply(dw_rect)
                            screen.blit(dw_surf, dw_rect_transformed)

                if self.type == 'BUSH': 
                    from levels.level_manager import count_berries

                    dw_surf, dw_rect = dialogue_window.show(screen, camera, self, 'Press ENTER')
                    dw_rect_transformed = camera.apply(dw_rect)
                    screen.blit(dw_surf, dw_rect_transformed)

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                            count_berries()
                            self.image = pygame.image.load('images/tileset_day/bush_5.png')
                            self.can_interact = False
                            """
                            СЮДА ВСТАВИТЬ ЗВУК СБОРА ЯГОД
                            """
