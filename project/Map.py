import pygame as pg
import constants as const
import libtcodpy as libt
import Tile, Generator, Actor


class Map:
    """
    The Map object is used to create the game map using the Tile object, which then receives attribute values
    according to how the map is set to be generated. We hope to implement libtcod's random map generator soon.

    Map also checks actor locations when they move, updating tiles to let them know where the actors can't step,
    and calculates the field of view for the player according to player's coordinates.
    """
    def __init__(self, floor):
        self.game_map = list()
        self.bit_map = list()
        self.fov_map = libt.map_new(const.MAP_WIDTH, const.MAP_HEIGHT+1)
        self.first_room_center = (1, 1)
        self.rooms = list()
        self.floor = floor

    def create_map(self):
        self.game_map.clear()
        self.bit_map.clear()
        self.fov_map = libt.map_new(const.MAP_WIDTH, const.MAP_HEIGHT + 1)
        self.first_room_center = (1, 1)
        self.rooms.clear()
        for y in range(const.MAP_HEIGHT):
            self.game_map.append(list())
            for x in range(const.MAP_WIDTH):
                self.game_map[y].append(Tile.Tile(x, y + 1, True, False, "SPRITE_WALL", "SPRITE_WALLEXPLORED"))

        for n in range(const.POSSIBLE_ROOM_NUM):
            width = libt.random_get_int(0, const.MIN_ROOM_SIZE, const.MAX_ROOM_SIZE)
            height = libt.random_get_int(0, const.MIN_ROOM_SIZE, const.MAX_ROOM_SIZE)
            x = libt.random_get_int(0, 0, const.MAP_WIDTH - width - 1)
            y = libt.random_get_int(0, 0, const.MAP_HEIGHT - height - 1)

            room = Room(x, y, width, height)

            if not any(room.check_intersection(other_room) for other_room in self.rooms):
                self.rooms.append(room)
                self.insert_room(room)

                if len(self.rooms) >= 2:
                    if libt.random_get_int(0, 0, 1):  # Randomizes whether it goes horizontal or vertical tunnel first
                        self.x_tunnel(self.rooms[-2], self.rooms[-1])
                        self.y_tunnel(self.rooms[-2], self.rooms[-1])
                    else:
                        self.y_tunnel(self.rooms[-2], self.rooms[-1])
                        self.x_tunnel(self.rooms[-2], self.rooms[-1])

        self.first_room_center = self.rooms[0].center_x, self.rooms[0].center_y
        if len(self.rooms) <= 1:
            hole_x = self.rooms[0].center_x
            hole_y = self.rooms[0].center_y
        else:
            hole_x = self.rooms[1].center_x
            hole_y = self.rooms[1].center_y

        self.game_map[hole_y][hole_x] = Tile.Tile(hole_x, hole_y + 1, False, False,
                                                  "SPRITE_FLOOR_LADDER",
                                                  "SPRITE_FLOOR_LADDER_EXPLORED",
                                                  True)

        self.create_fov_map()

    def destroy_surfaces(self):
        for y, row in enumerate(self.game_map):
            for x, tile in enumerate(row):
                self.game_map[y][x].explored_sprite = None
                self.game_map[y][x].sprite = None

    def initialize_surfaces(self):
        self.fov_map = libt.map_new(const.MAP_WIDTH, const.MAP_HEIGHT + 1)
        for y, row in enumerate(self.game_map):
            for x, tile in enumerate(row):
                self.game_map[y][x].explored_sprite = const.WALL_AND_FLOOR_DICT[self.game_map[y][x].explored_sprite_key]
                self.game_map[y][x].sprite = const.WALL_AND_FLOOR_DICT[self.game_map[y][x].sprite_key]
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

    def get_tile_exists(self, x, y):
        try:
            if self.game_map[y][x]:
                return True
        except IndexError:
            print("AA")
            return False

    def find_line(self, xy1, xy2, penetrate_npc=True, alist=None, penetrate_wall=False):
        x1, y1 = xy1
        x2, y2 = xy2
        libt.line_init(x1, y1, x2, y2)
        diff_x, diff_y = libt.line_step()
        coord_list = []
        if x1 == x2 and y1 == y2:
            coord_list.append((x1, y1))
        while diff_x is not None and diff_y is not None:
            coord_list.append((diff_x, diff_y))
            diff_x, diff_y = libt.line_step()
        if not penetrate_npc:
            for e in coord_list:
                for npc in alist:
                    if e == npc.get_location() and isinstance(npc, Actor.Enemy):
                        try:
                            coord_list = coord_list[:coord_list.index(e)+1]
                        except ValueError:
                            pass
        if not penetrate_wall:
            for e in coord_list:
                if self.get_tile(e[0], e[1]).get_is_wall():
                    coord_list = coord_list[:-coord_list.index(e)]
                    break
        return coord_list

    def create_fov_map(self):
        for y in range(const.MAP_HEIGHT):
            for x in range(const.MAP_WIDTH):
                libt.map_set_properties(self.fov_map, x, y+1,
                                        not self.game_map[y][x].get_is_wall(),
                                        not self.game_map[y][x].get_is_wall())

    def calculate_fov_map(self, player):
        libt.map_compute_fov(self.fov_map, player.x, player.y+1, const.TORCH_RADIUS, const.FOV_LIGHT_WALLS, const.FOV_ALGORITHM)



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
        random = libt.random_get_int(0, 1, 8)
        while random != 1 and bias != 12:
            bias += 1
            random = libt.random_get_int(0, 1, 8)
        return Tile.Tile(x, y+1, False, False, "SPRITE_FLOOR" + str(random), "SPRITE_FLOOREXPLORED" + str(random))

    def populate_rooms(self, generator):
        for room in self.rooms:
            room_width = abs(room.x1 - room.x2)
            room_height = abs(room.y1 - room.y2)
            room_area = room_width * room_height

            for i in range(room_area // 110):
                rand_num = libt.random_get_int(0, 0, 100)
                if rand_num >= 55:
                    x = libt.random_get_int(0, room.x1+2, room.x2-2)
                    y = libt.random_get_int(0, room.y1+2, room.y2-2)
                    if x == room.center_x and y == room.center_y:
                        x += 1
                    generator.gen_container(x, y)

            for i in range(room_area // 75):
                x = libt.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libt.random_get_int(0, room.y1 + 1, room.y2 - 1)
                generator.gen_monster(x, y)

            for i in range(room_area // 70):
                rand_num = libt.random_get_int(0, 0, 100)
                x = libt.random_get_int(0, room.x1 + 1, room.x2 - 1)
                y = libt.random_get_int(0, room.y1 + 1, room.y2 - 1)
                if x == room.center_x and y == room.center_y:
                    x += 1
                if rand_num >= 10:
                    generator.gen_item(x, y)
                elif rand_num < 10+self.floor*2:
                    generator.gen_equipable(x, y)


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
