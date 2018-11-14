import pygame as pg
import constants as const


class Actor:
    def __init__(self, x, y, sprites, world_map, surface):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.world_map = world_map
        self.surface = surface
    
    def set_sprite(self, sprite):
        self.sprite = sprite

    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))
    
    def get_location(self):
        return self.x, self.y

class Creature(Actor):
    def __init__(self, x, y, sprites, mirror, world_map, surface, idle_frames=30, frame_counter=0):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.sprites_mirrored = [pg.transform.flip(e, True, False) for e in sprites]
        self.mirror = mirror
        self.world_map = world_map
        self.surface = surface
        self.idle_frames = idle_frames
        self.frame_counter = frame_counter
        
        if self.mirror == True :
            self.sprite = self.sprites_mirrored[0]
        else:
            self.sprite = self.sprites[0]
            
    def control(self, x_change, y_change):
        if not self.world_map[self.y + y_change][self.x + x_change].get_is_wall() and not self.world_map[self.y + y_change][self.x + x_change].get_is_creature():  # Checks if can step there
            self.x += x_change
            self.y += y_change

        if x_change == -1 and self.mirror == False:
            self.sprite = (pg.transform.flip(self.sprite, True, False))
            self.mirror = True
        elif x_change == 1 and self.mirror == True:
            self.sprite = (pg.transform.flip(self.sprite, True, False))
            self.mirror = False

class Container(Actor):
    def __init__(self, x, y, sprites, world_map, surface, inventory=[]):
        self.x = x
        self.y = y
        self.sprites = sprites
        self.world_map = world_map
        self.surface = surface
        self.inventory = inventory
        self.sprite = sprites
    
    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, (self.y + 1) * const.TILE_HEIGHT))