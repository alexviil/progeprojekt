import pygame as pg
import libtcodpy as libt
import constants as const
import Actor


class Generator:
    def __init__(self, game_map, surface, actors, containers, items, buffs, messages, floor):
        self.actors = actors
        self.containers = containers
        self.items = items
        self.gm = game_map
        self.sm = surface
        self.buffs = buffs
        self.msgs = messages
        self.floor = floor
        self.hp_buff = 0
        self.dmg_buff = 0
        self.arm_buff = self.floor//3
        if self.floor % 2 == 0:
            self.hp_buff = self.floor//2
            self.dmg_buff = self.floor//2
        else:
            self.hp_buff = self.floor // 2
            self.dmg_buff = self.floor // 2 + 1

    def gen_equipable(self, x, y):
        random_num = libt.random_get_int(0, 0, 100)

        if random_num >= 35 + self.floor*3:
            self.gen_normal_staff(x, y)
        else:
            self.gen_magic_staff(x, y)

    def gen_normal_staff(self, x, y):
        hpbuff = libt.random_get_int(0, 1+self.hp_buff, 2+self.hp_buff)
        armorbuff = libt.random_get_int(0, 0+self.arm_buff, 1+self.arm_buff)
        dmgbuff = libt.random_get_int(0, 1+self.dmg_buff, 2+self.dmg_buff)

        name = self.gen_staff_name()

        self.items.append(Actor.Equipable(x, y, name, "SPRITE_WEAPON_STAFF", self.gm, self.sm,
                          self.msgs, hpbuff, armorbuff, dmgbuff))

    def gen_magic_staff(self, x, y):
        hpbuff = libt.random_get_int(0, 1+self.hp_buff, 2+self.hp_buff)
        armorbuff = libt.random_get_int(0, 0+self.arm_buff, 1+self.arm_buff)
        dmgbuff = libt.random_get_int(0, 1+self.dmg_buff, 2+self.dmg_buff)
        range = libt.random_get_int(0, 4, 7)
        spell_dmg = 12 - range
        cooldown = round(5 * spell_dmg)
        temp_num = libt.random_get_int(0, 0, 3)
        spell = ["Lightning", "Fireball", "Daze", "Ranged"][temp_num]
        name = {"Lightning": "Staff of Arc Lightning", "Fireball": "Staff of Fireball Explosion", "Daze": "Staff of Area Daze", "Ranged": "Wooden Longbow"}
        if self.floor <= 2:
            spell = "Ranged"
            range = libt.random_get_int(0, 6, 8)
            spell_dmg = 10 - range
            cooldown = 3
            sprite = "SPRITE_WEAPON_BOW"
        else:
            if temp_num == 3:
                range = libt.random_get_int(0, 6, 8)
                spell_dmg = 10 - range
                cooldown = 3
                sprite = "SPRITE_WEAPON_BOW"
            else:
                sprite = "SPRITE_WEAPON_STAFF"
        if spell == "Daze":
            spell_dmg = spell_dmg // 2
        self.items.append(Actor.Equipable(x, y, name[spell], sprite, self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False,
                          False, spell, spell_dmg, cooldown, range))

    def gen_item(self, x, y):
        random_num = libt.random_get_int(0, 0, 1)

        if random_num == 0:
            self.gen_healing_potion(x, y)
        elif random_num == 1:
            if self.floor <= 3:
                self.gen_plus_2_potion(x, y)
            elif self.floor <= 6:
                self.gen_plus_3_potion(x, y)
            else:
                self.gen_plus_4_potion(x, y)

    def gen_healing_potion(self, x, y):
        heal = libt.random_get_int(0, 6+self.hp_buff, 9+self.hp_buff)

        self.items.append(Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm,
                         self.msgs, 0, 0, 0,
                          0, heal))

    def gen_plus_2_potion(self, x, y):
        self.items.append(Actor.Consumable(x, y, "+2 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                          self.msgs, 2, 2, 2, 30, 0, "SPRITES_RED_BUFF"))

    def gen_plus_3_potion(self, x, y):
        self.items.append(Actor.Consumable(x, y, "+3 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                                           self.msgs, 3, 3, 3, 30, 0, "SPRITES_RED_BUFF"))

    def gen_plus_4_potion(self, x, y):
        self.items.append(Actor.Consumable(x, y, "+4 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                                           self.msgs, 4, 4, 4, 30, 0, "SPRITES_RED_BUFF"))

    def gen_container(self, x, y):
        random_num = libt.random_get_int(0, 1, 1)

        if random_num == 1:
            self.gen_chest(x, y)

    def gen_chest(self, x, y):
        hpbuff = libt.random_get_int(0, 1+self.hp_buff, 2+self.hp_buff)
        armorbuff = libt.random_get_int(0, 0+self.arm_buff, 1+self.arm_buff)
        dmgbuff = libt.random_get_int(0, 1+self.dmg_buff, 2+self.dmg_buff)
        heal = libt.random_get_int(0, 8+self.hp_buff, 11+self.hp_buff)
        brange = libt.random_get_int(0, 6, 8)
        bspell_dmg = 10 - brange
        bcooldown = 3
        if self.floor <= 2:
            chest_items = [Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm,
                             self.msgs, 0, 0, 0, 0, heal),
                           Actor.Consumable(x, y, "+4 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                                            self.msgs, 4, 4, 4, 30, 0, "SPRITES_RED_BUFF"),
                           Actor.Equipable(x, y, self.gen_staff_name(), "SPRITE_WEAPON_STAFF", self.gm, self.sm,
                                           self.msgs, hpbuff+2, armorbuff, dmgbuff+1),
                           Actor.Equipable(x, y, "Wooden Longbow", "SPRITE_WEAPON_BOW",
                                           self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False, False,
                                           "Ranged", bspell_dmg, bcooldown, brange)
                           ]
        else:
            range = libt.random_get_int(0, 4, 7)
            spell_dmg = 12 - range
            cooldown = round(5 * spell_dmg)
            chest_items = [Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm,
                                            self.msgs, 0, 0, 0, 0, heal),
                           Actor.Consumable(x, y, "+4 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                                            self.msgs, 4, 4, 4, 30, 0, "SPRITES_RED_BUFF"),
                           Actor.Equipable(x, y, "Staff of Fireball", "SPRITE_WEAPON_STAFF",
                                           self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False, False,
                                           "Fireball", spell_dmg, cooldown, range),
                           Actor.Equipable(x, y, "Staff of Arc Lightning", "SPRITE_WEAPON_STAFF",
                                           self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False, False,
                                           "Lightning", spell_dmg, cooldown, range),
                           Actor.Equipable(x, y, "Staff of Area Daze", "SPRITE_WEAPON_STAFF",
                                           self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False, False,
                                           "Daze", spell_dmg, cooldown, range),
                           Actor.Equipable(x, y, "Wooden Longbow", "SPRITE_WEAPON_BOW",
                                           self.gm, self.sm, self.msgs, hpbuff, armorbuff, dmgbuff, False, False,
                                           "Ranged", bspell_dmg, bcooldown, brange)
                           ]

        name = "Chest"
        random_num = libt.random_get_int(0, 1, 6)

        if random_num == 1:
            name = "Mimic"

        self.containers.append(Actor.Container(x, y, name, "SPRITE_CHEST", self.gm, self.sm, self.msgs,
                               [chest_items[libt.random_get_int(0, 0, len(chest_items)-1)]]))

    def gen_monster(self, x, y):
        random_num = libt.random_get_int(0, 0, 1)

        if random_num == 1:
            self.gen_demon(x, y)
        else:
            self.gen_ice_zombie(x, y)

    def gen_demon(self, x, y):
        demon_weapon = Actor.Equipable(0, 0, "Rusty Sword", "SPRITE_RUSTY_SWORD", self.gm, self.sm,
                                       self.msgs, 0, 0, libt.random_get_int(0, 1, 2)+self.dmg_buff, True)

        self.actors.append(Actor.Enemy(x, y, "Demon", "SPRITES_DEMON", True, self.gm, self.sm,
                                       self.msgs, 8+self.hp_buff, 1+self.arm_buff, libt.random_get_int(0, 3, 4), [],
                                       demon_weapon))

    def gen_ice_zombie(self, x, y):
        zombie_inventory = [Actor.Consumable(x, y, "Healing Potion", "SPRITE_POTION_RED", self.gm, self.sm,
                            self.msgs, 0, 0, 0, 0, 4+self.hp_buff),
                            Actor.Consumable(x, y, "+2 Potion", "SPRITE_POTION_RED_LARGE", self.gm, self.sm,
                                             self.msgs, 2, 2, 2, 30, 0, "SPRITES_RED_BUFF")
                            ]

        self.actors.append(Actor.Enemy(x, y, "Ice Zombie", "SPRITES_ICE_ZOMBIE", True, self.gm, self.sm,
                                       self.msgs, 10 + self.hp_buff, 2 + self.arm_buff, libt.random_get_int(0, 2, 3) + self.dmg_buff,
                                       zombie_inventory))
    def gen_staff_name(self):
        randint1 = libt.random_get_int(0, 0, 8)
        randint2 = libt.random_get_int(0, 0, 3)
        randint3 = libt.random_get_int(0, 0, 5)
        randint4 = libt.random_get_int(0, 0, 4)

        prefix = ["Wooden", "Ancient", "Forgotten", "Unenchanted", "Pine", "Weak", "Starter", "Feeble", "Frail"][randint1]
        itemname = ["Stick", "Staff", "Pole", "Rod"][randint2]
        suffix1 = ["Little", "Minor", "Slight", "Unsteady", "Decrepit", "Inefficient"][randint3]
        suffix2 = ["Use", "Empowerment", "Enhancement", "Self-Defence", "Power"][randint4]

        return "{0} {1} of {2} {3}".format(prefix, itemname, suffix1, suffix2)
