import pygame as pg
import constants as const


class Actor:
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
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))
    
    def get_location(self):
        return self.x, self.y

    def get_name(self):
        return self.name


class Creature(Actor):
    def __init__(self, x, y, name, sprites, mirror, world_map, surface, actors, actors_inanimate, messages, hp, idle_frames=30, frame_counter=0):
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
        self.messages.append(self.name + "'s health is " + str(self.hp) + "/" + str(self.max_hp))

        if self.hp <= 0:
            self.death()

    def death(self):
        self.messages.append(self.name + " is dead.")
        self.actors.remove(self)


class Enemy(Creature):
    pass


class Container(Actor):
    def __init__(self, x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages, inventory=[]):
        super().__init__(x, y, name, sprites, world_map, surface, actors, actors_inanimate, messages)
        self.inventory = inventory
        self.sprite = sprites
    
    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, (self.y + 1) * const.TILE_HEIGHT))
