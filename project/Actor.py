import pygame as pg
import constants as const


class Actor:
    def __init__(self, x, y, sprite, world_map, surface):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.world_map = world_map
        self.surface = surface

    def control(self, x_change, y_change):
        if not self.world_map[self.y + y_change][self.x + x_change]:  # Checks if can step there
            self.x += x_change
            self.y += y_change

    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))
