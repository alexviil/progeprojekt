import pygame as pg
import libtcodpy as libt
import constants as const


class Actor:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def control(self, x_change, y_change):
        if not MAP[self.y + y_change][self.x + x_change]:  # Checks if can step there
            self.x += x_change
            self.y += y_change

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x * const.TILE_WIDTH, self.y * const.TILE_HEIGHT))


def create_map():
    # new_map = [[False for y in range(0, const.MAP_HEIGHT)] for x in range(0, const.MAP_WIDTH)]
    new_map = list()
    for y in range(0, const.MAP_HEIGHT):
        row = []
        for x in range(0, const.MAP_WIDTH):
            if y == 0 or y == const.MAP_HEIGHT-1 or x == 0 or x == const.MAP_WIDTH-1:
                row.append(True)
                continue
            row.append(False)
        new_map.append(row)
    return new_map


def draw_map(map_list: list):
    global SURFACE_MAIN

    for x in range(0, const.MAP_WIDTH):
        for y in range(1, const.MAP_HEIGHT+1):
            if map_list[y-1][x]:
                SURFACE_MAIN.blit(const.SPRITE_WALL, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))
            else:
                SURFACE_MAIN.blit(const.SPRITE_FLOOR, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))


def draw_game():
    global SURFACE_MAIN

    # Reset the surface
    SURFACE_MAIN.fill(const.GRAY)

    # Draw the map
    draw_map(MAP)

    # Draw the character
    PLAYER.draw()

    # Update display
    pg.display.flip()


def game_loop():
    run = True
    while run:
        # Get input
        events = pg.event.get()

        # Process input
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    PLAYER.control(0, -1)
                elif event.key == pg.K_s:
                    PLAYER.control(0, 1)
                elif event.key == pg.K_a:
                    PLAYER.control(-1, 0)
                elif event.key == pg.K_d:
                    PLAYER.control(1, 0)

        # Draw game
        draw_game()


def game_init():
    global SURFACE_MAIN, MAP, PLAYER

    pg.init()
    SURFACE_MAIN = pg.display.set_mode((const.MAIN_SURFACE_HEIGHT, const.MAIN_SURFACE_WIDTH))
    PLAYER = Actor(1, 1, const.SPRITE_PLAYER)

    MAP = create_map()


if __name__ == '__main__':
    game_init()
    game_loop()
