import pygame

class DialogueWindow:
    def __init__(self):
        self.window_color = pygame.color.Color((255, 255, 255))
        self.window_surface = None
        self.window_rect = pygame.Rect(0, 0, 0, 0)
        self.padding = 2

        self.text = ''
        self.font_size = 20
        self.font_color = pygame.color.Color((0, 0, 0))
        self.font = pygame.font.Font('fonts/RetroSans.ttf', self.font_size)

    def show(self, screen, camera, target, text):

        text_surface = self.font.render(text, True, self.font_color)
        text_rect = text_surface.get_rect()

        window_width = text_rect.width + 2 * self.padding
        window_height = text_rect.height + 2 * self.padding
        if (self.window_surface is None or self.window_surface.get_size() != (window_width, window_height)):
            self.window_surface = pygame.Surface((window_width, window_height))
            self.window_rect.size = (window_width, window_height)
            self.window_rect.x += 3

        self.window_surface.fill(self.window_color)

        self.window_rect.midbottom = target.rect.midtop
        text_rect.center = self.window_surface.get_rect().center

        self.window_surface.blit(text_surface, text_rect)

        return self.window_surface, self.window_rect


'''
Идея на будущее: добавить белую обводку?
'''
