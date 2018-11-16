import pygame as pg
import libtcodpy as libt
import constants as const
import Actor, Draw, Map, Animations, Ai, Tile, Camera

"""
Simple python roguelike by Janar Aava and Alex Viil. Documentation is in English since libtcod's and pygame's
documentations are also in English and it makes it easier to explain things, without having to figure out
variable names or OOP terms in Estonian.
"""


"""TODO: Item system, Menus, Inventory, Map generation, Sound, win/loss conditions, different enemies."""


class Main:
    """
    The game object itself. This is where all the modules meet to form a single program.
    Upon initialization, initializes pygame, sets the main surface, creates the map and also creates
    the player and a bunch of actors to test out features as they're being implemented. Also has AI and
    a clock used for the FPS counter.
    """
    def __init__(self):
        pg.init()
        self.surface_main = pg.display.set_mode((const.MAIN_SURFACE_WIDTH, const.MAIN_SURFACE_HEIGHT))

        # Game Map

        self.map_obj = Map.Map()
        self.map_obj.create_map()
        self.game_map = self.map_obj.get_game_map()

        # self.test = []  # Collision attribute values of each tile for debugging
        # for y in self.game_map:
        #     row = []
        #     for tile in y:
        #         row.append(tile.get_is_wall())
        #     self.test.append(row)s
        # print(self.test)
        
        self.actors_inanimate = []
        self.actors = []

        # Game messages
        self.messages = []

        # Camera (aka offset to move the world instead of having a camera to move with the player, because pygame :)) )
        #        (MUST BE same coordinates as player, cannot be defined after player (or at least I haven't tried yet)
        self.camera = Camera.Camera(5, 5)

        # Actors
        self.actors_inanimate.append(Actor.Container(7, 7, "kirst", const.SPRITE_CHEST, self.game_map, self.surface_main, self.actors, self.actors_inanimate, self.messages))
        self.actors_inanimate.append(Actor.Container(3, 7, "kirst", const.SPRITE_CHEST, self.game_map, self.surface_main, self.actors, self.actors_inanimate, self.messages))
        self.actors.append(Actor.Enemy(8, 8, "Demon", const.SPRITES_DEMON, True, self.game_map, self.surface_main, self.actors, self.actors_inanimate, self.messages, 10))
        self.player = Actor.Player(5, 5, "Juhan", const.SPRITES_PLAYER, False, self.game_map, self.surface_main, self.actors, self.actors_inanimate, self.messages, 20)
        self.actors.append(self.player)
        
        self.actors_all = self.actors + self.actors_inanimate

        # Calculate initial FOV
        self.map_obj.calculate_fov_map(self.player)

        self.ai = Ai.Ai()

        self.clock = pg.time.Clock()

    def game_loop(self):
        """
        The main loop. Waits for events (player trying to move in some direction) and after every event gives the ai a turn,
        lets creatures attack each other, updates actor locations and updates the player's field of view. After an event,
        or even while there are no events, the while run cycle updates actor's sprites (idle frames), draws the game, and
        creates an FPS limit (to stop unwanted side effects, like actors seeming like they're on stimulants when the game
        runs on a fast computer).
        """
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
                    self.update_actor_locations()
                    self.map_obj.calculate_fov_map(self.player)

                    # Moves Enemy actors
                    for actor in self.actors:
                        if isinstance(actor, Actor.Enemy):
                            self.ai.aggressive_roam(actor, self.player)
                            self.update_actor_locations()
            
            # Update actors' sprites
            Animations.Animations(self.actors).update()

            # Draw game
            Draw.Draw(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_inanimate).draw_game(self.clock, self.messages, self.camera)

            # FPS limit and tracker
            self.clock.tick(const.FPS_LIMIT)

    def update_actor_locations(self):
        # Update actor's collision box location
        actor_locations = [actor.get_location() for actor in self.actors_all]
        self.map_obj.update(actor_locations)
        self.game_map = self.map_obj.get_game_map()


if __name__ == '__main__':
    game = Main()
    game.game_loop()
