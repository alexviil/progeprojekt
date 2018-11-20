import pygame as pg
import libtcodpy as libt

"""Contains all the constant values like window size, colors, fonts, sprites and other values that other modules use."""

# Assets from https://0x72.itch.io/dungeontileset-ii

pg.init()

# Init values
MAIN_SURFACE_HEIGHT = 600
MAIN_SURFACE_WIDTH = 800

# Colors
GRAY = (122, 122, 122)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Fonts
FONT_DEBUG = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 16)
FONT_CONSOLE = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 20)
FONT_INVENTORY = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 14)
FONT_MENU_BUTTON = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 30)

# Creature sprites; all Creature objects require four sprites for idle animations
SPRITES_PLAYER = [pg.image.load("sprites/wizzard_m_idle_anim_f0.png"),
                  pg.image.load("sprites/wizzard_m_idle_anim_f1.png"),
                  pg.image.load("sprites/wizzard_m_idle_anim_f2.png"),
                  pg.image.load("sprites/wizzard_m_idle_anim_f3.png")]
SPRITES_DEMON = [pg.image.load("sprites/chort_idle_anim_f0.png"),
                 pg.image.load("sprites/chort_idle_anim_f1.png"),
                 pg.image.load("sprites/chort_idle_anim_f2.png"),
                 pg.image.load("sprites/chort_idle_anim_f3.png")]
SPRITES_MIMIC = [pg.image.load("sprites/chest_mimic_open_anim_f1.png"),
                 pg.image.load("sprites/chest_mimic_open_anim_f2.png"),
                 pg.image.load("sprites/chest_mimic_open_anim_f1.png"),
                 pg.image.load("sprites/chest_mimic_open_anim_f2.png")]

SPRITE_CHEST = pg.image.load("sprites/chest_empty_open_anim_f0.png")
SPRITE_CHEST_OPEN = pg.image.load("sprites/chest_empty_open_anim_f2.png")

# Item sprites; all Item objects require dropped, equipped sprites and integers x offset and y offset
# Equipables

SPRITE_WEAPON_STAFF = [pg.image.load("sprites/weapon_red_magic_staffdropped.png"),
                       pg.image.load("sprites/weapon_red_magic_staff.png"),
                       0,
                       -1]
SPRITE_RUSTY_SWORD = [pg.image.load("sprites/weapon_rusty_sworddropped.png"),
                      pg.image.load("sprites/weapon_rusty_sword.png"),
                      -0.4,
                      -0.8]

# Consumables

SPRITE_POTION_RED = [pg.image.load("sprites/flask_red.png"),
                     pg.image.load("sprites/flask_red.png"),
                     0,
                     0]
SPRITE_POTION_RED_LARGE = [pg.image.load("sprites/flask_big_red.png"),
                           pg.image.load("sprites/flask_big_red.png"),
                           0,
                           0]

# Buffs

SPRITES_RED_BUFF = [pg.image.load("sprites/buff_red_f0.png"),
                    pg.image.load("sprites/buff_red_f1.png"),
                    pg.image.load("sprites/buff_red_f2.png"),
                    pg.image.load("sprites/buff_red_f3.png")]

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

# Audio, not sure if can use Hendy Marvin's music technically
# Also probably better things out there, just going with this for now
BACKGROUND_MUSIC = "audio/HendyMarvin/02-hendy_marvin-plan_revenge.ogg"
MENU_MUSIC = "audio/HendyMarvin/01-hendy_marvin-intro_story.ogg"

# Map values
MAP_WIDTH = 19
MAP_HEIGHT = 19

TILE_WIDTH = 32
TILE_HEIGHT = 32

STEP = 32

# Camera values (in tiles)
CAMERA_CENTER_X = MAIN_SURFACE_WIDTH / TILE_WIDTH // 2
CAMERA_CENTER_Y = MAIN_SURFACE_HEIGHT / TILE_HEIGHT // 2 - 1

# FOV values
TORCH_RADIUS = 10
FOV_LIGHT_WALLS = True
FOV_ALGORITHM = libt.FOV_BASIC

# FPS limit
FPS_LIMIT = 60

# Console messages
MESSAGE_NUMBER = 4

# Inventory Menu
INV_MENU_WIDTH = 300
INV_MENU_HEIGHT = 300
