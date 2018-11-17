import pygame as pg
import constants as const
import Draw


class Menu:
    def __init__(self, main_surface, player, clock):
        self.main_surface = main_surface
        self.player = player
        self.clock = clock
        self.inventory_surface = pg.Surface((const.INV_MENU_WIDTH, const.INV_MENU_HEIGHT))
        self.draw = Draw.Draw(self.inventory_surface)
        pass

    def inventory_menu(self):
        close = False

        text_height = self.draw.get_font_height(const.FONT_INVENTORY)

        while not close:
            self.inventory_surface.fill(const.BLACK)

            events = pg.event.get()
            current_index = self.player.selection

            # Close inventory if press I
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_i:
                        close = True
                    if event.key == pg.K_k:
                        self.player.next_selection()
                        current_index = self.player.selection
                    elif event.key == pg.K_j:
                        if self.player.inventory:
                            self.player.messages.append("Trying to equip/use " + self.player.inventory[current_index].name)
                        else:
                            self.player.messages.append("You have no items noob.")

            # Display list of items
            for i, item in enumerate(self.player.inventory):
                if i == current_index:
                    self.draw.draw_text(item.name, 0, 0 + (i * text_height), const.BLACK, const.FONT_INVENTORY,
                                        const.WHITE)
                else:
                    self.draw.draw_text(item.name, 0, 0 + (i * text_height), const.WHITE, const.FONT_INVENTORY)

            self.main_surface.blit(self.inventory_surface, (0, const.MAIN_SURFACE_HEIGHT // 2 - const.INV_MENU_HEIGHT // 2))

            self.clock.tick(const.FPS_LIMIT)

            pg.display.update()
