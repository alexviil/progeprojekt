import pygame as pg
import constants as const


class Animations:
    """
    The Animations object updates the frame_counter of each actor and their sprite once the frame_counter reaches
    a certain point. After the last sprite, the frame_counter gets reset and the animations begin from the first sprite.
    Uses mirrored sprites, if the Actor object's mirror attribute has the value of True.
    """
    def __init__(self, actors):
        self.frame_counter = 0
        self.actors = actors
    
    def update(self):
        for actor in self.actors:
            actor.frame_counter += 1
            
            if actor.mirror == False:
                if actor.frame_counter == actor.idle_frames*4:
                    actor.set_sprite(actor.sprites[0])
                    actor.frame_counter = 0
                elif actor.frame_counter % actor.idle_frames == 0:
                    actor.set_sprite(actor.sprites[int(actor.frame_counter // actor.idle_frames)])
                   
            elif actor.mirror == True:
                if actor.frame_counter == actor.idle_frames*4:
                    actor.set_sprite(actor.sprites_mirrored[0])
                    actor.frame_counter = 0
                elif actor.frame_counter % actor.idle_frames == 0:
                    actor.set_sprite(actor.sprites_mirrored[int(actor.frame_counter // actor.idle_frames)])
