import pygame as pg
import libtcodpy as libt

"""Contains all the constant values like window size, colors, fonts, sprites and other values that other modules use."""

# Assets from https://0x72.itch.io/dungeontileset-ii

pg.init()

# Init values
MAIN_SURFACE_HEIGHT = 800
MAIN_SURFACE_WIDTH = 1200
pg.display.set_mode((MAIN_SURFACE_WIDTH, MAIN_SURFACE_HEIGHT))

# Colors
GRAY = (122, 122, 122)
DARKISH_GRAY = (70, 70, 70)
DARK_GRAY = (30, 30, 30)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (138, 0, 0)

# Fonts
FONT_DEBUG = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 16)
FONT_CONSOLE = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 20)
FONT_INVENTORY = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 17)
FONT_MENU_BUTTON = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 30)
FONT_SETTINGS = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 23)
FONT_DEATH_MESSAGE = pg.font.Font("fonts/VCR_OSD_MONO_1.001.ttf", 160)

# HUD
HUD_HEART_FULL = pg.image.load("sprites/ui_heart_full.png").convert_alpha()
HUD_HEART_FLASH = pg.image.load("sprites/ui_heart_flash.png").convert_alpha()
HUD_HEART_EMPTY = pg.image.load("sprites/ui_heart_empty.png").convert_alpha()
HUD_SWORD = pg.image.load("sprites/ui_dmg_sword.png").convert_alpha()
HUD_SHIELD = pg.image.load("sprites/ui_shield.png").convert_alpha()

# Creature sprites; all Creature objects require four sprites for idle animations
SPRITES_PLAYER = [pg.image.load("sprites/wizzard_m_idle_anim_f0.png").convert_alpha(),
                  pg.image.load("sprites/wizzard_m_idle_anim_f1.png").convert_alpha(),
                  pg.image.load("sprites/wizzard_m_idle_anim_f2.png").convert_alpha(),
                  pg.image.load("sprites/wizzard_m_idle_anim_f3.png").convert_alpha()]
SPRITES_DEMON = [pg.image.load("sprites/chort_idle_anim_f0.png").convert_alpha(),
                 pg.image.load("sprites/chort_idle_anim_f1.png").convert_alpha(),
                 pg.image.load("sprites/chort_idle_anim_f2.png").convert_alpha(),
                 pg.image.load("sprites/chort_idle_anim_f3.png").convert_alpha()]
SPRITES_MIMIC = [pg.image.load("sprites/chest_mimic_open_anim_f1.png").convert_alpha(),
                 pg.image.load("sprites/chest_mimic_open_anim_f2.png").convert_alpha(),
                 pg.image.load("sprites/chest_mimic_open_anim_f1.png").convert_alpha(),
                 pg.image.load("sprites/chest_mimic_open_anim_f2.png").convert_alpha()]
SPRITES_SKELETON = [pg.image.load("sprites/skelet_idle_anim_f0.png").convert_alpha(),
                    pg.image.load("sprites/skelet_idle_anim_f1.png").convert_alpha(),
                    pg.image.load("sprites/skelet_idle_anim_f2.png").convert_alpha(),
                    pg.image.load("sprites/skelet_idle_anim_f3.png").convert_alpha()]
SPRITES_ICE_ZOMBIE = [pg.image.load("sprites/ice_zombie_idle_anim_f0.png").convert_alpha(),
                      pg.image.load("sprites/ice_zombie_idle_anim_f1.png").convert_alpha(),
                      pg.image.load("sprites/ice_zombie_idle_anim_f2.png").convert_alpha(),
                      pg.image.load("sprites/ice_zombie_idle_anim_f3.png").convert_alpha()]

SPRITE_CHEST = pg.image.load("sprites/chest_empty_open_anim_f0.png").convert_alpha()
SPRITE_CHEST_OPEN = pg.image.load("sprites/chest_empty_open_anim_f2.png").convert_alpha()

# Item sprites; all Item objects require dropped, equipped sprites and integers x offset and y offset
# Equipables

SPRITE_WEAPON_STAFF = [pg.image.load("sprites/weapon_red_magic_staffdropped.png").convert_alpha(),
                       pg.image.load("sprites/weapon_red_magic_staff.png").convert_alpha(),
                       0,
                       -1]
SPRITE_RUSTY_SWORD = [pg.image.load("sprites/weapon_rusty_sworddropped.png").convert_alpha(),
                      pg.image.load("sprites/weapon_rusty_sword.png").convert_alpha(),
                      -0.4,
                      -0.8]

SPRITE_WEAPON_BOW = [pg.image.load("sprites/weapon_bowdropped.png").convert_alpha(),
                     pg.image.load("sprites/weapon_bow.png").convert_alpha(),
                     -0.5,
                     -0.5]

# Consumables

SPRITE_POTION_RED = [pg.image.load("sprites/flask_red.png").convert_alpha(),
                     pg.image.load("sprites/flask_red.png").convert_alpha(),
                     0,
                     0]
SPRITE_POTION_RED_LARGE = [pg.image.load("sprites/flask_big_red.png").convert_alpha(),
                           pg.image.load("sprites/flask_big_red.png").convert_alpha(),
                           0,
                           0]

# Buffs

ACTOR_DICT = {
             "SPRITE_CHEST": SPRITE_CHEST,
             "SPRITE_CHEST_OPEN": SPRITE_CHEST_OPEN,
             "SPRITES_SKELETON": SPRITES_SKELETON,
             "SPRITES_MIMIC": SPRITES_MIMIC,
             "SPRITES_DEMON": SPRITES_DEMON,
             "SPRITES_PLAYER": SPRITES_PLAYER,
             "SPRITES_ICE_ZOMBIE": SPRITES_ICE_ZOMBIE,
             "HUD_HEART_FULL": HUD_HEART_FULL,
             "HUD_HEART_FLASH": HUD_HEART_FLASH,
             "HUD_HEART_EMPTY": HUD_HEART_EMPTY,
             "HUD_SWORD": HUD_SWORD,
             "HUD_SHIELD": HUD_SHIELD,
             "SPRITE_WEAPON_STAFF": SPRITE_WEAPON_STAFF,
             "SPRITE_RUSTY_SWORD": SPRITE_RUSTY_SWORD,
             "SPRITE_WEAPON_BOW": SPRITE_WEAPON_BOW,
             "SPRITE_POTION_RED": SPRITE_POTION_RED,
             "SPRITE_POTION_RED_LARGE": SPRITE_POTION_RED_LARGE
             }

SPRITES_RED_BUFF = [pg.image.load("sprites/buff_red_f0.png").convert_alpha(),
                    pg.image.load("sprites/buff_red_f1.png").convert_alpha(),
                    pg.image.load("sprites/buff_red_f2.png").convert_alpha(),
                    pg.image.load("sprites/buff_red_f3.png").convert_alpha()]

SPRITES_DAZED_BUFF = [pg.image.load("sprites/buff_dazed_f0.png").convert_alpha(),
                      pg.image.load("sprites/buff_dazed_f1.png").convert_alpha(),
                      pg.image.load("sprites/buff_dazed_f2.png").convert_alpha(),
                      pg.image.load("sprites/buff_dazed_f3.png").convert_alpha()]

BUFF_DICT = {
            "SPRITES_RED_BUFF": SPRITES_RED_BUFF,
            "SPRITES_DAZED_BUFF": SPRITES_DAZED_BUFF
            }

# Spells

SPRITES_SPELL_LIGHTNING = [pg.image.load("sprites/spell_lightning_f0.png").convert_alpha(),
                           pg.image.load("sprites/spell_lightning_f1.png").convert_alpha(),
                           pg.image.load("sprites/spell_lightning_f2.png").convert_alpha(),
                           pg.image.load("sprites/spell_lightning_f3.png").convert_alpha()]

SPRITES_SPELL_FIREBALL = [pg.image.load("sprites/spell_fireball_f0.png").convert_alpha(),
                          pg.image.load("sprites/spell_fireball_f1.png").convert_alpha(),
                          pg.image.load("sprites/spell_fireball_f2.png").convert_alpha(),
                          pg.image.load("sprites/spell_fireball_f3.png").convert_alpha()]

SPRITES_SPELL_DAZE = [pg.image.load("sprites/spell_daze_f0.png").convert_alpha(),
                      pg.image.load("sprites/spell_daze_f1.png").convert_alpha(),
                      pg.image.load("sprites/spell_daze_f2.png").convert_alpha(),
                      pg.image.load("sprites/spell_daze_f3.png").convert_alpha()]

SPRITES_PROJECTILE_ARROW = pg.image.load("sprites/weapon_arrow.png").convert_alpha()

# WALLS AND FLOORS
SPRITE_WALLEXPLORED = pg.image.load("sprites/wall_middarkened.png").convert()
SPRITE_WALL = pg.image.load("sprites/wall_mid.png").convert()

SPRITE_FLOOREXPLORED = pg.image.load("sprites/floor_1darkened.png").convert()
SPRITE_FLOOREXPLORED1 = pg.image.load("sprites/floor_1darkened.png").convert()
SPRITE_FLOOREXPLORED2 = pg.image.load("sprites/floor_2darkened.png").convert()
SPRITE_FLOOREXPLORED3 = pg.image.load("sprites/floor_3darkened.png").convert()
SPRITE_FLOOREXPLORED4 = pg.image.load("sprites/floor_4darkened.png").convert()
SPRITE_FLOOREXPLORED5 = pg.image.load("sprites/floor_5darkened.png").convert()
SPRITE_FLOOREXPLORED6 = pg.image.load("sprites/floor_6darkened.png").convert()
SPRITE_FLOOREXPLORED7 = pg.image.load("sprites/floor_7darkened.png").convert()
SPRITE_FLOOREXPLORED8 = pg.image.load("sprites/floor_8darkened.png").convert()
SPRITES_FLOOREXPLORED = [eval("SPRITE_FLOOREXPLORED" + str(i)) for i in range(1, 9)]

SPRITE_FLOOR = pg.image.load("sprites/floor_1.png").convert()
SPRITE_FLOOR1 = pg.image.load("sprites/floor_1.png").convert()
SPRITE_FLOOR2 = pg.image.load("sprites/floor_2.png").convert()
SPRITE_FLOOR3 = pg.image.load("sprites/floor_3.png").convert()
SPRITE_FLOOR4 = pg.image.load("sprites/floor_4.png").convert()
SPRITE_FLOOR5 = pg.image.load("sprites/floor_5.png").convert()
SPRITE_FLOOR6 = pg.image.load("sprites/floor_6.png").convert()
SPRITE_FLOOR7 = pg.image.load("sprites/floor_7.png").convert()
SPRITE_FLOOR8 = pg.image.load("sprites/floor_8.png").convert()
SPRITES_FLOOR = [eval("SPRITE_FLOOR" + str(i)) for i in range(1, 9)]

SPRITE_FLOOR_LADDER = pg.image.load("sprites/floor_ladder.png").convert()
SPRITE_FLOOR_LADDER_EXPLORED = pg.image.load("sprites/floor_ladderdarkened.png").convert()

WALL_AND_FLOOR_DICT = {
                      "SPRITE_WALLEXPLORED": SPRITE_WALLEXPLORED,
                      "SPRITE_WALL": SPRITE_WALL,
                      "SPRITE_FLOOREXPLORED": SPRITE_FLOOREXPLORED1,
                      "SPRITE_FLOOREXPLORED1": SPRITE_FLOOREXPLORED1,
                      "SPRITE_FLOOREXPLORED2": SPRITE_FLOOREXPLORED2,
                      "SPRITE_FLOOREXPLORED3": SPRITE_FLOOREXPLORED3,
                      "SPRITE_FLOOREXPLORED4": SPRITE_FLOOREXPLORED4,
                      "SPRITE_FLOOREXPLORED5": SPRITE_FLOOREXPLORED5,
                      "SPRITE_FLOOREXPLORED6": SPRITE_FLOOREXPLORED6,
                      "SPRITE_FLOOREXPLORED7": SPRITE_FLOOREXPLORED7,
                      "SPRITE_FLOOREXPLORED8": SPRITE_FLOOREXPLORED8,
                      "SPRITE_FLOOR": SPRITE_FLOOR,
                      "SPRITE_FLOOR1": SPRITE_FLOOR1,
                      "SPRITE_FLOOR2": SPRITE_FLOOR2,
                      "SPRITE_FLOOR3": SPRITE_FLOOR3,
                      "SPRITE_FLOOR4": SPRITE_FLOOR4,
                      "SPRITE_FLOOR5": SPRITE_FLOOR5,
                      "SPRITE_FLOOR6": SPRITE_FLOOR6,
                      "SPRITE_FLOOR7": SPRITE_FLOOR7,
                      "SPRITE_FLOOR8": SPRITE_FLOOR8,
                      "SPRITE_FLOOR_LADDER": SPRITE_FLOOR_LADDER,
                      "SPRITE_FLOOR_LADDER_EXPLORED": SPRITE_FLOOR_LADDER_EXPLORED
                      }


# Music by Hendy Marvin
# Also probably better things out there, just going with this for now
BACKGROUND_MUSIC = "audio/HendyMarvin/02-hendy_marvin-plan_revenge.ogg"
MENU_MUSIC = "audio/HendyMarvin/01-hendy_marvin-intro_story.ogg"
DEATH_MUSIC = "audio/HendyMarvin/12-hendy_marvin-it's_over.ogg"

# WIP SOUND EFFECTS
HIT_SOUND = "audio/Hit_Hurt13.wav"
FIREBALL_SOUND = "audio/Explosion5.wav"
RANGED_SOUND = "audio/Laser_Shoot30.wav"
LIGHTNING_SOUND = "audio/Randomize23.wav"
DEATH_SOUND = "audio/deathwip.wav"
BUFF_SOUND = "audio/Powerup.wav"
CHEST_SOUND = "audio/Pickup_Coin30.wav"
DAZE_SOUND = "audio/daze.wav"

# Map values
MAP_WIDTH = 100
MAP_HEIGHT = 100

MAX_ROOM_SIZE = 20
MIN_ROOM_SIZE = 7
POSSIBLE_ROOM_NUM = 500

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

# Settings Menu
SETTINGS_MENU_WIDTH = 500
SETTINGS_MENU_HEIGHT = 300

# Escape button menu
ESC_MENU_HEIGHT = 200
ESC_MENU_WIDTH = 700
