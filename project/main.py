import pygame as pg
import libtcodpy as libt
import constants as const
import Actor
import Draw
import Map


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
        Draw.Draw(SURFACE_MAIN, MAP, PLAYER).draw_game()


def game_init():
    global SURFACE_MAIN, MAP, PLAYER

    pg.init()
    SURFACE_MAIN = pg.display.set_mode((const.MAIN_SURFACE_HEIGHT, const.MAIN_SURFACE_WIDTH))

    map_obj = Map.Map()
    map_obj.create_map()
    MAP = map_obj.get_game_map()

    PLAYER = Actor.Actor(1, 1, const.SPRITE_PLAYER, MAP, SURFACE_MAIN)


if __name__ == '__main__':
    game_init()
    game_loop()
