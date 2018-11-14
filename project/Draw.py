import pygame as pg
import libtcodpy as libt
import constants as const


class Draw:
    def __init__(self, surface, game_map, player, fov_map, npcs=[], containers=[]):
        self.surface = surface
        self.game_map = game_map
        self.fov_map = fov_map
        self.player = player
        self.npcs = npcs
        self.containers = containers

    def draw_map(self):
        for y in self.game_map:
            for tile in y:
                if self.check_fov(tile.x, tile.y):  # only draws if area is in field of view
                    tile.explored = True
                    self.surface.blit(tile.sprite, (tile.x * const.TILE_WIDTH, tile.y * const.TILE_HEIGHT))
                elif tile.explored:
                    self.surface.blit(tile.explored_sprite, (tile.x * const.TILE_WIDTH, tile.y * const.TILE_HEIGHT))

    def draw_game(self):
        # Reset the surface
        self.surface.fill(const.GRAY)

        # Draw the map
        self.draw_map()

        # Draw Containers
        for container in self.containers:
            if self.check_fov(container.x, container.y+1):  # only draws if area is in field of view
                container.draw()

        # Draw the character
        self.player.draw()
        
        # Draw NPCs
        for npc in self.npcs:
            if self.check_fov(npc.x, npc.y+1):  # only draws if area is in field of view
                npc.draw()

        # Update display
        pg.display.flip()

    def check_fov(self, x, y):
        return libt.map_is_in_fov(self.fov_map, x, y)
