import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, image):
        super().__init__()

        self.x = x
        self.y = y

        self.tile_size = tile_size

        self.image_surf = pygame.Surface((tile_size, tile_size))
        self.image = image
        #self.image_surf.fill((255, 0, 0))
        self.rect = pygame.Rect(x, y, tile_size, tile_size)