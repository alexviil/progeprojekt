import constants as const
import pygame as pg


class Buff:
    def __init__(self, surface, sprites, target, hpbuff, dmgbuff, armorbuff, duration=5):
        self.surface = surface
        self.sprites = sprites
        self.sprite = sprites[0]
        self.target = target
        self.hpbuff = hpbuff
        self.dmgbuff = dmgbuff
        self.armorbuff = armorbuff
        self.duration = duration
        self.turn_counter = 0
        self.target.max_hp += hpbuff
        self.target.hp = min(target.hp + hpbuff, target.max_hp)
        self.target.dmg += dmgbuff
        self.target.armor += armorbuff
        self.x, self.y = self.target.get_location()
        self.mirror = self.target.mirror
        self.frame_counter = 0
        self.idle_frames = 4

    def update(self, blist):
        self.turn_counter += 1
        self.x, self.y = self.target.get_location()
        self.mirror = self.target.mirror
        if self.turn_counter == self.duration:
            self.target.max_hp -= self.hpbuff
            self.target.hp = max(1, self.target.hp - self.hpbuff)
            self.target.dmg -= self.dmgbuff
            self.target.armor -= self.armorbuff
            blist.pop(blist.index(self))

    def draw(self, camera):
        if self.mirror:
            self.surface.blit(self.sprite, ((self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
        else:
            self.surface.blit(pg.transform.flip(self.sprite, True, False), ((self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
