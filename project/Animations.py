import pygame as pg
import constants as const


class Animations:
    def __init__(self, actors):
        self.frame_counter = 0
        self.actors = actors
    
    def update(self):
        for actor in self.actors:
            actor.frame_counter += 1
            
            if actor.mirror == False:
                if actor.frame_counter == actor.idle_frames*3:
                    actor.set_sprite(actor.anim_sprites[0])
                    actor.frame_counter = 0
                elif actor.frame_counter % actor.idle_frames == 0:
                    actor.set_sprite(actor.anim_sprites[actor.frame_counter // actor.idle_frames])
                   
            elif actor.mirror == True:
                if actor.frame_counter == actor.idle_frames*3:
                    actor.set_sprite(actor.anim_sprites_mirrored[0])
                    actor.frame_counter = 0
                elif actor.frame_counter % actor.idle_frames == 0:
                    actor.set_sprite(actor.anim_sprites_mirrored[actor.frame_counter // actor.idle_frames])
