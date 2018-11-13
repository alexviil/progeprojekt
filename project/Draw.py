import pygame as pg
import constants as const


class Draw:
    def __init__(self, surface, game_map, player, npc):
        self.surface = surface
        self.game_map = game_map
        self.player = player
        self.npc = npc

    def draw_map(self):
        for x in range(0, const.MAP_WIDTH):
            for y in range(1, const.MAP_HEIGHT + 1):
                if self.game_map[y - 1][x][0]:
                    self.surface.blit(const.SPRITE_WALL, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))
                else:
                    self.surface.blit(const.SPRITE_FLOOR, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

    def draw_game(self):
        # Reset the surface
        self.surface.fill(const.GRAY)

        # Draw the map
        self.draw_map()

        # Draw the character
        self.player.draw()
        
        # Draw an NPC
        self.npc.draw()

        # Update display
        pg.display.flip()
