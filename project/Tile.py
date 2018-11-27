from typing import Any
import pygame as pg
import constants as const


class Tile:
    """
    The Tile object is used to set the properties of each tile in the game world. Each tile has it's coordinates
    and boolean values for whether it is a wall or a creature is on it, both used for actor interactions. It also
    has sprites, which are the regular floor by default (since that is the most used tile sprite). The explored
    sprite only gets used when a tile is not in the player's field of view but has been at least once.
    """
    def __init__(self, x, y, is_wall, is_creature, sprite_key="SPRITE_FLOOR", exp_sprite_key="SPRITE_FLOOREXPLORED",
                 doorway=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.is_creature = is_creature
        self.sprite_key = sprite_key
        self.sprite = const.WALL_AND_FLOOR_DICT[self.sprite_key]
        self.explored_sprite_key = exp_sprite_key
        self.explored_sprite = const.WALL_AND_FLOOR_DICT[self.explored_sprite_key]
        self.explored = False
        self.doorway = doorway

    def get_is_wall(self):
        return self.is_wall

    def get_is_creature(self):
        return self.is_creature
    
    def set_is_wall(self, boolean):
        self.is_wall = boolean
    
    def set_is_creature(self, boolean):
        self.is_creature = boolean
