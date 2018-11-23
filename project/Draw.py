import pygame as pg
import libtcodpy as libt
import constants as const
import Actor


class Draw:
    """
    The Draw object has the sole purpose of creating a single surface onto which it then draws the game_map, the
    fov_map (which follows the player), the player and all other actor objects like npcs and containers.
    """
    def __init__(self, surface):
        self.surface = surface

    def draw_text(self, text, text_x, text_y, text_color, font, center: bool=False, back_color=None):
        """Function used to draw text using pygame."""
        if back_color:
            text_surface = font.render(text, False, text_color, back_color)
        else:
            text_surface = font.render(text, False, text_color)
        text_rect = text_surface.get_rect()

        if center:
            text_rect.center = text_x, text_y
        else:
            text_rect.topleft = text_x, text_y

        self.surface.blit(text_surface, text_rect)

    def draw_fps(self, clock):
        self.draw_text(str(int(clock.get_fps())), 0, 0, const.BLACK, const.FONT_DEBUG)

    def draw_console_messages(self, messages: list, font):
        """Uses the draw_text function to draw a number of last messages created by actors to the console on thebottom left."""
        messages = messages[-const.MESSAGE_NUMBER:]
        # Places the console near bottom left
        font_height = self.get_font_height(const.FONT_CONSOLE)

        y = const.MAIN_SURFACE_HEIGHT - const.MESSAGE_NUMBER * font_height

        for i, message in enumerate(messages):
            self.draw_text(message, 0, y + i * font_height, const.WHITE, font, False, const.BLACK)

    def get_font_height(self, font):
        font_obj = font.render('test', False, const.BLACK)
        font_rect = font_obj.get_rect()
        return font_rect.height


class DrawWorld(Draw):
    def __init__(self, surface, game_map, player, fov_map, npcs=[], containers=[], items=[], buffs=[]):
        super().__init__(surface)
        self.game_map = game_map
        self.fov_map = fov_map
        self.player = player
        self.npcs = npcs
        self.containers = containers
        self.items = items
        self.buffs = buffs

    def draw_map(self, camera):
        """
        Draws the map. Checks each tile in the game_map and draws it if it is in the field of view of the player.
        Otherwise draws a darkened version of the tile that is outside of the field of view.
        """
        for y in self.game_map:
            for tile in y:
                if (0 <= (tile.x + camera.get_x_offset()) * const.TILE_WIDTH <= const.MAIN_SURFACE_WIDTH and
                        0 <= (tile.y + camera.get_y_offset()) * const.TILE_HEIGHT <= const.MAIN_SURFACE_HEIGHT):
                    if self.check_fov(tile.x, tile.y):  # only draws if area is in field of view
                        tile.explored = True
                        self.surface.blit(tile.sprite, ((tile.x + camera.get_x_offset()) * const.TILE_WIDTH,
                                                        (tile.y + camera.get_y_offset()) * const.TILE_HEIGHT))
                    elif tile.explored:
                        self.surface.blit(tile.explored_sprite, ((tile.x + camera.get_x_offset()) * const.TILE_WIDTH,
                                                                 (tile.y + camera.get_y_offset()) * const.TILE_HEIGHT))

    def draw_game(self, clock, messages, camera):
        """Draws the game and all elements, if they are within the field of view of the player."""
        # Reset the surface
        self.surface.fill(const.GRAY)

        # Draw the map
        self.draw_map(camera)

        # Draw debug text
        self.draw_fps(clock)

        # Draw Items
        for item in self.items:
            if self.check_fov(item.x, item.y + 1):
                item.draw(camera)

        # Draw Containers
        for container in self.containers:
            if self.check_fov(container.x, container.y + 1):  # only draws if area is in field of view
                container.draw(camera)

        # Draw the character
        self.player.draw(camera)

        # Draw NPCs
        for npc in self.npcs:
            if isinstance(npc, Actor.Player):
                npc.draw_hud()
            if self.check_fov(npc.x, npc.y + 1):  # only draws if area is in field of view
                npc.draw(camera)
                if npc.equipped:
                    npc.equipped.draw(camera, npc)

        # Draw Buffs
        for buff in self.buffs:
            buff.draw(camera)

        # Draw Console text
        self.draw_console_messages(messages, const.FONT_CONSOLE)

        # Update display
        pg.display.flip()

    def check_fov(self, x, y):
        return libt.map_is_in_fov(self.fov_map, x, y)
