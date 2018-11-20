import pygame as pg
import constants as const
import libtcodpy as libt
import Tile


class Map:
    """
    The Map object is used to create the game map using the Tile object, which then receives attribute values
    according to how the map is set to be generated. We hope to implement libtcod's random map generator soon.

    Map also checks actor locations when they move, updating tiles to let them know where the actors can't step,
    and calculates the field of view for the player according to player's coordinates.
    """
    def __init__(self):
        self.game_map = list()
        self.bit_map = list()
        self.fov_map = libt.map_new(const.MAP_WIDTH, const.MAP_HEIGHT+1)
        self.first_room_center = (1, 1)

    def create_map(self):
        """
        Creates the game map, currently a simple square to test things out. Has a set of floor sprites to choose
        from, with a strong bias towards the first, simplest floor tile sprite. Creates a FOV map for the player as well.
        """
        self.game_map = list()
        for y in range(const.MAP_HEIGHT):
            row = []
            for x in range(const.MAP_WIDTH):
                random = libt.random_get_int(0, 0, 7)
                bias = 0
                while random != 0 and bias != 12:
                    bias += 1
                    random = libt.random_get_int(0, 0, 7)
                if y == 0 or y == const.MAP_HEIGHT - 1 or x == 0 or x == const.MAP_WIDTH - 1:
                    row.append(Tile.Tile(x, y+1, True, False, const.SPRITE_WALL, const.SPRITE_WALLEXPLORED))
                    continue
                row.append(Tile.Tile(x, y+1, False, False, const.SPRITES_FLOOR[random], const.SPRITES_FLOOREXPLORED[random]))
            self.game_map.append(row)

        # TODO Need to figure out this +1 y thing, "it's probably just pygame being pygame" - Alex
        self.game_map[11][11] = Tile.Tile(11, 12, True, False, const.SPRITE_WALL, const.SPRITE_WALLEXPLORED)

        self.create_fov_map()

    def update(self, actor_locations):
        """
        Checks the location of all actors and updates all tiles that had actors and now have actors. Used for
        actor collision, to keep them from being on the same tile at once.
        """
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
                libt.map_set_properties(self.fov_map, x, y+1,
                                        not self.game_map[y][x].get_is_wall(),
                                        not self.game_map[y][x].get_is_wall())

    def calculate_fov_map(self, player):
        libt.map_compute_fov(self.fov_map, player.x, player.y+1, const.TORCH_RADIUS, const.FOV_LIGHT_WALLS, const.FOV_ALGORITHM)

    def create_test_map(self):
        for y in range(const.MAP_HEIGHT):
            self.game_map.append(list())
            for x in range(const.MAP_WIDTH):
                self.game_map[y].append(Tile.Tile(x, y+1, True, False, const.SPRITE_WALL, const.SPRITE_WALLEXPLORED))
        rooms = list()

        for n in range(const.POSSIBLE_ROOM_NUM):
            width = libt.random_get_int(0, const.MIN_ROOM_SIZE, const.MAX_ROOM_SIZE)
            height = libt.random_get_int(0, const.MIN_ROOM_SIZE, const.MAX_ROOM_SIZE)
            x = libt.random_get_int(0, 0, const.MAP_WIDTH-width-1)
            y = libt.random_get_int(0, 0, const.MAP_HEIGHT-height-1)

            room = Room(x, y, width, height)

            if not any(room.check_intersection(other_room) for other_room in rooms):
                rooms.append(room)
                self.insert_room(room)

                if len(rooms) >= 2:
                    if libt.random_get_int(0, 0, 1):  # Randomizes whether it goes horizontal or vertical tunnel first
                        self.x_tunnel(rooms[-2], rooms[-1])
                        self.y_tunnel(rooms[-2], rooms[-1])
                    else:
                        self.y_tunnel(rooms[-2], rooms[-1])
                        self.x_tunnel(rooms[-2], rooms[-1])

        self.first_room_center = rooms[0].center_x, rooms[0].center_y

        self.create_fov_map()

    def insert_room(self, room):
        for y in range(room.y1+1, room.y2):
            for x in range(room.x1+1, room.x2):
                self.game_map[y][x] = self.create_floor_tile(x, y)

    def x_tunnel(self, room1, room2):
        for x in range(min(room1.center_x, room2.center_x), max(room1.center_x, room2.center_x)+1):
            self.game_map[room1.center_y][x] = self.create_floor_tile(x, room1.center_y)

    def y_tunnel(self, room1, room2):
        for y in range(min(room1.center_y, room2.center_y), max(room1.center_y, room2.center_y)+1):
            self.game_map[y][room2.center_x] = self.create_floor_tile(room2.center_x, y)

    def create_floor_tile(self, x, y):
        bias = 0
        random = libt.random_get_int(0, 0, 7)
        while random != 0 and bias != 12:
            bias += 1
            random = libt.random_get_int(0, 0, 7)
        return Tile.Tile(x, y+1, False, False, const.SPRITES_FLOOR[random], const.SPRITES_FLOOREXPLORED[random])


class Room:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.center_x = (self.x1 + self.x2) // 2
        self.center_y = (self.y1 + self.y2) // 2

    def check_intersection(self, other_room):
        return self.x1 <= other_room.x2 and self.x2 >= other_room.x1 and self.y1 <= other_room.y2 and self.y2 >= other_room.y1


if __name__ == '__main__':
    level = Map()
    level.create_map()
    level.create_test_map()
