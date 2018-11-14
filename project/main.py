import pygame as pg
import libtcodpy as libt
import constants as const
import Actor, Draw, Map, Animations, Ai


class Main:
    def __init__(self):
        pg.init()
        self.surface_main = pg.display.set_mode((const.MAIN_SURFACE_HEIGHT, const.MAIN_SURFACE_WIDTH))

        self.map_obj = Map.Map()
        self.map_obj.create_map()
        self.game_map = self.map_obj.get_game_map()
        
        self.actors_inanimate = []
        self.actors = []

        self.actors_inanimate.append(Actor.Container(7, 7, "kirst", const.SPRITE_CHEST, self.game_map, self.surface_main, self.actors))
        self.actors_inanimate.append(Actor.Container(3, 7, "kirst", const.SPRITE_CHEST, self.game_map, self.surface_main, self.actors))

        self.actors.append(Actor.Enemy(5, 7, "deemon", const.SPRITES_DEMON, True, self.game_map, self.surface_main, self.actors, 10))

        self.player = Actor.Creature(1, 1, "Juhan", const.SPRITES_PLAYER, False, self.game_map, self.surface_main, self.actors, 20)
        self.actors.append(self.player)
        
        self.actors_all = self.actors + self.actors_inanimate

        self.ai = Ai.Ai()

    def game_loop(self):
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
                    elif event.key == pg.K_s:
                        self.player.control(0, 1)
                    elif event.key == pg.K_a:
                        self.player.control(-1, 0)
                    elif event.key == pg.K_d:
                        self.player.control(1, 0)
                    self.update_actor_locations()

                    # Moves Enemy actors
                    for actor in self.actors:
                        if isinstance(actor, Actor.Enemy):
                            self.ai.move_randomly(actor, self.actors_all)
                            self.update_actor_locations()
            
            # Update actors' sprites
            Animations.Animations(self.actors).update()

            # Draw game
            Draw.Draw(self.surface_main, self.game_map, self.player, self.actors, self.actors_inanimate).draw_game()

    def update_actor_locations(self):
        # Update actor's collision box location
        actor_locations = [actor.get_location() for actor in self.actors_all]
        self.map_obj.update(actor_locations)
        self.game_map = self.map_obj.get_game_map()


if __name__ == '__main__':
    game = Main()
    game.game_loop()
