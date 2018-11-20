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

    def menu_main(self):
        play_button = Button.Button(self.main_surface, "PLAY", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 - 110, const.MAIN_SURFACE_HEIGHT // 2))
        exit_button = Button.Button(self.main_surface, "EXIT", (200, 100),
                                         (const.MAIN_SURFACE_WIDTH // 2 + 110, const.MAIN_SURFACE_HEIGHT // 2))

        self.main_surface.fill(const.WHITE)

        music = pg.mixer.Sound(const.MENU_MUSIC)
        music.set_volume(0.05)
        music.play(-1)  # Infinitely looping music

        menu_open = True
        while menu_open:
            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            if play_button.update(input):
                music.stop()
                menu_open = False

            if exit_button.update(input):
                pg.quit()
                exit()

            play_button.draw()
            exit_button.draw()

            pg.display.update()

    def inventory_menu(self):
        close = False

        text_height = self.draw.get_font_height(const.FONT_INVENTORY)

        while not close:
            self.inventory_surface.fill(const.BLACK)

            events = pg.event.get()
            if self.player.selection > len(self.player.inventory) - 1:
                current_index = self.player.selection = 0
            else:
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
                        if self.player.inventory == []:
                            self.player.messages.append("You have no items noob")
                        else:
                            if self.player.inventory and not self.player.equipped and isinstance(self.player.inventory[current_index], Actor.Equipable):
                                self.player.equip(self.player.inventory[current_index])
                            elif isinstance(self.player.equipped, Actor.Equipable) and not isinstance(self.player.inventory[current_index], Actor.Consumable):
                                self.player.messages.append("You already have something equipped.")
                            elif self.player.inventory:
                                self.player.consume(self.player.inventory[current_index])
                    elif event.key == pg.K_m:
                        if self.player.equipped is not None:
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
