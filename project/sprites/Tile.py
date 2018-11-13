from typing import Any

import pygame as pg
import constants as const


class Tile:
    def __init__(self, is_wall, is_creature):
        self.is_wall = is_wall
        self.is_creature = is_creature

    def get_is_wall(self):
        return self.is_wall

    def get_is_creature(self):
        return self.is_creature
