import pygame as py

class Sprite:
    def __init__(self, image):
        size = image.get_size()
        tinted = self.tint_image(image, size, (0, 255, 0))

        self.original_image = image
        self.image = image
        self.original_size = size
        self.size = size
        self.original_tinted = tinted
        self.tinted = tinted

    def tint_image(self, image, size, color):
        tinted_image = image.copy()
        color_surface = py.Surface(size)
        color_surface.fill(color)
        tinted_image.blit(color_surface, (0, 0), special_flags=py.BLEND_RGBA_MULT)
        
        return tinted_image