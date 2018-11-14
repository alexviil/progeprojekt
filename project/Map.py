import pygame as pg
import constants as const
import libtcodpy as libt
import Tile


class Map:
    def __init__(self):
        self.game_map = list()
        self.fov_map = libt.map_new(const.MAP_WIDTH, const.MAP_HEIGHT+1)

    def create_map(self):
        self.game_map = list()
        for y in range(const.MAP_HEIGHT):
            row = []
            for x in range(const.MAP_WIDTH):
                if y == 0 or y == const.MAP_HEIGHT - 1 or x == 0 or x == const.MAP_WIDTH - 1:
                    row.append(Tile.Tile(x, y + 1, True, False, const.SPRITE_WALL, const.SPRITE_WALLEXPLORED))
                    continue
                row.append(Tile.Tile(x, y + 1, False, False))
            self.game_map.append(row)

        # TODO Need to figure out this +1 y thing
        self.game_map[11][11] = Tile.Tile(11, 12, True, False, const.SPRITE_WALL, const.SPRITE_WALLEXPLORED)

        self.create_fov_map()

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

    def create_fov_map(self):
        for y in range(const.MAP_HEIGHT):
            for x in range(const.MAP_WIDTH):
                libt.map_set_properties(self.fov_map, x, y+1, not self.game_map[y][x].get_is_wall(), not self.game_map[y][x].get_is_wall())

    def calculate_fov_map(self, player):
        libt.map_compute_fov(self.fov_map, player.x, player.y+1, const.TORCH_RADIUS, const.FOV_LIGHT_WALLS, const.FOV_ALGORITHM)
