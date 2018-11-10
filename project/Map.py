import pygame as pg
import constants as const


class Map:
    def __init__(self):
        self.game_map = list()

    def create_map(self):
        # self.game_map = [[False for y in range(0, const.MAP_HEIGHT)] for x in range(0, const.MAP_WIDTH)]
        self.game_map = list()
        for y in range(0, const.MAP_HEIGHT):
            row = []
            for x in range(0, const.MAP_WIDTH):
                if y == 0 or y == const.MAP_HEIGHT-1 or x == 0 or x == const.MAP_WIDTH-1:
                    row.append(True)
                    continue
                row.append(False)
            self.game_map.append(row)

    def get_game_map(self):
        return self.game_map
