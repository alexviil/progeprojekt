import pygame as pg
import os
import libtcodpy as libt
import constants as const
import pickle, gzip
import Actor, Draw, Map, Animations, Ai, Camera, Menu, Buffs, Generator, Spells, Tile

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

        self.floor = 1

        self.map_obj = Map.Map(self.floor)
        self.map_obj.create_map()
        self.game_map = self.map_obj.get_game_map()

        self.items = []
        self.actors_containers = []
        self.actors = []
        self.buffs = []

        # Game messages
        self.messages = []

        # Camera (aka offset to move the world surface instead of having a camera to move with the player, because pygame :)
        #         NB! Set initial coordinates same as player
        player_x, player_y = self.map_obj.first_room_center
        self.camera = Camera.Camera(player_x, player_y)

        # Actors (Creatures, containers, items)

        self.generator = Generator.Generator(self.game_map, self.surface_main, self.actors, self.actors_containers, self.items, self.buffs, self.messages, self.floor)
        self.map_obj.populate_rooms(self.generator)

        self.player = Actor.Player(player_x, player_y, "Juhan", "SPRITES_PLAYER", False, self.game_map, self.surface_main, self.messages, hp=20, armor=3, dmg=3, inventory_limit=10)
        self.player.inventory.clear()


        # STAFFS WITH SPELLS FOR DEBUGGING

        """
        self.items.append(Actor.Equipable(player_x-1, player_y, "Staff of Fireball", "SPRITE_WEAPON_STAFF", self.game_map, self.surface_main, self.messages, 1, 1, 0, False, False, "Fireball", 5, 0, 5))
        self.items.append(Actor.Equipable(player_x-1, player_y-1, "Staff of ICBM with Pu-239 (for debugging only ofc)", "SPRITE_WEAPON_STAFF", self.game_map, self.surface_main, self.messages, 0, 0, 0, False, False, "Nuke", 999, 0, 999))
        self.items.append(Actor.Equipable(player_x+1, player_y, "Staff of Arc Lightning", "SPRITE_WEAPON_STAFF", self.game_map, self.surface_main, self.messages, 1, 1, 0, False, False, "Lightning", 5, 0, 5))
        self.items.append(Actor.Equipable(player_x, player_y+1, "Bow of rooty tooty point n' shooty", "SPRITE_WEAPON_BOW", self.game_map, self.surface_main, self.messages, 0, -1, 0, False, False, "Ranged", 2, 0, 8))
        self.items.append(Actor.Equipable(player_x, player_y-1, "Staff of Confusion (aka Staff of Calculus)", "SPRITE_WEAPON_STAFF", self.game_map, self.surface_main, self.messages, 1, 1, 0, False, False, "Daze", 1, 0, 5))
        """

        self.actors.append(self.player)

        # Actor locations used for collision boxes
        self.actors_all = self.actors + self.actors_containers

        # Calculate initial FOV
        self.map_obj.calculate_fov_map(self.player)

        self.clock = pg.time.Clock()

        self.music_volume = 0.05
        self.effect_volume = 0.05
        self.settings_load()

        self.menu = Menu.Menu(self.surface_main, self.player, self.clock, self.items, self.buffs, self.music_volume, self.effect_volume)

        self.ai = Ai.Ai(self.actors, self.actors_containers, self.items, self.effect_volume)
        self.spells = Spells.Spells(self.player, self.camera, self.map_obj, self.game_map, self.surface_main, self.actors, self.actors_containers, self.items, self.buffs, self.clock, self.messages, self.effect_volume, self.floor)

    def game_loop(self):
        """
        The main loop. Waits for events (player trying to move in some direction) and after every event gives the ai a turn,
        lets creatures attack each other, updates actor locations and updates the player's field of view. After an event,
        or even while there are no events, the while run cycle updates actor's sprites (idle frames), draws the game, and
        creates an FPS limit (to stop unwanted side effects, like actors seeming like they're on stimulants when the game
        runs on a fast computer).
        """
        self.game_menu()

        run = True
        while run:
            # Get input

            events = pg.event.get()

            # Process input
            for event in events:
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    self.ai.effect_volume = self.effect_volume
                    self.spells.effect_volume = self.effect_volume
                    if event.key == pg.K_w:
                        self.player.control(0, -1, self.actors, self.actors_containers, self.items, self.effect_volume)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_s:
                        self.player.control(0, 1, self.actors, self.actors_containers, self.items, self.effect_volume)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_a:
                        self.player.control(-1, 0, self.actors, self.actors_containers, self.items, self.effect_volume)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_d:
                        self.player.control(1, 0, self.actors, self.actors_containers, self.items, self.effect_volume)
                        self.camera.set_offset(self.player.x, self.player.y)
                    elif event.key == pg.K_e:
                        if self.map_obj.get_tile(self.player.x, self.player.y).doorway:
                            self.change_levels()
                        else:
                            self.player.pick_up(self.items)
                        continue
                    elif event.key == pg.K_i:
                        self.menu.inventory_menu()
                        continue
                    elif event.key == pg.K_SPACE:
                        self.spells.cast_spell()
                        if self.player.spell_status == "cancelled":
                            continue
                    elif event.key == pg.K_ESCAPE:
                        command = self.menu.esc_menu()
                        if command == "EXIT":
                            self.game_quit()
                        elif command == "MAIN_MENU":
                            self.music.stop()
                            self.game_save()
                            self.game_menu()
                        elif command == "SETTINGS":
                            self.menu.settings_menu(self.music)
                            self.music_volume = self.menu.music_volume
                            self.effect_volume = self.menu.effect_volume
                            self.settings_save()
                    else:
                        continue

                    # Moves Enemy actors
                    for actor in self.actors:
                        if (isinstance(actor, Actor.Enemy) and
                                0 <= (actor.x + self.camera.get_x_offset()) * const.TILE_WIDTH <= const.MAIN_SURFACE_WIDTH and
                                0 <= (actor.y + self.camera.get_y_offset()) * const.TILE_HEIGHT <= const.MAIN_SURFACE_HEIGHT):
                            self.ai.ai_turn(actor, self.player)

                    self.map_obj.calculate_fov_map(self.player)
                    self.player.turns_since_spell += 1

                    # Update active buffs
                    for buff in self.buffs:
                        buff.update(self.buffs, self.actors)

                    self.ai.update_turn_counter()

            # Update actors' sprites
            Animations.Animations(self.actors).update()

            # Draw game
            draw_obj = Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs)
            draw_obj.draw_game(self.clock, self.messages, self.camera, self.floor)

            # FPS limit and tracker
            self.clock.tick(const.FPS_LIMIT)

            # death thingy
            if self.player.hp <= 0:
                self.player_death()

        self.game_quit()

    def update_actor_locations(self):
        # Update actor's collision box location
        actor_locations = [actor.get_location() for actor in self.actors]
        self.map_obj.update(actor_locations)
        self.game_map = self.map_obj.get_game_map()

    def change_levels(self):
        self.actors.clear()
        self.actors_containers.clear()
        self.items.clear()
        self.actors.append(self.player)
        self.floor += 1
        self.map_obj = Map.Map(self.floor)
        self.map_obj.create_map()
        self.game_map.clear()
        self.game_map = self.map_obj.get_game_map()
        self.player.set_location(self.map_obj.first_room_center[0], self.map_obj.first_room_center[1])
        self.camera.x_offset = const.CAMERA_CENTER_X - self.player.get_location()[0]
        self.camera.y_offset = const.CAMERA_CENTER_Y - self.player.get_location()[1]
        self.generator = Generator.Generator(self.game_map, self.surface_main, self.actors, self.actors_containers, self.items, self.buffs, self.messages, self.floor)
        self.map_obj.populate_rooms(self.generator)
        self.spells = Spells.Spells(self.player, self.camera, self.map_obj, self.game_map, self.surface_main, self.actors, self.actors_containers, self.items, self.buffs, self.clock, self.messages, self.effect_volume, self.floor)
        self.player.set_world_map(self.game_map)
        for buff in self.buffs:
            if buff.target == self.player:
                buff.x, buff.y = self.player.get_location()

    def settings_load(self):
        if os.path.isfile("savedata\savesettings") and os.path.getsize("savedata\savesettings") > 0:
            with gzip.open("savedata\savesettings", "rb") as f:
                self.music_volume, self.effect_volume = pickle.load(f)

    def settings_save(self):
        with gzip.open("savedata\savesettings", "wb") as f:
            pickle.dump([self.music_volume, self.effect_volume], f)

    def game_save(self):
        self.map_obj.destroy_surfaces()
        for actor in self.actors:
            if actor.inventory:
                for item in actor.inventory:
                    item.set_surface(None)
                    item.set_sprites(None)
                    item.set_sprite(None)
            if actor.equipped:
                actor.equipped.set_surface(None)
                actor.equipped.set_sprites(None)
                actor.equipped.set_sprite(None)
            actor.set_surface(None)
            actor.destroy_sprites()
        for actor in self.actors_containers:
            if actor.inventory:
                for item in actor.inventory:
                    item.set_surface(None)
                    item.set_sprites(None)
                    item.set_sprite(None)
            actor.set_surface(None)
            actor.set_sprites(None)
            actor.set_sprite(None)
        for item in self.items:
            item.set_surface(None)
            item.set_sprites(None)
            item.set_sprite(None)
        for buff in self.buffs:
            buff.set_surface(None)
            buff.destroy_sprites()

        with gzip.open("savedata\savegame", "wb") as f:
            pickle.dump([
                         self.player,
                         self.camera,
                         self.map_obj,
                         self.game_map,
                         self.actors,
                         self.actors_containers,
                         self.items,
                         self.buffs,
                         self.messages,
                         self.floor
                        ], f)

    def game_load(self):
        if os.path.isfile("savedata\savegame") and os.path.getsize("savedata\savegame") > 0:
            with gzip.open("savedata\savegame", "rb") as f:
                self.player, self.camera, self.map_obj, self.game_map, self.actors, self.actors_containers, self.items, self.buffs, self.messages, self.floor = pickle.load(f)

            for actor in self.actors:
                actor.set_surface(self.surface_main)
                actor.init_sprites()
                if actor.inventory:
                    for item in actor.inventory:
                        item.set_surface(self.surface_main)
                        item.init_sprites()
                if actor.equipped:
                    actor.equipped.set_surface(self.surface_main)
                    actor.equipped.init_sprites()
            for actor in self.actors_containers:
                actor.set_surface(self.surface_main)
                actor.init_sprites()
                if actor.inventory:
                    for item in actor.inventory:
                        item.set_surface(self.surface_main)
                        item.init_sprites()
            for item in self.items:
                item.set_surface(self.surface_main)
                item.init_sprites()
            for buff in self.buffs:
                buff.set_surface(self.surface_main)
                buff.init_sprites()

            self.map_obj.initialize_surfaces()
            self.map_obj.calculate_fov_map(self.player)

            self.ai = Ai.Ai(self.actors, self.actors_containers, self.items, self.effect_volume)

            self.spells = Spells.Spells(self.player, self.camera, self.map_obj, self.game_map, self.surface_main,
                                        self.actors, self.actors_containers, self.items, self.buffs, self.clock,
                                        self.messages, self.effect_volume, self.floor)

            self.menu = Menu.Menu(self.surface_main, self.player, self.clock, self.items, self.buffs, self.music_volume, self.effect_volume)

    def game_quit(self):
        self.game_save()
        pg.quit()
        exit()

    def game_menu(self):
        self.music = pg.mixer.Sound(const.BACKGROUND_MUSIC)
        command = self.menu.menu_main()
        self.music_volume = self.menu.music_volume
        self.effect_volume = self.menu.effect_volume
        self.settings_save()
        self.music.set_volume(self.music_volume)
        self.music.play(-1)
        if command == "CONTINUE":
            if os.path.isfile("savedata\savegame") and os.path.getsize("savedata\savegame") > 0:
                self.game_load()
            else:
                command = "NEW_GAME"
        if command == "NEW_GAME":
            self.__init__()

    def player_death(self):
        self.music.stop()
        effect = pg.mixer.Sound(const.DEATH_SOUND)
        effect.set_volume(self.effect_volume)
        effect.play()

        command = self.menu.death_screen_menu(self.floor)
        if os.path.isfile("savedata\savegame") and os.path.getsize("savedata\savegame") > 0:
            os.remove("savedata/savegame")
        if command == "EXIT":
            self.game_quit()
        elif command == "MAIN_MENU":
            self.game_menu()


if __name__ == '__main__':
    game = Main()
    game.game_loop()
