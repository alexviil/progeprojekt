import pygame as pg
import libtcodpy as libt
import constants as const


def create_map():
    new_map = [[False for y in range(0, const.MAP_HEIGHT)] for x in range(0, const.MAP_WIDTH)]
    return new_map


def draw_map(map_list: list):
    global SURFACE_MAIN

    for x, row in enumerate(map_list):
        for y, tile in enumerate(row):
            if tile:  # If tile == True, then it blocks path
                SURFACE_MAIN.blit(const.WALL, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))
            else:
                SURFACE_MAIN.blit(const.FLOOR, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))


def draw_game():
    global SURFACE_MAIN

    # Reset the surface
    SURFACE_MAIN.fill(const.GRAY)

    # Draw the map
    draw_map(create_map())

    # Draw the character
    SURFACE_MAIN.blit(const.PLAYER, (0, 0))

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

        # Draw game
        draw_game()


def game_init():
    global SURFACE_MAIN

    pg.init()
    SURFACE_MAIN = pg.display.set_mode((const.MAIN_SURFACE_HEIGHT, const.MAIN_SURFACE_WIDTH))


if __name__ == '__main__':
    game_init()
    game_loop()
