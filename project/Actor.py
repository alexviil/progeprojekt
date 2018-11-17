import pygame as pg
import constants as const


class Actor:
    """
    The Actor class is the parent class for interactive objects like the player, enemies, chests and items. Each
    object has it's starting coordinates, a name, a sprite (or multiple for animations), the world map
    to follow, a surface to be drawn on, the list of all actors and inanimate actors and messages related
    to the actor.
    """
    def __init__(self, x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages):
        self.x = x
        self.y = y
        self.name = name
        self.sprites = sprites
        self.world_map = world_map
        self.surface = surface
        self.actors = actors
        self.actors_inanimate = actors_inanimate
        self.messages = messages

    def set_sprite(self, sprite):
        self.sprite = sprite

    def get_sprite(self):
        return self.sprite

    def draw(self, camera):
        """Draws the actor object onto a pygame surface with the coordinates multiplied by the game's tile width and height'"""
        self.surface.blit(self.sprite, ((self.x + camera.get_x_offset())* const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
    
    def get_location(self):
        return self.x, self.y

    def get_name(self):
        return self.name


class Creature(Actor):
    """
    A child of Actor, the Creature class inherits all previous attributes and receives some new attributes. For every sprite
    the Creature class also has each sprite mirrored and a mirrored attribute with a boolean value. This is used for when
    the object moves to the left, as to leave the impression that the object is actually walking in that direction and not
    moonwalking. Creature also has idle_frames, which specifies the amount of frames to display each idle sprite, and
    a frame_counter to keep track of when each Creature needs to have their idle sprite updated. max_hp and hp are used for
    combat, with the latter being the upper limit or maximum possible hp.
    """
    def __init__(self, x, y, name, sprites, mirror, world_map, surface, actors, actors_inanimate, messages, hp=10, armor=0, dmg=3, inventory=[], equipped=None, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in sprites]
        self.mirror = mirror
        self.idle_frames = idle_frames
        self.frame_counter = frame_counter
        self.inventory = inventory
        self.equipped = equipped
        self.max_hp = hp
        self.hp = hp
        self.armor = armor
        self.dmg = dmg
        
        if self.mirror == True :
            self.sprite = self.sprites_mirrored[0]
        else:
            self.sprite = self.sprites[0]
            
    def control(self, x_change, y_change):
        """
        Whether by AI or events, a Creature object can move in some direction. To do that, first, this function checks
        if the destination tile is already occupied by another creature. If so, the Creature object will set the other
        Creature object as it's target, check whether it exists and cause it to take_damage as described below.
        Otherwise, if no Creature object is present, it will check if the destination tile is an impassable object (wall, container)
        and if not, step there. If the movement is done to the opposite direction of the Creature's sprite, the sprite will now become
        mirrored.
        """
        target = None
        for actor in self.actors + self.actors_inanimate:  # Checks if creature exists and target location
            if actor is not self and actor.get_location() == (self.x + x_change, self.y + y_change) and isinstance(actor, Actor) and not isinstance(actor, Item):
                target = actor
                break

        if isinstance(target, Creature) and not isinstance(target, self.__class__):  # if creature exists and is not same class, attacks it
            self.messages.append(self.name + " attacks " + target.name + " for " + str(max(0, self.dmg - target.armor)) + " damage.")
            target.take_damage(max(0, self.dmg - target.armor))

        elif isinstance(target, Container) and isinstance(self, Player):
            if target.is_open():
                self.messages.append("The chest has already been opened.")
            elif target.inventory == []:
                self.messages.append("The chest contains nothing of value.")
            else:
                self.messages.append("The chest contains an item!")
            target.set_open(True)
            target.set_sprite(const.SPRITE_CHEST_OPEN)

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

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0 # to avoid negative health
        self.messages.append(self.name + "'s health is " + str(self.hp) + "/" + str(self.max_hp))

        if self.hp <= 0:
            self.death()

    def death(self):
        self.messages.append(self.name + " is dead.")
        self.actors.remove(self)
    
    def get_location(self):
        return (self.x, self.y)


class Enemy(Creature):
    """Used to help Ai decide who to move."""
    pass


class Player(Creature):
    def __init__(self, x, y, name, sprites, mirror, world_map, surface, actors, actors_inanimate, items, messages, hp=20, armor=0, dmg=3, inventory=[], equipped=None, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites, mirror, world_map, surface, actors, actors_inanimate, messages, hp, armor, dmg, inventory, equipped, idle_frames, frame_counter)
        self.items = items
        self.inventory_limit = 3
        self.selection = 0

    def pick_up(self):
        for item in self.items:
            if item.get_location() == self.get_location():
                item.become_picked_up(self, self.items)
                self.messages.append("Picked up " + item.name + "!")

    def next_selection(self):
        self.selection += 1
        if self.selection >= len(self.inventory):
            self.selection = 0

    def equip(self, item):
        if not self.equipped and item in self.inventory:
            item.equipped = True
            self.equipped = self.inventory.pop(self.inventory.index(item))
            self.hp += item.hpbuff
            self.max_hp += item.hpbuff
            self.armor += item.armorbuff
            self.dmg += item.dmgbuff

    def unequip(self, item):
        if self.equipped == item:
            item.equipped = False
            self.inventory.append(item)
            self.equipped = None
            self.hp -= item.hpbuff
            self.max_hp -= item.hpbuff
            self.armor -= item.armorbuff
            self.dmg -= item.dmgbuff


class Item(Actor):
    def __init__(self, x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages, equipped=False, mirror=False):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.mirror = mirror
        self.sprites = sprites
        self.sprite = sprites[0]
        self.equipped = equipped

    def become_picked_up(self, player, items):
        player.inventory.append(items.pop(items.index(self)))
        self.sprite = self.sprites[1]

    def drop(self, creature, items):
        self.x, self.y = creature.get_location()
        self.sprite = self.sprites[0]
        items.append(creature.inventory.pop(creature.inventory.index(self)))

    def is_equipped(self):
        return self.equipped

    def draw(self, camera):
        if self.x != 0 and self.y != 0:
            self.surface.blit(self.sprite, ((self.x + camera.get_x_offset())* const.TILE_WIDTH, (self.y + 1 + camera.get_y_offset()) * const.TILE_HEIGHT))
        elif self.equipped:
            self.surface.blit(self.sprite, ((creature.x + camera.get_x_offset()) * const.TILE_WIDTH, (creature.y + 1 + camera.get_y_offset()) * const.TILE_HEIGHT))


class Equipable(Item):
    def __init__(self, x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages, hpbuff=0, armorbuff=0, dmgbuff=0):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.hpbuff = hpbuff
        self.armorbuff = armorbuff
        self.dmgbuff = dmgbuff


class Consumable(Item):
    pass


class Container(Actor):
    """
    Child of Actor, the Container object is an object in the game world that is inanimate but has an inventory (empty by default).
    Once items are implemented, this will be one of the ways for the Player object to obtain items.
    """

    def __init__(self, x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages, inventory=[]):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.inventory = inventory
        self.sprite = sprites
        self.open = False

    def draw(self, camera):
        self.surface.blit(self.sprite, (
        (self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + 1 + camera.get_y_offset()) * const.TILE_HEIGHT))

    def is_open(self):
        return self.open

    def set_open(self, boolean):
        self.open = boolean
