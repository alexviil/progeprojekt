import pygame as pg

pg.init()

# Init values
MAIN_SURFACE_HEIGHT = 800
MAIN_SURFACE_WIDTH = 600

# Colors
GRAY = (122, 122, 122)

# Sprites
SPRITE_PLAYER = pg.transform.scale2x(pg.image.load("sprites/wizzard_m_idle_anim_f0.png"))
SPRITE_WALL = pg.transform.scale2x(pg.image.load("sprites/wall_mid.png"))
SPRITE_FLOOR = pg.transform.scale2x(pg.image.load("sprites/floor_1.png"))

# Map values
MAP_WIDTH = 10
MAP_HEIGHT = 10

TILE_WIDTH = 32
TILE_HEIGHT = 32

STEP = 32
