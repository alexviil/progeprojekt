import pygame as pg
import constants as const


class Map:
    def __init__(self):
        self.game_map = list()

    def create_map(self):
        # self.game_map = [[False for y in range(0, const.MAP_HEIGHT)] for x in range(0, const.MAP_WIDTH)]
        self.game_map = list() # Tile structure: [is_wall, is_actor/is_movingobject]
        for y in range(0, const.MAP_HEIGHT):
            row = []
            for x in range(0, const.MAP_WIDTH):
                if y == 0 or y == const.MAP_HEIGHT-1 or x == 0 or x == const.MAP_WIDTH-1:
                    row.append([True, False])
                    continue
                row.append([False, False])
            self.game_map.append(row)
            
    def update(self, actor_locations):
        for y in range(0, const.MAP_HEIGHT):
            for x in range(0, const.MAP_WIDTH):
                # Actor collision boxes
                for actor_location in actor_locations:
                    if actor_location[0] == x and actor_location[1] == y:
                        self.game_map[y][x][1] = True
                    else:
                        self.game_map[y][x][1] = False

    def get_game_map(self):
        return self.game_map

    def get_tile(self, x, y):
        return self.game_map[y][x]
