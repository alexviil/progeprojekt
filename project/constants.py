import pygame as pg
import libtcodpy as libt
from random import randint

"""Contains all the constant values like window size, colors, fonts, sprites and other values that other modules use."""

# Assets from https://0x72.itch.io/dungeontileset-ii

pg.init()

# Init values
MAIN_SURFACE_HEIGHT = 705
MAIN_SURFACE_WIDTH = 615

# Colors
GRAY = (122, 122, 122)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
FONT_DEBUG = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 16)
FONT_CONSOLE = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 20)

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
SPRITE_WALLEXPLORED = pg.image.load("sprites/wall_middarkened.png")
SPRITE_WALL = pg.image.load("sprites/wall_mid.png")
SPRITE_FLOOREXPLORED = pg.image.load("sprites/floor_1darkened.png")
SPRITE_FLOOREXPLORED1 = pg.image.load("sprites/floor_1darkened.png")
SPRITE_FLOOREXPLORED2 = pg.image.load("sprites/floor_2darkened.png")
SPRITE_FLOOREXPLORED3 = pg.image.load("sprites/floor_3darkened.png")
SPRITE_FLOOREXPLORED4 = pg.image.load("sprites/floor_4darkened.png")
SPRITE_FLOOREXPLORED5 = pg.image.load("sprites/floor_5darkened.png")
SPRITE_FLOOREXPLORED6 = pg.image.load("sprites/floor_6darkened.png")
SPRITE_FLOOREXPLORED7 = pg.image.load("sprites/floor_7darkened.png")
SPRITE_FLOOREXPLORED8 = pg.image.load("sprites/floor_8darkened.png")
SPRITES_FLOOREXPLORED = [eval("SPRITE_FLOOREXPLORED" + str(i)) for i in range(1, 9)]
SPRITE_FLOOR = pg.image.load("sprites/floor_1.png")
SPRITE_FLOOR1 = pg.image.load("sprites/floor_1.png")
SPRITE_FLOOR2 = pg.image.load("sprites/floor_2.png")
SPRITE_FLOOR3 = pg.image.load("sprites/floor_3.png")
SPRITE_FLOOR4 = pg.image.load("sprites/floor_4.png")
SPRITE_FLOOR5 = pg.image.load("sprites/floor_5.png")
SPRITE_FLOOR6 = pg.image.load("sprites/floor_6.png")
SPRITE_FLOOR7 = pg.image.load("sprites/floor_7.png")
SPRITE_FLOOR8 = pg.image.load("sprites/floor_8.png")
SPRITES_FLOOR = [eval("SPRITE_FLOOR" + str(i)) for i in range(1, 9)]

# Map values
MAP_WIDTH = 19
MAP_HEIGHT = 19

TILE_WIDTH = 32
TILE_HEIGHT = 32

STEP = 32

# FOV values
TORCH_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = libt.FOV_BASIC

# FPS limit
FPS_LIMIT = 60

# Console messages
MESSAGE_NUMBER = 4
