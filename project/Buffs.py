import constants as const
import pygame as pg
import Actor


class Buff:
    def __init__(self, surface, sprites_key, target, hpbuff, dmgbuff, armorbuff, duration=5, ai_change=None):
        self.surface = surface
        self.sprites_key = sprites_key
        self.sprites = const.BUFF_DICT[self.sprites_key]
        self.sprite = self.sprites[0]
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
        self.idle_frames = 7
        self.initial_ai = None
        self.initial_idle_frames = target.idle_frames
        if isinstance(target, Actor.Enemy):
            self.initial_ai = target.ai
            self.ai_change = ai_change

    def update(self, blist, alist):
        if self.target not in alist:
            blist.pop(blist.index(self))
            return
        self.turn_counter += 1
        self.x, self.y = self.target.get_location()
        self.mirror = self.target.mirror
        if self.turn_counter == self.duration:
            if self.initial_ai:
                self.target.ai = self.initial_ai
            self.target.idle_frames = self.initial_idle_frames
            self.target.frame_counter = 0
            self.target.max_hp -= self.hpbuff
            self.target.hp = max(1, self.target.hp - self.hpbuff)
            self.target.dmg -= self.dmgbuff
            self.target.armor -= self.armorbuff
            blist.pop(blist.index(self))
            btype = ""
            if self.dmgbuff + self.hpbuff + self.armorbuff < 0:
                btype = "de"
            if isinstance(self.target, Actor.Player):
                self.target.messages.append(self.target.name + "'s {0}buff wanes off.".format(btype))

    def draw(self, camera):
        if self.frame_counter == self.idle_frames * 4:
            self.frame_counter = 0
        self.sprite = self.sprites[self.frame_counter // self.idle_frames]
        if self.mirror:
            self.surface.blit(self.sprite, ((self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
        else:
            self.surface.blit(pg.transform.flip(self.sprite, True, False), ((self.x + camera.get_x_offset()) * const.TILE_WIDTH, (self.y + camera.get_y_offset()) * const.TILE_HEIGHT))
        self.frame_counter += 1

    def destroy_sprites(self):
        self.sprites = None
        self.sprite = None

    def init_sprites(self):
        self.sprites = const.BUFF_DICT[self.sprites_key]
        self.sprite = self.sprites[0]

    def set_surface(self, surface):
        self.surface = surface
