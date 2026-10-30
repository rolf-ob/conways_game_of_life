import pygame as py

class TextCache:
    def __init__(self, font):
        self._fonts = {
            "world": font,
            "screen": font
        }
        self._surfaces = {
            "world": {},
            "screen": {}
        }

    def get_surface(self, text, layer, color=(0,)*3):
        key = (text, color)

        if key not in self._surfaces[layer]:
            self._surfaces[layer][key] = self._fonts[layer].render(text, True, color)
        
        return self._surfaces[layer][key]

    def change_surface_font(self, layer, new_size):
        self.clear_fonts(layer)
        self._fonts[layer] = py.font.SysFont("Arial", new_size)

    def clear_fonts(self, layer):
        self._surfaces[layer].clear()