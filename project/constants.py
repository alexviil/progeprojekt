import pygame as pg
import libtcodpy as libt
from random import randint

# Assets from https://0x72.itch.io/dungeontileset-ii

pg.init()

# Init values
MAIN_SURFACE_HEIGHT = 800
MAIN_SURFACE_WIDTH = 600

# Colors
GRAY = (122, 122, 122)

# Sprites; all actors require four sprites for idle animations
SPRITES_PLAYER = [pg.image.load("sprites/wizzard_m_idle_anim_f0.png"),
                       pg.image.load("sprites/wizzard_m_idle_anim_f1.png"),
                       pg.image.load("sprites/wizzard_m_idle_anim_f2.png"),
                       pg.image.load("sprites/wizzard_m_idle_anim_f3.png")]
SPRITES_DEMON = [pg.image.load("sprites/chort_idle_anim_f0.png"),
                      pg.image.load("sprites/chort_idle_anim_f1.png"),
                      pg.image.load("sprites/chort_idle_anim_f2.png"),
                      pg.image.load("sprites/chort_idle_anim_f3.png")]
SPRITE_CHEST = pg.image.load("sprites/chest_empty_open_anim_f0.png")
SPRITE_WALLEXPLORED = pg.image.load("sprites/wall_goo.png")  # TODO Placeholder
SPRITE_WALL = pg.image.load("sprites/wall_mid.png")
SPRITE_FLOOREXPLORED = pg.image.load("sprites/floor_8.png")  # TODO Placeholder
SPRITE_FLOOR = pg.image.load("sprites/floor_1.png")

# Map values
MAP_WIDTH = 16
MAP_HEIGHT = 16

TILE_WIDTH = 32
TILE_HEIGHT = 32

STEP = 32

# FOV values
TORCH_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = libt.FOV_BASIC
