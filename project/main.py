import pygame as pg
import libtcodpy as libt
import constants as const
import Actor, Draw, Map, Animations, Ai, Camera, Menu, Buffs, Generator

"""
Simple python roguelike by Janar Aava and Alex Viil. Documentation is in English since libtcod's and pygame's
documentations are also in English and it makes it easier to explain things, without having to figure out
variable names or OOP terms in Estonian.
"""

# TODO: comment code... one day... maybe...


class Main:
    """
    The game object itself. This is where all the modules meet to form a single program.
    Upon initialization, initializes pygame, sets the main surface, creates the map and also creates
    the player and a bunch of actors to test out features as they're being implemented. Also has AI and
    a clock used for the FPS counter.
    """
    def __init__(self):
        pg.init()

        # Continuous movement
        pg.key.set_repeat(200, 100)

        self.surface_main = pg.display.set_mode((const.MAIN_SURFACE_WIDTH, const.MAIN_SURFACE_HEIGHT))

        # Game Map

        self.map_obj = Map.Map()
        self.map_obj.create_test_map()
        self.game_map = self.map_obj.get_game_map()

        # self.test = []  # Collision attribute values of each tile for debugging
        # for y in self.game_map:
        #     row = []
        #     for tile in y:
        #         row.append(tile.get_is_wall())
        #     self.test.append(row)s
        # print(self.test)

        self.items = []
        self.actors_containers = []
        self.actors = []
        self.buffs = []

        # Game messages
        self.messages = []

        # Camera (aka offset to move the world surface instead of having a camera to move with the player, because pygame :)
        #         NB! Set initial coordinates same as player to avoid
        player_x, player_y = self.map_obj.first_room_center
        self.camera = Camera.Camera(player_x, player_y)

        # Actors (Creatures, containers, items)

        gm = self.game_map
        sm = self.surface_main
        alist = self.actors
        aclist = self.actors_containers
        ilist = self.items
        blist = self.buffs
        msg = self.messages

        self.generator = Generator.Generator(gm, sm, alist, aclist, ilist, blist, msg)
        self.map_obj.populate_rooms(self.generator)
        '''
        # NB!: If item is not present in game world (in an inventory) then x = 0 and y = 0
        # Equipable template: Actor.Equipable(x, y, name, sprites, gm, sm, alist, aclist, ilist, blist, msg, hpbuff, armorbuff, dmgbuff, equipped=False, mirror=False)

        self.items.append(Actor.Equipable(4, 4, "Staff of Five HP", const.SPRITE_WEAPON_STAFF, gm, sm, alist, aclist, ilist, blist, msg, 5, 0, 0))
        self.items.append(Actor.Equipable(3, 4, "Enhcanted Trinket of Five Armor", const.SPRITE_WEAPON_STAFF, gm, sm, alist, aclist, blist, ilist, msg, 0, 5, 0))
        self.items.append(Actor.Equipable(4, 3, "Something Wizards Something Five Damage", const.SPRITE_WEAPON_STAFF, gm, sm, alist, aclist, blist, ilist, msg, 0, 0, 5))

        self.enemy_weapons = [Actor.Equipable(0, 0, "Rusty Sword", const.SPRITE_RUSTY_SWORD, gm, sm, alist, aclist, ilist, blist, msg, 0, 0, 1, True),
                              Actor.Equipable(0, 0, "Rusty Sword", const.SPRITE_RUSTY_SWORD, gm, sm, alist, aclist, ilist, blist, msg, 0, 0, 1, True),
                              Actor.Equipable(0, 0, "Wooden Stick", const.SPRITE_WEAPON_STAFF, gm, sm, alist, aclist, ilist, blist, msg, 0, 0, 0, True)]

        # Consumable template: Actor.Consumable(x, y, name, sprites, gm, sm, alist, aclist, ilist, blist, msg, hpbuff, armorbuff, dmgbuff, buff_duration, heal, equipped=False)

        self.chest_items = [Actor.Consumable(0, 0, "Chest Potion", const.SPRITE_POTION_RED, gm, sm, alist, aclist, ilist, blist, msg, 0, 0, 0, 0, 3)]

        self.items.append(Actor.Consumable(2, 2, "Healing Potion", const.SPRITE_POTION_RED, gm, sm, alist, aclist, ilist, blist, msg, 0, 0, 0, 0, 8))
        self.items.append(Actor.Consumable(2, 3, "All +3 Potion", const.SPRITE_POTION_RED_LARGE, gm, sm, alist, aclist, ilist, blist, msg, 3, 3, 3, 30, 0, const.SPRITES_RED_BUFF))

        # NB!: Maximum value for frame_counter -> int is 4 * idle_frames - 1
        # Actor template: Actor.Enemy(x, y, name, sprites, mirror, gm, sm, alist, aclist, ilist, blist, msg, hp, armor, dm, equipped, inventory, idle_frames, frame_counter)

        self.actors.append(Actor.Enemy(10, 10, "Demon", const.SPRITES_DEMON, True, gm, sm, alist, aclist, ilist, blist, msg, 10, 0, 1, [], self.enemy_weapons[0], libt.random_get_int(0, 5, 9), libt.random_get_int(0, 0, 19)))
        self.actors.append(Actor.Enemy(11, 9, "Demon", const.SPRITES_DEMON, True, gm, sm, alist, aclist, ilist, blist, msg, 10, 0, 1, [], self.enemy_weapons[1], libt.random_get_int(0, 5, 9), libt.random_get_int(0, 0, 19)))
        self.actors.append(Actor.Enemy(11, 10, "Demon", const.SPRITES_DEMON, True, gm, sm, alist, aclist, ilist, blist, msg, 10, 0, 1, [], self.enemy_weapons[2], libt.random_get_int(0, 5, 9), libt.random_get_int(0, 0, 19)))
        self.actors.append(Actor.Enemy(10, 11, "Demon", const.SPRITES_DEMON, True, gm, sm, alist, aclist, ilist, blist, msg, 10, 0, 1, [], None, libt.random_get_int(0, 5, 9), libt.random_get_int(0, 0, 19)))

        self.actors_containers.append(Actor.Container(7, 7, "kirst", const.SPRITE_CHEST, gm, sm, alist, aclist, ilist, blist, msg, [self.chest_items[0]]))
        self.actors_containers.append(Actor.Container(3, 7, "kirst", const.SPRITE_CHEST, gm, sm, alist, aclist, ilist, blist, msg))

        self.actors_containers.append(Actor.Container(3, 9, "Mimic", const.SPRITE_CHEST, gm, sm, alist, aclist, ilist, blist, msg, "MIMIC"))
        '''
        self.player = Actor.Player(player_x, player_y, "Juhan", const.SPRITES_PLAYER, False, gm, sm, alist, aclist, ilist, blist, msg, 21, 2, 3, 3, [], None)

        self.actors.append(Actor.Enemy(player_x-2, player_y-2, "asd", const.SPRITES_DEMON, True, gm, sm, alist, aclist, ilist, blist, msg))

        self.actors.append(self.player)

        # Actor locations used for collision boxes
        self.actors_all = self.actors + self.actors_containers

        # Calculate initial FOV
        self.map_obj.calculate_fov_map(self.player)

        self.ai = Ai.Ai()

        self.clock = pg.time.Clock()

        self.menu = Menu.Menu(self.surface_main, self.player, self.clock, self.items)

    def game_loop(self):
        """
        The main loop. Waits for events (player trying to move in some direction) and after every event gives the ai a turn,
        lets creatures attack each other, updates actor locations and updates the player's field of view. After an event,
        or even while there are no events, the while run cycle updates actor's sprites (idle frames), draws the game, and
        creates an FPS limit (to stop unwanted side effects, like actors seeming like they're on stimulants when the game
        runs on a fast computer).
        """
        self.game_start()

        music = pg.mixer.Sound(const.BACKGROUND_MUSIC)
        music.set_volume(0.05)
        music.play(-1)

        run = True
        while run:
            # Get input

            events = pg.event.get()

            # Process input
            for event in events:
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.player.control(0, -1)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_s:
                        self.player.control(0, 1)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_a:
                        self.player.control(-1, 0)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_d:
                        self.player.control(1, 0)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_e:
                        self.player.pick_up()
                        continue
                    elif event.key == pg.K_i:
                        self.menu.inventory_menu()
                        continue
                    else:
                        continue

                    # Moves Enemy actors
                    for actor in self.actors:
                        if (isinstance(actor, Actor.Enemy) and
                                0 <= (actor.x + self.camera.get_x_offset()) * const.TILE_WIDTH <= const.MAIN_SURFACE_WIDTH and
                                0 <= (actor.y + self.camera.get_y_offset()) * const.TILE_HEIGHT <= const.MAIN_SURFACE_HEIGHT):
                            self.ai.aggressive_roam(actor, self.player)

                    #TODO: On a big map it takes too long to update actor locations !!!, 100x100 is too much 50x50 was fine, could be fixed with lower spawn rates prob.
                    # Don't think update_actor_locations is necessary anymore, also lags the game a lot
                    # self.update_actor_locations()

                    self.map_obj.calculate_fov_map(self.player)

                    # Update active buffs
                    for buff in self.buffs:
                        buff.update(self.buffs)

            # Update actors' sprites
            Animations.Animations(self.actors).update()

            # Draw game
            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera)

            # FPS limit and tracker
            self.clock.tick(const.FPS_LIMIT)

        self.game_quit()

    def update_actor_locations(self):
        # Update actor's collision box location
        actor_locations = [actor.get_location() for actor in self.actors]
        self.map_obj.update(actor_locations)
        self.game_map = self.map_obj.get_game_map()

    def game_quit(self):
        pg.quit()
        exit()

    def game_start(self):
        self.menu.menu_main()


if __name__ == '__main__':
    game = Main()
    game.game_loop()
