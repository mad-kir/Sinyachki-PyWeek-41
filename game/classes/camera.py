import pygame 

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.offset = pygame.math.Vector2(0, 0)

        self.zoom = 2

        self.dead_zone_width = 150
        self.dead_zone_height = 100


    def apply(self, entity):
        x = entity.rect.x - self.camera.x
        y = entity.rect.y - self.camera.y
        
        center_x = self.width / 2
        center_y = self.height / 2  
        x = center_x + (x - center_x) * self.zoom
        y = center_y + (y - center_y) * self.zoom

        #print(self.camera.x, self.camera.y)

        width = entity.rect.width * self.zoom
        height = entity.rect.height * self.zoom

        return pygame.Rect(x, y, width, height)

    def update(self, target):
        x = (target.rect.centerx - self.width / 2)
        y = (target.rect.centery/ 2)

        self.offset.x = 0
        self.offset.y = 0

        if target.rect.centerx < self.camera.centerx - self.dead_zone_width / 2:
            self.offset.x = target.rect.centerx - (self.camera.centerx - self.dead_zone_width / 2)
        elif target.rect.centerx > self.camera.centerx + self.dead_zone_width / 2:
            self.offset.x = target.rect.centerx - (self.camera.centerx + self.dead_zone_width / 2)

        if target.rect.centery < self.camera.centery - self.dead_zone_height / 2:
            self.offset.y = target.rect.centery - (self.camera.centery - self.dead_zone_height / 2)
        elif target.rect.centery > self.camera.centery + self.dead_zone_height / 2:
            self.offset.y = target.rect.centery - (self.camera.centery + self.dead_zone_height / 2)


        self.camera.x += self.offset.x
        self.camera.y += self.offset.y

        print(self.camera.x, self.camera.y)
        print(self.offset)


    def set_bounds(self, level_width, level_height):
        self.camera.left = max(-(level_width - self.width), min(0, self.camera.left))
        self.camera.top = max(-(level_height - self.height), min(0, self.camera.top))