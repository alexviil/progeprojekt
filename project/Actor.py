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

    def draw(self):
        """Draws the actor object onto a pygame surface with the coordinates multiplied by the game's tile width and height'"""
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))
    
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
    def __init__(self, x, y, name, sprites, mirror, world_map, surface, actors, actors_inanimate, messages, hp, idle_frames=10, frame_counter=0):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in sprites]
        self.mirror = mirror
        self.idle_frames = idle_frames
        self.frame_counter = frame_counter
        self.max_hp = hp
        self.hp = hp
        
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
            if actor is not self and actor.get_location() == (self.x + x_change, self.y + y_change) and isinstance(actor, Actor):
                target = actor
                break

        if isinstance(target, Creature):  # if creature exists, attacks it
            self.messages.append(self.name + " attacks " + target.name + " for 3 damage.")
            target.take_damage(3)

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


class Enemy(Creature):
    """Used to help Ai decide who to move."""
    pass


class Player(Creature):
    """No function as of yet."""
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
    
    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, (self.y + 1) * const.TILE_HEIGHT))
