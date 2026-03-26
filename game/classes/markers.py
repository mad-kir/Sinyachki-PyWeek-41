import pygame

class Marker(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, type):
        super().__init__()

        self.x = x
        self.y = y

        self.width, self.height = width, height

        self.image_surface = pygame.Surface((width, height))

        self.image = image

        self.rect = self.image_surface.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.type = type

        self.is_triggered = False

        self.alive = True

    def update(self, screen, player, items, level):
        
        if not self.alive:
            return

        if self.rect.colliderect(player.rect):
            self.is_triggered = True
            print('triggered marker. is triggered = ', self.is_triggered)