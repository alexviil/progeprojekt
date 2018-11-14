import pygame as pg
import libtcodpy as libt
import constants as const


class Ai:
    """Currently only affects Enemy objects in game_loop. Causes all enemies to move in a random direction
        every time an event occurs (keys W A S D are pressed).
    """
    def move_randomly(self, creature):
        creature.control(libt.random_get_int(0, -1, 1), libt.random_get_int(0, -1, 1))
