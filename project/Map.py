import pygame as pg
import constants as const
import Tile


class Map:
    def __init__(self):
        self.game_map = list()

    def create_map(self):
        # self.game_map = [[False for y in range(0, const.MAP_HEIGHT)] for x in range(0, const.MAP_WIDTH)]
        self.game_map = list()
        for y in range(const.MAP_HEIGHT):
            row = []
            for x in range(const.MAP_HEIGHT):
                if y == 0 or y == const.MAP_HEIGHT - 1 or x == 0 or x == const.MAP_WIDTH - 1:
                    row.append(Tile.Tile(x, y + 1, True, False, const.SPRITE_WALL))
                    continue
                row.append(Tile.Tile(x, y + 1, False, False))
            self.game_map.append(row)

    def update(self, actor_locations):
        
        for y in range(0, const.MAP_HEIGHT):
            for x in range(0, const.MAP_WIDTH):
                # Actor collision boxes
                for actor_location in actor_locations:
                    if (x, y) in actor_locations:
                        self.game_map[y][x].is_creature = True
                    else:
                        self.game_map[y][x].is_creature = False

    def get_game_map(self):
        return self.game_map

    def get_tile(self, x, y):
        return self.game_map[y][x]
