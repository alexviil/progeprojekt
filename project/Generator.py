import pygame as pg
import libtcodpy as libt
import constants as const
import Actor


class Generator:
    def __init__(self, game_map, surface, actors, containers, items, buffs, messages):
        self.actors = actors
        self.containers = containers
        self.items = items
        self.gm = game_map
        self.sm = surface
        self.buffs = buffs
        self.msgs = messages

    def gen_equipable(self, x, y):
        random_num = libt.random_get_int(0, 1, 1)

        if random_num == 1:
            self.gen_staff(x, y)

    def gen_staff(self, x, y):
        hpbuff = libt.random_get_int(0, 1, 4)
        armorbuff = libt.random_get_int(0, 1, 4)
        dmgbuff = libt.random_get_int(0, 1, 4)

        self.items.append(Actor.Equipable(x, y, "A Pretty Neat Staff", "SPRITE_WEAPON_STAFF", self.gm, self.sm, self.actors,
                          self.containers, self.items, self.buffs, self.msgs, hpbuff, armorbuff, dmgbuff))

    def gen_item(self, x, y):
        random_num = libt.random_get_int(0, 0, 1)

        if random_num == 0:
            self.gen_healing_potion(x, y)
        elif random_num == 1:
            self.gen_plus_3_potion(x, y)

    def gen_healing_potion(self, x, y):
        heal = libt.random_get_int(0, 6, 9)

        self.items.append(Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm, self.actors,
                          self.containers, self.items, self.buffs, self.msgs, 0, 0, 0,
                          0, heal))

    def gen_plus_3_potion(self, x, y):
        self.items.append(Actor.Consumable(x, y, "+3 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm, self.actors,
                          self.containers, self.items, self.buffs, self.msgs, 3, 3, 3, 30, 0, const.SPRITES_RED_BUFF))

    def gen_container(self, x, y):
        random_num = libt.random_get_int(0, 1, 1)

        if random_num == 1:
            self.gen_chest(x, y)

    def gen_chest(self, x, y):
        hpbuff = libt.random_get_int(0, 1, 4)
        armorbuff = libt.random_get_int(0, 1, 4)
        dmgbuff = libt.random_get_int(0, 1, 4)
        chest_items = [Actor.Consumable(0, 0, "Chest Potion", "SPRITE_POTION_RED", self.gm, self.sm, self.actors,
                                        self.containers, self.items, self.buffs, self.msgs, 0, 0, 0, 0, 3),
                       Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm, self.actors,
                                        self.containers, self.items, self.buffs, self.msgs, 0, 0, 0,
                                        0, libt.random_get_int(0, 6, 9)),
                       Actor.Equipable(x, y, "A Pretty Neat Staff", "SPRITE_WEAPON_STAFF", self.gm, self.sm, self.actors,
                                       self.containers, self.items, self.buffs, self.msgs, hpbuff, armorbuff, dmgbuff)
                       ]

        name = "Chest"
        random_num = libt.random_get_int(0, 1, 6)

        if random_num == 1:
            name = "Mimic"

        self.containers.append(Actor.Container(x, y, name, "SPRITE_CHEST", self.gm, self.sm, self.actors,
                               self.containers, self. items, self.buffs, self.msgs,
                               [chest_items[libt.random_get_int(0, 0, 2)]]))

    def gen_monster(self, x, y):
        random_num = libt.random_get_int(0, 1, 1)

        if random_num == 1:
            self.gen_demon(x, y)

    def gen_demon(self, x, y):
        self.actors.append(Actor.Enemy(x, y, "Demon", "SPRITES_DEMON", True, self.gm, self.sm, self.actors,
                                       self.containers, self.items, self.buffs,
                                       self.msgs, 10, 0, 1, [],
                                       Actor.Equipable(0, 0, "Rusty Sword", "SPRITE_RUSTY_SWORD", self.gm, self.sm,
                                                       self.actors, self.containers, self.items, self.buffs, self.msgs, 0, 0, 3, True),
                                       libt.random_get_int(0, 5, 9), libt.random_get_int(0, 0, 19)))
