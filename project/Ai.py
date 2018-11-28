import pygame as pg
import libtcodpy as libt
import constants as const
from math import sqrt


class Ai:
    def __init__(self, actors, actors_containers, items):
        self.actors = actors
        self.actors_containers = actors_containers
        self.items = items

    def ai_turn(self, creature, player):
        if creature.ai == "aggressive_roam":
            self.aggressive_roam(creature, player)
        elif creature.ai == "dazed":
            pass

    def move_randomly(self, creature):
        creature.control(libt.random_get_int(0, -1, 1), libt.random_get_int(0, -1, 1), self.actors, self.actors_containers, self.items)

    def aggressive_roam(self, creature, player):
        player_location = player.get_location()
        creature_location = creature.get_location()
        if sqrt((player_location[0] - creature_location[0]) ** 2 + (player_location[1] - creature_location[1]) ** 2) >= 6:
            self.move_randomly(creature)
        elif player_location[0] < creature_location[0]:
            if player_location[1] < creature_location[1]:
                creature.control(- 1, - 1, self.actors, self.actors_containers, self.items)
            elif player_location[1] > creature_location[1]:
                creature.control(- 1, 1, self.actors, self.actors_containers, self.items)
            else:
                creature.control(- 1, 0, self.actors, self.actors_containers, self.items)
        elif player_location[0] > creature_location[0]:
            if player_location[1] < creature_location[1]:
                creature.control(1, - 1, self.actors, self.actors_containers, self.items)
            elif player_location[1] > creature_location[1]:
                creature.control(1, 1, self.actors, self.actors_containers, self.items)
            else:
                creature.control(1, 0, self.actors, self.actors_containers, self.items)
        else:
            if player_location[1] < creature_location[1]:
                creature.control(0, - 1, self.actors, self.actors_containers, self.items)
            elif player_location[1] > creature_location[1]:
                creature.control(0, 1, self.actors, self.actors_containers, self.items)
