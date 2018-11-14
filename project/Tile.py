from typing import Any

import pygame as pg
import constants as const


class Tile:
    def __init__(self, x, y, is_wall, is_creature, sprite=const.SPRITE_FLOOR, exp_sprite=const.SPRITE_FLOOREXPLORED):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.is_creature = is_creature
        self.sprite = sprite
        self.explored_sprite = exp_sprite
        self.explored = False

    def get_is_wall(self):
        return self.is_wall

    def get_is_creature(self):
        return self.is_creature
    
    def set_is_wall(self, bool):
        self.is_wall = bool
    
    def set_is_creature(self, bool):
        self.is_creature = bool
