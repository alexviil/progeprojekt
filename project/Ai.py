import pygame as pg
import libtcodpy as libt
import constants as const
from math import sqrt


class Ai:
    def move_randomly(self, creature):
        creature.control(libt.random_get_int(0, -1, 1), libt.random_get_int(0, -1, 1))

    def aggressive_roam(self, creature, player):
        player_location = player.get_location()
        creature_location = creature.get_location()
        if sqrt((player_location[0] - creature_location[0]) ** 2 + (player_location[1] - creature_location[1]) ** 2) >= 6:
            self.move_randomly(creature)
        elif player_location[0] < creature_location[0]:
            if player_location[1] < creature_location[1]:
                creature.control(- 1, - 1)
            elif player_location[1] > creature_location[1]:
                creature.control(- 1, 1)
            else:
                creature.control(- 1, 0)
        elif player_location[0] > creature_location[0]:
            if player_location[1] < creature_location[1]:
                creature.control(1, - 1)
            elif player_location[1] > creature_location[1]:
                creature.control(1, 1)
            else:
                creature.control(1, 0)
        else:
            if player_location[1] < creature_location[1]:
                creature.control(0, - 1)
            elif player_location[1] > creature_location[1]:
                creature.control(0, 1)
        