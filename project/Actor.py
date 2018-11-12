import pygame as pg
import constants as const


class Actor:
    def __init__(self, x, y, sprite, anim_sprites, mirror, world_map, surface, idle_frames=45, frame_counter=0):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.anim_sprites = anim_sprites
        self.anim_sprites_mirrored = [pg.transform.flip(e, True, False) for e in anim_sprites]
        self.mirror = mirror
        self.world_map = world_map
        self.surface = surface
        self.idle_frames = idle_frames
        self.frame_counter = frame_counter
    
    def set_sprite(self, sprite):
        self.sprite = sprite

    def control(self, x_change, y_change):
        if not self.world_map[self.y + y_change][self.x + x_change]:  # Checks if can step there
            self.x += x_change
            self.y += y_change
        
        if x_change == -1 and self.mirror == False:
            self.sprite = (pg.transform.flip(self.sprite, True, False))
            self.mirror = True
        elif x_change == 1 and self.mirror == True:
            self.sprite =(pg.transform.flip(self.sprite, True, False))
            self.mirror = False
            

    def draw(self):
        self.surface.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))
        