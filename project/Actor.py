import pygame as pg
import constants as const
import Buffs, Menu


class Actor:
    """
    The Actor class is the parent class for interactive objects like the player, enemies, chests and items. Each
    object has it's starting coordinates, a name, a sprite (or multiple for animations), the world map
    to follow, a surface to be drawn on, the list of all actors and inanimate actors and messages related
    to the actor.
    """
    def __init__(self, x, y, name, sprites_key, world_map, surface, messages):
        self.x = x
        self.y = y
        self.name = name
        self.sprites_key = sprites_key
        self.sprites = const.ACTOR_DICT[sprites_key]
        self.world_map = world_map
        self.surface = surface
        self.messages = messages
        self.sprite = None

    def set_sprite(self, sprite):
        self.sprite = sprite

    def get_sprite(self):
        return self.sprite

    def draw(self, camera):
        """Draws the actor object onto a pygame surface with the coordinates multiplied by the game's tile width and height'"""
        self.surface.blit(self.sprite, ((self.x + camera.get_x_offset())* const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
    
    def get_location(self):
        return self.x, self.y

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_name(self):
        return self.name

    def set_world_map(self, game_map):
        self.world_map = game_map

    def set_surface(self, surface):
        self.surface = surface

    def set_sprites(self, sprites):
        self.sprites = sprites


class Creature(Actor):
    """
    A child of Actor, the Creature class inherits all previous attributes and receives some new attributes. For every sprite
    the Creature class also has each sprite mirrored and a mirrored attribute with a boolean value. This is used for when
    the object moves to the left, as to leave the impression that the object is actually walking in that direction and not
    moonwalking. Creature also has idle_frames, which specifies the amount of frames to display each idle sprite, and
    a frame_counter to keep track of when each Creature needs to have their idle sprite updated. max_hp and hp are used for
    combat, with the latter being the upper limit or maximum possible hp.
    """
    def __init__(self, x, y, name, sprites_key, mirror, world_map, surface, msgs, hp=10, armor=0, dmg=3, inventory=[], equipped=None, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites_key, world_map, surface, msgs)
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in const.ACTOR_DICT[self.sprites_key]]
        self.mirror = mirror
        self.idle_frames = idle_frames
        self.frame_counter = frame_counter
        self.inventory = inventory
        self.equipped = equipped
        self.max_hp = hp
        self.hp = hp
        self.armor = armor
        self.dmg = dmg
        
        if self.mirror:
            self.sprite = self.sprites_mirrored[0]
        else:
            self.sprite = self.sprites[0]
            
    def control(self, x_change, y_change, actors, actors_inanimate, ilist, sound_volume):
        """
        Whether by AI or events, a Creature object can move in some direction. To do that, first, this function checks
        if the destination tile is already occupied by another creature. If so, the Creature object will set the other
        Creature object as it's target, check whether it exists and cause it to take_damage as described below.
        Otherwise, if no Creature object is present, it will check if the destination tile is an impassable object (wall, container)
        and if not, step there. If the movement is done to the opposite direction of the Creature's sprite, the sprite will now become
        mirrored.
        """
        target = None
        for actor in actors + actors_inanimate:  # Checks if creature exists and target location
            if actor is not self and actor.get_location() == (self.x + x_change, self.y + y_change) and isinstance(actor, Actor) and not isinstance(actor, Item):
                target = actor
                break

        if isinstance(target, Creature) and not isinstance(target, self.__class__):  # if creature exists and is not same class, attacks it
            self.messages.append(self.name + " attacks " + target.name + " for " + str(max(1, self.dmg - target.armor)) + " damage.")
            effect = pg.mixer.Sound(const.HIT_SOUND)
            effect.set_volume(sound_volume)
            effect.play()
            target.take_damage(max(1, self.dmg - target.armor), actors, ilist)

        elif isinstance(target, Container) and isinstance(self, Player):
            if target.is_open():
                self.messages.append("The chest has already been opened.")
            elif target.name == "Mimic":
                actors.append(Enemy(target.get_location()[0], target.get_location()[1], "Mimic", "SPRITES_MIMIC", False, self.world_map, self.surface, self.messages, 9, 0, 5))
                self.messages.append("The chest is a Mimic!")
                actors_inanimate.remove(target)
            elif target.inventory:
                for item in target.inventory:
                    self.messages.append("The chest contained something!")
                    target.y += 1  # very bootleg way of making the item(s) drop in front of the chest but  ¯\_(ツ)_/¯
                    item.drop(target, ilist)
                    target.y -= 1
                    effect = pg.mixer.Sound(const.CHEST_SOUND)
                    effect.set_volume(sound_volume)
                    effect.play()
            else:
                self.messages.append("The chest contains nothing of value.")
            target.set_open(True)
            target.set_sprite(const.ACTOR_DICT["SPRITE_CHEST_OPEN"])

        if not self.world_map[self.y + y_change][self.x + x_change].get_is_wall() and target is None:  # Checks if can step there
            self.x += x_change
            self.y += y_change

        # Turns sprite around to the direction the character is walking towards
        if x_change == -1 and self.mirror == False:
            self.sprite = (pg.transform.flip(self.sprite, True, False))
            self.mirror = True
        elif x_change == 1 and self.mirror == True:
            self.sprite = (pg.transform.flip(self.sprite, True, False))
            self.mirror = False

    def take_damage(self, damage, actors, ilist):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0  # to avoid negative health
        self.messages.append(self.name + "'s health is " + str(self.hp) + "/" + str(self.max_hp))

        if self.hp <= 0:
            self.death(actors, ilist)

    def death(self, actors, ilist):
        self.messages.append(self.name + " is dead.")
        if self.equipped is not None:
            self.equipped.death_drop(self, ilist)
        actors.remove(self)
        if self.inventory:
            for item in self.inventory:
                item.drop(self, ilist)
    
    def get_location(self):
        return self.x, self.y

    def destroy_sprites(self):
        self.sprites = None
        self.sprite = None
        self.sprites_mirrored = None

    def init_sprites(self):
        self.sprite = const.ACTOR_DICT[self.sprites_key][0]
        self.sprites = const.ACTOR_DICT[self.sprites_key]
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in const.ACTOR_DICT[self.sprites_key]]


class Enemy(Creature):
    """Used to help Ai decide who to move."""
    def __init__(self, x, y, name, sprites_key, mirror, world_map, surface, messages, hp=10, armor=0, dmg=1, inventory=[], equipped=None, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites_key, mirror, world_map, surface, messages, hp, armor, dmg, inventory, equipped, idle_frames, frame_counter)
        self.ai = "aggressive_roam"
        if equipped:
            self.hp += equipped.hpbuff
            self.max_hp += equipped.hpbuff
            self.armor += equipped.armorbuff
            self.dmg += equipped.dmgbuff


class Player(Creature):
    def __init__(self, x, y, name, sprites_key, mirror, world_map, surface, messages, hp=20, armor=0, dmg=3, inventory_limit=3, inventory=[], equipped=None, spell=None, spell_cooldown=5, spell_range=5, spell_damage=5, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites_key, mirror, world_map, surface, messages, hp, armor, dmg, inventory, equipped, idle_frames, frame_counter)
        self.inventory_limit = inventory_limit
        self.selection = 0
        self.spell = spell
        self.spell_cooldown = spell_cooldown
        self.spell_range = spell_range
        self.spell_damage = spell_damage
        self.turns_since_spell = spell_cooldown
        self.spell_status = None
        self.hud_heart_sprite = const.ACTOR_DICT["HUD_HEART_FULL"]

    def pick_up(self, ilist):
        for item in ilist:
            if item.get_location() == self.get_location():
                if self.inventory is None or len(self.inventory) >= self.inventory_limit:
                    self.messages.append("Your inventory is already at it's limit " + str(len(self.inventory)) + "/" + str(self.inventory_limit) + ".")
                else:
                    item.become_picked_up(self, ilist)
                    self.messages.append("Picked up " + item.name + "!")

    def next_selection(self):
        self.selection += 1
        if self.selection >= len(self.inventory):
            self.selection = 0

    def prev_selection(self):
        self.selection -= 1
        if self.selection < 0:
            self.selection = len(self.inventory)-1

    def equip(self, item):
        if not self.equipped and item in self.inventory and isinstance(item, Equipable):
            self.messages.append("Equipped " + item.name + ".")
            item.equipped = True
            self.equipped = self.inventory.pop(self.inventory.index(item))
            self.hp += item.hpbuff
            self.max_hp += item.hpbuff
            self.armor += item.armorbuff
            self.dmg += item.dmgbuff
            self.spell = item.spell
            self.spell_range = item.spell_range
            self.spell_cooldown = item.spell_cooldown
            self.spell_damage = item.spell_damage

    def unequip(self, item):
        if self.equipped == item:
            if self.inventory_limit == len(self.inventory):
                self.messages.append("Your inventory is full, you need to drop something first.")
            else:
                self.messages.append("Unequipped " + item.name + ".")
                item.equipped = False
                self.inventory.append(item)
                self.equipped = None
                self.hp -= item.hpbuff
                self.max_hp -= item.hpbuff
                self.armor -= item.armorbuff
                self.dmg -= item.dmgbuff
                self.spell = None
                self.spell_range = 0
                self.spell_cooldown = 0
                self.spell_damage = 0

    def consume(self, item, buffs, volume):
        if isinstance(item, Consumable):
            if item.heal > 0:
                if self.hp == self.max_hp:
                    self.messages.append("Already at full health.")
                elif item.heal >= 0:
                    self.messages.append("Used " + item.name + "!")
                    hp_before = self.hp
                    self.hp = min(self.max_hp, self.hp + item.heal)
                    self.messages.append("Healed for " + str(self.hp - hp_before) + " health points!")
                    self.inventory.pop(self.inventory.index(item))
            elif item.armorbuff > 0 or item.hpbuff > 0 or item.dmgbuff > 0:
                effect = pg.mixer.Sound(const.BUFF_SOUND)
                effect.set_volume(volume)
                effect.play()
                buffs.append(Buffs.Buff(self.surface, item.buff_sprites_key, self, item.hpbuff, item.dmgbuff, item.armorbuff, item.buff_duration))
                self.messages.append("Buffed for " + str(item.buff_duration) + " turns! HP+: {0} DMG+: {1} ARM+: {2}".format(item.hpbuff, item.dmgbuff, item.armorbuff))
                self.inventory.pop(self.inventory.index(item))

    def draw_hud(self):
        self.hud_heart_sprite = const.ACTOR_DICT["HUD_HEART_FULL"]
        drawn_hearts = 0
        y = 0
        for x in range(self.max_hp):
            if drawn_hearts >= 10:
                y = drawn_hearts // 10
                x -= 10*y
            self.surface.blit(self.hud_heart_sprite, (x*32, y*32))
            drawn_hearts += 1
            if drawn_hearts == self.hp:
                self.hud_heart_sprite = const.ACTOR_DICT["HUD_HEART_EMPTY"]
        y += 1
        for x in range(self.armor):
            self.surface.blit(const.ACTOR_DICT["HUD_SHIELD"], (x*32, y*32))
        y += 1
        for x in range(self.dmg):
            self.surface.blit(const.ACTOR_DICT["HUD_SWORD"], (x*32, y*32))

    def destroy_sprites(self):
        self.sprites = None
        self.sprite = None
        self.sprites_mirrored = None
        self.hud_heart_sprite = None

    def init_sprites(self):
        self.sprite = const.ACTOR_DICT[self.sprites_key][0]
        self.sprites = const.ACTOR_DICT[self.sprites_key]
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in const.ACTOR_DICT[self.sprites_key]]


class Item(Actor):
    def __init__(self, x, y, name, sprites_key, world_map, surface, messages, equipped=False, mirror=False):
        super().__init__(x, y, name, sprites_key, world_map, surface, messages)
        self.mirror = mirror
        self.sprites_key = sprites_key
        self.sprite_index = 0
        if equipped:
            self.sprite = const.ACTOR_DICT[self.sprites_key][1]
            self.sprite_index = 1
        else:
            self.sprite = const.ACTOR_DICT[self.sprites_key][0]
            self.sprite_index = 0
        self.equipped = equipped
        self.x_offset = const.ACTOR_DICT[self.sprites_key][2]
        self.y_offset = const.ACTOR_DICT[self.sprites_key][3]

    def become_picked_up(self, player, items):
        # NB, Changed this so inventory items are counted in overall items
        player.inventory.append(items.pop(items.index(self)))
        self.sprite = self.sprites[1]
        self.sprite_index = 1

    def drop(self, creature, items):
        self.x, self.y = creature.get_location()
        self.sprite = self.sprites[0]
        self.sprite_index = 0
        items.append(creature.inventory.pop(creature.inventory.index(self)))

    def death_drop(self, creature, items):
        self.x, self.y = creature.get_location()
        self.sprite = self.sprites[0]
        self.sprite_index = 0
        self.mirror = False
        self.equipped = False
        items.append(creature.equipped)

    def is_equipped(self):
        return self.equipped

    def draw(self, camera, creature=None):
        if not creature:
            self.surface.blit(self.sprite, ((self.x + camera.get_x_offset())* const.TILE_WIDTH, (self.y + 1 + camera.get_y_offset()) * const.TILE_HEIGHT))
        elif self.equipped:
            if isinstance(self, Equipable):
                if creature.mirror is not self.mirror:
                    self.mirror = creature.mirror
                    self.sprite = pg.transform.flip(self.sprite, True, False)
                self.surface.blit(self.sprite, ((creature.x + self.x_offset + camera.get_x_offset()) * const.TILE_WIDTH, (creature.y + self.y_offset + 1 + camera.get_y_offset()) * const.TILE_HEIGHT))

    def init_sprites(self):
        if self.mirror:
            self.sprites = [pg.transform.flip(e, True, False) for e in const.ACTOR_DICT[self.sprites_key][:2]]
            self.sprite = self.sprites[self.sprite_index]
        else:
            self.sprites = const.ACTOR_DICT[self.sprites_key]
            self.sprite = const.ACTOR_DICT[self.sprites_key][self.sprite_index]


class Equipable(Item):
    def __init__(self, x, y, name, sprites_key, world_map, surface, messages, hpbuff=0, armorbuff=0, dmgbuff=0, equipped=False, mirror=False, spell=None, spell_damage=0, spell_cooldown=0, spell_range=0):
        super().__init__(x, y, name, sprites_key, world_map, surface, messages, equipped, mirror)
        self.hpbuff = hpbuff
        self.armorbuff = armorbuff
        self.dmgbuff = dmgbuff
        self.spell = spell
        self.spell_damage = spell_damage
        self.spell_cooldown = spell_cooldown
        self.spell_range = spell_range


class Consumable(Item):
    def __init__(self, x, y, name, sprites, world_map, surface, messages, hpbuff=0, armorbuff=0, dmgbuff=0, buff_duration=0, heal=0, buff_sprites_key=None, equipped=False):
        super().__init__(x, y, name, sprites, world_map, surface, messages, equipped)
        self.hpbuff = hpbuff
        self.armorbuff = armorbuff
        self.dmgbuff = dmgbuff
        self.buff_duration = buff_duration
        self.heal = heal
        self.buff_sprites_key = buff_sprites_key


class Container(Actor):
    """
    Child of Actor, the Container object is an object in the game world that is inanimate but has an inventory (empty by default).
    Once items are implemented, this will be one of the ways for the Player object to obtain items.
    """

    def __init__(self, x, y, name, sprites_key, world_map, surface, messages, inventory=[]):
        super().__init__(x, y, name, sprites_key, world_map, surface, messages)
        self.inventory = inventory
        self.sprite_key = sprites_key
        self.sprite = const.ACTOR_DICT[self.sprite_key]
        self.open = False

    def draw(self, camera):
        self.surface.blit(self.sprite, ((self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))

    def is_open(self):
        return self.open

    def set_open(self, boolean):
        self.open = boolean

    def init_sprites(self):
        self.sprite = const.ACTOR_DICT[self.sprite_key]
        self.sprites = const.ACTOR_DICT[self.sprites_key]
