from encodings.punycode import T
import pygame 
import time

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

        self.offset = pygame.math.Vector2(0, 0)

        self.zoom = 3

        self.dead_zone_width = 70
        self.dead_zone_height = 40

        #эффекты
        #self.fade_alpha = 0
        self.fade_surface = pygame.Surface((self.width, self.height))
        self.fade_surface.fill((0, 0, 0))


    def apply(self, entity, surf=None):
        
        try:
            x = entity.rect.x - self.camera.x
            y = entity.rect.y - self.camera.y

            center_x = self.width / 2
            center_y = self.height / 2  
            x = center_x + (x - center_x) * self.zoom
            y = center_y + (y - center_y) * self.zoom

            #print(self.camera.x, self.camera.y)

            width = entity.rect.width * self.zoom
            height = entity.rect.height * self.zoom

            image = pygame.transform.scale(entity.image, (int(width), int(height)))

        except:
            x = entity.x - self.camera.x
            y = entity.y - self.camera.y

            center_x = self.width / 2
            center_y = self.height / 2  
            x = center_x + (x - center_x) * self.zoom
            y = center_y + (y - center_y) * self.zoom


            width = entity.width * self.zoom
            height = entity.height * self.zoom

            image = pygame.transform.scale(surf, (int(width), int(height)))

        return pygame.Rect(x, y, width, height), image

    def update(self, target, screen):

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

        #print(self.camera.x, self.camera.y)
        #print(self.offset)


    def set_bounds(self, level_width, level_height):
        self.camera.left = max(-(level_width - self.width), min(0, self.camera.left))
        self.camera.top = max(-(level_height - self.height), min(0, self.camera.top))



    def render_scene(self, screen, background_color, platforms, items, player, enemy=None, enemy_spawn_xy=None):
        screen.fill(background_color)

        for platform in platforms:

            platform_rect_transformed, platform_image_transformed = self.apply(platform)
            screen.blit(platform_image_transformed, platform_rect_transformed)

        for item in items:

            item_rect_transformed, item_image_transformed = self.apply(item)
            screen.blit(item_image_transformed, item_rect_transformed)
        
        player_rect_transformed, player_image_transformed = self.apply(player)
        screen.blit(player_image_transformed, player_rect_transformed)

        if enemy:
            enemy_rect_transformed, enemy_image_transformed = self.apply(enemy)
            screen.blit(enemy_image_transformed, enemy_rect_transformed)



    #эффекты

    def fade_out(self, screen, color=(0, 0, 0)):
        #print('triggered fade out')
        self.fade_surface = pygame.Surface((self.width, self.height))
        self.fade_surface = self.fade_surface.convert()
        self.fade_surface.fill(color)
        
        start_time = time.time()
        duration = 5

        for i in range(255):
            time_dif = round(time.time() - start_time, 2)
            alpha_goal = int((time_dif / duration) * 255)
            
            alpha = min(alpha_goal, 255)
            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))

            
            pygame.display.flip()

    def fade_in(self, screen, color=(0, 0, 0), background_color=None, platforms=None, items=None, player=None):
        #print('triggered fade in')

        print('self x y ', self.camera.x, self.camera.y)
        self.fade_surface = pygame.Surface((self.width, self.height))
        self.fade_surface = self.fade_surface.convert()
        self.fade_surface.fill(color)

        
        if platforms:
            #print('got platforms, items, player = ', platforms, items, player)
            self.render_scene(screen, background_color, platforms, items, player)
        
        duration = 1 #секунд
        total_frames = int(duration * 60)

        #print('total frames ', total_frames)
        for i in range(total_frames + 1):
            #print('i ', i)
            alpha = min(255, 255 - int(i * 255 / total_frames))
            #print('255 - int(i * 255 / (duration*60)) = ', alpha)

            if platforms:
                self.render_scene(screen, background_color, platforms, items, player)

            self.fade_surface.set_alpha(alpha)
            screen.blit(self.fade_surface, (0, 0))
            
            pygame.display.flip()

            time.sleep(1 / 60.0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        