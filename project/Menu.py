import pygame as pg
import constants as const
import Draw, Button, Actor


class Menu:
    def __init__(self, main_surface, player, clock, items):
        self.main_surface = main_surface
        self.player = player
        self.clock = clock
        self.items = items
        self.inventory_surface = pg.Surface((const.INV_MENU_WIDTH, const.INV_MENU_HEIGHT))
        self.draw = Draw.Draw(self.inventory_surface)

        self.play_button = Button.Button(self.main_surface, "PLAY", (200, 100), (const.MAIN_SURFACE_WIDTH//2, const.MAIN_SURFACE_HEIGHT//2))

    def menu_main(self):
        menu_open = True
        while menu_open:
            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            if self.play_button.update(input):
                menu_open = False

            self.main_surface.fill(const.WHITE)
            self.play_button.draw()

            pg.display.update()

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
                    if event.key == pg.K_l:
                        if not self.player.inventory:
                            self.player.messages.append("You have no items to drop")
                        else:
                            item_here = False
                            for item in self.items:
                                if item.get_location() == self.player.get_location():
                                    self.player.messages.append("There is already an item here.")
                                    item_here = True
                                    break
                            if not item_here:
                                self.player.messages.append("Dropped " + self.player.inventory[current_index].name + ".")
                                self.player.inventory[current_index].drop(self.player, self.items)
                    elif event.key == pg.K_j:
                        if self.player.inventory and not self.player.equipped:
                            if isinstance(item, Actor.Equipable):
                                self.player.messages.append("Equipped " + self.player.inventory[current_index].name + ".")
                                self.player.equip(self.player.inventory[current_index])
                            elif isinstance(item, Actor.Consumable):
                                pass  # TODO consumables
                        elif self.player.equipped is not None:
                            self.player.messages.append("You already have something equipped.")
                        else:
                            self.player.messages.append("You have no items noob.")
                    elif event.key == pg.K_m:
                        if self.player.equipped is not None:
                            self.player.messages.append("Unequipped " + self.player.equipped.name + ".")
                            self.player.unequip(self.player.equipped)
                        else:
                            self.player.messages.append("You have nothing equipped.")

            # Display list of items
            for i, item in enumerate(self.player.inventory):
                if i == current_index:
                    self.draw.draw_text(item.name, 0, 0 + (i * text_height), const.BLACK, const.FONT_INVENTORY,
                                        False, const.WHITE)
                else:
                    self.draw.draw_text(item.name, 0, 0 + (i * text_height), const.WHITE, const.FONT_INVENTORY)

            self.main_surface.blit(self.inventory_surface, (0, const.MAIN_SURFACE_HEIGHT // 2 - const.INV_MENU_HEIGHT // 2))

            self.clock.tick(const.FPS_LIMIT)

            pg.display.update()
