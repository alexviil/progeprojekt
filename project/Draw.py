import pygame as pg
import libtcodpy as libt
import constants as const


class Draw:
    def __init__(self, surface, game_map, player, fov_map, npcs=[], containers=[]):
        self.surface = surface
        self.game_map = game_map
        self.fov_map = fov_map
        self.player = player
        self.npcs = npcs
        self.containers = containers

    def draw_map(self):
        for y in self.game_map:
            for tile in y:
                if self.check_fov(tile.x, tile.y):  # only draws if area is in field of view
                    tile.explored = True
                    self.surface.blit(tile.sprite, (tile.x * const.TILE_WIDTH, tile.y * const.TILE_HEIGHT))
                elif tile.explored:
                    self.surface.blit(tile.explored_sprite, (tile.x * const.TILE_WIDTH, tile.y * const.TILE_HEIGHT))

    def draw_game(self, clock, messages):
        # Reset the surface
        self.surface.fill(const.GRAY)

        # Draw the map
        self.draw_map()

        # Draw debug text
        self.draw_fps(clock)

        # Draw Console text
        self.draw_console_messages(messages, const.FONT_CONSOLE)

        # Draw Containers
        for container in self.containers:
            if self.check_fov(container.x, container.y+1):  # only draws if area is in field of view
                container.draw()

        # Draw the character
        self.player.draw()
        
        # Draw NPCs
        for npc in self.npcs:
            if self.check_fov(npc.x, npc.y+1):  # only draws if area is in field of view
                npc.draw()

        # Update display
        pg.display.flip()

    def draw_text(self, text, text_x, text_y, text_color, font, back_color=None):
        if back_color:
            text_surface = font.render(text, False, text_color, back_color)
        else:
            text_surface = font.render(text, False, text_color)
        text_rect = text_surface.get_rect()

        text_rect.topleft = text_x, text_y

        self.surface.blit(text_surface, text_rect)

    def draw_fps(self, clock):
        self.draw_text(str(int(clock.get_fps())), 0, 0, const.BLACK, const.FONT_DEBUG)

    def draw_console_messages(self, messages: list, font):
        messages = messages[-const.MESSAGE_NUMBER:]
        # Places the console near bottom right
        font_height = self.get_font_height(const.FONT_CONSOLE)

        y = const.MAIN_SURFACE_HEIGHT - const.MESSAGE_NUMBER * font_height

        for i, message in enumerate(messages):
            self.draw_text(message, 0, y + i * font_height, const.WHITE, font, const.BLACK)

    def check_fov(self, x, y):
        return libt.map_is_in_fov(self.fov_map, x, y)

    def get_font_height(self, font):
        font_obj = font.render('test', False, const.BLACK)
        font_rect = font_obj.get_rect()
        return font_rect.height
