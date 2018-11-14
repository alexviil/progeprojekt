import pygame as pg
import constants as const


class Draw:
    def __init__(self, surface, game_map, player, npcs=[], containers=[]):
        self.surface = surface
        self.game_map = game_map
        self.player = player
        self.npcs = npcs
        self.containers = containers

    def draw_map(self):
        for y in self.game_map:
            for tile in y:
                self.surface.blit(tile.sprite, (tile.x * const.TILE_WIDTH, tile.y * const.TILE_HEIGHT))

    def draw_game(self):
        # Reset the surface
        self.surface.fill(const.GRAY)

        # Draw the map
        self.draw_map()

        # Draw Containers
        for container in self.containers: container.draw()

        # Draw the character
        self.player.draw()
        
        # Draw NPCs
        for npc in self.npcs: npc.draw()

        # Update display
        pg.display.flip()
