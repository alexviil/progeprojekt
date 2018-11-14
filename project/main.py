import pygame as pg
import libtcodpy as libt
import constants as const
import Actor, Draw, Map, Animations, Tile


class Main:
    def __init__(self):
        pg.init()
        self.surface_main = pg.display.set_mode((const.MAIN_SURFACE_HEIGHT, const.MAIN_SURFACE_WIDTH))

        # Game Map

        self.map_obj = Map.Map()
        self.map_obj.create_map()
        self.game_map = self.map_obj.get_game_map()
        
        self.test = [] # Collision attribute values of each tile for debugging
        for y in self.game_map:
            row = []
            for tile in y:
                row.append(tile.get_is_wall())
            self.test.append(row)
        print(self.test)
        
        self.actors_inanimate = []
        self.actors = []

        # Actors

        self.player = Actor.Creature(1, 1, const.SPRITES_PLAYER, False, self.game_map, self.surface_main)
        self.actors.append(self.player)
        
        self.actors.append(Actor.Creature(5, 7, const.SPRITES_DEMON, True, self.game_map, self.surface_main))
        
        self.actors_inanimate.append(Actor.Container(7, 7, const.SPRITE_CHEST, self.game_map, self.surface_main))
        self.actors_inanimate.append(Actor.Container(3, 7, const.SPRITE_CHEST, self.game_map, self.surface_main))
        
        self.actors_all = self.actors + self.actors_inanimate

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
            
            # Update actor's collision box location
            actor_locations = [actor.get_location() for actor in self.actors_all]
            self.map_obj.update(actor_locations)
            self.game_map = self.map_obj.get_game_map()
            
            # Update actors' sprites
            Animations.Animations(self.actors).update()

            # Draw game
            Draw.Draw(self.surface_main, self.game_map, self.player, self.actors, self.actors_inanimate).draw_game()


if __name__ == '__main__':
    game = Main()
    game.game_loop()
