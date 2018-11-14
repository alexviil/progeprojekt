import pygame as pg
import libtcodpy as libt
import constants as const


class Ai:
    def move_randomly(self, creature):
        creature.control(libt.random_get_int(0, -1, 1), libt.random_get_int(0, -1, 1))
